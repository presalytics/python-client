import pkgutil
import importlib
import os
import typing
import logging
import importlib.util


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
                    config_spec.loader.exec_module(config_mod) #type: ignore
                    config_dict = getattr(config_mod, "PRESALYTICS", None)
                    if not config_dict:
                        config_dict = config_mod.__dict__
                    if config_dict:
                        break
            if config_dict:
                break
        if config_dict:
            return config_dict
        else:
            return {}
    except Exception as ex:
        logger.exception(ex)
        return {}
        
