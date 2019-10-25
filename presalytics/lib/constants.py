""" Constants for api.presalytics.io client """
HOST = "https://api.presaltyics.io"
OIDC_WELL_KNOWN = "https://auth.presalytics.io/auth/realms/presalytics/.well-known/openid-configuration"
OIDC_TOKEN = "https://auth.presalytics.io/auth/realms/presalytics/protocol/openid-connect/token"
PORT = 443
OIDC_AUTH_HOST = "https://auth.presalytics.io/auth/"
OIDC_AUTH_PORT = 443
PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsBQPBlYfkG2OQv6iE52HpWuCBxwVheGaesBOeNZFQV3NmIrH36tmXaqqOvn9JW8eGGo4a6tBfLGEqTb08/avLOypK1fni2ayh9UAKv9ajfBDbdqs5Qmoe3gr9WIrtjopxlUV6xabKyFVlD41vHFM9fTXAG8gRrPPbGmel081Egjjfqs6xM76Rtzz5E5puEpz1dWk7eClNhyL2W2gVAc8ldj6bZhjou3h+qn5k8rN4v/p98uUazselxcOArJ1QRpFdNuyqzUjAKsA6UmdM478bU9T68GUrMqo/mPIC7W3yevCKLGRwrFuE/ewCWRYfVpFcvwEHNsgNn9iqeAQY8Ce9QIDAQAB'
JWT_KEY = "-----BEGIN PUBLIC KEY-----\n{0}\n-----END PUBLIC KEY-----".format(PUBLIC_KEY)
REDIRECT_URI = "https://presalytics.io/login-success"
OIDC_REALM = "presalytics"
DEFAULT_CLIENT_ID = "python-client"
TOKEN_FILE = "token.json"
LOCALHOST_SERVER = "127.0.0.1"
LOCALHOST_PORT = 8052
LOGIN_PATH = "/accounts/login/"
API_CODE_URL = "/user/client-get-auth-code/"
