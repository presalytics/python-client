"""
Unit test for Client class
"""
import unittest
import os
import uuid
from presalytics.client.api import Client
from presalytics.lib.exceptions import ApiException

class test_client(unittest.TestCase):
    """ Test whether client accurately creates a configuration
        and establishes a connection to the server
    """
    def setUp(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'files', 'config.py')

    def test_client(self):
        """ 
        Tests for client configuration into presalytics api
        """
        client = Client(config_file=self.config_file)
        username = os.environ["PRESALYTICS_USERNAME"]
        self.assertEqual(client.doc_converter.api_client.username, username)
        self.assertEqual(client.ooxml_automation.api_client.configuration.host, os.environ["OOXML_AUTOMATION_HOST"])

    def test_module_config(self):
        from test.files.config import PRESALYTICS
        client = Client(config=PRESALYTICS)
        self.assertIsNotNone(client.ooxml_automation.api_client.client_id)

    def test_api_exception(self):
        exception_client = Client(config_file=self.config_file)
        bad_story_id = str(uuid.uuid4())
        try:
            body, status, headers = exception_client.story.story_id_get(bad_story_id)
        except Exception as e:
            self.assertEqual(ApiException, e.__class__)
        ignore_client = Client(config_file=self.config_file, ignore_api_exceptions=True)
        body, status, headers = ignore_client.story.story_id_get(bad_story_id)
        self.assertEqual(status, 404)


        


if __name__ == '__main__':
    unittest.main()
