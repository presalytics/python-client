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


def htmlize(widget):
    """
    Jinja filter to render a widget to a html string
    """
    html = widget.to_html()
    try:
        html = html.decode('utf-8')
    except Exception:
        pass
    return html
    


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
        
        {{ widgets[widget_index.next()].to_html() }}  // renders widget and increments widget_index

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
        self.template_paths = [pkg_templates, os.getcwd()]
        if len(self.__template_paths__) > 0:
            self.template_paths[0:0] = self.__template_paths__
        self.is_template_local = self.check_for_file()
        if self.is_template_local:
            self.template_string = self.read_template_string()
        elif self.outline_page.additional_properties.get("template_string", None):
            self.template_string = self.outline_page.additional_properties.get("template_string")
        else:
            self.template_string = None
        if len(kwargs.keys()) > 0:
            self.outline_page.additional_properties.update(kwargs)

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
        if self.template_string:
            self.outline_page.additional_properties["template_string"] = self.template_string
        return self.outline_page

    def get_template_name(self):
        """
        Requires subclasses have either a `__template_file__` class property, or override this method
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
            return self.render_from_backup_string(**kwargs)
        else:
            raise presalytics.lib.exceptions.MissingConfigException("Missing __template_file__: {}".format(self.get_template_name()))

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
        env = jinja2.Environment(**options)
        env.filters['htmlize'] = htmlize
        template = env.from_string(self.template_string)
        return template.render(**context)

    def read_template_string(self) -> typing.Optional[str]:
        """
        Finds the template file and reads it into a string
        """
        for _dir in self.template_paths:
            fpath = os.path.join(_dir, self.get_template_name())
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
        env.filters['htmlize'] = htmlize
        return env.get_template(self.get_template_name())

    def check_for_file(self):
        """
        Checks whether `__template_file__` exists locally
        """
        for _dir in self.template_paths:
            fpath = os.path.join(_dir, self.get_template_name())
            if os.path.exists(fpath):
                return True
        return False


class TitleWithSingleItem(JinjaTemplateBuilder):
    """
    Simple single-widget page with a title
    """
    __component_kind__ = 'TitleWithSingleItem'
    __css__ = ['flex_row', 'light_grey', 'responsive_title']
    __template_file__ = 'title_with_single_widget.html'


class TwoUpWithTitle(JinjaTemplateBuilder): 
    """
    View two widgets side-by-side on one page
    """
    __component_kind__ = "TwoUpWithTitle"
    __css__ = ['flex_row', 'light_grey', 'responsive_title']
    __template_file__ = 'two_up_with_title.html'


class BootstrapCustomTemplate(JinjaTemplateBuilder):
    """
    Build customer repsonsive tempaltes using bootstrap to layout widgets
    
    The `presalytics.story.outline.Page` must contain an entry named "template_file" in the its data dictionary.
    The values of the "template_file" varialble must a file path to an html file in the
    current working directory

    Parameters:
    ----------
    name: str
        the page instance name

    page: presalytics.story.outline.Page
        A story outline page object to create the widget from
    
    template_file: str
        A local file path to an html file that wil be used as a template for rendering the page.
        The file path is relative to the current working directory.

    kwargs: dict, optional
        **kwargs can include parameters to pass to the template rendering context. For example, 
        when kwargs is passed `title="An Example Title"`, during rendering, the template's
         `{{title}}` place holder will be replaced with with `An Example Title` 
        
    """
    template_file: str

    __component_kind__ = "bootstrap-custom"

    __plugins__ = [
        {
            'name': 'external_scripts',
            'kind': 'script',
            'config': {
                'approved_scripts_key': 'jquery'
            }
        },
        {
            'name': 'external_scripts',
            'kind': 'script',
            'config': {
                'approved_scripts_key': 'popper'
            }
        },
        {
            'name': 'external_scripts',
            'kind': 'script',
            'config': {
                'approved_scripts_key': 'bootstrap4'
            }
        },
        {
            'name': 'external_links',
            'kind': 'style',
            'config': {
                'approved_styles_key': 'bootstrap4'
            }
        },
    ]


    def __init__(self, page: 'Page', name=None, template_file=None, **kwargs) -> None:
        try:        
            self.template_file = template_file
            if not self.template_file:
                self.template_file = page.additional_properties["template_file"]
        except (KeyError, AttributeError):
            raise presalytics.lib.exceptions.InvalidConfigurationError(message="BootstrapCustomTemplate requires a 'template_file' passed either via 'additional_properties` or a keyword argument")
        super(BootstrapCustomTemplate, self).__init__(page, **kwargs)
        self.outline_page.additional_properties["template_file"] = self.template_file
        self.name = name
        if not self.name:
            self.name = page.name
        self.outline_page.name = self.name
        self.outline_page.kind = self.__component_kind__

    def get_template_name(self):
        return self.template_file

    def serialize(self):
        if self.template_string:
            self.outline_page.additional_properties["template_string"] = self.template_string
        return self.outline_page




