import requests, os, webbrowser, json, logging
import importlib.util
from queue import Queue
from threading import Thread
from datetime import datetime, timedelta
from dateutil import parser as dateparser
from keycloak.keycloak_openid import KeycloakOpenID
from keycloak.exceptions import KeycloakGetError
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

logger = logging.getLogger(__name__)

q = Queue()

def put_data_in_queue(data):
    global q
    q.put(data)

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
        try:
            expire_datetime = dateparser.parse(self.token['access_token_expire_time'])
            if expire_datetime < datetime.now():
                return True
            return False
        except:
            return True

    def is_api_refresh_token_expired(self):
        try:
            expire_datetime = dateparser.parse(self.token['refresh_token_expire_time'])
            if expire_datetime < datetime.now():
                return True
            return False
        except:
            return True
 
    def _load_token_file(self):
        self.token = self.load_token_from_file(self.token_file)

    def _put_token_file(self):
        self.put_token_file(self.token, self.token_file)

    def process_keycloak_token(self, keycloak_token):
        access_token_expire_time = datetime.now() + timedelta(seconds=keycloak_token['expires_in'])
        refresh_token_expire_time = datetime.now() + timedelta(seconds=keycloak_token['refresh_expires_in'])
        
        self.token = {
            'access_token': keycloak_token['access_token'],
            'refresh_token': keycloak_token['refresh_token'],
            'access_token_expire_time': access_token_expire_time.isoformat(),
            'refresh_token_expire_time': refresh_token_expire_time.isoformat()
        }

        return self.token

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
    def __init__(self, config_file=None, **kwargs):
        if config_file is None:
            config_file = os.getcwd() + os.path.sep + "config.py"
        if not os.path.exists(config_file):
            raise MissingConfigException
        config_spec = importlib.util.spec_from_file_location("config", config_file)
        config = importlib.util.module_from_spec(config_spec)
        config_spec.loader.exec_module(config)
        try:
            self.username = config.PRESALYTICS['USERNAME']
        except KeyError:
            raise MissingConfigException("Mandatory configuration variable PRESALYTICS_USERNAME is missing from environment variables.  Please reconfigure and retry.")
        try:
            self.password = config.PRESALYTICS['PASSWORD']
            self.direct_grant = True
        except KeyError:
            self.password = None
            self.direct_grant = True
        try:
            self.client_id = config.PRESALYTICS['CLIENT_ID']
        except KeyError:
            self.client_id = DEFAULT_CLIENT_ID

        self.oidc = KeycloakOpenID(
            server_url=OIDC_AUTH_HOST,
            realm_name=OIDC_REALM,
            client_id=self.client_id,
            verify=True
        )
        self.token_util = TokenUtil()
        self.token_util.token = self.refresh_token()
        self.server_thread = FlaskThread()

        super(AuthenticationMixIn, self).__init__(**kwargs)


    def login(self):
        if self.direct_grant:
            try:
                keycloak_token = self.oidc.token(username=self.username, password=self.password)
                self.token_util.process_keycloak_token(keycloak_token)
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
        else:
            url = self.oidc.auth_url(REDIRECT_URI)
            token = self._get_new_token_browser(url)
        return self.token_util.token

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
                self.login()
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

                


        



            