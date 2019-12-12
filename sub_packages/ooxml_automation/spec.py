import os
from environs import Env

env = Env()
env.read_env()

ooxml_host = env("OOXML_AUTOMATION_HOST", "https://api.presalytics.io")

SPEC = {
        "update": False,
        "update_type": "patch",
        "endpoint": "{0}/ooxml-automation/docs/v1-no-tags/openapi.json".format(ooxml_host),
        "package_name": "presalytics_ooxml_automation",
        "package_url": "https://github.com/presalytics/ooxml-automation-python-client.git",
        "readme_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md"),
        "setuppy_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "setup.py"),
        "pypi_url": "https://pypi.org/project/presalytics-ooxml-automation/"
}
