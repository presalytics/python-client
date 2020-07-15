import abc
import typing
import os
import logging
import webbrowser
import re
import six
import sys
import urllib.parse
import presalytics.lib
import presalytics.lib.registry
import presalytics.lib.exceptions
import presalytics.lib.constants
import presalytics.client.api
if typing.TYPE_CHECKING:
    from presalytics.story.outline import Widget, Page, Plugin, OutlineBase, StoryOutline


logger = logging.getLogger("presalytics.story.components")


class ComponentBase(abc.ABC):
    """
    This class serves as the primary interface clas for the story components.  Instances of
    this interface carry enough information to rendered to html.  Developers, analysts and
    users should inherit from base class if they want components to be registered in the
    rendering pipeline for presalytics stories.

    Instance of this class must:
    1. Initialize with a name parameter
    2  Serialize to a subclass of presalytics.story.outline.OutlineBase
    3. Deserialize from an instance of presalytics.story.OutlineBase
    4. Render to html

    The __component_type__ and __component_name__ metadata on subclasses is required in
    order for instances to be registered in rendering pipeline for automatic updates

    Note: When inheriting from this base class, call "super().__init__(self, *args, **kwargs)" before add your
    own custom initialization.

    Attributes
    ----------

    name : str
        The name of the instance of the component.  Used in component as a key to lookup
        instances to re-calcute during rendering

    css : list of str
        A list of keys in dot notation that point to links in the ALLOWED_STYLES dictionary
        in the presalytics.lib.templates.base module.

    js: list of str
        A list of keys in dot notation that point to links in the ALLOWED_SCRIPTS dictionary
        in the presalytics.lib.templates.base module.

    __component_type__ : str
        The identifier for the component superclass (e.g. widget, page_template, renderer, theme).
        Used for component registration.

    __component_kind__ : str
        An identifier for this component class.  Used for component registration.

    __plugins__ : list of dict
        A list of dictionaries that reference `presalytics.story.outline.Plugin` configurations.  When a 
        `presaltytics.story.components.Renderer` is initialized, it will load these plugins into the
        rendered.  This allows plugins to be statically configured on `presalytics.story.components` classes,
        in lieu dynamic configurations on `presalytics.story.outline.StoryOutline` instances.

    client_info : str
        A `dict` to be unpacked and passed to `presalytics.client.api.Client` object when subclasses of
        `ComponentBase` require interaction with the Presalytics API.
    """
    __component_type__: str
    __component_kind__: str
    __plugins__: typing.List[typing.Optional[typing.Dict[str, typing.Any]]]
    name: str

    __plugins__ = []

    def __init__(self, client_info: typing.Dict = None, *args, **kwargs):
        if client_info:
            self.client_info = client_info
        else:
            self.client_info = {}
            if kwargs.get('delegate_login', None):
                self.client_info.update({'delegate_login': kwargs.get('delegate_login')})
            if kwargs.get('cache_tokens', None):
                self.client_info.update({'cache_tokens': kwargs.get('cache_tokens')})
            if kwargs.get('token', None):
                self.client_info.update({'token': kwargs.get('token')})

    @abc.abstractmethod
    def render(self, **kwargs):
        """
        Renders `component` to html.  Must be overridden in subclass.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def serialize(self):
        """
        Initializes `component` object from `presalytics.story.outline` attributes. Must be overridden in subclass.
        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls, component, **kwargs):
        """
        Converts `component` instance to a `presalytics.story.outline` object. Must be overridden in subclass.
        """
        raise NotImplementedError

    def get_client(self, **kwargs):
        """
        Initializes `presalytics.client.api.Client` using `client_info`
        """
        params = self.client_info
        params.update(kwargs)
        return presalytics.client.api.Client(**params)


class WidgetBase(ComponentBase):
    """
    Inherit from this base class to create widget components that can be rendered to html via the
    `presalytics.story.components.Renderer` class.  This component also needs to build a method
    that allows the widget to be serialzed into a `presalytics.story.outline.Widget` object.

    Parameters
    ----------
    widget: Widget
        A `presalytics.story.outline.Widget` object use for initialized the component class.

    Attributes
    ----------
    outline_widget: Widget
        A `presalytics.story.outline.Widget` object
    """
    outline_widget: typing.Optional['Widget']

    __component_type__ = 'widget'

    def __init__(self, name, *args, **kwargs) -> None:
        super(WidgetBase, self).__init__(*args, **kwargs)
        self.name = name
        self.outline_widget = None

    def render(self, component, **kwargs):
        self.to_html(component, **kwargs)

    @abc.abstractmethod
    def to_html(self, data: typing.Dict = None, **kwargs) -> str:
        """
        Returns valid html that renders the widget in a browser.

        Parameters
        ----------
        data: dict
            The data parameter is a dictionary should contain the minimum amount of that is required to
            successfully render the object.  As the widget is update, data control how the display of
            information changes.

        **kwargs:
            Optional keyword arguments can be used in subclass to modify the behavior of the `to_html` function.
            these keyword arguments should be invariant through successive updates to the chart.  For example,
            keyword arguments could control the styling of the widget, which should not change as the data in
            the object (e.g., a chart) is updated.  Keyword arguments are loaded via `additional_properties`
            parameter in in the `presalytics.story.outline.Widget` object.

        Returns
        ----------
        A str of containing an html fragment that will be loaded into a template in successive operations
        """
        raise NotImplementedError

    @abc.abstractmethod
    def serialize(self, **kwargs) -> 'Widget':
        """
        Creates `presalytics.story.outline.Widget` object from instance data. This widget should
        have the correct `name`, `data` and `additional_properties` so the same widget can be reconstituted
        via the to_html method, given the same set of data.

        Typically, this method will call an update method that run a local script with updates this
        Widget's data Dictionary prior being loading into the Widget outline object for serialization.

        Parameters
        ----------
        **kwargs:
            Optional keyword arguments can be used in subclass to modify the behavior of the to_html function.
            these keyword arguments should be be invariant through successive updates to the chart. Overrides
            for this widgets default additional_properties should be loaded via these keyword arguments.

        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls, component: 'Widget', **kwargs) -> 'WidgetBase':
        """
        Creates an instance of the widget from the data object in the `presalytics.story.outline.Widget`
        object. This method exists to ensure widgets can be portable across environments.  To clarify,
        widgets built on the client-side via the `__init__` method can be reconstructed server-side via
        the deserialize method.  This allows decoupling of the widget generation/updating of data and
        the rendering of the widget in a UI.  Renderers (e.g., `presalytics.story.revealer.Revealer` object)
        need not know about how the data get updated, but can update the graphic with data generated by
        the widget when the serialize method is called.

        Parameters
        ----------

        widget: Widget
            A `presalytics.story.outline.Widget` object

        Returns
        ----------
        `presalytics.story.components.WidgetBase` subclass instance
        """
        raise NotImplementedError


class PageTemplateBase(ComponentBase):
    """
    Inherit from this base class to render templates to html via the
    `presalytics.story.revealer.Revealer` class.

    Parameters
    ----------
    page: Page
        A presalytics.story.outline.Page object for instalizing the class

    Attributes
    ----------
    outline_page: presalytics.story.outline.Page
        The page data

    widgets: list of subclasses of presalytics.story.components.WidgetBase
        A list widget that will be loaded into templates and rendered via placeholders.
        These widgets must have a "to_html(self, data, **kwargs)" method.

    """

    outline_page: 'Page'
    widgets: typing.List['WidgetBase']
    plugins: typing.List[typing.Dict]

    __component_type__ = 'page'

    def __init__(self, page: 'Page', **kwargs) -> None:
        super(PageTemplateBase, self).__init__(**kwargs)
        self.outline_page = page
        self.widgets = self.get_page_widgets(self.outline_page)
        

    @abc.abstractmethod
    def render(self, **kwargs) -> str:
        """
        Returns valid html that renders the template in a broswer with data loaded from widgets.
        """
        raise NotImplementedError

    def load_widget(self, widget: 'Widget'):
        """
        Converts a presalytics.story.outline.Widget object to a subclass of WidgetComponentBase
        via the `presalytics.COMPONENTS` registry.
        """
        class_key = "widget." + widget.kind
        key = class_key + "." + widget.name
        try:
            if presalytics.COMPONENTS.get_instance(key):
                widget_instance = presalytics.COMPONENTS.get_instance(key)
            else:
                klass = presalytics.COMPONENTS.get(class_key)
                deserialize_method = getattr(klass, "deserialize", None)
                if callable(deserialize_method):
                    widget_instance = deserialize_method(widget, client_info=self.client_info)
                else:
                    message = "Widget component instance or class (kind) {0} unavailable in component registry".format(key)
                    raise presalytics.lib.exceptions.MissingConfigException(message)
        except Exception as ex:
            logger.exception(ex)
            if not presalytics.CONFIG.get("DEBUG", False):
                widget_instance = presalytics.lib.exceptions.RenderExceptionHandler(ex)
            else:
                t, v, tb = sys.exc_info()
                six.reraise(t, v, tb)
        return widget_instance

    def get_page_widgets(self, page: 'Page'):
        """
        Converts the widgets within a `presalytics.story.outline.Page` object to a list
        of widgets subclassed from `presalytics.story.components.WidgetBase`
        """
        widget_instances = []
        for widget_outline in page.widgets:
            next_widget = self.load_widget(widget_outline)
            widget_instances.append(next_widget)
        return widget_instances
    
    def serialize(self):
        return self.outline_page.dump()

    @classmethod
    def deseriailize(cls, component, **kwargs):
        return cls(page=component)


class ThemeBase(ComponentBase):
    """
    Themes are containers for plugins should be rendered once
    across the entire document.  The init method should configure
    parameters with get passed to plugins via serialization and 
    deserialization.
    """
    plugins: typing.Optional[typing.List['Plugin']]

    __component_type__ = 'theme'

    def __init__(self, **kwargs):
        pass

    def render(self, **kwargs):
        pass


class Renderer(ComponentBase):
    """
    Base class for objects that convert `presalytics.story.outline.StoryOutline` 
    objects into html and rendering them over the web

    With this class, users can push changes to their `presalytics.story.outline.StoryOutline`
    to the Presalytics API and web clients.  Renderer class contains a couplemethods for 
    syncing changes from component instances in the `presalytics.CONFIG` to the Presalytics API 
    Story service.

    * The `view` method allows users programattically view their stories at https://presalytics.io 
    after changes are made

    * The `manage` method takes users to to the story management interface, where users can share their 
    work with other users, continue making edits or change story properties.


    Parameters
    ----------
    story_outline : presalytics.story.outline.StoryOutline
        The presalytics StoryOutline to be rendered and presented
    
    Attributes
    -----------
    plugins : list of dict
        Plugin data that transform to html `<script>` and `<link>` tags through
        the rendering process
    
    site_host : str
        The host of the website.  Defaults to https://presalytics.io.

    view_url : str, optional
         The url to view the story.  Unavailable if story outline has not been pushed to
         the Presalytics API story service

    manage_url : str, optional
         The url to view the story.  Unavailable if story outline has not been pushed to
         the Presalytics API story service
    """
    story_outline: 'StoryOutline'
    plugins: typing.List[typing.Dict]
    view_url: typing.Optional[str]
    manage_url: typing.Optional[str]

    __component_type__ = 'renderer'
    
    def __init__(self, story_outline : 'StoryOutline', **kwargs):
        super(Renderer, self).__init__(**kwargs)
        self.story_outline = story_outline
        try:
            self.site_host = presalytics.CONFIG["HOSTS"]["SITE"]
        except (KeyError, AttributeError):
            self.site_host = presalytics.lib.constants.SITE_HOST
        try:
            story_id = self.story_outline.story_id
            view_endpoint = presalytics.lib.constants.STORY_VIEW_URL.format(story_id)
            self.view_url = urllib.parse.urljoin(self.site_host, view_endpoint)
            manage_endpoint = presalytics.lib.constants.STORY_MANAGE_URL.format(story_id)
            self.manage_url = urllib.parse.urljoin(self.site_host, manage_endpoint)
        except (KeyError, AttributeError):
            self.view_url = None
            self.manage_url = None

    def render(self, **kwargs):
        """
        Renders server-side (i.e., opens the story on https://presalytics.io)
        """
        return self.view()

            
    
    def strip_unauthorized_scripts(self, body):
        """
        Finds and removes unauthorized scripts from that the html document.  For security reasons,
        content in `<script>` tags that has not been vetted by presalytics.io devops 

        If you would like to get a tag included in the base library, raise an issue on 
        [Github](https://github.com/presalytics/python-client/issues/new).  We'd love to hear from you and learn 
        about your use case, and will respond promptly to help.
        """
        allowed_scripts = presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().values()
        script_elements = body.findall(".//script")
        for ele in script_elements:
            remove_ele = True
            script_id = ele.get("id")
            if script_id in self.story_outline.allowed_ids:
                remove_ele = False
            link = ele.get("src")
            if link in allowed_scripts:
                remove_ele = False
            if remove_ele:
                ele.getparent().remove(ele)
        return body
        
    @classmethod
    def deserialize(cls, component: 'StoryOutline', **kwargs):
        """
        Initializes the class from a `presalytics.story.outline.StoryOutline`.  See __init___.
        """
        return cls(component, **kwargs)

    def serialize(self) -> 'StoryOutline':
        """
        Updates the story_outline

        Returns
        -----------
        A refreshed `presalytics.story.outline.StoryOutline`
        """
        self.update_outline_from_instances()
        return self.story_outline

    def update_outline_from_instances(self, sub_dict: typing.Dict = None):
        """
        If a component instance for the widget is available in `presalytics.COMPONENTS`, 
        this method find the instance and regenerates the component data 
        so the latest data is available during the renering process.
        """
        if not sub_dict:
            sub_dict = self.story_outline.to_dict()
        if sub_dict:
            for key, val in sub_dict.items():
                if key in ["widgets", "themes", "pages"]:
                    if isinstance(val, list):
                        for list_item in val:
                            if isinstance(list_item, dict):
                                if "kind" in list_item:
                                    class_key = key.rstrip("s") + "." + list_item["kind"]
                                    klass = presalytics.COMPONENTS.get(class_key)
                                    if klass:
                                        if "name" in list_item:
                                            instance_key = class_key + "." + list_item["name"]
                                            inst = presalytics.COMPONENTS.get_instance(instance_key)
                                            if inst:
                                                self._set_outline_data_from_instance(inst)
                if isinstance(val, dict):
                    if len(val.keys()) > 0:
                        self.update_outline_from_instances(val)
                if isinstance(val, list):
                    for list_item in val:
                        if isinstance(list_item, dict):
                            self.update_outline_from_instances(list_item)

    def get_component_implicit_plugins(self, sub_dict: typing.Dict = None):
        """
        Retrieves plugin data from plugins attached to `presalytics.story.components`
        classes referenced in the `presalytics.story.outline.StoryOutline`
        """
        if not sub_dict:
            sub_dict = self.story_outline.to_dict()
        if sub_dict:
            for key, val in sub_dict.items():
                if key in ["widgets", "themes", "pages"]:
                    if isinstance(val, list):
                        for list_item in val:
                            if isinstance(list_item, dict):
                                if "kind" in list_item:
                                    class_key = key.rstrip("s") + "." + list_item["kind"]
                                    klass = presalytics.COMPONENTS.get(class_key)
                                    if klass:
                                        if len(klass.__plugins__) > 0:
                                            self.plugins.extend(klass.__plugins__)                           
                if isinstance(val, dict):
                    if len(val.keys()) > 0:
                        self.get_component_implicit_plugins(val)
                if isinstance(val, list):
                    for list_item in val:
                        if isinstance(list_item, dict):
                            self.get_component_implicit_plugins(list_item)

    def _set_outline_data_from_instance(self, inst):
        
        if inst.__component_type__ == 'widget':
            self._set_widget_outline_data(inst)
        if inst.__component_type__ == 'page':
            self._set_page_outline_data(inst)
        if inst.__component_type__ == 'theme':
            self._set_theme_outline_data(inst)

    def _set_theme_outline_data(self, inst: 'ThemeBase'):
        theme_index = None
        for t in range(0, len(self.story_outline.themes)):
            if inst.name == self.story_outline.themes[t].name:
                theme_index = t
            if theme_index:
                break
        theme_outline = inst.serialize()
        if theme_index:
            self.story_outline.themes[theme_index] = theme_outline    

    def _set_page_outline_data(self, inst: 'PageTemplateBase'):
        page_index = None
        for p in range(0, len(self.story_outline.pages)):
            if inst.name == self.story_outline.pages[p].name:
                page_index = p
            if page_index:
                break
        page_outline = inst.serialize()
        if page_index:
            self.story_outline.pages[page_index] = page_outline

    def _set_widget_outline_data(self, inst: 'WidgetBase'):
        widget_index: typing.Optional[int]
        page_index: typing.Optional[int]
        widget_index = None
        page_index = None
        for p in range(0, len(self.story_outline.pages)):
            for w in range(0, len(self.story_outline.pages[p].widgets)):
                widget = self.story_outline.pages[p].widgets[w]
                if widget.name == inst.name:
                    page_index = p
                    widget_index = w
                if page_index:
                    break
            if page_index:
                break
        w_outline = inst.serialize()
        if isinstance(page_index, int) and isinstance(widget_index, int): #  Causes 'unsupported target for assingment error`
            self.story_outline.pages[page_index].widgets[widget_index] = w_outline #type: ignore

    def update_story(self):
        """
        Updates the StoryOutline and pushes those updates to the Presalytics API Story service
        """
        self.update_outline_from_instances()
        client = presalytics.client.api.Client(**self.client_info)
        story = client.story.story_id_get(self.story_outline.story_id)
        story.outline = self.story_outline.dump()
        client.story.story_id_put(story.id, story)
    
    def view(self, update=False):
        """
        Updates a story and opens it on the presalytics.io website

        Parameters
        ----------
        update : bool
            Defaults to True.  Indicates whether the StoryOutline should be updated
            prior to opening in the web browser
        """
        if not self.view_url:
            message = "The outline has not been pushed to the Presalytics API yet, and therefore cannot be viewed via preslaytics.io"
            raise presalytics.lib.exceptions.InvalidConfigurationError(message=message)
        if update:
            self.update_story()
        webbrowser.open_new_tab(self.view_url)


    def manage(self, update=False):
        """
        Updates a story and opens the management page on the presalytics.io website

        Parameters
        ----------
        update : bool
            Defaults to True.  Indicates whether the StoryOutline should be updated
            prior to opening in the web browser
        """
        if not self.manage_url:
            message = "The outline has not been pushed to the Presalytics API yet, and therefore cannot be viewed via preslaytics.io"
            raise presalytics.lib.exceptions.InvalidConfigurationError(message=message)
            
        if update:
            self.update_story()
        webbrowser.open_new_tab(self.manage_url)


class ComponentRegistry(presalytics.lib.registry.RegistryBase):
    """
    A registry of classes and class instances of objects that inherit from
    `presalytics.story.components.ComponentBase`.

    """
    def __init__(self, **kwargs):
        self.instances = {}
        self.instance_regex = re.compile(r'(.*)\.(.*)\.(.*)')
        super(ComponentRegistry, self).__init__(**kwargs)

    def get_type(self, klass):
        """
        Returns the `__component_type__` attribute on a class
        """
        return getattr(klass, "__component_type__", None)

    def get_name(self, klass):
        """
        Returns the `__component_kind__` attribute on a class
        """
        return getattr(klass, "__component_kind__", None)

    def get_instance_name(self, klass):
        """
        Returns the `name` attribute on an instance
        """
        return getattr(klass, "name", None)

    def get_instance_registry_key(self, klass):
        """
        Creates a registry key from a class instance by concatenating the 
        `__component_type__`, `__component_kind__`, and `name` attributes of an instance
        """
        key = None
        klass_type = self.get_type(klass)
        if klass_type:
            klass_name = self.get_name(klass)
            instance_name = self.get_instance_name(klass)
            if instance_name and klass_name:
                key = "{0}.{1}.{2}".format(klass_type, klass_name, instance_name)
            else:
                # For now. always show this error, good for user debugging, rather than developer debugging
                message = '{0} instance missing "__component_kind__" or "name" attribute'.format(klass_type)
                logger.error(message)
        return key


    def load_class(self, klass):
        """
        Loads a class or instance into the registry
        """
        super().load_class(klass)
        if isinstance(klass, ComponentBase):
            try:
                key = self.get_instance_registry_key(klass)
                if key:
                    if key not in self.instances.keys():
                        self.instances[key] = klass
                    
            except Exception:
                if self.show_errors:
                    klass_type = self.get_type(klass)
                    message = "Unable to register instance {0} with type {1}".format(klass.__name__, klass_type)
                    logger.error(message)

    def get_instance(self, key):
        self.load_deferred_modules()
        return self.instances.get(key, None)

    def unregister(self, klass):
        """
        Removes a class or instance from the registry
        """
        super().unregister(klass)
        key = self.get_instance_registry_key(klass)
        if key:
            self.instances.pop(key)

    def find_instance(self, string_with_key_or_name) -> typing.List[str]:
        is_key = self.instance_regex.match(string_with_key_or_name)
        if is_key:
            return [self.get_instance(string_with_key_or_name)]
        else:
            self.load_deferred_modules()
            return [x for x in self.instances.keys() if string_with_key_or_name in x]
