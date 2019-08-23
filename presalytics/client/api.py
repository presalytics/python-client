import presalytics_doc_converter
import presalytics_ooxml_automation
from .auth import AuthenticationMixIn


class DocConverterApiClientWithAuth(AuthenticationMixIn, presalytics_doc_converter.api_client.ApiClient):
    def __init__(self, config_file=None, **kwargs):
        AuthenticationMixIn.__init__(self, config_file=config_file)
        presalytics_doc_converter.api_client.ApiClient.__init__(self, **kwargs)
        self.update_configuration()

class OoxmlAutomationApiClientWithAuth(AuthenticationMixIn, presalytics_ooxml_automation.api_client.ApiClient):
    def __init__(self, config_file=None, **kwargs):
        AuthenticationMixIn.__init__(self, config_file=config_file)
        presalytics_ooxml_automation.api_client.ApiClient.__init__(self, **kwargs)
        self.update_configuration()


class Client(object):
    def __init__(self, config_file=None, **kwargs):
        doc_converter_api_client = DocConverterApiClientWithAuth(config_file, **kwargs)
        self.doc_converter = presalytics_doc_converter.DefaultApi(api_client=doc_converter_api_client)
        ooxml_automation_api_client = OoxmlAutomationApiClientWithAuth(config_file, **kwargs)
        self.ooxml_automation = presalytics_ooxml_automation.DefaultApi(api_client=ooxml_automation_api_client)

