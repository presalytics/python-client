import pkgutil
import importlib
import traceback
import sys
import os
import inspect
import logging
import typing
import abc


logger = logging.getLogger('presalytics.lib.registry')


class RegistryBase(abc.ABC):
    registry: typing.Dict[str, typing.Type]
    show_errors = False

    def __init__(self, show_errors=False, autodiscover_paths=[], reserved_names: typing.List[str] = None, **kwargs):
        RegistryBase.show_errors = show_errors
        self.autodiscover_paths = autodiscover_paths
        self.registry = {}
        self.reserved_names = ["config.py", "setup.py"]
        try:
            if reserved_names:
                self.reserved_names.extend(reserved_names)
        except Exception:
            pass
        self.discover()

    @abc.abstractmethod
    def get_type(self, klass):
        raise NotImplementedError

    @abc.abstractmethod
    def get_name(self, klass):
        raise NotImplementedError

    @staticmethod
    def onerror(name):
        if RegistryBase.show_errors:
            print("Error importing module %s" % name)
            t, value, tb = sys.exc_info()
            traceback.print_tb(tb)

    def get(self, key):
        return self.registry.get(key, None)

    def get_classes_from_module(self, module):
        self.get_classes(module)
        for loader, name, is_pkg in pkgutil.walk_packages(module.__path__, onerror=RegistryBase.onerror):
            full_name = module.__name__ + '.' + name
            sub_module = importlib.import_module(full_name)
            if sub_module.__name__.startswith('presalytics'):
                if is_pkg:
                    self.get_classes_from_module(sub_module)
                else:
                    self.get_classes(sub_module)

    def load_class(self, klass):
        if inspect.isclass(klass):
            klass_type = self.get_type(klass)
            if klass_type:
                try:
                    klass_name = self.get_name(klass)
                    if klass_name:
                        key = "{0}.{1}".format(klass_type, klass_name)
                        if key not in self.registry.keys():
                            self.registry[key] = klass
                except Exception:
                    message = "Unable to register class {0} with type {1}".format(klass.__name__, klass_type)
                    logger.error(message)
        else:
            try:
                message = "{0} is not a class".format(klass.__class__.__name__)
                logger.error(message)
            except Exception:
                pass

    def get_classes(self, module):
        for key, val in module.__dict__.items():
            if inspect.isclass(val) or isinstance(val, abc.ABC):
                self.load_class(val)

    def discover(self):
        current_path = os.getcwd()
        if current_path not in self.autodiscover_paths:
            self.autodiscover_paths.append(current_path)
        for path in self.autodiscover_paths:
            for name in os.listdir(path):
                if name.endswith(".py") and name not in self.reserved_names:
                    try:
                        mod_path = os.path.join(path, name)
                        mod_spec = importlib.util.spec_from_file_location(name, mod_path)
                        mod = importlib.util.module_from_spec(mod_spec)
                        mod_spec.loader.exec_module(mod)
                        self.get_classes(mod)
                    except Exception:
                        message = "Could not load classes from file {0}".format(name)
                        logger.error(message)
        for finder, name, ispkg in pkgutil.iter_modules():
            if name.startswith('presalytics'):
                mod = importlib.import_module(name)
                self.get_classes_from_module(mod)

    def register(self, klass):
        self.load_class(klass)
