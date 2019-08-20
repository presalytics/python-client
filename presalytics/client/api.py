import presalytics_doc_converter
from .auth import AuthenticationMixIn

class ApiClientWithAuth(AuthenticationMixIn, presalytics_doc_converter.api_client.ApiClient):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

presalytics_doc_converter.api_client.ApiClient = ApiClientWithAuth

class Client(object):
    def __init__(self, *args, **kwargs):
        self.doc_converter = presalytics_doc_converter.DefaultApi()

