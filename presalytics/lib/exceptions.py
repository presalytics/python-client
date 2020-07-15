import typing
import logging
import lxml
import sys
import traceback


class PresalyticsBaseException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = "An Error occur in the presalytics module.  Consult log for stacktrace."
        message = args[0]
        if message:
            self.message = message
        else:
            self.message = default_message
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
    def __init__(self, message=None):
        if not message:
            message = "This token is invalid.  Please login again to get a new token."
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
        self.status_code = status_code
        if not message:
            if not status_code:
                message = "A error occured while commuicating with the presalytics API.  Please Check your configuration values and try again."
            else:
                message = "Status Code: {0}".format(status_code)
        else:
            if status_code:
                try:
                    message = message.decode('utf-8')
                except Exception:
                    pass
                message = str(message) + ".  Status Code: {0}".format(status_code)
        super().__init__(message)


class InvalidConfigurationError(PresalyticsBaseException):
    def __init__(self, message=None):
        if not message:
            message = "One of the input parameters to your component is incorrectly defined (e.g., a typo).  Please re-check and try again."
        super().__init__(message)


class RegistryError(PresalyticsBaseException):
     def __init__(self, registry, message=None):
        if not message:
            message = "The was an unknown error in inside the registry"
        message = "{0} Error: ".format(registry.__class__.__name__) + message
        super().__init__(message)


class InvalidArgumentException(PresalyticsBaseException):
    def __init__(self, message=None):
        if not message:
            message = "One of the arguments supplied to this method is invalid."
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


class RenderExceptionHandler(object):
    def __init__(self, exception: Exception, target_type="widget", traceback=None):
        self.exception = exception
        self.target_type = target_type
        self.exception_type = self.exception.__class__.__name__
        self.line_no = None

        try: 
            first_frame = self.get_source_frame(traceback)
            self.source_module = first_frame.tb_frame.f_globals['__name__']
            self.line_no = first_frame.tb_lineno
        except Exception:
            self.source_module = "unidentified"
            self.line_no = "unknown"
    
        if isinstance(self.exception, PresalyticsBaseException):
            self.message = self.exception.message
        else:
            try:
                self.message = self.exception.args[0]
            except (AttributeError, KeyError):
                self.message = "No message was included with this exception."

    def get_source_frame(self, tb):
        next = tb.tb_next
        if next:
            return self.get_source_frame(next)
        else:
            return tb
        

    def render_exception(self):
        container = lxml.html.Element("div", {
            'class': "exception-container"
        })
        header = lxml.html.Element("h3")
        message = lxml.html.Element("p")
        header.text = "Oops! A rendering error occured."
        message.text = "This {} could not be rendered.  Please see the information below to help you diagnose the problem".format(self.target_type)

        _type = lxml.html.Element("p")
        _type.text = "Exception Type: {}".format(self.exception_type)

        exception_message = lxml.html.Element("p")
        exception_message.text = "Exception message: {}".format(self.message)
        source = lxml.html.Element("p")
        source.text = "Error at line number: {0} in module {1}".format(self.line_no, self.source_module)
        note = lxml.html.Element("p")
        note.text = "If you have trouble understainding this error message, try building your story using " \
            "with the presalytics.Revealer's `present()` method.  If should give you more thorough error logging."
        
        container.extend([header, message, _type, exception_message, source, note])
        return lxml.html.tostring(container).decode('utf-8')
    
    def to_html(self):
        return self.render_exception()
         