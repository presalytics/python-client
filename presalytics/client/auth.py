
import json
import logging
import pkg_resources
import sys
import weakref
from dateutil import parser as dateparser
from six import reraise
from datetime import datetime, timedelta
from presalytics.lib.exceptions import (
    MissingConfigException,
    MisConfiguredTokenException,
    ApiException
)
from presalytics.lib.constants import TOKEN_FILE

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from presalytics.client.api import Client

logger = logging.getLogger(__name__)


class TokenUtil(object):
    def __init__(self, token=None, token_file=None):
        if token_file is None:
            self.token_file = TOKEN_FILE
        else:
            self.token_file = token_file
        try:
            self._load_token_file()
        except Exception:
            pass
        if token is not None:
            try:
                self.token = {
                    'access_token': token['access_token'],
                    'access_token_expire_time': token["access_token_expire_time"],
                    'refresh_token': token["refresh_token"],
                    'refresh_token_expire_time': token["refresh_token_expire_time"]
                }
                self._put_token_file()
            except Exception:
                raise MisConfiguredTokenException

    def is_api_access_token_expired(self):
        try:
            expire_datetime = dateparser.parse(self.token['access_token_expire_time'])
            if expire_datetime < datetime.now():
                return True
            return False
        except Exception:
            return True

    def is_api_refresh_token_expired(self):
        try:
            expire_datetime = dateparser.parse(self.token['refresh_token_expire_time'])
            if expire_datetime < datetime.now():
                return True
            return False
        except Exception:
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
    def __init__(self, parent: 'Client', config=None, config_file=None, ignore_api_exceptions=False, **kwargs):
        self.parent: 'Client' = weakref.ref(parent)
        self._ignore_api_exceptions = ignore_api_exceptions
        super(AuthenticationMixIn, self).__init__(**kwargs)

    def get_auth_header(self):
        self.parent.refresh_token()
        auth_header = {
            "Authorization": "Bearer " + self.parent.token_util.token["access_token"]
        }
        return auth_header

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

        auth_header = self.get_auth_header()
        if header_params is not None:
            header_params.update(auth_header)
        else:
            header_params = auth_header
        try:
            return super(AuthenticationMixIn, self).call_api(
                resource_path, method, path_params,
                query_params, header_params, body, post_params, files, response_type,
                auth_settings, async_req, _return_http_data_only, collection_formats, _preload_content,
                _request_timeout, _host
            )
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
            self.set_host(self.parent.auth_config.PRESALYTICS['HOSTS'])

    @staticmethod
    def get_user_agent():
        try:
            VER = pkg_resources.require("presalytics")[0].version
        except Exception:
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
