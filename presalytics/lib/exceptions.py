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
            _attrs = [a for a in dir(default_exception) if not a.startswith('__')]
            for key in _attrs:
                setattr(self, key, getattr(default_exception, key))
    
    def __str__(self):
        """Custom error messages for exception"""
        try:
            error_message = "({0})\n"\
                            "Reason: {1}\n".format(self.status, self.reason)

            if self.body:
                error_message += "HTTP response body: {0}\n".format(self.body)

            return error_message
        except:
             return "An unknown error occured.  Please set default_exception to learn more."


