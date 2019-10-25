import json
import logging

logger = logging.getLogger('presalytics.teller')
logger.info("Importing presalytics story teller")

class StoryWriter(object):
    """
    This class takes input of various MimeTypes and transforms them
    into standarized json object - a 'Story Outline' that the revealer class and can
    parse into a reveal.js presentation
    """
    def __init__(self):
        pass

    def create_from_document(self, document):

        dummy_dict = {}
        return dummy_dict


class Revealer(object):
    """
    This class renders 'Story Outines' to reveal.js presentations
    """
    def __init__(self, story_outline):
        self.story_outline = story_outline
        pass

    def render(self, include_scripts=False):
        return ''

logger.info("Presalytics story teller import complete")
    
