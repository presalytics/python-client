"""
Presalytics python client
https://presalytics.io
"""
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
from presalytics.client.api import Client
from presalytics.lib.plugins.base import PluginBase
from presalytics.lib.plugins.external import ApprovedExternalLinks, ApprovedExternalScripts
from presalytics.lib.plugins.jinja import JinjaPluginMakerMixin
from presalytics.lib.plugins.local import LocalStylesPlugin
from presalytics.lib.plugins.matplotlib import Mpld3Plugin
from presalytics.lib.plugins.ooxml import OoxmlTheme
from presalytics.lib.plugins.reveal import RevealConfigPlugin
from presalytics.lib.plugins.reveal_theme import RevealCustomTheme
from presalytics.lib.templates.base import JinjaTemplateBuilder
from presalytics.lib.widgets.matplotlib import MatplotlibFigure
from presalytics.lib.widgets.ooxml import OoxmlFileWidget, OoxmlEndpointMap
from presalytics.story.outline import StoryOutline
from presalytics.story.revealer import Revealer
from presalytics.story.components import WidgetBase, PageTemplateBase, Renderer, ThemeBase
from presalytics.lib.tools.ooxml_tools import (
    create_theme_from_ooxml_document,
    create_pages_from_ooxml_document,
    create_story_from_ooxml_file,
    create_outline_from_ooxml_document
)
from presalytics.lib.widgets.ooxml_editors import (
    OoxmlEditorWidget,
    XmlTransformBase,
    ChangeShapeColor
)

__all__ = [
    'CONFIG',
    'COMPONENTS',
    'PLUGINS',
    'Client',
    'PluginBase',
    'ApprovedExternalLinks',
    'ApprovedExternalScripts',
    'JinjaPluginMakerMixin',
    'LocalStylesPlugin',
    'Mpld3Plugin',
    'OoxmlTheme',
    'RevealConfigPlugin',
    'RevealCustomTheme',
    'JinjaTemplateBuilder',
    'MatplotlibFigure',
    'OoxmlFileWidget',
    'OoxmlEndpointMap',
    'StoryOutline',
    'Revealer',
    'WidgetBase',
    'PageTemplateBase',
    'Renderer',
    'ThemeBase',
    'create_theme_from_ooxml_document',
    'create_pages_from_ooxml_document',
    'create_story_from_ooxml_file',
    'create_outline_from_ooxml_document',
    'OoxmlEditorWidget',
    'XmlTransformBase',
    'ChangeShapeColor'
]

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
