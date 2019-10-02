import os

SPEC = {
        "update": False,
        "update_type": "patch",
        "endpoint": "https://api.presalytics.io/ooxml-automation/docs/v1-no-tags/openapi.json",
        "package_name": "presalytics_ooxml_automation",
        "package_url": "https://github.com/presalytics/ooxml-automation-python-client.git",
        "readme_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md"),
        "setuppy_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "setup.py"),
        "pypi_url": "https://pypi.org/project/presalytics-ooxml-automation/"
}