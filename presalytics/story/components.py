import abc
import typing
import os
import logging
import presalytics.lib
import presalytics.lib.registry
import presalytics.lib.exceptions
if typing.TYPE_CHECKING:
    from presalytics.story.outline import Widget, Page, Plugin, OutlineBase


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

    def __init__(self, name, *args, **kwargs):
        self.name = name

    @abc.abstractmethod
    def render(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def serialize(self):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, component: typing.Type['OutlineBase'], **kwargs):
        raise NotImplementedError


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
        super().__init__(self, name, *args, **kwargs)
        self.outline_widget = None

    def render(self, component, **kwargs):
        self.to_html(component, None, **kwargs)

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
    def deserialize(cls, widget: 'Widget', **kwargs) -> 'WidgetBase':
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

    def __init__(self, page: 'Page') -> None:
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
                widget_instance = deserialize_method(widget)
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
    __component_type__ = 'renderer'


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

    def load_class(self, klass):
        super().load_class(klass)
        if isinstance(klass, ComponentBase):
            klass_type = self.get_type(klass)
            try:
                if klass_type:
                    klass_name = self.get_name(klass)
                    instance_name = self.get_instance_name(klass)
                    if instance_name and klass_name:
                        key = "{0}.{1}.{2}".format(klass_type, klass_name, instance_name)
                        if key not in self.instances.keys():
                            self.instances[key] = klass
                    else:
                        # For now. always show this error, good for user debugging, rather than developer debugging
                        message = '{0} instance missing "__component_kind__" or "name" attribute'.format(klass_type)
                        logger.error()
            except Exception:
                if self.show_errors:
                    message = "Unable to register instance {0} with type {1}".format(klass.__name__, klass_type)
                    logger.error(message)

    def get_instance(self, key):
        return self.instances.get(key, None)
