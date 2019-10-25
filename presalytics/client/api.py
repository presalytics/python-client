import os
import cgi
import webbrowser
import time
import requests
import urllib.parse
import importlib.util
import logging
import json
from keycloak.keycloak_openid import KeycloakOpenID
from keycloak.exceptions import KeycloakGetError
from uuid import uuid4
import presalytics_doc_converter
import presalytics_ooxml_automation
import presalytics_story
from presalytics.lib.exceptions import LoginTimeout, MissingConfigException
from presalytics.lib.constants import (
    HOST,
    OIDC_REALM,
    DEFAULT_CLIENT_ID,
    OIDC_AUTH_HOST,
    JWT_KEY,
    LOGIN_PATH,
    API_CODE_URL,
    REDIRECT_URI
)
from presalytics.client.auth import AuthenticationMixIn, AuthConfig, TokenUtil

logger = logging.getLogger(__name__)


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
    """ Main PresalyticsClient base object """
    def __init__(
            self,
            config=None,
            config_file=None,
            delegate_login=False,
            **kwargs):

        if config:
            if "PRESALYTICS" in config:
                self.auth_config = AuthConfig(config["PRESALYTICS"])
            else:
                self.auth_config = AuthConfig(config)
        else:
            if config_file is None:
                config_file = os.getcwd() + os.path.sep + "config.py"
            if not os.path.exists(config_file):
                config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.py')
                if not os.path.exists(config_file):
                    raise MissingConfigException("Could not initialize. Config file 'config.py' not found.")
            config_spec = importlib.util.spec_from_file_location("config", config_file)
            self.auth_config = importlib.util.module_from_spec(config_spec)
            config_spec.loader.exec_module(self.auth_config)
        try:
            self.username = self.auth_config.PRESALYTICS['USERNAME']
        except KeyError:
            raise MissingConfigException("Mandatory configuration variable PRESALYTICS_USERNAME is missing from configuration.  Please reconfigure and retry.")
        try:
            self.password = self.auth_config.PRESALYTICS['PASSWORD']
            self.direct_grant = True
        except KeyError:
            self.password = None
            self.direct_grant = False
        try:
            self.client_id = self.auth_config.PRESALYTICS['CLIENT_ID']
        except KeyError:
            self.client_id = DEFAULT_CLIENT_ID
        try:
            self.client_secret = self.auth_config.PRESALYTICS['CLIENT_SECRET']
            self.confidential_client = True
        except KeyError:
            self.client_secret = None
            self.confidential_client = False

        try:
            self.site_host = self.auth_config.PRESALYTICS["HOSTS"]["SITE"]
        except KeyError:
            self.site_host = HOST
        self.login_sleep_interval = 5  # seconds
        self.login_timeout = 60  # seconds
        self._delegate_login = delegate_login
        self.oidc = KeycloakOpenID(
            server_url=OIDC_AUTH_HOST,
            realm_name=OIDC_REALM,
            client_id=self.client_id,
            verify=True
        )
        self.token_util = TokenUtil()
        self.token_util.token = self.refresh_token()

        doc_converter_api_client = DocConverterApiClientWithAuth(self, **kwargs)
        self.doc_converter = presalytics_doc_converter.DefaultApi(api_client=doc_converter_api_client)
        ooxml_automation_api_client = OoxmlAutomationApiClientWithAuth(self, **kwargs)
        self.ooxml_automation = presalytics_ooxml_automation.DefaultApi(api_client=ooxml_automation_api_client)
        story_api_client = StoryApiClientWithAuth(self, **kwargs)
        self.story = presalytics_story.DefaultApi(api_client=story_api_client)

    def login(self):
        try:
            if self.direct_grant:
                keycloak_token = self.oidc.token(username=self.username, password=self.password)
            else:
                keycloak_token = self._get_new_token_browser()
        except KeycloakGetError as e:
            if e.response_code == 404:
                logger.error("Received reponse code 404 from api authentication.  Indicates username does not exist.  Please recheck config and try again.")
            elif e.response_code == 401:
                logger.error("Received 401 response code from api authentication.  This user's access to this resource is unauthorized")
            elif e.response_code >= 500:
                logger.error("Server error.  Please try again later.")
            else:
                logger.error(e.error_message)
            raise MissingConfigException(e.error_message)
        self.token_util.process_keycloak_token(keycloak_token)
        return self.token_util.token

    def delegated_login(self, original_token, audience=None):
        """ Requires developer account and authorized client credentials """
        self.oidc.decode_token(original_token, JWT_KEY)
        kwargs = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": original_token
        }
        if audience is not None:
            kwargs.update(
                {
                    "audience": audience
                }
            )
        keycloak_token = self.oidc.token(**kwargs)
        self.token_util.process_keycloak_token(keycloak_token)
        return self.token_util.token["access_token"]

    def _get_new_token_browser(self):
        """
        Opens browser in on presalytics.io and prompts for user login.
        Retrieves authorization code from website and obtains api token
        """
        api_otp = uuid4()
        query = {
            "api_otp": api_otp
        }
        query_string = '?{}'.format(urllib.parse.urlencode(query))
        url = urllib.parse.urljoin(self.site_host, urllib.parse.urljoin(LOGIN_PATH, query_string))
        webbrowser.open_new_tab(url)
        auth_code = None
        payload = {
            "username": self.username,
            "api_otp": str(api_otp)
        }

        auth_code_url = urllib.parse.urljoin(self.site_host, API_CODE_URL)
        interval = 0
        while True:
            response = requests.post(auth_code_url, json=payload)
            if response.status_code != 200:
                if interval <= self.login_timeout:
                    interval += self.login_sleep_interval
                    time.sleep(self.login_sleep_interval)
                else:
                    raise LoginTimeout
            else:
                data = json.loads(response.content)
                break
        auth_code = data["authorization_code"]
        token = self.oidc.token(username=self.username, grant_type="authorization_code", code=auth_code, redirect_uri=REDIRECT_URI)
        return token

    def refresh_token(self):
        if self.token_util.is_api_access_token_expired():
            if self.token_util.is_api_refresh_token_expired():
                if not self._delegate_login:  # do not automatically log in at init
                    self.login()
                else:
                    self.token_util.token = None
            else:
                try:
                    refresh_token = self.token_util.token["refresh_token"]
                    self.token_util.token = self.oidc.refresh_token(refresh_token)
                except KeycloakGetError:
                    self.login()
            self.token_util._put_token_file()
        return self.token_util.token

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
