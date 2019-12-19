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
        super(WidgetPage, self).__init__(page)

    @classmethod
    def deserialize(cls, component, **kwargs):
        return cls(component, **kwargs)

    def serialize(self):
        return self.outline_page

    def render(self, **kwargs):
        return self.widgets[0].to_html()


class JinjaTemplateBuilder(presalytics.story.components.PageTemplateBase):
    __css__: typing.Sequence[str]
    __template_file__: str
    __template_paths__: typing.List[str]
    template_paths: typing.List[str]

    __template_paths__ = []

    def __init__(self, page: 'Page', **kwargs) -> None:
        super().__init__(page, **kwargs)
        pkg_templates = os.path.join(os.path.dirname(__file__), "html")
        self.template_paths = [pkg_templates]
        if len(self.__template_paths__) > 0:
            self.template_paths[0:0] = self.__template_paths__

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
        Requires subclasses have either a "__template___" property or override this method
        """
        if self.__template_file__:
            return self.__template_file__
        else:
            raise NotImplementedError

    def render(self, **kwargs) -> str:
        template = self.load_jinja_template()
        context = {
            "widgets": self.widgets,
            "widget_index": 0
        }
        if self.outline_page.additional_properties:
            context.update(self.outline_page.additional_properties)
        return template.render(**context)

    def load_jinja_template(self) -> jinja2.Template:
        loader = jinja2.FileSystemLoader(self.template_paths)
        env = jinja2.Environment(loader=loader)
        return env.get_template(self.get_template_name())


class TitleWithSingleItem(JinjaTemplateBuilder):
    __component_kind__ = 'TitleWithSingleItem'
    __css__ = ['single_item_grid']
    __template_file__ = 'title_with_single_widget.html'
