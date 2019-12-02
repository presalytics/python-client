import pkgutil
import importlib
import os
import typing
import importlib.util


def load_config(additional_paths: typing.List[str] = []) -> typing.Dict:
    current_path = os.getcwd()
    additional_paths.append(current_path)
    config_dict = None
    for path in additional_paths:
        for name in os.listdir(path):
            if name == "config.py":
                config_path = os.path.join(path, name)
                config_spec = importlib.util.spec_from_file_location("config", config_path)
                config_mod = importlib.util.module_from_spec(config_spec)
                config_spec.loader.exec_module(config_mod)
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
