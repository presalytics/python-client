import os
from environs import Env

env = Env()
env.read_env()

PRESALYTICS = {
    'USERNAME': os.environ['PRESALYTICS_USERNAME'],
    'PASSWORD': os.environ['PRESALYTICS_PASSWORD'],
    'HOSTS': {}
}

try:
    ooxml_host = {
        'OOXML_AUTOMATION' : os.environ['OOXML_AUTOMATION_HOST']
    }
    PRESALYTICS['HOSTS'].update(ooxml_host)
except KeyError:
    pass

try:
    story_host = {
        'STORY' : os.environ['STORY_HOST']
    }
    PRESALYTICS['HOSTS'].update(story_host)
except KeyError:
    pass

