import typing
import os
import sys
import json
import jsonpatch
import jsonpointer
import logging
import presalytics.client.api
import presalytics.lib.tools.story_tools
import presalytics.story.outline
import presalytics.story.components
if typing.TYPE_CHECKING:
    from presalytics.story.components import ComponentBase, WidgetBase
    from presalytics.story.outline import StoryOutline

logger = logging.getLogger(__name__)

def update_components(filename=None):
    autodiscover_paths = presalytics.COMPONENTS.autodiscover_paths
    dirname = os.path.dirname(filename)
    if os.path.exists(dirname) and dirname not in autodiscover_paths:
        autodiscover_paths.append(dirname)
    cwd = os.getcwd()
    abs_filedir = os.path.join(cwd, dirname)
    if os.path.exists(abs_filedir) and abs_filedir not in autodiscover_paths:
        autodiscover_paths.append(abs_filedir)
    if len(autodiscover_paths) > len(presalytics.COMPONENTS.autodiscover_paths):
        presalytics.COMPONENTS = presalytics.story.components.ComponentRegistry(autodiscover_paths=autodiscover_paths, 
                                                                                reserved_names=presalytics.CONFIG.get("RESERVED_NAMES", []))

def get_component(name, filename=None):
    inst: 'ComponentBase'

    if filename:
        update_components(filename=filename)            
    component_list = presalytics.COMPONENTS.find_instance(name)
    if len(component_list) == 0:
        message = "Could not find an instance with name '{0}' in the COMPONENTS registry".format(name)
        presalytics.COMPONENTS.raise_error(message)
    elif len(component_list) > 1:
        components_str = ", ".join(component_list)
        message = "Multiple matches for name in COMPONENTS registry.  Choose from: " + components_str
        presalytics.COMPONENTS.raise_error(message)
    elif len(component_list) == 1:
        return presalytics.COMPONENTS.get_instance(component_list[0])
    else:
        message = "Error searching the COMPONENTS registry"
        presalytics.COMPONENTS.raise_error(message)

def add_widget_instance(widget_name, outline, position=None, page_number=0, filename=None):
    inst: 'WidgetBase'
    outline: 'StoryOutline'

    inst = get_component(widget_name, filename=filename)
    widget = inst.serialize()
    if not page_number:
        page_number = 0
    if page_number > len(outline.pages):
        message = "The story has fewer than {} pages".format(page_number)
        raise presalytics.lib.exceptions.InvalidArgumentException(message=message)
    if not position:
        position = len(outline.pages[page_number].widgets)
    outline.pages[page_number].widgets.insert(position, widget)

    return outline

def remove_widget_by_name(widget_name, outline, page_number=None, filename=None):
    inst: 'WidgetBase'
    outline: 'StoryOutline'

    if page_number:
        start = page_number
        stop = page_number
    else:
        start = 0
        stop = len(outline.pages)
    
    for p in range(start, stop):
        page = outline.pages[p]
        for w in range(0, len(page.widgets)):
            if page.widgets[w].name == widget_name:
                page.widgets.pop(w)
    
    return outline



def create_from_instance(name, widget=False, page=False, filename=None) -> 'StoryOutline': #type: ignore
    """
    Creates a Story Outline from an instance name in `presalytics.COMPONENTS`
    """
    inst: 'ComponentBase'

    inst = get_component(name)
    if page:
        outline = presalytics.lib.tools.component_tools.create_outline_from_page(inst) #type: ignore
    elif widget:
        outline = presalytics.lib.tools.component_tools.create_outline_from_widget(inst) #type: ignore
    else:
        raise presalytics.lib.exceptions.InvalidArgumentException("Either the 'widget' or 'page' paramters must be true.")
    return outline



def push_outline(outline, username=None, password=None) -> 'StoryOutline':
    """
    Updates an outline in the Presalytics API Story service
    """
    client = presalytics.client.api.Client(username=username, password=password)
    if outline.story_id == "empty" or not outline.story_id:
        story = client.story.story_post({"outline": outline.dump()})
    else:
        old_story = client.story.story_id_get(outline.story_id)
        old_story.outline = outline.dump()
        story = client.story.story_id_put(outline.story_id, old_story)
    return presalytics.story.outline.StoryOutline.load(story.outline)


def pull_outline(story_id, username=None, password=None) -> 'StoryOutline':
    """
    Retrives an outline from the Presalytics API Story service
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
    Share stories with other users. Either by email or Presalytics API user Id.
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
    return client.story.story_id_get(story_id, include_relationships=True)

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
        cron_command = "* * * * * cd {0} && {1} -m presalytics push".format(os.getcwd(), sys.executable)
        print("Place the following line in your cron file:")
        print(cron_command)
    elif sys.platform.startswith("win"):
        command = os.environ["VIRTUAL_ENV"] + "/Scripts/activate.bat && python -m presalytics push"
        filename = os.path.join(os.getcwd(), "story-push.bat")
        with open(filename, 'w') as f:
            f.write(command)
        print("A file named 'story-push.bat was just placed in the current working directory.  Add this file in the 'Windows Task Scheduler'.")
    else:
        logger.error("Unknown operating system.")
        raise ValueError

def apply_json_patch(outline, patch):
    """
    Allows users to apply json patches to thier Story Outlines.

    See https://python-json-patch.readthedocs.io/en/latest/index.html for more info.

    Parameters:
    ----------

    outline: presaltyics.story.outline.StoryOutline
        A Story Outline object

    patch: str or dict
        Either an RFC 6901 compliant string or a dictionary with op, path, and value keys.  The
        dictionary is for ease of use and will get parsed into a compliant string.
    """
    outline: 'StoryOutline'

    if isinstance(patch, dict):
        _json = json.dumps(patch)
        patch = '[{}]'.format(_json)
    outline_dict = outline.to_dict()
    try:
        new_dict = jsonpatch.apply_patch(outline_dict, patch)
    except (jsonpatch.JsonPatchException, jsonpointer.JsonPointerException) as ex:
        message = "Unable to apply Json patch: {}".format(ex.args[0])
        raise presalytics.lib.exceptions.InvalidArgumentException(message=message)
    new_outline = presalytics.story.outline.StoryOutline.deserialize(new_dict)
    return new_outline

def update_outline(outline, filename=None, message=None):
    """
    Updates the the outline from active instances in the workspace
    """
    if not message:
        message = "Automated update via presalytics.lib.tools.workflows.update_outline()"
    
    update_components(filename=filename)

    for p in range(0, len(outline.pages)):
        page = outline.pages[p]

        page_key = "page.{}.{}".format(page.kind, page.name)
        page_inst = presalytics.COMPONENTS.get_instance(page_key)
        if page_inst:
            outline.pages[p] = page_inst.serialize()
        
        for w in range(0, len(page.widgets)):
            widget = outline.pages[p].widgets[w]

            widget_key = "widget.{}.{}".format(widget.kind, widget.name)
            widget_inst = presalytics.COMPONENTS.get_instance(widget_key)
            if widget_inst:
                outline.pages[p].widgets[w] = widget_inst.serialize() 

    
    for t in range(0, len(outline.themes)):
        theme = outline.themes[t]

        theme_key = "theme.{}.{}".format(theme.kind, theme.name)
        theme_inst = presalytics.COMPONENTS.get_instance(theme_key)
        if theme_inst:
            outline.themes[t] = theme_inst.serialize()
    
    outline.info.revision_notes = message
    return outline


    
    


    