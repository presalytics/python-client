import os

# Automatically configure default logger
try:
    use_logger = os.environ['USE_LOGGER']
except KeyError:
    use_logger = True

if use_logger:
    try:
        from presalytics.lib.logger import configure_logger
        configure_logger()
    except Exception:
        pass

from presalytics.client.api import Client as PresalyticsClient
