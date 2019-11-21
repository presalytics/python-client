# Automatically configure default logger
import os
import environs
import logging
import presalytics.lib
import presalytics.lib.logger
import presalytics.lib.plugins
import presalytics.lib.plugins.base
import presalytics.lib.config_loader
import presalytics.story
import presalytics.story.components

env = environs.Env()
env.read_env()


# A comma-separated list of paths to search of config.py, plugin classes, and component classes
autodiscover_paths = env.list('AUTODISCOVER_PATHS', [])

CONFIG = presalytics.lib.config_loader.load_config(additional_paths=autodiscover_paths)

file_logger = CONFIG.get("USE_LOGGER", True)
log_level = CONFIG.get("LOG_LEVEL", logging.DEBUG)

presalytics.lib.logger.configure_logger(log_level=log_level, file_logger=file_logger)

registry_kwargs = {
    'show_errors': False,
    'autodiscover_paths': autodiscover_paths
}

PLUGINS = presalytics.lib.plugins.base.PluginRegistry(**registry_kwargs)

COMPONENTS = presalytics.story.components.ComponentRegistry(**registry_kwargs)
