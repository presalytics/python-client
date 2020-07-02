"""
Command Line Interface for Presalytics Python Library

Run "presalytics -h" for details
"""
import os
import logging
import argparse
import presalytics
import urllib.parse
import webbrowser
import yaml
import json
import ast
import datetime
import presalytics.lib.constants
import presalytics.lib.tools.story_tools
import presalytics.lib.tools.ooxml_tools
import presalytics.lib.tools.workflows


logger = logging.getLogger(__name__)

description = """
Presalytics Python Library
--------------------------
Version: {version}

Create live presentations, dashboards, and persistent analytics,
and interact with the Presalytics API.

Please review the push, pull, and create subcommands for more options.

For more information about the Presalytics API, please visit 
<https://presalytics.io> or send your questions to inquires@presalytics.io.

Command Line Instructions
-------------------------
""".format(version=presalytics.__version__)

parser = argparse.ArgumentParser(
    description=description,
    epilog="Further documentation is available at <https://presalytics.io/docs/>.",
    formatter_class=argparse.RawTextHelpFormatter,
    prog='presalytics'
)
file_help = "The filename of the Story Outline. Defaults to 'story.yaml'"
parser.add_argument('-f', '--file', default='story.yaml', action='store', help=file_help)
parser.add_argument('--version', action='version', version=presalytics.__version__)
parser.add_argument('--view', default=False, action='store_true', help='View a Story in the browser')
parser.add_argument('--manage', default=False, action='store_true', help="""Go to the Story's management page""")
parser.add_argument('--show-story', default=False, action='store_true', help="Print Story metadata to the console")
parser.add_argument('--cron', default=False, action='store_true', help="Print information on how automate updates to your story to the console.")
verbosity = parser.add_mutually_exclusive_group(required=False)
verbosity.add_argument('-v', '--verbose', default=False, action='store_true', help="Increases the detail in log output")
verbosity.add_argument('-q', '--quiet', default=False, action='store_true', help="Decrease the detail in log output. Supresseses non-critical errors.")


yaml_help = "Writes file updates to YAML format.  Yaml is the default."
json_help = "Writes file updates to JSON format"
overwrite_help = "Forces (o)verwrite of file with returned Story Outline (if exists)"
username_help = "Overrides the username in presalytics.CONFIG (if present)"
password_help = "The user's Presalytics API password"
subparsers = parser.add_subparsers(title='Story API Commands', prog='presalytics', dest='story_api')

push_description = """
Pushes a Story Outline revision to the Presalytics API
Story service, and writes the updated story outline to a local file (--file)
"""
push = subparsers.add_parser('push', description=push_description, help='Push a Story Outline revision')
push.add_argument('--update', default=False, action='store_true', help="Update the Story Outline from Local Scripts before pushing")
push.add_argument('-o', '--overwrite', default=False, action='store_true', help=overwrite_help)
push.add_argument('-u', '--username', default=None, action='store', help=username_help)
push.add_argument('-p', '--password', default=None, action='store', help=password_help)
push.add_argument('-m', '--message', default=None, action='store', help="Revision message (added to outline).  Automatically populates by default.")
push_options = push.add_mutually_exclusive_group(required=False)
push_options.add_argument('-y', '--yaml', default=False, action='store_true', help=yaml_help)
push_options.add_argument('-j', '--json', default=False, action='store_true', help=json_help)

pull_description = """
Retrives a Story Outline from the the Presalytics API Story Service,
and writes the retrieved story outline to a local file (--file)
"""

id_help = """
The Preslytics API Story Service Id for the story (type: UUID-v4)
If not supplied, the tool searches the file from the --file option 
for a 'storyId' attribute 
"""

pull = subparsers.add_parser('pull', description=pull_description, help='Pull a Story Outline revision')
pull.add_argument('--id', default=None, action='store', help=id_help)
pull.add_argument('-o', '--overwrite', default=False, action='store_true', help=overwrite_help)
pull.add_argument('-u', '--username', default=None, action='store', help=username_help)
pull.add_argument('-p', '--password', default=None, action='store', help=password_help)
pull_options = pull.add_mutually_exclusive_group(required=False)
pull_options.add_argument('-y', '--yaml', default=False, action='store_true', help=yaml_help)
pull_options.add_argument('-j', '--json', default=False, action='store_true', help=json_help)


create_description = """

The widget or page instance in the [name] arguemnt must be avialable in 
`presalytics.COMPONENTS` at run-time.  Widget and page instances are loaded 
into `presalytics.COMPONENTS` from the current working directory and other 
configured folders at import of the presalytics module.
"""

create_epilog = """
See https://presalytics.io/docs/configuration/ for more information.
"""

name_help = """
The name of the widget or page instance to create a Story Outline from.  If using options
`ooxml_file`, the name is the path the file that you would like to create from.
"""
create = subparsers.add_parser('create', description=create_description, help='Create a Story Outline', epilog=create_epilog)
create.add_argument('name', action='store', help=name_help)
create_options = create.add_mutually_exclusive_group(required=True)
create_options.add_argument('--widget', default=False, action='store_true', help="Create a Story Outline from a widget instance")
create_options.add_argument('--page', default=False, action='store_true', help="Create a Story Outline from a page instance")
create_options.add_argument('--ooxml_file', default=False, action='store_true', help="Create a Story Outline from an Ooxml Document")
create.add_argument('-o', '--overwrite', default=False, action='store_true', help=overwrite_help)
create.add_argument('-u', '--username', default=None, action='store', help=username_help)
create.add_argument('-p', '--password', default=None, action='store', help=password_help)
create.add_argument('-s', '--source', default=None, action='store', help="The module containing the instance.  Needed only if instance not auto-loaded into presalytics.CONFIG")
create_output_options = create.add_mutually_exclusive_group(required=False)
create_output_options.add_argument('-y', '--yaml', default=False, action='store_true', help=yaml_help)
create_output_options.add_argument('-j', '--json', default=False, action='store_true', help=json_help)

update_description = """
Update the Story outline from instances contained in scripts in the active workspace 
"""

update = subparsers.add_parser('update', description=update_description, help='Update a Story Outline From Local Scripts')
update.add_argument('-m', '--message', default=None, action='store', help="Revision message (added to outline).  Automatically populates by default.")
update_options = update.add_mutually_exclusive_group(required=False)
update_options.add_argument('-y', '--yaml', default=False, action='store_true', help=yaml_help)
update_options.add_argument('-j', '--json', default=False, action='store_true', help=json_help)


modify_description = """
Modify a Story's outline

You can either 'add' or 'remove' a widget to or from a page in story outline.

For more complex operations, you can apply a JSON 'patch' to to the story outline per 
[RFC 6902](https://tools.ietf.org/html/rfc6902).  You can find good exmaples at 
www.jsonpatch.com
""" 
modify = subparsers.add_parser('modify', description=modify_description, help='Modify a Story Outline')
modify.add_argument('action', choices=['add', 'remove', 'patch'], action='store', help="You can either add or remove a widget (quick & easy), or apply a json patch (more complex)")
modify.add_argument('-n', '--name', default=None, action='store', help="The name of the widget you would like to add or remove")
modify.add_argument('--position', default=None, action='store', type=int, help="The position in the widget list to place the widget")
modify.add_argument('--page_number', default=None, action='store', type=int, help="The page number to add or remove the widget to/from" )
modify.add_argument('--patch', default=None, action='store', help="The json patch (per RFC 6902) you want to apply to the Story Outline.")
modify_output_options = modify.add_mutually_exclusive_group(required=False)
modify_output_options.add_argument('-y', '--yaml', default=False, action='store_true', help=yaml_help)
modify_output_options.add_argument('-j', '--json', default=False, action='store_true', help=json_help)

share_description = """
Control permissions for owners, editors, promoters, and viewer or your stories
"""

share = subparsers.add_parser('share', description=share_description, help='Share Stories')
share.add_argument('--user-ids', action='store', help='A comma-separated list of the Presalytics API user IDs of users you what to share this story with.')
share.add_argument('--emails', action='store', help='A comma-separated list of the email addresses of users you what to share this story with.')
share.add_argument('--collaborator-type', choices=['owner', 'viewer', 'promoter', 'editor'], action='store', help='The permission type to grant to the new user. Defaults to viewer.')
share.add_argument('-u', '--username', default=None, action='store', help=username_help)
share.add_argument('-p', '--password', default=None, action='store', help=password_help)


account_description = """
Utilities for managing and you account and your stories.  Use the [--delete]
option to delete stories
"""

account = subparsers.add_parser('account', description=account_description, help='Account & Story Management Utlities')
account_action_group = account.add_mutually_exclusive_group(required=True)
account_action_group.add_argument('--delete', default=False, action='store_true', help='Delete Stories')
delete_group = account.add_mutually_exclusive_group(required=True)
delete_group.add_argument('--all', default=False, action='store_true', help='WARNING!!! Delete all stories on account.')
delete_group.add_argument('--id', default=None, help='The Presalytics API Story service Id of the story you want to delete.')
account.add_argument('-u', '--username', default=None, action='store', help=username_help)
account.add_argument('-p', '--password', default=None, action='store', help=password_help)

ooxml_description = """
Utilities for managing references to the Presaltyics API Ooxml Automation Service in your stracts
"""
ooxml = subparsers.add_parser('ooxml', description=account_description, help='Modify Stories using Ooxml Documents')
ooxml.add_argument('ooxml_filepath', action='store', default=None, help="The relative or absolute file path to the ooxml-file")
ooxml.add_argument('action', choices=['add', 'replace'], default=None, action='store', help="Whether to add the ooxml to a story or replace an existing one.")
ooxml.add_argument('--story-id', action='store', default=None, help="The Presalytics API Story service Id of the story you want associate this file with.  Defaults to the story at the [--file] option.")
ooxml.add_argument('--replace-id', action='store', default=None, help="The Ooxml Automation service if id for the associated document that you want to replace")
ooxml.add_argument('-u', '--username', default=None, action='store', help=username_help)
ooxml.add_argument('-p', '--password', default=None, action='store', help=password_help)

config_description = """
Create and manage presalytics `config.py` files
"""

config = subparsers.add_parser('config', description=config_description, help='Create and manage presalytics `config.py` files')
config.add_argument('username', action='store', help=username_help)
config.add_argument('-p', '--password', default=None, action='store', help=password_help)
config.add_argument('-s', "--set", metavar="KEY=VALUE", default=None, nargs='+', help="Pass config values to to `config.py` with KEY=VALUE stucture (e.g., '-s USE_LOGGER=False'")
config.add_argument('-o', '--overwrite', default=False, action='store_true', help=overwrite_help)

def parse_var(s):
    """
    Parse a key, value pair, separated by '='
    That's the reverse of ShellArgs.

    On the command line (argparse) a declaration will typically look like:
        foo=hello
    or
        foo="hello world"
    """
    items = s.split('=')
    key = items[0].strip() # we remove blanks around keys, as is logical
    if len(items) > 1:
        # rejoin the rest:
        value = '='.join(items[1:])
        if value == 'True' or value == 'true':
            value = True
        if value == 'False'or value == 'false':
            value = False
    return (key, value)


def parse_vars(items):
    """
    Parse a series of key-value pairs and return a dictionary
    """
    d = {}

    if items:
        for item in items:
            key, value = parse_var(item)
            d[key] = value
    return d

def _load_file(filename):
    if filename.endswith('yaml') or filename.endswith('yml'):
        outline = presalytics.StoryOutline.import_yaml(filename)
    if filename.endswith('json'):
        with open(filename, 'r') as f:
            outline_string = f.read()
        outline = presalytics.StoryOutline.load(outline_string)
    return outline


def _make_url(story_id, url_type):
    route = "/story/{0}/{1}/".format(url_type, story_id)
    try:
        host = presalytics.CONFIG["HOSTS"]["SITE"]
    except (KeyError, AttributeError):
        host = presalytics.lib.constants.SITE_HOST
    return urllib.parse.urljoin(host, route)

def _open_page(story_id, url_type):
    url = _make_url(story_id, url_type)
    webbrowser.open_new_tab(url)

def _write(outline, filename, json=False):
    if json:
        with open(filename, 'w') as f:
            f.write(outline.dump())
    else:
        outline.export_yaml(filename)
    
def _dump(outline, filename, overwrite=False, json=False):
    if os.path.exists(filename):
        if not overwrite:
            logger.error("A file already exists at {}.  Use option [--overwrite] to overwrite the existing file".format(filename))
        else:
            os.remove(filename)
            _write(outline, filename, json)
    else:
        _write(outline, filename, json)


def main():
    """ Command-line entry point 
    
    Run the following from the command line for more information:

        python3 -m presalytics --help
    
    or inside a python virtual environment:

        presalytics -h
    
    """
    try:
        args = parser.parse_args()
        filename = args.file
        file_extension = filename.split(".")[-1]
        if file_extension == "yaml" or file_extension == "yml":
            original_file_is_yaml = True
        else:
            original_file_is_yaml - False
        lgs = [logging.getLogger(n) for n in logging.root.manager.loggerDict]
        if args.verbose or args.quiet:
            for lg in lgs:
                lg.setLevel(logging.DEBUG)
        elif args.quiet:
            for lg in lgs:
                lg.setLevel(logging.CRITICAL)
        else:
            for lg in lgs:
                lg.setLevel(logging.ERROR)
        write = False
        pull = False
        push = False
        account = False
        share = False
        outline = None
        ooxml = False
        config = False
        modify = False
        update = False
        message = getattr(args, "message", None)
        if args.story_api == "create":
            # create outline from page/widget
            if args.ooxml_file:
                ooxml_file = args.name
                if not os.path.exists(ooxml_file):
                    cwd = os.getcwd()
                    test_path = os.path.join(cwd, ooxml_file)
                    if os.path.exists(test_path):
                        ooxml_file = test_path
                    else:
                        logger.error("Could not find a path to file: {0}".format(ooxml_file))
                        return
                story = presalytics.lib.tools.ooxml_tools.create_story_from_ooxml_file(ooxml_file)
                outline = presalytics.story.outline.StoryOutline.load(story.outline)
            else:
                outline = presalytics.lib.tools.workflows.create_from_instance(args.name, page=args.page, widget=args.widget, filename=args.source)
            # dump to file
            push = True
            pull = True
            write = True
            message = outline.info.revision_notes
        elif args.story_api == "push":
            push = True
            pull = False
            write = False
            if args.update:
                update = True
        elif args.story_api == "pull":
            push = False
            pull = True
            write = True
        elif args.story_api == "account":
            account = True
        elif args.story_api == "share":
            share = True
        elif args.story_api == "ooxml":
            ooxml = True
            pull = True
        elif args.story_api == "config":
            config = True
        elif args.story_api == "modify":
            modify = True
        elif args.story_api == "update":
            update = True
        else:
            push = False
            pull = False
            write = False
            #load story outline from file
        if config:
            set_dict = {} if not args.set else parse_vars(args.set)
            presalytics.lib.tools.workflows.create_config_file(args.username, 
                                                               password=args.password, 
                                                               set_dict=set_dict, 
                                                               overwrite=args.overwrite)
            logger.info("File 'config.py creating in folder " + os.getcwd())
            return
        try:
            if not outline:
                if not os.path.exists(filename):
                    current_dir = os.getcwd()
                    abs_filename = os.path.join(current_dir, filename)
                    if os.path.exists(abs_filename):
                        filename = abs_filename
                    else:
                        logger.error("Could not find file: {}".format(filename))
                        return
                outline = _load_file(filename)
        except Exception:
            logger.error("Error handling file: {}".format(filename))
            return
        if modify:
            if args.action == "add" or args.action == "remove":
                if not args.name:
                    logger.error("Modifying an outline using the 'add' or 'remove' actions requires a [--name] argument")
                    return
                if args.action == "add":
                    outline = presalytics.lib.tools.workflows.add_widget_instance(args.name, outline, position=args.position, page_number=args.page_number, filename=filename)
                elif args.action == "remove":
                    outline = presalytics.lib.tools.workflows.remove_widget_by_name(args.name, outline, page_number=args.page_number, filename=filename)
            elif args.action == "patch":
                if not args.patch:
                    logger.error("Modifying an outline using the 'patch' action requires a [--patch] argument")
                    return
                try:
                    try:
                        patch = json.loads(args.patch)
                    except json.JSONDecodeError:
                        patch = ast.literal_eval(args.patch)
                except Exception as ex:
                    logger.error("A patch could not be created from [--patch]: {}".format(args.patch))
                    return
                outline = presalytics.lib.tools.workflows.apply_json_patch(outline, patch)
            _dump(outline, filename, True, args.json)
        if update:
            outline = presalytics.lib.tools.workflows.update_outline(outline, filename=filename, message=args.message)      
            _dump(outline, filename, True, args.json)  
        if push:
            if not message:
                pretty_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M")
                message = "Pushed from command line interface on " + pretty_time
            outline.info.revision_notes = message
            outline = presalytics.lib.tools.workflows.push_outline(outline, username=args.username, password=args.password)
        try:
            story_id = outline.story_id
        except:
            logger.error("A story outline could not be found or created.  Please use the [--file] option to designate a target outline.")
            return
        if ooxml:
            if args.story_id:
                story_id = args.story_id
            if not args.replace_id and args.action == "replace":
                logger.error("the [--replace-id] option is required when the 'action' argument is [replace]")
                return
            ooxml_file = args.ooxml_filepath
            if not os.path.exists(ooxml_file):
                cwd = os.getcwd()
                test_path = os.path.join(cwd, ooxml_file)
                if os.path.exists(test_path):
                    ooxml_file = test_path
                else:
                    logger.error("Could not find a path to file: {0}".format(ooxml_file))
                    return
            if args.action == "add" or args.action == "replace": 
                presalytics.lib.tools.ooxml_tools.add_ooxml_document_to_story(story_id, ooxml_file, replace_id=args.replace_id, username=args.username, password=args.password)
        if pull:
            if story_id == "empty":
                logger.error("A story outline needs a Story Id to be pulled from the Presalytics API. Please run 'presalytics push'")
                return
            else:
                if getattr(args, "id", None):
                    _id = args.id
                else:
                    _id = outline.story_id
                outline = presalytics.lib.tools.workflows.pull_outline(_id, username=args.username, password=args.password)
       
        if write:
            _dump(outline, filename, args.overwrite, args.json)
        if account:
            if args.delete:
                if args.all:
                    presalytics.lib.tools.workflows.delete_all_stories(username=args.username, password=args.password)
                else:
                    presalytics.lib.tools.workflows.delete_by_id(args.id, username=args.username, password=args.password)
        if share:
            presalytics.lib.tools.workflows.share_story(story_id, 
                                                           emails=args.emails, 
                                                           user_ids=args.user_ids, 
                                                           username=args.username,
                                                           password=args.password,
                                                           collaborator_type=args.collaborator_type)
        if story_id != 'empty':
            try:
                if args.view:
                    _open_page(story_id, "view")
                if args.manage:
                    _open_page(story_id, "manage")
                if args.show_story:
                    story = presalytics.lib.tools.workflows.get_story(story_id)
        
            except webbrowser.Error:
                logger.error("This environment does not have a webrowser loaded for use with python.")
                return
        else:
            logger.error("This outline does not yet have a story_id.  Please run 'presalytics push'.")
            return
        logger.info("\n\nStory Outline\n-------------\n\n{0}".format(yaml.dump(outline.to_dict())))
        if args.cron:
            presalytics.lib.tools.workflows.create_cron_target()
    except Exception as ex:
        if isinstance(ex, presalytics.lib.exceptions.PresalyticsBaseException):
            logger.error(ex.message) # noqa
        else:
            logger.exception(ex)
    finally:
        return


if __name__ == "__main__":
    main()