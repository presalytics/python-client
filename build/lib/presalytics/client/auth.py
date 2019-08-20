import requests, os, webbrowser, json
import importlib.util
from queue import Queue
from threading import Thread
from datetime import datetime, timedelta
from dateutil import parser as dateparser
from keycloak.keycloak_openid import KeycloakOpenID
from presalytics.localhost.server import app
from presalytics.lib.exceptions import MissingConfigException, MisConfiguredTokenException, InvalidTokenException
from presalytics.lib.constants import (
    HOST, 
    PORT, 
    OIDC_WELL_KNOWN, 
    OIDC_TOKEN, 
    OIDC_REALM, 
    DEFAULT_CLIENT_ID, 
    OIDC_AUTH_HOST,
    OIDC_AUTH_PORT,
    REDIRECT_URI,
    TOKEN_FILE,
    LOCALHOST_SERVER,
    LOCALHOST_PORT
)


q = Queue()

class FlaskThread(Thread):
    def __init__(self, *args, **kwargs):
        self.server = LOCALHOST_SERVER
        self.port = LOCALHOST_PORT
        super(FlaskThread, self).__init__(*args, **kwargs)
        
    def run(self):
        app.run(self.server, self.port, debug=False, load_dotenv=False)
        return

class TokenUtil(object):
    def __init__(self, token=None, token_file=None):
        if token_file is None:
            self.token_file = TOKEN_FILE
        else:
            self.token_file = token_file
        try:
            self._load_token_file()
        except:
            pass
        if token is not None:
            try:
                self.token = {
                    'access_token':  token['access_token'],
                    'access_token_expire_time': token["access_token_expire_time"],
                    'refresh_token': token["refresh_token"],
                    'refresh_token_expire_time': token["refresh_token_expire_time"]
                }
                self._put_token_file()
            except:
                raise MisConfiguredTokenException
        
    def is_api_access_token_expired(self):
        expire_datetime = dateparser.parse(self.token['access_token_expire_time'])
        if expire_datetime < datetime.now():
            return True
        return False

    def is_api_refresh_token_expired(self):
        expire_datetime = dateparser.parse(self.token['refresh_token_expire_time'])
        if expire_datetime < datetime.now():
            return True
        return False
 
    def _load_token_file(self):
        self.token = self.load_token_from_file(self.token_file)

    def _put_token_file(self):
        self.put_token_file(self.token, self.token_file)

    @staticmethod
    def put_token_file(token, token_filepath):
        with open(token_filepath, mode='w+') as newtoken:
            json.dump(token, newtoken)

    @staticmethod
    def load_token_from_file(token_filepath):
        with open(token_filepath, 'r') as token_file:
            token = json.load(token_file)
        return token
 
class AuthenticationMixIn(object):
    def __init__(self, config_file=None, *args, **kwargs):
        if config_file is None:
            config_file = os.getcwd() + os.path.sep + "config.py"
        if not os.path.exists(config_file):
            raise MissingConfigException
        config_spec = importlib.util.spec_from_file_location("config", config_file)
        config = importlib.util.module_from_spec(config_spec)
        config_spec.loader.exec_module(config)
        if config.PRESALYTICS['PASSWORD'] is None:
            self.direct_grant = False
            self.password = None
        else:
            self.direct_grant = True
            self.password = config.PRESALYTICS['PASSWORD']
        if config.PRESALYTICS['CLIENT_ID'] is None:
            self.client_id = DEFAULT_CLIENT_ID
        else:
            self.client_id = config.PRESALTYICS['CLIENT_ID']
        self.oidc = KeycloakOpenID(
            server_url=OIDC_AUTH_HOST,
            realm_name=OIDC_REALM,
            client_id=self.client_id,
            verify=False
        )
        self.token_util = TokenUtil(TOKEN_FILE)
        self.token_util.token = self.refresh_token()
        self.server_thread = FlaskThread()

        super(AuthenticationMixIn, self).__init__(*args, **kwargs)


    def login(self):
        if self.direct_grant:
            if config_file is None:
                config_file = os.getcwd() + os.path.sep + "config.py"
            if not os.path.exists(config_file):
                raise MissingConfigException
            config_spec = importlib.util.spec_from_file_location("config", config_file)
            config = importlib.util.module_from_spec(config_spec)
            config_spec.loader.exec_module(config)
            self.password = config.PRESALYTICS['PASSWORD']
            token = self.oidc.token(username=self.username, password=self.password)
        else:
            url = self.oidc.auth_url(REDIRECT_URI)
            token = self._get_new_token_browser(url)
        return token

    def _get_new_token_browser(self, url):
        self.server_thread.start()
        webbrowser.open_new(url)
        auth_code = None
        while True:
            item  = q.get()
            if item is not None:    
                auth_code = item
                q.task_done()

        q.join()
        token = self.oidc.token(username=self.username, grant_type="code", code=auth_code)
        return token



    def refresh_token(self):
        if self.token_util.is_api_access_token_expired():
            if self.token_util.is_api_refresh_token_expired():
                self.token_util.token = self.login()
            else:
                refresh_token = self.token_util.token["refresh_token"]
                self.token_util.token = self.oidc.refresh_token(refresh_token)
            self.token_util._put_token_file()
        return self.token_util.token

    def get_auth_header(self):
        self.refresh_token()
        auth_header = {
            "Authorization": "Bearer " + self.token_util.token["access_token"]
        }
        return auth_header

    
    def __call_api(self, resource_path, method, path_params=None,
            query_params=None, header_params=None, body=None, post_params=None,
            files=None, response_type=None, auth_settings=None,
            _return_http_data_only=None, collection_formats=None,
            _preload_content=True, _request_timeout=None, _host=None):
        """
        Overrideing __call_api to force token check, refresh on each api call, 
        rather than at class initialized (good the ipython notebooks)
        """

        auth_header = self.get_auth_header()
        super(AuthenticationMixIn, self).__call_api(header_params=auth_header)

                


        



            