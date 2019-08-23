import pkg_resources
import presalytics_doc_converter
import presalytics_ooxml_automation
from .auth import AuthenticationMixIn

def get_user_agent():
    try:
        VER = pkg_resources.require("presalytics")[0].version
    except:
        VER = 'build'
    return "presalytics-python-client/{0}".format(VER)


class DocConverterApiClientWithAuth(AuthenticationMixIn, presalytics_doc_converter.api_client.ApiClient):
    def __init__(self, config_file=None, **kwargs):
        AuthenticationMixIn.__init__(self, config_file=config_file)
        presalytics_doc_converter.api_client.ApiClient.__init__(self, **kwargs)
        self.user_agent = get_user_agent()

class OoxmlAutomationApiClientWithAuth(AuthenticationMixIn, presalytics_ooxml_automation.api_client.ApiClient):
    def __init__(self, config_file=None, **kwargs):
        AuthenticationMixIn.__init__(self, config_file=config_file)
        presalytics_ooxml_automation.api_client.ApiClient.__init__(self, **kwargs)
        self.user_agent = get_user_agent()


class Client(object):
    def __init__(self, config_file=None, **kwargs):
        doc_converter_api_client = DocConverterApiClientWithAuth(config_file, **kwargs)
        self.doc_converter = presalytics_doc_converter.DefaultApi(api_client=doc_converter_api_client)
        ooxml_automation_api_client = OoxmlAutomationApiClientWithAuth(config_file, **kwargs)
        self.ooxml_automation = presalytics_ooxml_automation.DefaultApi(api_client=ooxml_automation_api_client)

