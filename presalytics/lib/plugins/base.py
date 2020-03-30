import abc
import typing
import logging
import collections
import lxml
import lxml.etree
import sys
import six
import lxml
import presalytics
import presalytics.lib.exceptions
import presalytics.lib.registry


logger = logging.getLogger('presalytics.lib.plugins.base')


class PluginBase(abc.ABC):
    """
    A plugin converts a dictionary of configuration values into an html script.
    Typically plugins are are used as reusable mapping classes to add script or link tags to
    to a rendered html body.

    Attributes
    ----------

    __plugin_kind__ : str
        The __plugin_kind__ is a static string that instructs classes 
        the render story outlines (e.g., presalytics.story.revealer.Revealer) where
        to where render the plugin (i.e., at the bottom of the html body for scripts).

    __plugin_name__ : str
        The __plugin_name__ is a static string that uniquely identifies this plugin to classes
        the render story outlines (e.g., `presalytics.story.revealer.Revealer`).

    __dependencies__ : list of dict
        A list of plugs that should be rendered above this plugin in an html document.  This ensures
        the needed javascript or css is loaded prior user's plugin runs.
        
        For example, if a user creates plugin requires d3.js to function, dependencies should include
        the following configuration:

            __dependencies__ = [
                {
                    'kind': 'script',
                    'name': 'external_scripts',
                    'config': {
                        'approved_scripts_key': 'd3'
                    }
                }
            ]

        This ensures that the `presalytics.lib.plugins.external.ApprovedExternalScripts` loads during the
        rendering pushes a `<script>` tag into the render html that tells the browser to download d3.js from
        a CDN.

    """
    __plugin_kind__: str
    __plugin_name__: str
    __dependencies__: typing.List[typing.Dict]

    __dependencies__ = []

    config: typing.Dict

    def __init__(self, **kwargs):
        self.validate_metadata()

    def validate_metadata(self):
        if self.__plugin_kind__ == "" or self.__plugin_name__ == "":
            message = "Plugin class {0} has not defined either __plugin_kind__ or __plugin_name__ metadata".format(self.__class__.__name__)
            raise presalytics.lib.exceptions.ValidationError(message)

    @abc.abstractmethod
    def get_tag(self, config: typing.Dict[str, typing.Any], **kwargs) -> str:
        """
        Generic method to be implemented by all inheriting classes. Allow plugin
        to be render without knowledge of the underlying plugin kind.

        Parameters:
        ----------

        config: Dict
            A set configuration values for the plugin.  Required keys should be
            specified by the docstring of the inheriting classes.
            Can be implemented via a mypy_extensions.TypedDict object if warranted.
            The presalytics.story.outline.Plugin's config element should be passed
            as this value to render the script.

        Returns:
        ----------

        A string carrying a html script that can be embedded in a html document

        """
        raise NotImplementedError


class ScriptPlugin(PluginBase):
    """
    A script plugin incorporates whitelisted or local `<script>` tags into a 
    rendered story
    """
    __plugin_kind__ = 'script'

    def get_tag(self, config, **kwargs):
        return self.to_script(config, **kwargs)

    @abc.abstractmethod
    def to_script(self, config: typing.Dict[str, typing.Any], **kwargs) -> str:
        """
        The to_script method maps a dictionary to an html script tag.

        Parameters:
        ----------

        config: Dict
            A set configuration values for the plugin.  Required keys should be
            specified by the docstring of the inheriting classes.
            Can be implemented via a `mypy_extensions.TypedDict` object if warranted.
            The `presalytics.story.outline.Plugin`'s config element should be passed
            as this value to render the script.

        Returns:
        ----------

        A string carrying a html `<script>` fragments that can be embedded in a html document

        """
        raise NotImplementedError


class StylePlugin(PluginBase):
    """
    A style plugin to incorporates `<link>` and `<style>` tags into a rendered story
    """
    __plugin_kind__ = 'style'

    def get_tag(self, config, **kwargs):
        return self.to_style(config, **kwargs)

    @abc.abstractmethod
    def to_style(self, config: typing.Dict[str, typing.Any], **kwargs) -> str:
        """
        The to_style method maps a dictionary to an html style tag.

        Parameters:
        ----------

        config: Dict
            A set configuration values for the plugin.  Required keys should be
            specified by the docstring of the inheriting classes.
            Can be implemented via a `mypy_extensions.TypedDict` object if warranted.
            The `presalytics.story.outline.Plugin`'s config element should be passed
            as this value to render the script.

        Returns:
        ----------

        A string carrying a `<link>` or `<style>` tags that can be embedded in a html document

        """
        raise NotImplementedError


class PluginRegistry(presalytics.lib.registry.RegistryBase):
    """
    The Plugin Registry class
    """
    def __init__(self, **kwargs):
        super(PluginRegistry, self).__init__(**kwargs)

    def get_name(self, klass):
        return getattr(klass, "__plugin_name__", None)

    def get_type(self, klass):
        return getattr(klass, "__plugin_kind__", None)


class Graph():
    """
    Utility for identifying circular dependencies in plugins

    Adapted from https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
    """
    def __init__(self, vertices):
        self.graph = collections.defaultdict(list)
        self.V = vertices

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def isCyclicUtil(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        for neighbour in self.graph[v]:
            if not visited[neighbour]:
                if self.isCyclicUtil(neighbour, visited, recStack):
                    return True
            elif recStack[neighbour] is True:
                return True

        # The node needs to be poped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    # Returns true if graph is cyclic else false
    def isCyclic(self):
        visited = [False] * self.V
        recStack = [False] * self.V
        for node in range(self.V):
            if not visited[node]:
                if self.isCyclicUtil(node, visited, recStack):
                    return True
        return False


class PluginManager(object):
    """
    Manager class for sorting, validating and rendering plugins
    """
    dependency_map: typing.Dict[str, typing.Dict[str, typing.Any]]
    dependency_order: typing.List[str]

    def __init__(self, plugins: typing.List[typing.Dict], ignore_errors=True):
        self.ignore_errors = ignore_errors
        self.dependency_map = {}
        self.dependency_order = []
        self.load_dependencies(plugins)
        self.dependency_graph = Graph(len(self.dependency_map))
        self.load_graph()
        self.check_for_cyclic_dependencies()
        self.sort_plugins()

    def sort_plugins(self):
        resort = False
        for key in self.dependency_order:
            current_index = self.dependency_order.index(key)
            lowest_dep = None
            deps = self.dependency_map[key]["dependencies"]
            for dep in deps:
                for dep_key, dep_map in self.dependency_map.items():
                    if dep == dep_map["plugin"]:
                        dep_index = self.dependency_order.index(dep_key)
                        if lowest_dep:
                            if dep_index < lowest_dep:
                                lowest_dep = dep_index
                        else:
                            lowest_dep = dep_index
                        break
            if lowest_dep:
                if lowest_dep > current_index:
                    self.dependency_order.insert(lowest_dep + 1, self.dependency_order.pop(current_index))
                    resort = True
                    break
        if resort:
            self.sort_plugins()

    def add_plugin_to_dep_map(self, plugin):
        current_plugins = [x["plugin"] for x in self.dependency_map.values()]
        if plugin not in current_plugins:
            lookup_key = plugin["kind"] + "." + plugin["name"]
            plugin_class = presalytics.PLUGINS.get(lookup_key)
            if plugin_class is None:
                message = "Required plugin {0} not found.".format(lookup_key)
                if self.ignore_errors:
                    logger.error(message)
                else:
                    raise presalytics.lib.exceptions.ValidationError(message)
            else:
                index = len(self.dependency_map.keys())
                dict_key = str(index) + "." + lookup_key
                self.dependency_order.append(dict_key)
                entry = {
                    dict_key: {
                        "plugin": plugin,
                        "class": plugin_class,
                        "dependencies": plugin_class.__dependencies__
                    }
                }
                self.dependency_map.update(entry)
                if len(plugin_class.__dependencies__) > 0:
                    self.load_dependencies(plugin_class.__dependencies__)

    def load_dependencies(self, plugins):
        for plugin in plugins:
            self.add_plugin_to_dep_map(plugin)

    def load_graph(self):
        for key, val in self.dependency_map.items():
            for dep in val["dependencies"]:
                key_node = list(self.dependency_map.keys()).index(key)
                plugin_list = [x["plugin"] for x in self.dependency_map.values()]
                dep_node = plugin_list.index(dep)
                self.dependency_graph.addEdge(key_node, dep_node)

    def check_for_cyclic_dependencies(self) -> None:
        if self.dependency_graph.isCyclic():
            message = "Loaded plugins container circular dependencies.  Plugins may not load in correct order"
            if self.ignore_errors:
                logger.error(message)
            else:
                raise presalytics.lib.exceptions.ValidationError(message)

    def get_styles(self) -> typing.List[str]:
        return self.render_plugins('style')

    def get_scripts(self) -> typing.List[str]:
        return self.render_plugins('script')

    def render_plugins(self, plugin_kind: str) -> typing.List[str]:
        rendered_list: typing.List[str]

        rendered_list = []
        for key in self.dependency_order:
            dep_map = self.dependency_map[key]
            if dep_map["plugin"]["kind"] == plugin_kind:
                plugin_config = dep_map["plugin"]
                plugin_class = dep_map["class"]
                try:
                    plugin_instance = plugin_class()
                    tag = plugin_instance.get_tag(config=plugin_config["config"])
                except Exception as ex:
                    logger.exception(ex)
                    t, v, tb = sys.exc_info()
                    if not presalytics.CONFIG.get("DEBUG", False):
                        div = presalytics.lib.exceptions.RenderExceptionHandler(ex, "plugin", traceback=tb).render_exception()
                        template = lxml.html.Element('template')
                        template.extend(list(lxml.html.fragment_fromstring(div)))
                        tag = lxml.html.tostring(template).decode('utf-8')
                    else:
                        six.reraise(t, v, tb)
                rendered_list.append(tag)
        return rendered_list

    @staticmethod
    def get_plugins_from_nested_dict(source_dict: typing.Dict, plugin_list: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
        if not plugin_list:
            plugin_list = []
    
        for key, val in source_dict.items():
            if key == "plugins":
                if isinstance(val, list):
                    for list_item in val:
                        if isinstance(list_item, dict):
                            if "config" in list_item and "name" in list_item and "kind" in list_item:
                                plugin_list.append(list_item)
                continue
            if isinstance(val, dict):
                plugin_list.extend(PluginManager.get_plugins_from_nested_dict(val, plugin_list))
            if isinstance(val, list):
                for list_item in val:
                    if isinstance(list_item, dict):
                        plugin_list.extend(PluginManager.get_plugins_from_nested_dict(list_item, plugin_list))
        return plugin_list
