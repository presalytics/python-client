"""
Base Configuration File for presalytics client

By default, the presalytics client attempts to read its configuration values from 
a `config.py`.  Users can use this file to read a configuration from the host machine's 
environment variables.  Just rename it config.py.  This way, user do not have to leaving configuration 
data in plain text on their host machines and create potential security risks.
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
