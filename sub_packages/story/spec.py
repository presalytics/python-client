import os

SPEC = {
        "update": False,
        "update_type": "patch",
        "endpoint": "https://api.presalytics.io/story/openapi.json",
        "package_name": "presalytics_story",
        "package_url": "https://github.com/presalytics/story-python-client.git",
        "readme_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md"),
        "setuppy_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "setup.py"),
        "pypi_url": "https://pypi.org/project/presalytics-story/"
}