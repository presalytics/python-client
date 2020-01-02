import logging


class PresalyticsBaseException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = "An Error occur in the presalytics module.  Consult log for stacktrace."
        message = args[0]
        if len(message) > 0:
            logger = logging.getLogger('presalytics.lib.exceptions')
            logger.error(message)
        if not (args or kwargs):
            args = (default_message,)
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


class LoginTimeout(PresalyticsBaseException):
    def __init__(self):
        message = "User took too long to login on website to obtain token.  Please try again."
        super().__init__(message)


class ValidationError(PresalyticsBaseException):
    def __init__(self, message):
        if not message:
            message = "Validation Error occured"
        super().__init__(message)


class ApiError(PresalyticsBaseException):
    def __init__(self, message=None, status_code=None):
        if not message:
            if not status_code:
                message = "A error occured while commuicating with the presalytics API.  Please Check your configuration values and try again."
            else:
                message = "Status Code: {0}".format(status_code)
        else:
            if status_code:
                message = message + ".  Status Code: {0}".format(status_code)
        super().__init__(message)


class InvalidConfigurationError(PresalyticsBaseException):
    def __init__(self, message=None):
        if not message:
            message = "One of the input parameters to your component is incorrectly defined (e.g., a typo).  Please re-check and try again."
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
            error_message = "({0})\nReason: {1}\n".format(self.status, self.reason)

            if self.body:
                error_message += "HTTP response body: {0}\n".format(self.body)

            return error_message
        except Exception:
            return "An unknown error occured.  Please set default_exception to learn more."
