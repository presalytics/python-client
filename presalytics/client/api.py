import os, cgi
import presalytics_doc_converter
import presalytics_ooxml_automation
import presalytics_story
from presalytics.client.auth import AuthenticationMixIn


class DocConverterApiClientWithAuth(AuthenticationMixIn, presalytics_doc_converter.api_client.ApiClient):
    def __init__(self, **kwargs):
        AuthenticationMixIn.__init__(self, **kwargs)
        presalytics_doc_converter.api_client.ApiClient.__init__(self)
        self.update_configuration()

class OoxmlAutomationApiClientWithAuth(AuthenticationMixIn, presalytics_ooxml_automation.api_client.ApiClient):
    def __init__(self, **kwargs):
        AuthenticationMixIn.__init__(self, **kwargs)
        presalytics_ooxml_automation.api_client.ApiClient.__init__(self)
        self.update_configuration()

class StoryApiClientWithAuth(AuthenticationMixIn, presalytics_story.api_client.ApiClient):
    def __init__(self, **kwargs):
        AuthenticationMixIn.__init__(self, **kwargs)
        presalytics_story.api_client.ApiClient.__init__(self)
        self.update_configuration()



class Client(object):
    def __init__(self, **kwargs):
        doc_converter_api_client = DocConverterApiClientWithAuth(**kwargs)
        self.doc_converter = presalytics_doc_converter.DefaultApi(api_client=doc_converter_api_client)
        ooxml_automation_api_client = OoxmlAutomationApiClientWithAuth(**kwargs)
        self.ooxml_automation = presalytics_ooxml_automation.DefaultApi(api_client=ooxml_automation_api_client)
        story_api_client = StoryApiClientWithAuth(**kwargs)
        self.story =presalytics_story.DefaultApi(api_client=story_api_client)

    def download_file(self, story_id, ooxml_automation_id, download_folder=None, filename=None, **kwargs):
        response, status, headers = self.story.story_id_file_ooxmlautomationid_get_with_http_info(story_id, ooxml_automation_id, _preload_content=False)
        if download_folder is None:
            download_folder = os.getcwd()
        if filename is None:            
            cd_header = headers.get('Content-Disposition')
            _, params = cgi.parse_header(cd_header)
            filename = params["filename"]
        filepath = os.path.join(download_folder, filename)
        with open(filepath, 'wb') as f:
            f.write(response.data)

        
        
        
        

        
        
