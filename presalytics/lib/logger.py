import logging, os, sys
import logging.config

default_log_path = os.getcwd() + os.path.sep + 'presalytics.log'

def configure_logger(log_path=default_log_path):
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': log_path,
                'maxBytes': 1024,
                'backupCount': 3
            }
        },
        'loggers': {
            'presalytics': {
                'level': 'DEBUG',
                'handlers': ['console', 'file']
            }
        },
        'disable_existing_loggers': False
    })

def handle_exception(exc_type, exc_value, exc_traceback):
    """ Catches unhandled exceiptions for logger """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return


sys.excepthook = handle_exception


configure_logger()