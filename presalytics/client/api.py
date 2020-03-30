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
import wsgi_microservice_middleware
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
    """ Class for interacting with Presalytics API endpoints

    The Client class creates a simple interface for user to interactive with the 
    Presalytics API and is the primary building block for user-built automation of stories, 
    dashboards, and interactive presentations.

    A client instance wraps python functions around Presalytics API endpoints and
    manages user authentication. On initialization, he client checks the status of 
    a user authentication the expiry of their refresh an access tokens.  When needed,
    the client will open a browser to prompt the user to login at the presalytics.io
    login page (or raise an `presalytics.lib.exceptions.InvalidTokenException` when 
    `delegate_login` is `True`).

    After authenication, users can call the methods bound to the story, ooxml_automation, 
    and doc_converter attributes to make calls in into the Presalytics API.

    *A note for server-side development*:

    By default, the client class automatically caches tokens in a file called 
    "token.json", located in the python's current working directory.  This is done so
    users running scripts do not have to acquire a new token every time an API call is
    made. If building a client to operate in a multi-user environment, this behavior 
    should be turned off so that user do not pull one another's tokens.
    To do this, ensure the following parameters are pass to the configuration either 
    via initialization or in a `presalytics.CONFIG` file: 
    
        cache_tokens = False,
        delegate_login = True
    
    When delegate login is True, the client assumes that the application creating 
    instances of the client object will handle user authentication.  The simplest way
    to do this is to pass a token to the client via the "token" keyword argument.

    Parameters
    ----------

    username : str, optional
        Defaults to None.  The user's Presalytics API username.  This keyword will take precedence over a passed to the client
        via `presalytics.CONFIG`.  The username must either be present in `presalytics.CONFIG` or be passed in 
        via keyword, otherwise the client will raise a `presalytics.lib.exceptions.MissingConfigException`.

    password : str, optional
        Defaults to None.  The user's Presalytics API password.  This useful for quickly testing scripts, but in most 
        scenario users should not be passing plaintext into the client via this keyword.  In a secure, single-user 
        environment, passwords are better placed in the `presalytics.CONFIG` object for reuseability.  A more secure
        is to leave passwords out of the configuration, keep `delegate_login` = `False`, and acquire tokens via the browser.
 
    delegate_login : bool, optional
        Defaults to False.  Indicates whether the client would redirect to a browser to 
        acquire an API token. If `DELEGATE_LOGIN` is `True`, when the `presalytics.client.api.Client` does not have 
        access to a valid API token, the client will raise a `presalytics.lib.exceptions.InvalidTokenException`.
        The default operation will automatically open a new browser tab to acquire a new token 
        via website client from the presalytics.io login page.  Putting this setting to True is
        useful for server-side development.

    token : dict, optional
        Defaults to None.  A dictionary contain information about tokens acquire from auth.presalytics.io.  The 
        dictionary must contain an `access_token`, a `refresh_token`, and entries contiaing information about token expiry.  

        Token expiry information can either passed in ISO 8601 formatted string with a UTC offset as dictionary keys
        `access_token_expire_time` and `refresh_token_expire_time` or an integer in seconds with the corresponding 
        dictionary keys`expires_in` and `refresh_expires_in`.
        
        if the `dict` passed in via this keywork does is not have the correct entries, the client will
        raise an `presalytics.lib.exceptions.InvalidTokenException`.

    cache_tokens : bool, optional
        Defaults to True.  Toggles whether or the client should cache its acquired tokens in file called "token.json"
        in the current working directory.  Minimizes the number of times a user is required to login.  Set to False
        in multi-user environments.

    Attributes
    ----------

    direct_grant : bool
        Indicates whether an token will be acquire via the "direct_grant" OpenID Connect flow.  Usually indicates
        whether the user has supplied a passwork to the client either through `presalytics.CONFIG` ro 
        during object initialization.

    doc_converter : presalytics.client.presalytics_doc_converter.api.default_api.DefaultApi
        Interface to the Presalytics API Doc Converter service.  The object contains methods that enable
        the client to make api calls that return deserialized objects from the Presalytics API,
        simplying user and developer interaction with the Presaltytics API.  API calls can be generated
        as follows:

            client = presalytics.Client()
            api_obj = client.doc_converter.{operation_id}(*args)

        where `{operation_id}` is the `operationId` assocated with the endpoint specified the [Doc Converter 
        Service OpenAPI Contract](https://presalytics.io/docs/api-specifications/doc-converter/) , and *args
        are the corresponding arguments that are passed to the method.  A complete list of the avialable
        methods is shown on the `presalytics.client.presalytics_doc_converter.api.default_api.DefaultApi` object.
        
        *Note*:
        This attribute contains automatically generated methods via 
        the [OpenAPI generator](https://github.com/OpenAPITools/openapi-generator).  The 
        `presalytics.client.presalytics_doc_converter.api.default_api.DefaultApi` has been passed an an `api_client`
        keyword argument with an instance of `presalytics.client.api.DocConverterApiClientWithAuth`, which adds 
        an authentication and request processing middleware layer to the default sub package 
        built via code generatation.

    ooxml_automation : presalytics.client.presalytics_ooxml_automation.api.default_api.DefaultApi
        Interface to the Presalytics API Ooxml Automation service.  The object contains methods that enable
        the client to make api calls that return deserialized objects from the Presalytics API,
        simplying user and developer interaction with the Presaltytics API.  API calls can be generated
        as follows:

            client = presalytics.Client()
            api_obj = client.ooxml_automation.{operation_id}(*args)

        where `{operation_id}` is the `operationId` assocated with the endpoint specified the [Ooxml Automation
        Service OpenAPI Contract](https://presalytics.io/docs/api-specifications/ooxml-automation/) , and *args
        are the corresponding arguments that are passed to the method.  A complete list of the avialable
        methods is shown on the `presalytics.client.presalytics_ooxml_automation.api.default_api.DefaultApi` object.
        
        *Note*:
        This attribute contains automatically generated methods via 
        the [OpenAPI generator](https://github.com/OpenAPITools/openapi-generator).  The 
        `presalytics.client.presalytics_ooxml_automation.api.default_api.DefaultApi` has been passed an an `api_client`
        keyword argument with an instance of `presalytics.client.api.OoxmlAutomationApiClientWithAuth`, which adds 
        an authentication and request processing middleware layer to the default sub package 
        built via code generatation.

    story : presalytics.client.presalytics_story.api.default_api.DefaultApi
        Interface to the Presalytics API Ooxml Automation service.  The object contains methods that enable
        the client to make api calls that return deserialized objects from the Presalytics API,
        simplying user and developer interaction with the Presaltytics API.  API calls can be generated
        as follows:

            client = presalytics.Client()
            api_obj = client.story.{operation_id}(*args)

        where `{operation_id}` is the `operationId` assocated with the endpoint specified the [Ooxml Automation
        Service OpenAPI Contract](https://presalytics.io/docs/api-specifications/story/) , and *args
        are the corresponding arguments that are passed to the method.  A complete list of the avialable
        methods is shown on the `presalytics.client.presalytics_story.api.default_api.DefaultApi` object.
        
        *Note*:
        This attribute contains automatically generated methods via 
        the [OpenAPI generator](https://github.com/OpenAPITools/openapi-generator).  The 
        `presalytics.client.presalytics_story.api.default_api.DefaultApi` has been passed an an `api_client`
        keyword argument with an instance of `presalytics.client.api.StoryApiClientWithAuth`, which adds 
        an authentication and request processing middleware layer to the default sub package 
        built via code generatation.

    client_id : str
        The client_id that is used OpenID Connect login.  Defaults to "python-client".  

    client_secret : str, optional
        The client_secret used during OpenID Connect login.  Useful `confidential_client` is True.

    confidential_client : bool
        Indicates whether a this client can obtain tokens from auth.presalytics.io without a user under
        OpenID Connect grant type "confidential_client".  Requires a `client_secret`.  Default is False. 

    oidc : `keycloak.KeycloakOpenID`
        A middleware class for to help acquire tokens from auth.presalytics.io.  For more information, review
        the docs at https://python-keycloak.readthedocs.io/en/latest/ .

    token_util : `presalytics.client.auth.TokenUtil`
        A handler for managing an caching tokens acquired from auth.presalytics.io.

    site_host : str
        The login site host for acquiring tokens.  Set from `presalytics.CONFIG` with keyword `["SITE"]["HOST"]`.
        Defaults to https://presalytics.io.

    redirect_uri : str
        Useful if implementing authorization code flow for and OpenID Connect client.  Redirect URIs must 
        be approved by Presalytics API devops for use in client applications. Set from Set from 
        `presalytics.CONFIG` with keyword `["REDIRECT_URI"]`.  Defaults to https://presalytics.io/user/login-success. 

    login_sleep_interval : int
        The duration (in seconds) between attempts to acquire a token after browser-based authentication. Defaults
        to 5 seconds.        

    login_timeout : int
        Defaults to 60 seconds.  The amount of time the client will attempt to acquire a token after the 
        https://presalytics.io authenicates a user. Raises a `presalytics.lib.exceptions.LoginTimeout`
        if the user has not authenticated by the time the interval has expired.

    """
    def __init__(
            self,
            username=None,
            password=None,
            delegate_login=False,
            token=None,
            cache_tokens=True,
            **kwargs):
    
        if username:
            self.username = username
        else:
            try:
                self.username = presalytics.CONFIG['USERNAME']
            except KeyError:
                if token:
                    self.username = None
                else:
                    raise presalytics.lib.exceptions.MissingConfigException("Configuration variable PRESALYTICS_USERNAME is required when client is not initalized with an API token.  Please reconfigure and retry.")
        try:
            if password:
                self.password = password
            else:
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
        self.verify_https = presalytics.CONFIG.get("VERIFY_HTTPS", True)
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
        if presalytics.CONFIG.get("CACHE_TOKENS", None):
            cache_tokens = presalytics.CONFIG.get("CACHE_TOKENS")
        self.token_util = presalytics.client.auth.TokenUtil(token_cache=cache_tokens)
        if token:
            if token.get('access_token_expire_time', None):
                self.token_util.token = token
            elif token.get('expires_in', None):
                self.token_util.process_keycloak_token(token)
            else:
                raise presalytics.lib.exceptions.InvalidTokenException(message="Unknown token format.")
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
        """
        Triggers a an attempt to acquire an API token based on the the client configuration
        """
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
        """
        Conduct IETF [token exchange](https://tools.ietf.org/id/draft-ietf-oauth-token-exchange-19.html).
        Use for client applications to modify the scope of token granted by user authenication so they 
        do not get misused by 3rd party services. 

        Parameters
        ----------

        original_token : str
            A str with JWT Bearer access token obtained from auth.presalytics.io

        audience : str
            A str naming the referrring to audience of the server that will consume the new token

        Returns:
        ---------
        A str containing a JWT Bearer token with reduced scope

        """
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
            "next": urllib.parse.urlparse(self.redirect_uri).path
        }
        query_string = '?{}'.format(urllib.parse.urlencode(query))
        url = urllib.parse.urljoin(self.site_host, urllib.parse.urljoin(cnst.LOGIN_PATH, query_string))
        logger.info("Opening new browser tab.  Please input login credentials...")
        logger.info("Requesting login at location: <{0}>".format(url))
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
        if token:
            logger.info("Login Succeeded.  Proceeding.")
        return token

    def refresh_token(self):
        """
        Obtains a new access token if the access token is expired. if refresh token is expired, 
        this method prompt user to re-authenticate when `delegate_login` is `False` or raise
        an `presalytics.lib.exceptions.InvalidTokenException` when `deletegate_login` is True.
        """
        if self.token_util.is_api_access_token_expired():
            if self.token_util.is_api_refresh_token_expired():
                if not self._delegate_login:  # do not automatically log in at init
                    self.login()
                else:
                    raise presalytics.lib.exceptions.InvalidTokenException(message="This token has expired.")
            else:
                try:
                    refresh_token = self.token_util.token["refresh_token"]
                    keycloak_token = self.oidc.refresh_token(refresh_token)
                    self.token_util.process_keycloak_token(keycloak_token)
                    logger.debug("Refresh token granted successfully.")
                except keycloak.exceptions.KeycloakGetError:
                    if not self._delegate_login:
                        self.login()
            if self.token_util.token_cache:
                self.token_util._put_token_file()
        return self.token_util.token

    def get_auth_header(self):
        """
        Creates a JWT Bearer Authorization token header

        Returns
        ----------
        A `dict` authorization crediential to be attached to an API request
        """
        self.refresh_token()
        auth_header = {
            "Authorization": "Bearer " + self.token_util.token["access_token"]
        }
        return auth_header

    def get_request_id_header(self):
        """
        Creates an 'X-Request-Id' token header for tracing requests through Presalytics API
        services.  If deployed alongside the [WSGI Microservice Middleware](https://github.com/presalytics/WSGI-Microservice-Middleware) 
        package, this method will pull the request id from the call stack.
        
        Returns
        ----------
        A `dict` header representation with an 'X-Request-Id' key to be attached to an API request
        """
        
        current_request_id = wsgi_microservice_middleware.current_request_id()
        if not current_request_id:
            current_request_id = str(uuid4())
        header = {
            "X-Request-Id": current_request_id
        }
        return header

    def download_file(self, story_id, ooxml_automation_id, download_folder=None, filename=None, **kwargs):
        """
        Downloads an updated Ooxml Automation file and places the file in a designated folder

        Parameters
        ---------
        story : str
            The id of the Presalytics Story API object that manages access to document
        
        ooxml_automation_id : str
            The id of the Presalytics API Ooxml Automation service object that you want to download
        
        download_folder : str, optional
            The filepath to the local directory that you want to download the file to. Defaults to the 
            current working directory.
        
        filename: str, optional
            The name of the downloaded file. Defaults to the original filename the the object was created.

        """
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
    """
    Wraps `presalytics.client.presalytics_doc_converter.api_client.ApiClient` with 
    `presalytics.client.auth.AuthenticationMixIn` middleware
    """
    def __init__(self, parent: Client, **kwargs):
        presalytics.client.auth.AuthenticationMixIn.__init__(self, parent, **kwargs)
        presalytics.client.presalytics_doc_converter.api_client.ApiClient.__init__(self)
        self.update_configuration()


class OoxmlAutomationApiClientWithAuth(presalytics.client.auth.AuthenticationMixIn, presalytics.client.presalytics_ooxml_automation.api_client.ApiClient):
    """
    Wraps `presalytics.client.presalytics_ooxml_automation.api_client.ApiClient` with
    `presalytics.client.auth.AuthenticationMixIn` middleware
    """
    def __init__(self, parent: Client, **kwargs):
        presalytics.client.auth.AuthenticationMixIn.__init__(self, parent, **kwargs)
        presalytics.client.presalytics_ooxml_automation.api_client.ApiClient.__init__(self)
        self.update_configuration()

class StoryApiClientWithAuth(presalytics.client.auth.AuthenticationMixIn, presalytics.client.presalytics_story.api_client.ApiClient):
    """
    Wraps `presalytics.client.presalytics_story.api_client.ApiClient` with
    `presalytics.client.auth.AuthenticationMixIn` middleware
    """
    def __init__(self, parent: Client, **kwargs):
        presalytics.client.auth.AuthenticationMixIn.__init__(self, parent, **kwargs)
        presalytics.client.presalytics_story.api_client.ApiClient.__init__(self)
        self.update_configuration()




        


