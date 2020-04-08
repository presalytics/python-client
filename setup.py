# coding: utf-8

"""
    Presalytics Python Client

    Tools to interfacing with the Presalytics.io API.
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "presalytics"
VERSION = "0.4.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "urllib3 >= 1.15",
    "six >= 1.10",
    "certifi",
    "python-dateutil",
    "flask",
    "requests",
    "python-keycloak",
    "environs",
    "matplotlib",
    "lxml",
    "pyyaml",
    "mpld3",
    "libsass",
    "jsonschema",
    "semantic_version",
    "jsonpatch",
    "pandas",
    "wsgi_microservice_middleware>=0.1.5"
]

with open("README.md", "r") as fh:
    long_description = fh.read()
    

setup(
    name=NAME,
    version=VERSION,
    description="Prealytics Python Client",
    author_email="inquiries@presalytics.io",
    url="https://presalytics.io/docs",
    keywords=["Presalytics"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=long_description,
    entry_points={
        "console_scripts": [
            "presalytics = presalytics.cli:main",
        ],
    },
)
