import os
from environs import Env

env = Env()
env.read_env()

PRESALYTICS = {
    'USERNAME': os.environ['PRESALYTICS_USERNAME'],
    'PASSWORD': os.environ['PRESALYTICS_PASSWORD'],
    'CLIENT_ID': os.environ.get('CLIENT_ID'),
    'CLIENT_SECRET': os.environ.get('CLIENT_SECRET'),
    'HOSTS': {}
}

try:
    ooxml_host = {
        'OOXML_AUTOMATION': os.environ['OOXML_AUTOMATION_HOST']
    }
    PRESALYTICS['HOSTS'].update(ooxml_host)
except KeyError:
    pass

try:
    story_host = {
        'STORY': os.environ['STORY_HOST'] + "/story"
    }
    PRESALYTICS['HOSTS'].update(story_host)
except KeyError:
    pass


try:
    site_host = {
        'SITE': os.environ['SITE_HOST']
    }
    PRESALYTICS['HOSTS'].update(site_host)
except KeyError:
    pass

try:
    PRESALYTICS['BROWSER_API_HOST'] = os.environ['BROWSER_API_HOST']
except KeyError:
    pass
