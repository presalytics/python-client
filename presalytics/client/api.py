import os
import cgi
import webbrowser
import time
import requests
import urllib.parse
import importlib.util
import logging
import json
import keycloak
import environs
import presalytics
import presalytics.lib.exceptions
import presalytics.lib.constants as cnst
import presalytics.client.auth
import presalytics.client.presalytics_ooxml_automation.api_client
import presalytics.client.presalytics_story.api_client
import presalytics.client.presalytics_doc_converter.api_client
from uuid import uuid4

logger = logging.getLogger(__name__)

env = environs.Env()


class Client(object):
    """ Main PresalyticsClient base object """
    def __init__(
            self,
            delegate_login=False,
            token=None,
            cache_tokens=True,
            **kwargs):
        try:
            self.username = presalytics.CONFIG['USERNAME']
        except KeyError:
            raise presalytics.lib.exceptions.MissingConfigException("Mandatory configuration variable PRESALYTICS_USERNAME is missing from configuration.  Please reconfigure and retry.")
        try:
            self.password = presalytics.CONFIG['PASSWORD']
            self.direct_grant = True
        except KeyError:
            self.password = None
            self.direct_grant = False
        try:
            self.client_id = presalytics.CONFIG['CLIENT_ID']
        except KeyError:
            self.client_id = cnst.DEFAULT_CLIENT_ID
        try:
            self.client_secret = presalytics.CONFIG['CLIENT_SECRET']
            self.confidential_client = True
        except KeyError:
            self.client_secret = None
            self.confidential_client = False
        self.verify_https = env.bool("VERIFY_HTTPS", True)
        try:
            self.site_host = presalytics.CONFIG["HOSTS"]["SITE"]
        except KeyError:
            self.site_host = cnst.SITE_HOST
        self.login_sleep_interval = 5  # seconds
        self.login_timeout = 60  # seconds
        try:
            self.redirect_uri = presalytics.CONFIG["REDIRECT_URI"]
        except KeyError:
            self.redirect_uri = cnst.REDIRECT_URI
        if delegate_login or presalytics.CONFIG.get("DELEGATE_LOGIN", False):
            self._delegate_login = True
        else:
            self._delegate_login = False
        self.oidc = keycloak.KeycloakOpenID(
            server_url=cnst.OIDC_AUTH_HOST,
            realm_name=cnst.OIDC_REALM,
            client_id=self.client_id,
            verify=self.verify_https
        )
        self.token_util = presalytics.client.auth.TokenUtil(token_cache=cache_tokens)
        if token:
            self.token_util.token = token
            if self.token_util.token_cache:
                self.token_util._put_token_file()
        if not self._delegate_login:
            self.token_util.token = self.refresh_token()

        doc_converter_api_client = DocConverterApiClientWithAuth(self, **kwargs)
        self.doc_converter = presalytics.client.presalytics_doc_converter.DefaultApi(api_client=doc_converter_api_client)
        ooxml_automation_api_client = OoxmlAutomationApiClientWithAuth(self, **kwargs)
        self.ooxml_automation = presalytics.client.presalytics_ooxml_automation.DefaultApi(api_client=ooxml_automation_api_client)
        story_api_client = StoryApiClientWithAuth(self, **kwargs)
        self.story = presalytics.client.presalytics_story.DefaultApi(api_client=story_api_client)

    def login(self):
        try:
            if self.direct_grant:
                keycloak_token = self.oidc.token(username=self.username, password=self.password)
            else:
                keycloak_token = self._get_new_token_browser()
        except keycloak.exceptions.KeycloakGetError as e:
            if e.response_code == 404:
                logger.error("Received reponse code 404 from api authentication.  Indicates username does not exist.  Please recheck config and try again.")
            elif e.response_code == 401:
                logger.error("Received 401 response code from api authentication.  This user's access to this resource is unauthorized")
            elif e.response_code >= 500:
                logger.error("Server error.  Please try again later.")
            else:
                logger.error(e.error_message)
            raise presalytics.lib.exceptions.MissingConfigException(e.error_message)
        self.token_util.process_keycloak_token(keycloak_token)
        return self.token_util.token

    def exchange_token(self, original_token, audience=None):
        """ Requires developer account and authorized client credentials """
        self.oidc.decode_token(original_token, cnst.JWT_KEY)
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
            "api_otp": api_otp,
            "client_id": self.client_id,
            "next": self.redirect_uri
        }
        query_string = '?{}'.format(urllib.parse.urlencode(query))
        url = urllib.parse.urljoin(self.site_host, urllib.parse.urljoin(cnst.LOGIN_PATH, query_string))
        webbrowser.open_new_tab(url)
        auth_code = None
        payload = {
            "username": self.username,
            "api_otp": str(api_otp),
            "client_id": self.client_id
        }

        auth_code_url = urllib.parse.urljoin(self.site_host, cnst.API_CODE_URL)
        interval = 0
        while True:
            response = requests.post(auth_code_url, json=payload, verify=self.verify_https)
            if response.status_code != 200:
                if interval <= self.login_timeout:
                    interval += self.login_sleep_interval
                    time.sleep(self.login_sleep_interval)
                else:
                    raise presalytics.lib.exceptions.LoginTimeout()
            else:
                data = json.loads(response.content)
                break
        if data.get("token", None):
            #  pick up otp token off presalytics backend
            token = data.get("token") 
        else:
            # support oidc authorization code flow
            auth_code = data["authorization_code"]
            token = self.oidc.token(username=self.username, grant_type="authorization_code", code=auth_code, redirect_uri=self.redirect_uri)
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
                except keycloak.exceptions.KeycloakGetError:
                    if not self._delegate_login:
                        self.login()
            if self.token_util.token_cache:
                self.token_util._put_token_file()
        return self.token_util.token

    def get_auth_header(self):
        self.refresh_token()
        auth_header = {
            "Authorization": "Bearer " + self.token_util.token["access_token"]
        }
        return auth_header

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


class DocConverterApiClientWithAuth(presalytics.client.auth.AuthenticationMixIn, presalytics.client.presalytics_doc_converter.api_client.ApiClient):
    def __init__(self, parent: Client, **kwargs):
        presalytics.client.auth.AuthenticationMixIn.__init__(self, parent, **kwargs)
        presalytics.client.presalytics_doc_converter.api_client.ApiClient.__init__(self)
        self.update_configuration()


class OoxmlAutomationApiClientWithAuth(presalytics.client.auth.AuthenticationMixIn, presalytics.client.presalytics_ooxml_automation.api_client.ApiClient):
    def __init__(self, parent: Client, **kwargs):
        presalytics.client.auth.AuthenticationMixIn.__init__(self, parent, **kwargs)
        presalytics.client.presalytics_ooxml_automation.api_client.ApiClient.__init__(self)
        self.update_configuration()


class StoryApiClientWithAuth(presalytics.client.auth.AuthenticationMixIn, presalytics.client.presalytics_story.api_client.ApiClient):
    def __init__(self, parent: Client, **kwargs):
        presalytics.client.auth.AuthenticationMixIn.__init__(self, parent, **kwargs)
        presalytics.client.presalytics_story.api_client.ApiClient.__init__(self)
        self.update_configuration()
