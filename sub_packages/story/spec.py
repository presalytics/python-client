import os
from environs import Env

env = Env()
env.read_env()

host = env("STORY_HOST", "https://api.presalytics.io")

SPEC = {
        "update": True,
        "update_type": "patch",
        "endpoint": "{0}/story/no_tags_spec".format(host),
        "package_name": "presalytics_story",
        "package_url": "https://github.com/presalytics/story-python-client.git",
        "readme_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md"),
        "setuppy_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "setup.py"),
        "pypi_url": "https://pypi.org/project/presalytics-story/"
}