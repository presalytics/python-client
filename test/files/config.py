import os
from environs import Env

env = Env()
env.read_env()

PRESALYTICS = {
    'USERNAME': os.environ['PRESALYTICS_USERNAME'],
    'PASSWORD': os.environ['PRESALYTICS_PASSWORD']
    
}
