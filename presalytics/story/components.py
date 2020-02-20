import abc
import typing
import os
import logging
import webbrowser
import posixpath
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

    Attributes:
    ----------

    name: str
        The name of the instance of the component.  Used in component as a key to lookup
        instances to re-calcute during rendering

    css: List[str]
        A list of keys in dot notation that point to links in the ALLOWED_STYLES dictionary
        in the presalytics.lib.templates.base module.

    js: List[str]
        A list of keys in dot notation that point to links in the ALLOWED_SCRIPTS dictionary
        in the presalytics.lib.templates.base module.

    __component_type__: str
        The idenifier for the component superclass (e.g. widget, page_template, renderer, theme).
        Used for component registration.

    __component_kind__:
        An identifier for this component class.  Used for component registration.
    """
    __component_type__: str
    __component_kind__: str
    __plugins__: typing.List[str]
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
        raise NotImplementedError

    @abc.abstractmethod
    def serialize(self):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, component, **kwargs):
        raise NotImplementedError

    def get_client(self):
        return presalytics.client.api.Client(**self.client_info)


class WidgetBase(ComponentBase):
    """
    Inherit from this base class to create widget components that can be rendered to html via the
    presalytics.story.revealer.Revealer class.  This component also need to build a method
    that allows the widget to be serialzed into a presalytics.story.outline.Widget object.

    Parameters:
    ----------
    widget: Widget
        A presalytics.story.outline.Widget object use for initialized the component class.

    Attributes:
    ----------
    outline_widget: Widget
        A presalytics.story.outline.Widget object

    css: List[str]
        A list of keys in dot notation that point to links in the ALLOWED_STYLES dictionary
        in the presalytics.lib.templates.base module.

    js: List[str]
        A list of keys in dot notation that point to links in the ALLOWED_SCRIPTS dictionary
        in the presalytics.lib.templates.base module.
    """
    outline_widget: typing.Optional['Widget']

    __component_type__ = 'widget'

    def __init__(self, name, *args, **kwargs) -> None:
        """
        Note: When inheriting from this base class, call "super().__init__(self, *args, **kwargs)" before add your
        own custom initialization.

        """
        super(WidgetBase, self).__init__(*args, **kwargs)
        self.name = name
        self.outline_widget = None

    def render(self, component, **kwargs):
        self.to_html(component, **kwargs)

    @abc.abstractmethod
    def to_html(self, data: typing.Dict = None, **kwargs) -> str:
        """
        Returns valid html that renders the widget in a broswer.

        Parameters:
        ----------
        data: Dict
            The data parameter is a dictionary should contain the minimum amount of that is required to
            successfully render the object.  As the widget is update, data control how the disply of
            information changes.
        **kwargs:
            Optional keyword arguments can be used in subclass to modify the behavior of the to_html function.
            these keyword arguments should be geinvariant through successive updates to the chart.  For example,
            keycloak argument should control the styling of the widget, which should not change as the data in
            the object (e.g., a chart) is updated.  Keyword arguments are loaded via additional_properties
            parameter in in the presalytics.story.outline.Widget object.

        Returns
        ----------
        A string of containing an html fragment that will be loaded into a template in successive operations
        """
        raise NotImplementedError

    @abc.abstractmethod
    def serialize(self, **kwargs) -> 'Widget':
        """
        Creates presalytics.story.outline.Widget object from instance data. This widget should
        have the correct name, data and additional_properties so the same widget can be reconstituted
        via the to_html method, given the same set of data.

        Typically, this method will call an update method that run a local script with updates this
        Widget's data Dictionary prior being loading into the Widget outline object for serialization.

        Parameters:
        ----------
        **kwargs:
            Optional keyword arguments can be used in subclass to modify the behavior of the to_html function.
            these keyword arguments should be be invariant through successive updates to the chart. Overrides
            for this widgets default additional_properties shoudl be loaded via these keyword argments.

        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls, component: 'Widget', **kwargs) -> 'WidgetBase':
        """
        Creates an instance of the widget from the data object in the presalytics.story.outline.Widget
        object. This method exists to ensure widgets can be portable across environments.  To clarify,
        widgets built on the client-side via the __init__ method can be reconstructed server-side via
        the deserialize method.  This allows decoupling of the widget generation/updating of data and
        the rendering of the widget in a UI.  Renderers (e.g., presalytics.story.revealer.Revealer object)
        need not know about how the data get updated, but can update the graphic with data generated by
        the widget when the serialize method is called.

        Parameters:
        ----------

        widget: Widget
            A prealytics.story.outline.Widget object

        Returns:
        ----------

        An instance the widget class
        """
        raise NotImplementedError


class PageTemplateBase(ComponentBase):
    """
    Inherit from this base class to render templates to html via the
    presalytics.story.revealer.Revealer class.

    Parameters:
    ----------
    page: Page
        A presalytics.story.outline.Page object for instalizing the class

    Attributes:
    ----------
    outline_page: Page
        A presalytics.story.outline.Page object

    widgets: List[WidgetComponentBase]
        A list widget that will be loaded into templates and rendered via placeholders.
        These widgets must have a "to_html(self, data, **kwargs)" method.

    css: List[str]
        A list of keys in dot notation that point to links in the ALLOWED_STYLES dictionary
        in the presalytics.lib.templates.base module.

    js: List[str]
        A list of keys in dot notation that point to links in the ALLOWED_SCRIPTS dictionary
        in the presalytics.lib.templates.base module.
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

        Parameters:
        ----------
        widgets: Sequence[WidgetComponentBase]
            List of widget instances a one to many different class that inhereit from the WidgetComponentBase
            abstract class. Defaults tot he widget list that the class as initilazed with.

        **kwargs:
            Optional keyword arguments can be used in subclass to modify the behavior of the to_html function.
            these keyword arguments should be geinvariant through successive updates to the chart.  For example,
            keycloak argument should control the styling of the widget, which should not change as the data in
            the object (e.g., a chart) is updated.  Keyword arguments are loaded via additional_properties
            parameter in in the presalytics.story.outline.Widget object.

        Returns
        ----------
        A string of containing an html fragment that will be loaded into a template in successive operations
        """
        raise NotImplementedError

    def load_widget(self, widget: 'Widget'):
        """
        Converts a presalytics.story.outline.Widget object to a subclass of WidgetComponentBase
        via a presalytics.story.loaders.WidgetLoaderBase object.
        """
        class_key = "widget." + widget.kind
        key = class_key + "." + widget.name
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
        return widget_instance

    def get_page_widgets(self, page: 'Page'):
        """
        Converts the widgets within a presaltytics.story.outline.Page object to a list
        of widgets subclassed from WidgetComponentBase
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
    story_outline: 'StoryOutline'
    plugins: typing.List[typing.Dict]

    __component_type__ = 'renderer'
    
    def __init__(self, story_outline : 'StoryOutline', **kwargs):
        super(Renderer, self).__init__(**kwargs)
        self.story_outline = story_outline
        try:
            self.site_host = presalytics.CONFIG["HOSTS"]["SITE"]
        except (KeyError, AttributeError):
            self.site_host = presalytics.lib.constants.SITE_HOST
        
            
    
    def strip_unauthorized_scripts(self, body):
        """
        Finds and remove unauthorized scripts from that the html document.  For security reasons,
        content in `<script>` tags that has not been vetted by presalytics.io devops 

        If you would like to get a tag included int eh base library, raise an issue on 
        [Github](https://github.com/presalytics/python-client/issues/new).  We'd love to hear from you and learn 
        about your use case, and will respond promptly to help.
        """
        allowed_scripts = presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().values()
        script_elements = body.findall(".//script")
        for ele in script_elements:
            try:
                link = ele.get("src")
            except KeyError:
                ele.getparent().remove(ele)
            if link not in allowed_scripts:
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
        so the latest data is avialable during the renering process.
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
        objects reference in the `presaltyics.story.outline.StoryOutline`
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
        story = client.story.story_id_get(self.story_outline.info.story_id)
        story.outline = self.story_outline.dump()
        client.story.story_id_put(story.id, story)
    
    def view(self, update=True):
        """
        Updates a story and opens it on the presalytics.io website

        Parameters
        ----------
        update : bool
            Defaults to True.  Indicates whether the StoryOutline should be updated
            prior to opening in the web browser
        """
        if update:
            self.update_story()
        endpoint = presalytics.lib.constants.STORY_VIEW_URL.format(self.story_outline.info.story_id)
        url = posixpath.join(self.site_host, endpoint)
        webbrowser.open_new_tab(url)


    def manage(self, update=True):
        """
        Updates a story and opens the management page on the presalytics.io website

        Parameters
        ----------
        update : bool
            Defaults to True.  Indicates whether the StoryOutline should be updated
            prior to opening in the web browser
        """
        if update:
            self.update_story()
        endpoint = presalytics.lib.constants.STORY_MANAGE_URL.format(self.story_outline.info.story_id)
        url = posixpath.join(self.site_host, endpoint)
        webbrowser.open_new_tab(url)



class ComponentRegistry(presalytics.lib.registry.RegistryBase):
    def __init__(self, **kwargs):
        self.instances = {}
        super(ComponentRegistry, self).__init__(**kwargs)

    def get_type(self, klass):
        return getattr(klass, "__component_type__", None)

    def get_name(self, klass):
        return getattr(klass, "__component_kind__", None)

    def get_instance_name(self, klass):
        return getattr(klass, "name", None)

    def get_instance_registry_key(self, klass):
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
        return self.instances.get(key, None)

    def unregister(self, klass):
        super().unregister(klass)
        key = self.get_instance_registry_key(klass)
        if key:
            self.instances.pop(key)
