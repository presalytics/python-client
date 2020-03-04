import pkgutil
import importlib
import traceback
import sys
import os
import inspect
import logging
import typing
import abc
import re
import types
import ast
import presalytics.lib.exceptions


logger = logging.getLogger('presalytics.lib.registry')


class RegistryBase(abc.ABC):
    """
    In-memory container for python objects that return attributes from both the
    `get_type` and `get_name` abstract functions. 

    The `discover` method searches the current working directory, directories at
    in the `autodiscover_paths` attribute, and packages in the current python environment
    prefixed with "presalytics" (i.e., extensions).
    """
    registry: typing.Dict[str, typing.Type]
    deferred_modules: typing.List[typing.Dict[str, typing.Any]]
    show_errors = False

    def __init__(self, 
                 show_errors=False, 
                 autodiscover_paths=[], 
                 reserved_names: typing.List[str] = None, 
                 ignore_paths: typing.List[str] = None,
                 **kwargs):
        RegistryBase.show_errors = show_errors
        self.error_class = presalytics.lib.exceptions.RegistryError
        self.autodiscover_paths = autodiscover_paths
        self.ignore_paths = ignore_paths if ignore_paths else []
        self.registry = {}
        self.reserved_names = ["config.py", "setup.py"]
        self.deferred_modules = []  # modules to load at at runtime, if theres a ciruclat dependency at import-time
        try:
            if reserved_names:
                self.reserved_names.extend(reserved_names)
        except Exception:
            pass
        remove_paths = []
        for path in self.ignore_paths:
            for search_path in self.autodiscover_paths:
                if path in search_path:
                    remove_paths.append(search_path)
        for remove_path in remove_paths:
            self.autodiscover_paths.remove(remove_path)
        self.discover()
        self.key_regex = re.compile(r'(.*)\.(.*)')

    def raise_error(self, message):
        raise self.error_class(self, message)

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
        self.load_deferred_modules()
        return self.registry.get(key, None)

    def get_classes_from_module(self, module):
        self.get_classes(module)
        if getattr(module, "__path__", None):
            for loader, name, is_pkg in pkgutil.walk_packages(module.__path__, onerror=RegistryBase.onerror):
                full_name = module.__name__ + '.' + name
                try:
                    if not self.module_is_in_stackframe(full_name):
                        sub_module = importlib.import_module(full_name)
                        if sub_module.__name__.startswith('presalytics'):
                            if is_pkg:
                                self.get_classes_from_module(sub_module)
                            else:
                                self.get_classes(sub_module)
                except Exception:
                    pass

    def get_registry_key(self, klass):
        key = None
        klass_type = self.get_type(klass)
        if klass_type:
            klass_name = self.get_name(klass)
            if klass_name:
                key = "{0}.{1}".format(klass_type, klass_name)
        return key

    def load_class(self, klass):
        if inspect.isclass(klass):
            try:
                key = self.get_registry_key(klass)
                if key:
                    if key not in self.registry.keys():
                        self.registry[key] = klass
            except Exception as ex:
                if self.show_errors:
                    logger.exception(ex)
                    klass_type = self.get_type(klass)
                    message = "Unable to register class {0} with type {1}".format(klass.__name__, klass_type)
                    logger.error(message)
        else:
            try:
                if self.show_errors:
                    message = "{0} is not a class".format(klass.__class__.__name__)
                    logger.error(message)
            except Exception:
                pass

    def get_classes(self, module):
        for key, val in module.__dict__.items():
            if inspect.isclass(val) or isinstance(val, abc.ABC):
                self.load_class(val)


    def load_deferred_modules(self):
        if len(self.deferred_modules) > 0:
            new_deferred = []
            for mod in self.deferred_modules:
                try:
                    name = mod.get("name") 
                    if name in sys.modules: 
                        module = sys.modules[name] 
                    else: 
                        spec = mod.get("spec")
                        module = mod.get("module")
                        sys.modules[name] = module
                        spec.loader.exec_module(module) 
                    self.get_classes(module)
                except Exception as ex:
                    logger.exception(ex)
                    message = "Failure to execute deferred load on module '{}'.  Please check exception message and review for errors.".format(mod.get("name", None))
                    logger.error(message)
                    new_deferred.append(mod)
            self.deferred_modules = new_deferred # removes modules successfully loaded from the list
                 
                
    def discover(self):
        current_path = os.getcwd()
        if current_path not in self.autodiscover_paths:
            self.autodiscover_paths.append(current_path)
        for path in self.autodiscover_paths:
            for name in os.listdir(path):
                if name.endswith(".py") and name not in self.reserved_names:
                    module_name = name.replace(".py", "")
                    try:
                        mod_path = os.path.join(path, name)
                        mod_spec = importlib.util.spec_from_file_location(module_name, mod_path)
                        if not self.module_is_in_stackframe(module_name):
                            """
                            Defer workspace-level imports so these modules only load once
                            This avoids memory errors in computationally-intensive packages (in some environments)
                            and packages built using Intel's MKL (e.g., scipy, numpy, sklearn), which
                            raises ValueErrors when modules are re-executed under the same interpreter w/o a ipython kernel.
                            TODO: Add note to docs saying not to put components and plugins in the same file
                            """
                            mod = importlib.util.module_from_spec(mod_spec)
                            self.deferred_modules.append({
                                "name": module_name,
                                "module": mod,
                                "spec": mod_spec
                            })
                    except (AttributeError, ImportError) as circ:
                        # Checks for targets of circular imports, and defer those imports to runtime
                        message = "Likely circular import in module '{}'. Deferring import to run-time.".format(mod.__name__)
                        logger.info(message)
                        self.deferred_modules.append({
                            "name": mod.__name__,
                            "module": mod,
                            "spec": mod_spec
                        })
                    except Exception as ex:
                        if self.show_errors:
                            logger.exception(ex)
                            message = "Could not load classes from file {0}".format(name)
                            logger.error(message)
        for finder, name, ispkg in pkgutil.iter_modules():
            if name.startswith('presalytics'):
                mod = importlib.import_module(name)
                self.get_classes_from_module(mod)

    def module_is_in_stackframe(self, module_name, frame=None) -> bool:
        """Prevent cycles by skipping modules already loaded in the stack frame
        """
        in_stack = False
        try:
            if not frame:
                frame = inspect.currentframe()
            frame_module = frame.f_globals['__name__']
            if frame_module == '__main__':
                try:
                    frame_module = inspect.getmodule(frame).__spec__.name #type: ignore
                except AttributeError:
                    # vscode and spyder's parent controllers load __main__ without a module spec
                    if not getattr(inspect.getmodule(frame), "__spec__", None):
                        try:
                            fname = inspect.getmodule(frame).__dict__['__file__']
                            frame_module = os.path.basename(fname).replace(".py", "")
                            if module_name == frame_module:
                                return True
                            else: 
                                return False
                        except AttributeError:
                            return in_stack
                        except Exception:
                            return True
                    else:
                        return True # Don't load this module for unknown errors
                except Exception:
                    return True
            if module_name == frame_module:
                in_stack = True
            else:
                if frame.f_back:
                    in_stack = self.module_is_in_stackframe(module_name, frame=frame.f_back)
        except Exception:
            # if something wonky happens, don't load this module
            # if loaded in IronPython or Jython, this will probably fire (untested)
            in_stack = True
        finally:
            del frame
        return in_stack


    def register(self, klass):
        self.load_class(klass)
    
    def unregister(self, klass):
        key = self.get_registry_key(klass)
        if key:
            self.registry.pop(key)

    def find_class(self, string_with_key_or_name) -> typing.List[str]:
        is_key = self.key_regex.match(string_with_key_or_name)
        if is_key:
            return [self.get(string_with_key_or_name)]
        else:
            self.load_deferred_modules()
            return [x for x in self.registry.keys() if string_with_key_or_name in x]
            
            
            

