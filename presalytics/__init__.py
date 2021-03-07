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
import pkg_resources
import presalytics.lib
import presalytics.lib.logger
import presalytics.lib.plugins
import presalytics.lib.plugins.base
import presalytics.lib.config_loader
import presalytics.story
import presalytics.story.components

settings = presalytics.lib.config_loader.Settings()
"""
The Presalytics Python Client settings instance.

Settings are are loaded into this instance via package defaults.  Users can override
default setting by (in order of precedence):

    1. Settings variable using a `settings.py` file in the current working directory
    2. Using a .env file
    3. Setting environment variables with same key as default setting

For a comprehsive list of settings values, please review `presalytics.lib.default_settings`.
"""

presalytics.lib.logger.configure_logger(log_level=settings.LOG_LEVEL, file_logger=settings.USE_LOGGER)  # type: ignore[attr-defined]


PLUGINS = presalytics.lib.plugins.base.PluginRegistry()
"""
Instance of `presalytics.lib.plugins.base.PluginRegistry`.  A container listing the
Presalytics Library Plugins available and loaded in this environment. This instance is used
by `presalytics.story.components.Renderer` subclasses (e.g., `presalytics.story.revealer.Revealer`)
to write scripts and links into stories.
"""

COMPONENTS = presalytics.story.components.ComponentRegistry()
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
from presalytics.lib.plugins.base import PluginBase  # noqa: F401
from presalytics.lib.plugins.external import ApprovedExternalLinks, ApprovedExternalScripts
from presalytics.lib.plugins.jinja import JinjaPluginMakerMixin  # noqa: F401
from presalytics.lib.plugins.local import LocalStylesPlugin
from presalytics.lib.plugins.matplotlib import Mpld3Plugin  # noqa: F401
from presalytics.lib.plugins.ooxml import OoxmlTheme
from presalytics.lib.plugins.reveal import RevealConfigPlugin
from presalytics.lib.plugins.reveal_theme import RevealCustomTheme
from presalytics.lib.plugins.scss import ScssPlugin
from presalytics.lib.templates.base import (
    JinjaTemplateBuilder,
    BootstrapCustomTemplate  # noqa: F401
)
from presalytics.lib.widgets.matplotlib import MatplotlibFigure, MatplotlibResponsiveFigure
from presalytics.lib.widgets.d3 import (
    D3Widget
)
from presalytics.lib.widgets.chart import ChartWidget
from presalytics.lib.widgets.data_table import DataTableWidget
from presalytics.lib.widgets.url import UrlWidget
from presalytics.lib.widgets.markdown import MarkdownWidget  # noqa: F401
from presalytics.lib.widgets.ooxml import (
    OoxmlWidgetBase,
    OoxmlFileWidget,
    OoxmlEndpointMap,
    ChartUpdaterWidget,
    TableUpdaterWidget
)
from presalytics.story.outline import StoryOutline
from presalytics.story.revealer import Revealer
from presalytics.story.renderers import ClientSideRenderer
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
    'COMPONENTS',
    'PLUGINS',
    'Client',
    'StoryOutline',
    'Renderer',
    'ClientSideRenderer',
    'Revealer',
    'MatplotlibFigure',
    'MatplotlibResponsiveFigure',
    'Mpld3Plugin',
    'MarkdownWidget',
    'OoxmlFileWidget',
    'OoxmlEndpointMap',
    'OoxmlWidgetBase',
    'OoxmlEditorWidget',
    'D3Widget',
    'ChartWidget',
    'DataTableWidget',
    'UrlWidget',
    'ChartUpdaterWidget',
    'TableUpdaterWidget',
    'BootstrapCustomTemplate',
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
    'ThemeBase',
    'create_story_from_ooxml_file',
    'story_post_file_bytes',
    'create_outline_from_page',
    'create_outline_from_widget'
]
