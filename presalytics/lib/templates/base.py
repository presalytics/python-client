import os
import typing
import jinja2
import presalytics.story.outline
import presalytics.story.components
import presalytics.lib.util as util
if typing.TYPE_CHECKING:
    from presalytics.story.components import WidgetBase
    from presalytics.story.outline import Page


class WidgetPage(presalytics.story.components.PageTemplateBase):
    __component_kind__ = 'widget-page'

    def __init__(self, page: 'Page', **kwargs):
        super(WidgetPage, self).__init__(page, **kwargs)

    @classmethod
    def deserialize(cls, component, **kwargs):
        return cls(component, **kwargs)

    def serialize(self):
        return self.outline_page

    def render(self, **kwargs):
        return self.widgets[0].to_html()


class JinjaTemplateBuilder(presalytics.story.components.PageTemplateBase):
    """
    Base class for building objects that render html from `presalytics.story.outline.Page` 
    objects that implementing the [Jinja2](https://jinja.palletsprojects.com/) 
    python library.

    Instances of this class will look for templates located at file location identified by the
    `__template_file__` attribute.  If not template is found, the content in the `template_string`
    attribute will be used. Templates should call each widget's `to_html()` method in a placeholder
    in order to generate valid html for the page.      

    *About building templates*: Templates are passed a `widgets` attribute and a `widget_index` 
    integer (initialized at 0) as part of the context during rendering,. To render 
    multiple widgets on a page, the following pattern can be used inside of templates to 
    increment through the widgets as the jinja2 rendering engine moves through the template:
        
        {{ widgets[widget_index].to_html() }}  // renders widget
        {% set widget_index = widget_index + 1 %}  // increments widget_index

    Please also note that if `<script>` tags are included in the template, they will be 
    stripped out downstream by a `presalytics.story.components.Renderer` for security
    reasons.  Scripts included in templates will not make it to the browser.

    Parameters
    ----------
    page : presalytics.story.outline.Page
        The page to be rendered

    Attributes
    ----------
    __template_file__ : str
        The filename to an html file containing a fragment that will be rendered into 
        a page by a `presalytics.story.components.Renderer`
    
    __template_paths__ : list of str
        user-defined filepaths to directories where Jinja2 should look for the `__template_file__`

    __css__ : list of str
        Each str in this list is a key that maps to an entry in the
        `presalytics.lib.plugins.local.LocalStylesPlugin.LOCAL_STYLES_MAP`. Ids matched here 
        load the css files as a dependent plugin.

    template_paths : list of str
        The folders Jinja2 will look in. Includes that html directory adjacent to this `__file__`, 
        appending with the files in the `__template_paths__`

    widgets : list of subclass instances of presalytics.story.components.WidgetBase
        Widget to be rendered into the placeholders in the template identified by `__template_file__`
    
    """
    __css__: typing.Sequence[str]
    __template_file__: str
    __template_paths__: typing.List[str]
    template_paths: typing.List[str]

    __template_paths__ = []
    __css__ = []

    class WidgetIndexer(object):
        """
        A counter class for 

        call `widgetindex.next()` in html templates to move this the widget list
        """
        def __init__(self):
            self._val = 0
        
        def next(self):
            """
            Returns the current widget index and increments the value for the next call 
            """
            cur = self._val
            self._val += 1
            return cur

    def __init__(self, page: 'Page', **kwargs) -> None:
        super().__init__(page, **kwargs)
        pkg_templates = os.path.join(os.path.dirname(__file__), "html")
        self.template_paths = [pkg_templates]
        if len(self.__template_paths__) > 0:
            self.template_paths[0:0] = self.__template_paths__
        self.is_template_local = self.check_for_file()
        if self.is_template_local:
            self.template_string = self.read_template_string()
        elif self.outline_page.additional_properties.get("template_string", None):
            self.template_string = self.outline_page.additional_properties.get("template_string")
        else:
            self.template_string = None
        

    @classmethod
    def deserialize(cls, component, **kwargs):
        return cls(component, **kwargs)

    @util.classproperty
    def __plugins__(cls):
        plugin_list = []
        for id in cls.__css__:
            new_item = {
                'kind': 'style',
                'name': 'local',
                'config': {
                    'css_file_id': id
                }
            }
            plugin_list.append(new_item)
        return plugin_list

    def serialize(self):
        updated_plugins = []
        for plugin_data in self.__plugins__:
            updated_plugins.append(presalytics.story.outline.Plugin(**plugin_data))
        self.outline_page.plugins = updated_plugins
        return self.outline_page

    def get_template_name(self):
        """
        Requires subclasses have either a `__template_file__` property or override this method
        """
        if self.__template_file__:
            return self.__template_file__
        else:
            raise NotImplementedError
    
    def render(self, **kwargs):
        """
        Renders the widgets to html
        """
        if self.is_template_local:
            return self.render_from_file(**kwargs)
        elif self.template_string:
            self.render_from_backup_string(**kwargs)
        else:
            raise presalytics.lib.exceptions.MissingConfigException("Missing __template_file__: {}".format(self.__template_file__))

    def _make_context(self):
        context = {
            "widgets": self.widgets,
            "widget_index": self.WidgetIndexer()
        }
        if self.outline_page.additional_properties:
            context.update(self.outline_page.additional_properties)
            context.pop("template_string", None)
        return context

    
    def render_from_file(self, **kwargs) -> str:
        """
        Returns rendered html with widgets rendered into template placeholders
        """
        template = self.load_jinja_template()
        context = self._make_context()
        return template.render(**context)

    def render_from_backup_string(self, **kwargs):
        """
        Returns rendered html with widgets rendered into template placeholders
        """
        context = self._make_context()
        options = {
            "loader": jinja2.BaseLoader()
        }
        if context.get("jinja_options", None):
            options.update(context.pop("jinja_options"))
        template = jinja2.Environment(**options).from_string(self.template_string)
        return template.render(**context)

    def read_template_string(self) -> typing.Optional[str]:
        """
        Finds the template file and reads it into a string
        """
        for _dir in self.template_paths:
            fpath = os.path.join(_dir, self.__template_file__)
            if os.path.exists(fpath):
                with open(fpath, 'r') as f:
                    template_string = f.read()
                return template_string
        return None



    def load_jinja_template(self) -> jinja2.Template:
        """
        Uses the fileloader to load a local template file into the jinja2 environment
        """
        loader = jinja2.FileSystemLoader(self.template_paths)
        env = jinja2.Environment(loader=loader)
        return env.get_template(self.get_template_name())

    def check_for_file(self):
        """
        Checks whether `__template_file__` exists locally
        """
        for _dir in self.template_paths:
            fpath = os.path.join(_dir, self.__template_file__)
            if os.path.exists(fpath):
                return True
        return False


class TitleWithSingleItem(JinjaTemplateBuilder):
    """
    Simple single-widget page with a title
    """
    __component_kind__ = 'TitleWithSingleItem'
    __css__ = ['single_item_grid']
    __template_file__ = 'title_with_single_widget.html'


class TwoUpWithTitle(JinjaTemplateBuilder): 
    """
    View two widgets side-by-side on one page
    """
    __component_kind__ = "TwoUpWithTitle"
    __css__ = ['single_item_grid', 'flex_row']
    __template_file = 'two_up_with_title.html'
