"""
Unit test for Client class
"""
import unittest
import os
from presalytics.client.api import Client

class test_client(unittest.TestCase):
    """ Test whether client accurately creates a configuration
        and establishes a connection to the server
    """
    def setUp(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'test_files', 'config.py')

    def test_codelens(self):
        pass

    def test_client_connection(self):
        """ 
        Tests for client connection to presalytics api
        TODO: integration test - eliminate later or add mock
        """
        client = Client(self.config_file)
        hello = client.doc_converter.say_hello()
        self.assertEqual("hello world!", hello.text)


if __name__ == '__main__':
    unittest.main()
