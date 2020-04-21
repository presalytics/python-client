import logging
import logging.config
import os
import sys
import presalytics

default_log_path = os.getcwd() + os.path.sep + 'presalytics.log'

USE_LOGGER = False

def configure_logger(log_path=default_log_path, log_level='DEBUG', file_logger=True):
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'}
        },
        'handlers': {
            'console': {
                'level': log_level,
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
    
    USE_LOGGER = file_logger

def handle_exception(exc_type, exc_value, exc_traceback):
    """ Catches unhandled exceptions for logger """
    try:
        logger = logging.getLogger('presalytics.exception_hook')
        if USE_LOGGER:
            logger.error("--------------------------")
            logger.error("UNHANDLED EXCEPTION: FATAL")
            logger.error(msg="--------------------------", exc_info=(exc_type, exc_value, exc_traceback,))
            logger.error("--------------------------")
            logger.error("UNHANDLED EXCEPTION: FATAL")
            logger.error("--------------------------")
        else:
            logger.error(msg="An unhandled exception occured.", exc_info=(exc_type, exc_value, exc_traceback,))
    except Exception:
        pass
    return


# users can override the except hook, but most analysts aren't that skilled yet.
# Makes their scripts more verbose without having to think about it
sys.excepthook = handle_exception
