"""
Base Configuration File for presalytics client

By default, the presalytics client attempts to read its configuration values from 
an env file or the host machine's system environment values.

Copy this file to the current working directory (commnad: 'os.getcwd()' ) of your python script to use.
These values can set directly as well, but it is not advised.  Leaving configuration data in plain text on 
your host machine can open security risks for your organization.
"""

import os
from environs import Env

env = Env()
try:
    env.read_env()
except:
    pass

PRESALYTICS = {
    'USERNAME': os.environ['PRESALYTICS_USERNAME'],
    'HOSTS': {}
}

try:
    user_pass = {
        'PASSWORD': os.environ['PRESALYTICS_PASSWORD']
    }
    PRESALYTICS.update(user_pass)
except KeyError:
    pass

try:
    ooxml_host = {
        'OOXML_AUTOMATION' : os.environ['OOXML_AUTOMATION_HOST']
    }
    PRESALYTICS['HOSTS'].update(ooxml_host)
except KeyError:
    pass
