import logging
import os
import sys

default_log_path = os.getcwd() + os.path.sep + 'presalytics.log'


def configure_logger(log_path=default_log_path):
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'}
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            'presalytics': {
                'level': 'DEBUG',
                'handlers': ['console']
            }
        },
        'disable_existing_loggers': False
    })


def handle_exception(exc_type, exc_value, exc_traceback):
    """ Catches unhandled exceptions for logger """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return


sys.excepthook = handle_exception
