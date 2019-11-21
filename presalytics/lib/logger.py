import logging
import logging.config
import os
import sys

default_log_path = os.getcwd() + os.path.sep + 'presalytics.log'


def configure_logger(log_path=default_log_path, log_level='DEBUG', file_logger=True):
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
                'level': log_level,
                'handlers': ['console']
            }
        },
        'disable_existing_loggers': False
    })

    if file_logger:
        logger = logging.getLogger('presalytics')
        log_dir = os.path.join(os.getcwd(), 'log')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_file = os.path.join(log_dir, 'presalytics.log')
        file_handler = logging.FileHandler(log_file)
        logger.addHandler(file_handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    """ Catches unhandled exceptions for logger """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        try:
            logger = logging.getLogger('presalytics.exception_hook')
            logger.error(exc_info=sys.exc_info())
        except Exception:
            pass
        return


sys.excepthook = handle_exception
