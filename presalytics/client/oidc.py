
import urllib.parse
import requests
import posixpath
import logging
import typing
import webbrowser
import json
import time
import jose
import jose.jwt
import presalytics.lib
import presalytics.lib.exceptions
import presalytics.lib.constants as cnst


logger = logging.getLogger(__name__)

class OidcClient(object):
    """
    A helper class for negotiating tokens from an oidc provider, defalting to https://login.presalytics.io

    Parameters
    ----------

    client_id: str, optional
        The client id for the application requesting a token. Defaults to python-client

    client_secret: str, optional
        The client secret for the application requesting a token.  Defaults to None (python-client
        is a public facing client with lower priviledge on the Presalytics API). Contact presalytics
        if need a higher-privleged client to access the Presalytics API

    audience: str, optional
        The default audience for client request.  Defaults to https://api.presalytics.io/

    validate_tokens: bool
        Whether to validate tokens when recieved from the token endpoint.  Defaults to True.


    """
    def __init__(self, client_id=None, client_secret=None, validate_tokens=True, *args, **kwargs):
        self.auth_host = kwargs.get("auth_host", cnst.OIDC_AUTH_HOST)
        self.well_known_endpoint = posixpath.join(self.auth_host, kwargs.get("well_known_path", ".well-known/openid-configuration"))
        self.token_endpoint = posixpath.join(self.auth_host, kwargs.get("token_path", "oauth/token"))
        self.authorization_endpoint = posixpath.join(self.auth_host, kwargs.get("authorization_path", "authorization"))
        self.device_endpoint = posixpath.join(self.auth_host, kwargs.get("device_path", "device/code"))
        self.jwks_endpoint = posixpath.join(self.auth_host, kwargs.get("jwks_path", ".well-known/jwks.json"))
        self.userinfo_endpoint = posixpath.join(self.auth_host, kwargs.get("userinfo_path", "userinfo"))
        self.client_id = client_id if client_id else cnst.DEFAULT_CLIENT_ID
        self.audience = kwargs.get("audience", cnst.DEFAULT_AUDIENCE)
        self.client_secret = client_secret
        self.default_scopes = "email profile offline_access"
        self.validate_tokens = validate_tokens

    def token(self, username, password=None, audience=None, scope=None, **kwargs) -> typing.Dict:
        """
        Get an access token
        """
        if not scope:
            scope = self.default_scopes
        if not audience:
            audience = self.audience
        if password and self.client_secret:
            #use password grant if present (not recommended)
            data = {
                "grant_type": "password",
                "username": username,
                "password": password,
                "audience": audience,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": scope
            }
            token_data = self._post(self.token_endpoint, data)
            
        else:
            # Use device grant as default
            device_data = {
                'client_id': self.client_id,
                'audience': self.audience,
                'scope': scope
            }

            device_code_response = self._post(self.device_endpoint, data)

            webbrowser.open_new_tab(device_code_response["verification_uri_complete"])
            sleep_interval = device_code_response["interval"]
            auth_data = {
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code_response["device_code"],
                "client_id": self.client_id
            }
            headers = {
                'content-type': 'application/x-www-form-urlencoded'
            }
            repoll_errors = [
                "authorization_pending",
                "slow_down"
            ]
            repoll = True
            while repoll:
                try:
                    token_response = requests.post(self.token_endpoint, auth_data, headers=headers)
                    if token_response.status_code != 200:
                        err_resp = token_response.json()
                        err_msg = err_resp["error"]
                        if err_msg in repoll_errors:
                            time.sleep(sleep_interval)
                            if err_msg == "slow_down":
                                time.sleep(sleep_interval)                            
                        else:
                            message = "Error: {0} -- {1}".format(err_msg, err_resp["error_description"])
                            raise presalytics.lib.exceptions.ApiError()
                except Exception as ex:
                    logger.exception(ex)
                    repoll = False
            token_data = token_response.json()
        if self.validate_tokens:
            self.validate_token(token_data["access_token"])
        return token_data

    def validate_token(self, token):
        """
        Validate a token
        """
        unverified_header = jose.jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jose.jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=self.audience,
                    issuer=self.auth_host
                )
            except jose.jwt.ExpiredSignatureError:
                raise presalytics.lib.exceptions.ApiError(message="token_expired", status_code=401)
            except jose.jwt.JWTClaimsError:
                raise presalytics.lib.exceptions.ApiError(message="invalid_claims: check audience and issuer", status_code=401)
            except Exception:
                raise presalytics.lib.exceptions.ApiError(message="invalid token (likely malformed)", status_code=401)
            return payload
        raise presalytics.lib.exceptions.ApiError(message="invalid_header: could not find key in jwks",status_code=401)


    def refresh_token(self, refresh_token, scope=None):
        """
        Exchange a refresh token for an access token
        """
        if not scope:
            scope = self.default_scopes
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": refresh_token,
            "scope": scope
        }

        self._post(self.token_endpoint, data)
        
        if self.validate_tokens:
            self.validate_token(token_data["access_token"])
        return token_data

    def _post(self, endpoint, data, headers={}):
        try:
            if 'content-type' not in [x.lower() for x in headers.keys()]:
                headers.update({'content-type': 'application/x-www-form-urlencoded'})
            response = requests.post(endpoint, data, headers=headers)
        except Exception as ex:
            logger.exception(ex)

        return self._handle_response(response)


    def _handle_response(self, response):
        if response.status_code == 401:
            raise presalytics.lib.exceptions.ApiError(message="Unauthorized")
        elif response.status_code == 409:
            logger.error("Value already exists")
            data = None
        elif response.status_code > 299:
            try:
                message = response.json()['message']
            except (KeyError, ValueError):
                message = response.content
            raise presalytics.lib.exceptions.ApiError(message=message, status_code=response.status_code)
        elif response.status == 204:
            data = None
        elif response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                try:
                    data = response.content.decode('utf-8')
                except Exception:
                    data = response.content
                try:
                    data = json.loads(data)
                except Exception:
                    pass
        return data
        

        



        