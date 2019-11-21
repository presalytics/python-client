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
