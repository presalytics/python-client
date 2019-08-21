import presalytics_doc_converter
from .auth import AuthenticationMixIn

class ApiClientWithAuth(AuthenticationMixIn, presalytics_doc_converter.api_client.ApiClient):
    def __init__(self, config_file=None, **kwargs):
        super(ApiClientWithAuth, self).__init__(config_file, **kwargs)

presalytics_doc_converter.api_client.ApiClient = ApiClientWithAuth

class Client(object):
    def __init__(self, config_file=None, **kwargs):
        api_client = ApiClientWithAuth(config_file, **kwargs)
        self.doc_converter = presalytics_doc_converter.DefaultApi(api_client=api_client)

