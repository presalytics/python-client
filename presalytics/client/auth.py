import requests, os, webbrowser, json, logging, pkg_resources, sys
import importlib.util
from six import reraise
from queue import Queue
from threading import Thread
from datetime import datetime, timedelta
from dateutil import parser as dateparser
from keycloak.keycloak_openid import KeycloakOpenID
from keycloak.exceptions import KeycloakGetError
from presalytics.localhost.server import app
from presalytics.lib.exceptions import MissingConfigException, MisConfiguredTokenException, InvalidTokenException, ApiException
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
    LOCALHOST_PORT,
    JWT_KEY
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

class AuthConfig(object):
    def __init__(self, config_dict):
        self.PRESALYTICS = config_dict
 
class AuthenticationMixIn(object):
    def __init__(self, config=None, config_file=None, delegate_login=False, ignore_api_exceptions=False, **kwargs):
        self._delegate_login = delegate_login
        self._ignore_api_exceptions = ignore_api_exceptions
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
            self.direct_grant = True
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
            if self.auth_config.PRESALYTICS["DOWNLOADS_FOLDER"]:
                os.environ["TMPDIR"] = self.auth_config.PRESALYTICS["DOWNLOADS_FOLDER"]
        except KeyError:
            os.environ["TMPDIR"] = os.getcwd()
        

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
        try:
            if self.direct_grant:
                keycloak_token = self.oidc.token(username=self.username, password=self.password)
            else:
                url = self.oidc.auth_url(REDIRECT_URI)
                keycloak_token = self._get_new_token_browser(url)
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
        decoded_token = self.oidc.decode_token(original_token, JWT_KEY)
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


    def _get_new_token_browser(self, url):
        """
        Change this code to leverage website
        generate OTP as uuid
        open website at standard login screen with query string params:
        - OTP - uuid 
        - type - auth_code
        
        to website, add:
        - step to login to process query string
        - endpoint POST /account/{username}/ with payload OTP, return encrypted access code
        - store auth_code in lieu of token in server side session

        - loop, querying new endpoint until LOGIN_TIMEOUT
        - on successfull login decrypt auth_code with OPT
        - send auth code to token endpoint to receive token
        """

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
                if not self._delegate_login: # do not automatically log in at init
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

    def get_auth_header(self):
        self.refresh_token()
        auth_header = {
            "Authorization": "Bearer " + self.token_util.token["access_token"]
        }
        return auth_header

    
    def call_api(self, resource_path, method,
                 path_params=None, query_params=None, header_params=None,
                 body=None, post_params=None, files=None,
                 response_type=None, auth_settings=None, async_req=None,
                 _return_http_data_only=None, collection_formats=None,
                 _preload_content=None, _request_timeout=None, _host=None):
        """
        Overriding call_api to force token check, refresh on each api call, 
        rather than at class initialized (good for ipython notebooks)
        """

        auth_header = self.get_auth_header()
        if header_params is not None:
            header_params.update(auth_header)
        else:
            header_params = auth_header
        try:
            return super(AuthenticationMixIn, self).call_api(resource_path, method, path_params,
                query_params, header_params, body, post_params, files, response_type,
                auth_settings, async_req, _return_http_data_only, collection_formats, _preload_content,
                _request_timeout, _host)
        except Exception as e:
            if type(e).__name__ == "ApiException":
                if self._ignore_api_exceptions:
                    return e.body, e.status, e.headers
                else:
                    raise ApiException(default_exception=e)
            else:
                t, v, tb = sys.exc_info()
                reraise(t, v, tb)


    def update_configuration(self):
        """
        updates the configuration from the base api client to parameters contained in the config file.
        base api client must be initialized prior to calling this method (i.e., self.configuration cannot equal None),
        so that configuration can automatically inherit default values.
        Mostly used for debugging purposes, but self-hosted API endpoints may require injection of these parameters
        """
        if self.configuration is None:
            raise MissingConfigException("Base API not yet configured, please reconstruct API initialization")
        self.user_agent = AuthenticationMixIn._get_user_agent
        if bool(self.auth_config.PRESALYTICS['HOSTS']):
            self.set_host(self.auth_config.PRESALYTICS['HOSTS'])

    
    @staticmethod
    def get_user_agent():
        try:
            VER = pkg_resources.require("presalytics")[0].version
        except:
            VER = 'build'
        return "presalytics-python-client/{0}".format(VER)   

    _get_user_agent = get_user_agent.__func__()


    def set_host(self, hosts_dict):
        for parent_cls in self.__class__.__bases__:
            module_name = parent_cls.__module__.split('.')[0]
            if module_name != 'presalytics':
                host_key = module_name.replace('presalytics_', '').upper()
                try:
                    self.configuration.host = hosts_dict[host_key]
                    break
                except KeyError:
                    pass



                


        



            