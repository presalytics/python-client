# coding: utf-8

"""
    Presalytics Python Client

    Tools to interfacing with the Presalytics.io API.
"""
import os
from setuptools import setup, find_packages  # noqa: H301

NAME = "presalytics"
VERSION = "0.6.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools


def get_requirements():
    thelibFolder = os.path.dirname(os.path.realpath(__file__))
    requirementPath = thelibFolder + '/requirements.txt'
    install_requires = []
    if os.path.isfile(requirementPath):
        with open(requirementPath) as f:
            install_requires = f.read().splitlines()
    return install_requires


REQUIRES = get_requirements()

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name=NAME,
    version=VERSION,
    description="Presalytics Python Client",
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
