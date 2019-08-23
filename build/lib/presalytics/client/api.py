import pkg_resources
import presalytics_doc_converter
from .auth import AuthenticationMixIn

class ApiClientWithAuth(AuthenticationMixIn, presalytics_doc_converter.api_client.ApiClient):
    def __init__(self, config_file=None, **kwargs):
        AuthenticationMixIn.__init__(self, config_file=config_file)
        presalytics_doc_converter.api_client.ApiClient.__init__(self, **kwargs)
        try:
            VER = pkg_resources.require("presalytics")[0].version
        except:
            VER = 'build'
        self.user_agent = 'presalytics-python-client/' + VER

class Client(object):
    def __init__(self, config_file=None, **kwargs):
        api_client = ApiClientWithAuth(config_file, **kwargs)
        self.doc_converter = presalytics_doc_converter.DefaultApi(api_client=api_client)

