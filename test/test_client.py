"""
Unit test for Client class
"""
import unittest
import os
import uuid
import presalytics.lib.exceptions
import presalytics.client.api


class TestClient(unittest.TestCase):
    """ Test whether client accurately creates a configuration
        and establishes a connection to the server
    """
    def setUp(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'files', 'config.py')

    def test_client(self):
        """
        Tests for client configuration into presalytics api via device grant
        """
        if not presalytics.CONFIG.get("PASSWORD", None):
            client = presalytics.client.api.Client(config_file=self.config_file)
            username = os.environ["PRESALYTICS_USERNAME"]
            self.assertEqual(client.username, username)
            self.assertEqual(client.ooxml_automation.api_client.configuration.host, os.environ["OOXML_AUTOMATION_HOST"])
            self.assertNotEqual(client.token_util.token.get("access_token", None), None)
       
    def test_password_grant(self):
        """
        tests if password grant works
        """
        if presalytics.CONFIG.get("PASSWORD", None):
            username = presalytics.CONFIG.get("USERNAME")
            password = presalytics.CONFIG.get("PASSWORD")
            client_id = os.environ.get("CLIENT_ID")
            client_secret = os.environ.get("CLIENT_SECRET")
            client = presalytics.client.api.Client(
                username=username, 
                password=password, 
                client_id=client_id, 
                client_secret=client_secret
            )

    def test_module_config(self):
        from test.files.config import PRESALYTICS
        client = presalytics.client.api.Client(config=PRESALYTICS)
        self.assertIsNotNone(client.client_id)

    def test_api_exception(self):
        exception_client = presalytics.client.api.Client(config_file=self.config_file)
        bad_story_id = str(uuid.uuid4())
        try:
            body, status, headers = exception_client.story.story_id_get(bad_story_id)
        except Exception as e:
            self.assertEqual(presalytics.lib.exceptions.ApiException, e.__class__)
        ignore_client = presalytics.client.api.Client(config_file=self.config_file, ignore_api_exceptions=True)
        body, status, headers = ignore_client.story.story_id_get(bad_story_id)
        self.assertEqual(status, 404)

    def test_file_download(self):
        test_upload_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'star.pptx')
        client = presalytics.client.api.get_client()
        try:
            test_story = client.story.story_post_file(file=test_upload_file)
            download_folder = os.path.dirname(os.path.abspath(__file__))
            test_filename = "test-file.pptx"
            client.download_file(test_story.id, test_story.ooxml_documents[0].ooxml_automation_id, filename=test_filename, download_folder=download_folder)
            target_path = os.path.join(download_folder, test_filename)
            self.assertTrue(os.path.exists(target_path))
        finally:
            try:
                os.remove(target_path)
            except Exception:
                pass
