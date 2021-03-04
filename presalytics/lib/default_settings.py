"""
Default settings for the Presalytics Python Client

This module contains a comprehesive set of values that can used to control the Presalytics
Python client's behavior.  The `presalytics.lib.loader` module contains to load these
settings into the `presalytics.settings` instance on initialization.  User should not reference
the settings in this module directly, but rather use the `presaltyics.settings` instacne in their
scripts and applications.  Settings can be referring to as `presaltyics.settings.[SETTING_NAME]`.

Users can override these default settings via two methods:

    1. Environment Variables:  Evironment variables (or a .env file in the working directory) with
    the same key as the variable in this file will override this, provide the value can be parsed by
    the [environs](https://pypi.org/project/environs/) python package.

    2. `settings.py` file:  A file named `settings.py` in the user's current working directory.  The active working
    direcotry can be determine by using the `os.getcwd()` command.  This `settings.py` file takes the highest
    priority.  Settings defined in this file will override both the `default_settings.py` file and any enviroment variables.
"""
import os
import logging
import typing
import presalytics.lib.constants


#################################
#     GENERAL CONFIGURATION     #
#################################

USE_LOGGER: bool = False
"""
Toggles whether the presalytics verbose file logger should be used.  Helpful for
tracing exceptions while writing code.
"""

LOG_LEVEL = logging.DEBUG
"""
Sets the logging verbosity
"""

DEBUG = False
"""
Use debugging features.  Useful for rendering widgets and pages.
"""

USERNAME: typing.Optional[str] = os.environ.get('PRESALYTICS_USERNAME', None)
"""
The user's Presalytics API email/username.  This is the email address that the user uses when logging in at
https://login.presalytics.io.  Will be passed to instances of the `presalytics.client.api.Client` object.
"""

PASSWORD: typing.Optional[str] = os.environ.get('PRESALYTICS_PASSWORD', None)
"""
The user's Presalytics API username.  Will be passed to instances of the
`presalytics.client.api.Client` object.  If running in an insecure or
multiuser environment, leave this blank and let the `presalytics.client.api.Client`
object handle token acquisition via browser-based login.
"""

DELEGATE_LOGIN: bool = False
"""
Defaults to False.  Indicates whether the client would redirect to a browser to
acquire an API token. If `DELEGATE_LOGIN` is `True`, when the `presalytics.client.api.Client` does not have
access to a valid API token, the client will raise a `presalytics.lib.exceptions.InvalidTokenException`.
The default operation will automatically open a new browser tab to acquire a new token
via website client from the presalytics.io login page.  Putting this setting to True is
useful for server-side development.
"""

CACHE_TOKENS: bool = False
"""
Indicates whether the `presalytics.client.api.Client` should store
tokens in the current working directory in a file call "token.json". This should be
set to False for mutli-user environments.
"""

CLIENT_ID: str = presalytics.lib.constants.DEFAULT_CLIENT_ID
"""
For developer use. Allows developers to implement a `client_credentials` OpenID
Connect login.  Defaults to "python-client".
"""

CLIENT_SECRET: typing.Optional[str] = None
"""
For developer use. Allows developers to implement a `client_credentials` OpenID
Connect login.  Defaults to None.
"""

VERIFY_HTTPS: bool = True
"""
For developer use.  Allows for unencrypted connections.  Defaults to True.  No
reason to turn this to False unless you're in a complex development scenario
and you know what you're doing.
"""


REDIRECT_URI: str = presalytics.lib.constants.REDIRECT_URI
"""
For developer use.  Useful if implementing authorization code flow for and OpenID Connect client.
Redirect URIs must be approved by Presalytics API devops for use in client applications.
"""

RESERVED_NAMES: typing.List[str] = []
"""
A list of filenames for *.py files in the current workspace that should be ignored by the
registries.
"""

USE_AUTODISCOVER: bool = False
"""
Allow registries to recurisively serach working directory and virtual environments for presalytics componets.
Good for development, but degrades performance.
"""

AUTODISCOVER_PATHS: typing.List[str] = []
"""
A list of extra paths to search when looking for classes to add to a registry.  By default, registries
already search the current directory and virtual environment folders when `USE_AUTODISCOVER` is
set to true.
"""

IGNORE_PATHS: typing.List[str] = []
"""
A list of paths to not to include in registry autosdiscover
"""

PRESALYTICS_SETTINGS_MODULE: str = 'settings.py'
"""
File path to the python module in the user's workspace with the user overrides for these settings.
Should should be change if naming conflict exist with another package (e.g., a Django `settings.py` file)
"""

INSTALLED_PACKAGES: typing.List[str] = ['presalytics']
"""
List of strings containing name of package containing Presalytics settings, plugins and components
"""

#################
#     HOSTS     #
#################

HOST_EVENTS: str = presalytics.lib.constants.DEFAULT_HOST_EVENTS
"""
The base url for calls to the Events API
"""

HOST_STORY: str = presalytics.lib.constants.DEFAULT_HOST_STORY
"""
The base url for calls into the Story API
"""

HOST_OOXML_AUTOMATION: str = presalytics.lib.constants.DEFAULT_HOST_OOXML_AUTOMATION
"""
The base url for calls into the Ooxml Automation API
"""

HOST_WORKSPACE_API: str = presalytics.lib.constants.DEFAULT_HOST_WORKSPACE_API
"""
The base url calls into the Workspace API
"""

HOST_DOC_CONVERTER: str = presalytics.lib.constants.DEFAULT_HOST_DOC_CONVERTER
"""
The base url for calls into the Doc Converter API
"""

HOST_SITE: str = presalytics.lib.constants.DEFAULT_HOST_SITE
"""
The base url for API calls into the presalytics website
"""

BROWSER_API_HOST_EVENTS: typing.Optional[str] = None
"""
The base url web broswers should use to make API calls into Events API.  Useful during rendering of stories.
Defaults to the `HOST_EVENTS` setting if not present.
"""

BROWSER_API_HOST_STORY: typing.Optional[str] = None
"""
The base url web broswers should use to make API calls into Story API.  Useful during rendering of stories.
Defaults to the `HOST_STORY` setting if not present.
"""

BROWSER_API_HOST_OOXML_AUTOMATION: typing.Optional[str] = None
"""
The base url web broswers should use to make API calls into Ooxml Automation API.  Useful during rendering of stories.
Defaults to the `HOST_OOXML_AUTOMATION` setting if not present.
"""

BROWSER_API_HOST_SITE: typing.Optional[str] = None
"""
The base url web broswers should use to make API calls into the presalytics website.  Mainly useful for custom authentication schemes.
Defaults to the `HOST_SITE` setting if not present.
"""

BROWSER_API_HOST_WORKSPACE_API: typing.Optional[str] = None
"""
The base url web broswers should use to make API calls into the Workspace API.  Useful during rendering of stories.
Defaults to the `HOST_WORKSPACE_API` setting if not present.
"""


######################
#     REGISTRIES     #
######################

OVERRIDE_REGISTRY_DEFAULTS: bool = False
"""
By default, registry settings are additive --> Registries import the default classes from this file and any `settings.py`
files found in packages in the `INSTALLED_PACKAGES` setting.
For a performance boost, a user can limit the imported list of classes in their registries to a defined
list in their `settings.py` file by setting `OVERRIDE_REGISTRY_DEFAULTS` to `True`
"""

COMPONENTS: typing.List[str] = [
    'presalytics.lib.widgets.chart.ChartWidget',
    'presalytics.lib.widgets.d3.D3Widget',
    'presalytics.lib.widgets.data_table.DataTableWidget',
    'presalytics.lib.widgets.markdown.MarkdownWidget',
    'presalytics.lib.widgets.matplotlib.MatplotlibFigure',
    'presalytics.lib.widgets.matplotlib.MatplotlibResponsiveFigure',
    'presalytics.lib.widgets.ooxml.OoxmlFileWidget',
    'presalytics.lib.widgets.ooxml.ChartUpdaterWidget',
    'presalytics.lib.widgets.ooxml.TableUpdaterWidget',
    'presalytics.lib.widgets.url.UrlWidget',
    'presalytics.lib.themes.ooxml.OoxmlTheme',
    'presalytics.lib.templates.base.WidgetPage',
    'presalytics.lib.templates.base.JinjaTemplateBuilder',
    'presalytics.lib.templates.base.TitleWithSingleItem',
    'presalytics.lib.templates.base.TwoUpWithTitle',
    'presalytics.lib.templates.base.BootstrapCustomTemplate'
]
"""
A list of string containing the dotted path names of Components that should be imported into the
Presalytics component registry at `presalytics.COMPONENTS`.  The dotted path name is the same name path used for an import statement
at the top of a python file
"""

PLUGINS: typing.List[str] = [
    'presalytics.lib.plugins.external.ApprovedExternalLinks',
    'presalytics.lib.plugins.external.ApprovedExternalScripts',
    'presalytics.lib.plugins.local.LocalStylesPlugin',
    'presalytics.lib.plugins.matplotlib.Mpld3Plugin',
    'presalytics.lib.plugins.matplotlib.Mpld3Plugin',
    'presalytics.lib.plugins.ooxml.OoxmlTheme',
    'presalytics.lib.plugins.reveal_theme.RevealCustomTheme',
    'presalytics.lib.plugins.reveal.RevealConfigPlugin',
    'presalytics.lib.plugins.scss.ScssPlugin'
]
"""
A list of string containing the dotted path names of Plugins that should be imported into the
Presalytics plugins registry at `presalytics.PLUGINS`.  The dotted path name is the same name path used for an import statement
at the top of a python file
"""

XML_TRANSFORMS: typing.List[str] = [
    'presalytics.lib.widgets.ooxml_editors.ChangeShapeColor',
    'presalytics.lib.widgets.ooxml_editors.TextReplace',
    'presalytics.lib.widgets.ooxml_editors.MultiXmlTransform'
]
"""
A list of string containing the dotted path names of Components that should be imported into the
Presalytics component registry.  The dotted path name is the same name path used for an import statement
at the top of a python file
"""
