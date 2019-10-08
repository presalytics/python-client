class PresalyticsBaseException(Exception):
     def __init__(self, *args, **kwargs):
         default_message = 'An Error occur in the presalytics module.  Consult log for stacktrace.'
         if not (args or kwargs): args = (default_message,)
         super().__init__(*args, **kwargs)

class MissingConfigException(PresalyticsBaseException):
    def __init__(self, message):
        if message is None:
            message = "Configuration file missing.  Please please a config.ini file in working directory"
        super().__init__(message)

class MisConfiguredTokenException(PresalyticsBaseException):
    def __init__(self):
        message = "Authenication token is missing or malformed.  Please acquire new token and try again."
        super().__init__(message)

class InvalidTokenException(PresalyticsBaseException):
    def __init__(self):
        message = "Configuration file missing.  Please please a config.ini file in working directory"
        super().__init__(message)

class ApiException(PresalyticsBaseException):
    def __init__(self, default_exception=None):
        if default_exception is not None:
            for key, val in default_exception.__dict__:
                setattr(self, key, val)


