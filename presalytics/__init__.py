"""
# Presalytics Python Library
For more information, visit https://presalytics.io.

# Overview

The Presalytics Python Library streamlines analytic operations across analysts, executives, consultants, 
and developers.  These tools enable for a simplified workflow for analysts to rapidly generate 
client-ready presentation materials and web content that update in real-time and easily scale across your user-base.  

Our objective when building this platform is make the analyst experience as simple as possible.  
Set up time for new user should take less than half an hour, and all features are self-service and self-explanatory.  

Of course, if you have any questions or need help to get going, you can [contact us](/contact-us) or 
quickly get the help you need on our [slack channel](https://presalytics.slack.com) 
([Join Here!](https://join.slack.com/t/presalytics/shared_invite/enQtODExMjc3MDE1Nzc5LWU0ZDlhZTgwZTM3MzQ4Yzc4Nzk4Zjc0NmQ3YjgzNTEwODdlYjM0ZjFkZWI4Y2ZhNzBmOTZhMzA2MzE3YjFiZTg)).

To get going quickly, you can browse our [Getting Started](https://presalytics.io/docs/getting-started/) page and review 
some [examples](https://presalytics.io/docs/examples).

For more advanced users and developers, you can learn more about the API by reviewing 
the [service structure](https://presalytics.io/docs/how-it-works) to build a better understanding 
of the API and its [security](https://presalytics.io/docs/develpers/security) features.

# Installation

The Presalytics Python Library is avialabe in python package index, and can be installed via pip:

~~~~python
pip install presalytics
~~~~

# Contributing

Presalytics.io is on [Github](https://github.com/presalytics).  Bug reports and pull requests are strongly encouraged at
the package [repository](https://github.com/presalytics/python-client). If you encounter any problems or have any suggestions for 
the API endpoints that this libary interacts with at https://api.presalytics.io, please open an issue in the 
[API repository](https://github.com/presalytics/Presalytics-API).

# License

The Presalytics Python Library can be used in any of your applications and is covered by the MIT License.  This library
exchanges infromation with other web APIs that may be proprietary and carry their own licensing restriction.  More more
information on licensing, please contact [inquires@presalytics.io](mailto:inquires@presalytics.io).

"""
import os
import environs
import logging
import pkg_resources
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
"""
Nested `dict` containing runtime configuration values for the Presalytics Python Library.
Typically, these are reuseable values stored in separate file that are loaded when the 
module in imported via the `import presalytics` command.  This top-level module then
runs the `presalytics.lib.config_loader.load_config` method into load values into the
the `CONFIG` global variable.  Modules through the package use the `CONFIG` variable to
simplify their API calls store conststants for use throughout the package.  See 
`presalytics.lib.config_loader.load_config` for ways to programmatically load the
`CONFIG`.

Configuration Values
----------

USE_LOGGER : bool, optional
    Toggles whether the presalytics verbose file logger should be used.  Helpful for 
    tracing exceptions while writing code.  Default is True.

LOG_LEVEL : str, optional
    Defaults to `DEBUG`

USERNAME : str, optional
    The user's Presalytics API email/username.  This is the email address that the user uses when logging in at 
    https://login.presalytics.io.  Will be passed to instances of the `presalytics.client.api.Client` object.

PASSWORD : str, optional
    The user's Presalytics API username.  Will be passed to instances of the 
    `presalytics.client.api.Client` object.  If running in an insecure or 
    multiuser environment, leave this blank and let the `presalytics.client.api.Client`
    object handle token acquisition via browser-based login.

DELEGATE_LOGIN: bool, optional
    Defaults to False.  Indicates whether the client would redirect to a browser to 
    acquire an API token. If `DELEGATE_LOGIN` is `True`, when the `presalytics.client.api.Client` does not have 
    access to a valid API token, the client will raise a `presalytics.lib.exceptions.InvalidTokenException`.
    The default operation will automatically open a new browser tab to acquire a new token 
    via website client from the presalytics.io login page.  Putting this setting to True is
    useful for server-side development.

CACHE_TOKENS: bool, optional
    Defaults to True.  Indicates whether the `presalytics.client.api.Client` should store
    tokens in the current working directory in a file call "token.json". This should be
    set to False for mutli-user environments.

CLIENT_ID : str, optional
    For developer use. Allows developers to implement a `client_credentials` OpenID
    Connect login.  Defaults to "python-client".  

CLIENT_SECRET : str, optional
    For developer use. Allows developers to implement a `client_credentials` OpenID
    Connect login.  Defaults to None.  

VERIFY_HTTPS : bool, optional
    For developer use.  Allows for unencrypted connections.  Defaults to True.  No 
    reason to turn this to False unless you're in a complex development scenario
    and you know what you're doing.

HOSTS : dict, optional
    For developer use.  Allows API class to target hosts other than api.presalytics.io

REDIRECT_URI : string, optional
    For developer use.  Useful if implementing authorization code flow for and OpenID Connect client.
    Redirect URIs must be approved by Presalytics API devops for use in client applications.

RESERVED_NAMES: list of str, optional
    A list of filenames for *.py files in the current workspace that should be ignored by the 
    registries. 

IGNORE_PATHS: list of str, optional
    A list of paths to not to include in registry autosdiscover

BROWSER_API_HOST: str, optional
    If present, the root url for browser-based api calls.  May be required when services are running on a cluster that
    deletegates certificate authentication to an external service.  See for more info: https://developer.mozilla.org/en-US/docs/Web/Security/Mixed_content

The object can also take on values for user-defined extensions, and please consult
the documentation for those package for those vairables definition.
"""



file_logger = CONFIG.get("USE_LOGGER", True)
log_level = CONFIG.get("LOG_LEVEL", logging.DEBUG)

presalytics.lib.logger.configure_logger(log_level=log_level, file_logger=file_logger)

registry_kwargs = {
    'show_errors': False,
    'autodiscover_paths': autodiscover_paths,
    'reserved_names': CONFIG.get("RESERVED_NAMES", []),
    'ignore_paths': CONFIG.get("IGNORE_PATHS", [])
}

PLUGINS = presalytics.lib.plugins.base.PluginRegistry(**registry_kwargs)
"""
Instance of `presalytics.lib.plugins.base.PluginRegistry`.  A container listing the
Presalytics Library Plugins available and loaded in this environment. This instance is used 
by `presalytics.story.components.Renderer` subclasses (e.g., `presalytics.story.revealer.Revealer`)
to write scripts and links into stories.
"""

COMPONENTS = presalytics.story.components.ComponentRegistry(**registry_kwargs)
"""
Instance of `presalytics.story.components.ComponentRegistry`.  Registry for Library components and 
component instances.  A container listing the Presalytics Library components and instances available 
and loaded in this environment. This instance is used by `presalytics.story.components.Renderer` subclasses 
(e.g., `presalytics.story.revealer.Revealer`) to convert widgets, pages, and themes into stories.
"""

try:
    __version__ = pkg_resources.require(presalytics.__name__)[0].version
except Exception:
    __version__ = "build"

from presalytics.client.api import Client
from presalytics.lib.plugins.base import PluginBase
from presalytics.lib.plugins.external import ApprovedExternalLinks, ApprovedExternalScripts
from presalytics.lib.plugins.jinja import JinjaPluginMakerMixin
from presalytics.lib.plugins.local import LocalStylesPlugin
from presalytics.lib.plugins.matplotlib import Mpld3Plugin
from presalytics.lib.plugins.ooxml import OoxmlTheme
from presalytics.lib.plugins.reveal import RevealConfigPlugin
from presalytics.lib.plugins.reveal_theme import RevealCustomTheme
from presalytics.lib.plugins.scss import ScssPlugin
from presalytics.lib.templates.base import (
    JinjaTemplateBuilder,
    BootstrapCustomTemplate
)
from presalytics.lib.widgets.matplotlib import MatplotlibFigure, MatplotlibResponsiveFigure
from presalytics.lib.widgets.d3 import (
    D3Widget
)
from presalytics.lib.widgets.ooxml import (
    OoxmlWidgetBase,
    OoxmlFileWidget, 
    OoxmlEndpointMap,
    ChartUpdaterWidget,
    TableUpdaterWidget
)
from presalytics.story.outline import StoryOutline
from presalytics.story.revealer import Revealer
from presalytics.story.components import WidgetBase, PageTemplateBase, Renderer, ThemeBase
from presalytics.lib.tools.ooxml_tools import (
    create_story_from_ooxml_file
)
from presalytics.lib.tools.story_tools import story_post_file_bytes
from presalytics.lib.tools.component_tools import (
    create_outline_from_page,
    create_outline_from_widget
)
from presalytics.lib.widgets.ooxml_editors import (
    OoxmlEditorWidget,
    XmlTransformBase,
    ChangeShapeColor,
    TextReplace,
    MultiXmlTransform
)


__all__ = [
    'CONFIG',
    'COMPONENTS',
    'PLUGINS',
    'Client',
    'StoryOutline',
    'Renderer',
    'Revealer',
    'MatplotlibFigure',
    'MatplotlibResponsiveFigure',
    'OoxmlFileWidget',
    'OoxmlEndpointMap',
    'OoxmlWidgetBase',
    'OoxmlEditorWidget',
    'D3Widget',
    'ChartUpdaterWidget',
    'TableUpdaterWidget',
    'XmlTransformBase',
    'ChangeShapeColor',
    'TextReplace',
    'MultiXmlTransform',
    'ApprovedExternalLinks',
    'ApprovedExternalScripts',
    'LocalStylesPlugin',
    'OoxmlTheme',
    'RevealConfigPlugin',
    'RevealCustomTheme',
    'JinjaTemplateBuilder',
    'WidgetBase',
    'PageTemplateBase',
    'ScssPlugin',
    'create_story_from_ooxml_file',
    'story_post_file_bytes',
    'create_outline_from_page',
    'create_outline_from_widget'
]