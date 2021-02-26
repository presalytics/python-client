import six
import importlib
import os
import typing
import types
import logging
import importlib.util
import environs
import presalytics.lib.default_settings
import presalytics.lib.util


logger = logging.getLogger(__name__)


def load_config(additional_paths: typing.List[str] = []) -> typing.Dict:
    """
    Searches the current working directory and `additional_paths` for a loadable
    module named `config.py`.  If a file is found and has a global variable named
    'PRESALYTICS', the dictionary contained in the 'PRESALYTICS' is returned.

    *Note*: A environment variable called `autodiscover_paths` is automatically
    loaded into the `additional_paths` keyword argument the the `presalytics` module
    is imported.

    Parameters
    ----------
    additional_paths : list of str, optional
        Additional filepaths to search for files named `config.py`

    Returns
    ----------
    a `dict` containing the PRESALYTICS module environment configuration

    """
    current_path = os.getcwd()
    additional_paths.append(current_path)
    config_dict = None
    try:
        for path in additional_paths:
            for name in os.listdir(path):
                if name == "config.py":
                    config_path = os.path.join(path, name)
                    config_spec = importlib.util.spec_from_file_location("config", config_path)
                    config_mod = importlib.util.module_from_spec(config_spec)
                    config_spec.loader.exec_module(config_mod)  # type: ignore
                    config_dict = getattr(config_mod, "PRESALYTICS", None)
                    if not config_dict:
                        config_dict = config_mod.__dict__
                    if config_dict:
                        break
            if config_dict:
                break
        if config_dict:
            return config_dict  # type: ignore[no-any-return]
        else:
            return {}
    except Exception as ex:
        logger.exception(ex)
        return {}


SETTING_ALLOWED_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'


def is_setting(key: str):
    for letter in key:
        if letter not in SETTING_ALLOWED_CHARS:
            return False
    return True


class SettingsMeta(type):
    def __dir__(cls):
        return [x for x in dir(presalytics.lib.default_settings) if is_setting(x)]


@six.add_metaclass(SettingsMeta)
class Settings(object):
    USE_LOGGER: bool
    LOG_LEVEL: int
    DEBUG: bool
    USERNAME: typing.Optional[str]
    PASSWORD: typing.Optional[str]
    DELEGATE_LOGIN: bool
    CACHE_TOKENS: bool
    CLIENT_ID: str
    CLIENT_SECRET: typing.Optional[str]
    VERIFY_HTTPS: bool
    REDIRECT_URI: str
    RESERVED_NAMES: typing.List[str]
    USE_AUTODISCOVER: bool
    IGNORE_PATHS: typing.List[str]
    PRESALYTICS_SETTINGS_MODULE: str
    INSTALLED_PACKAGES: typing.List[str]
    HOST_EVENTS: str
    HOST_STORY: str
    HOST_OOXML_AUTOMATION: str
    HOST_WORKSPACE_API: str
    HOST_SITE: str
    BROWSER_API_HOST_EVENTS: typing.Optional[str]
    BROWSER_API_HOST_STORY: typing.Optional[str]
    BROWSER_API_HOST_OOXML_AUTOMATION: typing.Optional[str]
    BROWSER_API_HOST_SITE: typing.Optional[str]
    BROWSER_API_HOST_WORKSPACE_API: typing.Optional[str]
    OVERRIDE_REGISTRY_DEFAULTS: bool
    COMPONENTS: typing.List[str]
    PLUGINS: typing.List[str]
    XML_TRANSFORMS: typing.List[str]
    AUTODISCOVER_PATHS = typing.List[str]

    def __init__(self, *args, **kwargs):
        self.get_settings_from_module(presalytics.lib.default_settings)
        self.get_subpackage_settings()
        self.get_settings_from_environment()
        self.get_workspace_settings()

    def __dir__(self):
        return [x for x in dir(presalytics.lib.default_settings) if is_setting(x)]

    def get_settings_from_module(self, mod: types.ModuleType):
        for k, v in mod.__dict__.items():
            if is_setting(k):
                setattr(self, k, v)

    def get_settings_from_environment(self):
        """
        Note: requires default settings already be loaded
        """
        env = environs.Env()
        env.read_env()
        for k, v in self.__dict__.items():
            if os.environ.get(k, None):
                if is_setting(k):
                    if isinstance(v, list):
                        setattr(self, k, env.list(k))
                    elif isinstance(v, bool):
                        setattr(self, k, env.bool(k))
                    elif isinstance(v, int):
                        setattr(self, k, env.int(k))
                    else:
                        setattr(self, k, env(k))

    def get_subpackage_settings(self):
        for pkg_name in self.INSTALLED_PACKAGES:
            if pkg_name != 'presalytics':
                try:
                    mod = presalytics.lib.util.import_string(pkg_name + ".settings")
                    if isinstance(mod, types.ModuleType):
                        self.get_settings_from_module(mod)
                    else:
                        raise ValueError
                except ImportError:
                    logger.error("Module [{}] do not contain a top-level settings attribute for Presalytics settings.".format(pkg_name))
                except ValueError:
                    logger.error("settings must be a Python module type.")

    def get_workspace_settings(self):
        try:
            import settings  # type: ignore
            if isinstance(settings, types.ModuleType):
                self.get_settings_from_module(settings)
            else:
                raise ValueError
        except ImportError:
            pass
        except ValueError:
            logger.error("settings must be a Python module type.")
