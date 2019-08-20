import os
from environs import Env

env = Env()
env.read_env()

PRESALYTICS = {
    'USERNAME': os.environ['PRESALYTICS_USERNAME'],
    'PASSWORD': os.environ['PRESALYTICS_PASSWORD'],
    'CLIENT_ID': os.environ['PRESALYTICS_CLIENT_ID'],
    'CLIENT_SECRET': os.environ['PRESALYTICS_CLIENT_SECRET']
    
}

CERT_PATH = os.environ['CERT_PATH']