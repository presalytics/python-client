import json
import logging
import pkg_resources
import sys
import weakref
import dateutil
import dateutil.parser
import datetime
import six
import posixpath
import presalytics
import presalytics.lib.exceptions
import presalytics.lib.constants
import presalytics.story.outline
import typing
if typing.TYPE_CHECKING:
    from presalytics.client.api import Client


logger = logging.getLogger(__name__)


class TokenUtil(object):
    def __init__(self, token=None, token_file=None, token_cache=False):
        self.token_cache = token_cache
        if token_file is None:
            self.token_file = presalytics.lib.constants.TOKEN_FILE
        else:
            self.token_file = token_file
        try:
            self._load_token_file()
        except Exception:
            pass
        if token is not None:
            try:
                self.process_token(token)    
                if self.token_cache:
                    self._put_token_file()
            except Exception:
                raise presalytics.lib.exceptions.MisConfiguredTokenException()
        else:
            if not hasattr(self, 'token'):
                self.token = {}

    def is_api_access_token_expired(self):
        try:
            if not self.token.get('access_token_expire_time', None):
                if self.token.get('access_token', None):
                    return False  # If expire time unknown, instruct client to call endpoint
                else:
                    return True  # If no token, instruct client to acquire token
            token_expiry = self.token['access_token_expire_time']
            if isinstance(token_expiry, datetime.datetime):
                expire_datetime = token_expiry.astimezone(datetime.timezone.utc)
            elif isinstance(token_expiry, str):
                expire_datetime = dateutil.parser.parse(self.token['access_token_expire_time']).astimezone(datetime.timezone.utc)
            else:
                logger.error("Token expire time not of type str (isoformat) or datetime.datetime")
                return True  # Get a new token on type error
            if expire_datetime < datetime.datetime.utcnow().astimezone(datetime.timezone.utc):
                return True
            else:
                return False
        except Exception as ex:
            logger.exception(ex)
            return True # Get a new token on unknown errors

    def _load_token_file(self):
        try:
            if self.token_cache:
                self.token = self.load_token_from_file(self.token_file)
        except Exception:
            logger.error("Unable to load token from cache.  If you do intend to cache tokens, use configuration CACHE_TOKENS=False")

    def _put_token_file(self):
        try:
            if self.token_cache:
                self.put_token_file(self.token, self.token_file)
        except Exception:
            logger.error("Failed to cache token.  Likely a write permissions error for the filesystem.")

    def process_token(self, token):
        self.token = {
            'access_token': token['access_token']
        }
        if not token.get('access_token_expire_time', None):
            if token.get('expires_in', None):
                access_token_expire_time = datetime.datetime.utcnow().astimezone(datetime.timezone.utc) + datetime.timedelta(seconds=token['expires_in'])
            else:
                pass    # TODO: add logic to introspect token for expire time 
        else:
            access_token_expire_time = token["access_token_expire_time"]
        if access_token_expire_time:
            self.token.update({
                "access_token_expire_time": access_token_expire_time
            })
        if token.get('refresh_token', None):
            self.token.update({
                "refresh_token": token["refresh_token"]
            })
        return self.token

    @staticmethod
    def put_token_file(token, token_filepath):
        with open(token_filepath, mode='w+') as newtoken:
            json.dump(token, newtoken, cls=presalytics.story.outline.OutlineEncoder)

    @staticmethod
    def load_token_from_file(token_filepath):
        with open(token_filepath, 'r') as token_file:
            token = json.load(token_file)
        return token


class AuthenticationMixIn(object):
    def __init__(self, parent: 'Client', ignore_api_exceptions=False, **kwargs):
        self._ignore_api_exceptions = ignore_api_exceptions
        self.parent = weakref.ref(parent)
        super(AuthenticationMixIn, self).__init__()
        self.update_configuration()

    def call_api(
            self, resource_path, method,
            path_params=None, query_params=None, header_params=None,
            body=None, post_params=None, files=None,
            response_type=None, auth_settings=None, async_req=None,
            _return_http_data_only=None, collection_formats=None,
            _preload_content=None, _request_timeout=None, _host=None):
        """
        Overriding call_api to force token check, refresh on each api call,
        rather than at class initialized (good for ipython notebooks)
        """
        if self.parent() is None:
            message = """
            Missing reference to Client class.  Client was like garbage collected by the intepreter.\n  
            Please initialize the Client class on its own line to avoid this error.  For example:\n\n
            client = presalytics.Client()\n
            story = client.story.story_id_get(story_id)
            """
            raise presalytics.lib.exceptions.InvalidConfigurationError(message=message)
        auth_header = self.parent().get_auth_header()
        if header_params is not None:
            header_params.update(auth_header)
        else:
            header_params = auth_header
        if not header_params.get("X-Request_Id"):
            req_id = self.parent().get_request_id_header()
            header_params.update(req_id)
        request_id = header_params.get("X-Request-Id")
        try:

            endpoint = self.configuration.host + resource_path
            logger.info("Sending {0} message to {1}. Request Id: {2}".format(method, endpoint, request_id))
            call_args = (
                resource_path, 
                method, 
                path_params,
                query_params, 
                header_params, 
                body, 
                post_params, 
                files, 
                response_type,
                auth_settings, 
                async_req, 
                _return_http_data_only, 
                collection_formats, 
                _preload_content,
                _request_timeout, 
                _host
            )
            response = super(AuthenticationMixIn, self).call_api(*call_args)
            logger.info("{0} response received from {1}".format(method, endpoint))
            return response
        except Exception as e:
            if type(e).__name__ == "ApiException":
                try:
                    d = json.loads(e.body)
                    addendum = " Host: {0}; Path: {1}; Method: {2}; Request Id: {3}".format(self.configuration.host, resource_path, method, request_id)
                    try:
                        d["detail"] = d["detail"] + addendum
                    except TypeError:
                        d = e.body + addendum
                    e.body = json.dumps(d)
                    logging.error(d)
                    if d["status"] == 401:
                        logging.debug("Refeshing token from unauathorized call and retrying")
                        self.parent().refresh_token()
                        return super(AuthenticationMixIn, self).call_api(*call_args)
                except Exception:
                    pass
                if self._ignore_api_exceptions:
                    return e.body, e.status, e.headers
                else:
                    raise presalytics.lib.exceptions.ApiException(default_exception=e)
            else:
                t, v, tb = sys.exc_info()
                six.reraise(t, v, tb)

    def update_configuration(self):
        """
        updates the configuration from the base api client to parameters contained in the config file.
        base api client must be initialized prior to calling this method (i.e., self.configuration cannot equal None),
        so that configuration can automatically inherit default values.
        Mostly used for debugging purposes, but self-hosted API endpoints may require injection of these parameters
        """
        if self.configuration is None:
            raise presalytics.lib.exceptions.MissingConfigException("Base API not yet configured, please reconstruct API initialization")
        self.user_agent = AuthenticationMixIn._get_user_agent
        if presalytics.CONFIG.get("HOSTS", None):
            self.set_host(presalytics.CONFIG.get('HOSTS'))

    @staticmethod
    def get_user_agent():
        try:
            VER = pkg_resources.require("presalytics")[0].version
        except Exception:
            VER = 'build'
        return "presalytics-python-client/{0}".format(VER)

    _get_user_agent = get_user_agent.__func__()  #type: ignore

    def set_host(self, hosts_dict):
        for parent_cls in self.__class__.__bases__:
            if parent_cls.__name__ == 'ApiClient':
                for k, v in hosts_dict.items():
                    if k.lower() in parent_cls.__module__:
                        host_key = k
                        break
        try:
            self.configuration.host = hosts_dict[host_key]
        except (KeyError, UnboundLocalError):
            pass

    def _ApiClient__deserialize_datetime(self, string):
        """Overwrites generated function to include UTC timezone on datetime object
        needs to account for name-mangling in parent class
        The string should be in iso8601 datetime format.

        :param string: str.
        :return: datetime.
        """
        return super()._ApiClient__deserialize_datetime(string).astimezone(datetime.timezone.utc)

    @property
    def external_root_url(self):
        if presalytics.CONFIG.get("BROWSER_API_HOST", None):
            base_uri = self.configuration.host.rstrip("/").split("/")[-1]
            target = presalytics.CONFIG["BROWSER_API_HOST"].rstrip("/") + "/story"
        else:
            target = self.configuration.host
        return target