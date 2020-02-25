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
import datetime
import presalytics.lib.constants
import presalytics.lib.tools.story_tools
import presalytics.lib.tools.workflows


logger = logging.getLogger(__name__)

description = """
Presaltyics Python Library
--------------------------
Version: {version}

Create live presentations, dashboards, and persistent analytics,
and interact with the Presaltyics API.

Please review the push, pull, and create subcommands for more options.

For more information about the Presaltyics API, please visit 
<https://presaltyics.io> or send your questions to inquires@presaltyics.io.

Command Line Instructions
-------------------------
""".format(version=presalytics.__version__)

parser = argparse.ArgumentParser(
    description=description,
    epilog="Further documentation is available at <https://presaltyics.io/docs/>.",
    formatter_class=argparse.RawTextHelpFormatter,
    prog='presalytics'
)
file_help = "The filename of the Story Outline. Defaults to 'story.yaml'"
parser.add_argument('-f', '--file', default='story.yaml', action='store', help=file_help)
parser.add_argument('--version', action='version', version=presalytics.__version__)
parser.add_argument('--view', default=False, action='store_true', help='View a Story in the browser')
parser.add_argument('--manage', default=False, action='store_true', help="""Go to the Story's management page""")
parser.add_argument('-v', '--verbose', default=False, action='store_true', help="Increases the detail in log output")


yaml_help = "Writes file updates to YAML format.  Yaml is the default."
json_help = "Writes file updates to JSON format"
overwrite_help = "Forces (o)verwrite of file with returned Story Outline (if exists)"
username_help = "Overrides the username in presalytics.CONFIG (if present)"
password_help = "The user's Presalytics API password"
metavar = "These commands come after the above optional arguments (when present)"
subparsers = parser.add_subparsers(title='Story API Commands', prog='presalytics', metavar=metavar, dest='story_api')

push_description = """
Pushes a Story Outline revision to the Presalytics API
Story service, and writes the updated story outline to a local file (--file)
"""
push = subparsers.add_parser('push', description=push_description, help='Push a Story Outline revision')
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
`presaltyics.COMPONENTS` at run-time.  Widget and page instances are loaded 
into `presalytics.COMPONENTS` from the current working directory and other 
configured folders at import of the presaltyics module.
"""

create_epilog = """
See https://presalytics.io/docs/configuration/ for more information.
"""

name_help = """
The name of the widget or page instance to create a Story Outline from.
"""
create = subparsers.add_parser('create', description=create_description, help='Create a Story Outline', epilog=create_epilog)
create.add_argument('name', action='store', help=name_help)
create_options = create.add_mutually_exclusive_group(required=True)
create_options.add_argument('--widget', default=False, action='store_true', help="Create a Story Outline from a widget instance")
create_options.add_argument('--page', default=False, action='store_true', help="Create a Story Outline from a page instance")
create.add_argument('-o', '--overwrite', default=False, action='store_true', help=overwrite_help)
create.add_argument('-u', '--username', default=None, action='store', help=username_help)
create.add_argument('-p', '--password', default=None, action='store', help=password_help)
create.add_argument('-s', '--source', default=None, action='store', help="The module containing the instance.  Needed only if instance not auto-loaded into presalytics.CONFIG")
create_output_options = create.add_mutually_exclusive_group(required=False)
create_output_options.add_argument('-y', '--yaml', default=False, action='store_true', help=yaml_help)
create_output_options.add_argument('-j', '--json', default=False, action='store_true', help=json_help)

share_description = """
Control permissions for owners, editors, promoters, and viewer or your stories
"""

share = subparsers.add_parser('share', description=share_description, help='Share Stories')
share.add_argument('--user-ids', action='store', help='A comma-separated list of the Presaltyics API user IDs of users you what to share this story with.')
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
delete_group.add_argument('--id', default=None, help='The Presaltyics API Story service Id of the story you want to delete.')
account.add_argument('-u', '--username', default=None, action='store', help=username_help)
account.add_argument('-p', '--password', default=None, action='store', help=password_help)




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
        if args.verbose:
            for lg in lgs:
                lg.setLevel(logging.DEBUG)
        else:
            for lg in lgs:
                lg.setLevel(logging.ERROR)
        write = False
        pull = False
        push = False
        account = False
        share = False
        outline = None
        message = getattr(args, "message", None)
        if args.story_api == "create":
            # create outline from page/widget
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
        elif args.story_api == "pull":
            push = False
            pull = True
            write = True
        elif args.story_api == "account":
            account = True
        elif args.story_api == "share":
            share = True
        else:
            push = False
            pull = False
            write = False
            #load story outline from file
        try:
            if not outline:
                if not os.path.exists(filename):
                    current_dir = os.getcwd()
                    abs_filename = os.path.join(current_dir, filename)
                    if os.path.exists(abs_filename):
                        filename = abs_filename
                    else:
                        logger.error("Could not file file: {}".format(filename))
                        return
                outline = _load_file(filename)
        except Exception:
            logger.error("Error handling file: {}".format(filename))
            return
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
        if pull:
            if story_id == "empty":
                logger.error("A story outline needs a Story Id to be pulled from the Presaltyics API. Please run 'presalytics push'")
                return
            else:
                if args.id:
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
            except webbrowser.Error:
                logger.error("This environment does not have a webrowser loaded for use with python.")
                return
        else:
            logger.error("This outline does not yet have a story_id.  Please run 'presalytics push'.")
            return
        logger.info("\n\nStory Outline\n-------------\n\n{0}".format(yaml.dump(outline.to_dict())))
    except Exception as ex:
        if isinstance(ex, presalytics.lib.exceptions.PresalyticsBaseException):
            logger.error(ex.message) # noqa
        else:
            logger.exception(ex)
    finally:
        return


if __name__ == "__main__":
    main()