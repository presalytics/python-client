import typing
import os
import sys
import json
import presalytics.client.api
import presalytics.lib.tools.story_tools
import presalytics.story.outline
import presalytics.story.components
if typing.TYPE_CHECKING:
    from presalytics.story.components import ComponentBase
    from presalytics.story.outline import StoryOutline


def create_from_instance(name, widget=False, page=False, filename=None) -> 'StoryOutline': #type: ignore
    """
    Creates a Story Outline from an instance name in `presalytics.COMPONENTS`
    """
    inst: 'ComponentBase'
    if filename:
        autodiscover_paths = presalytics.COMPONENTS.autodiscover_paths
        dirname = os.path.dirname(filename)
        if os.path.exists(dirname) and dirname not in autodiscover_paths:
            autodiscover_paths.append(dirname)
        cwd = os.getcwd()
        abs_filedir = os.path.join(cwd, dirname)
        if os.path.exists(abs_filedir) and abs_filedir not in autodiscover_paths:
            autodiscover_paths.append(abs_filedir)
        if len(autodiscover_paths) > len(presalytics.COMPONENTS.autodiscover_paths):
            presalytics.COMPONENTS = presalytics.story.components.ComponentRegistry(autodiscover_paths=autodiscover_paths)
            
    component_list = presalytics.COMPONENTS.find_instance(name)
    if len(component_list) == 0:
        message = "Could not find an instance with name '{0}' in the COMPONENTS registry".format(name)
        presalytics.COMPONENTS.raise_error(message)
    elif len(component_list) > 1:
        components_str = ", ".join(component_list)
        message = "Multiple matches for name in COMPONENTS registry.  Choose from: " + components_str
        presalytics.COMPONENTS.raise_error(message)
    elif len(component_list) == 1:
        inst = presalytics.COMPONENTS.get_instance(component_list[0])
        if page:
            outline = presalytics.lib.tools.component_tools.create_outline_from_page(inst) #type: ignore
        elif widget:
            outline = presalytics.lib.tools.component_tools.create_outline_from_widget(inst) #type: ignore
        else:
            raise presalytics.lib.exceptions.InvalidArgumentException("Either the 'widget' or 'page' paramters must be true.")
        return outline
    else:
        message = "Error searching the COMPONENTS registry"
        presalytics.COMPONENTS.raise_error(message)


def push_outline(outline, username=None, password=None) -> 'StoryOutline':
    """
    Updates an outline in the Presalytics API Story service
    """
    client = presalytics.client.api.Client(username=username, password=password)
    if outline.story_id == "empty" or not outline.story_id:
        story = client.story.story_post(outline.dump())
    else:
        old_story = client.story.story_id_get(outline.story_id)
        old_story.outline = outline.dump()
        story = client.story.story_id_put(outline.story_id, old_story)
    return presalytics.story.outline.StoryOutline.load(story.outline)


def pull_outline(story_id, username=None, password=None) -> 'StoryOutline':
    """
    Retrives an outline from the Presaltyics API Story service
    """
    client = presalytics.client.api.Client(username=username, password=password)
    if story_id == "empty" or not story_id:
        message = "The story_id must not be empty"
        raise presalytics.lib.exceptions.InvalidArgumentException(message)
    story = client.story.story_id_get(story_id)
    return presalytics.story.outline.StoryOutline.load(story.outline)


def delete_all_stories(username=None, password=None):
    """
    WARNING!!! 
    
    Delete all stories owned by this user

    BE CAREFUL!!!    
    """
    client = presalytics.client.api.Client(username=username, password=password)
    stories = client.story.story_get()
    ids = [s.id for s in stories]
    for id in ids:
        client.story.story_id_delete(id)


def delete_by_id(story_id, username=None, password=None):
    """
    Delete stories by Story Id
    """
    client = presalytics.client.api.Client(username=username, password=password)
    client.story.story_id_delete(story_id)

def share_story(story_id,
                emails=None, 
                user_ids=None, 
                username=None, 
                password=None,
                collaborator_type="viewer"):
    """
    Share stories with other users. Either by email or Presaltyics API user Id.
    """
    client = presalytics.client.api.Client(username=username, password=password)
    if emails:
        email_list = emails.split(",")
        for e in email_list:
            body = {
                "user_email": e,
                "collaborator_type": collaborator_type,
                "user_id": ""
            }
            client.story.story_id_collaborators_post(story_id, body)
    if user_ids:
        user_id_list = user_ids.split(",")
        for _id in user_id_list:
            body = {
                "user_email": "",
                "collaborator_type": collaborator_type,
                "user_id": _id
            }
            client.story.story_id_collaborators_post(story_id, body)

def get_story(story_id):
    """
    returns Story metadata from the story API
    """
    client = presalytics.client.api.Client()
    return client.story.story_id_get(story_id)

def create_config_file(username, password=None, set_dict={}, overwrite=False):
    config_file = os.path.join(os.getcwd(), "config.py")
    if os.path.exists(config_file):
        if overwrite:
            os.remove(config_file)
        else:
            logger.error("Configuration file exists.  Use option [--overwrite] to overwrite.")
            raise ValueError
    dump = {"USERNAME": username}
    if password:
        dump.update({"PASSWORD": password})
    if len(set_dict.keys()) > 0:
        dump.update(set_dict)
    content = "PRESALYTICS = " + repr(dump)
    with open(config_file, 'w') as f:
        f.write(content)

def create_cron_target():
    if sys.platform.startswith("linux"):
        cron_command = "* * * * * cd {0} && {1} -m presaltyics push".format(os.getcwd(), sys.executable)
        print("Place the following line in your cron file:")
        print(cron_command)
    elif sys.platform.startswith("win"):
        command = os.environ["VIRTUAL_ENV"] + "/Scripts/activate.bat && python -m presaltyics push"
        filename = os.path.join(os.getcwd(), "story-push.bat")
        with open(filename, 'w') as f:
            f.write(command)
        print("A file named 'story-push.bat was just placed in the current working directory.  Add this file in the 'Windows Task Scheduler'.")
    else:
        logger.error("Unknown operating system.")
        raise ValueError


    
    


    