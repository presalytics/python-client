import os
from environs import Env

env = Env()
env.read_env()

doc_converter_host = env("DOC_CONVERTER_HOST", "https://api.presalytics.io")

SPEC = {
        "update": False,
        "update_type": "patch",
        "endpoint": "{}/doc-converter/openapi.json".format(doc_converter_host),
        "package_name": "presalytics_doc_converter",
        "package_url": "https://github.com/presalytics/doc-converter-python-client.git",
        "readme_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md"),
        "setuppy_path": os.path.join(os.path.dirname(os.path.realpath(__file__)), "setup.py"),
        "pypi_url": "https://pypi.org/project/presalytics-doc-converter/"
}