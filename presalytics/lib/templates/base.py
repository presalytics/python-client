from abc import abstractmethod
from typing import Sequence, Dict
from jinja2 import FileSystemLoader, Environment
from lxml.html import etree
from presalytics.story.extension_base import TemplateExtensionBase, WidgetComponentClass
from presalytics.story.components import WidgetComponent

class JinjaTemplateBuilder(TemplateExtensionBase):
    fail_silently: bool
    template_paths: Sequence[str]
    context: Dict
    widgets: Sequence[WidgetComponentClass]
    css_file: str
    js_file: str

    def __init__(
        self, 
        widgets=[],
        template_context={}, 
        template_paths=[], 
        fail_silently=True, 
        *args, **kwargs):

        self.fail_silently = fail_silently
        self.template_paths = template_paths
        self.context = template_context
        self.widgets = widgets
        self.context[widgets] = widgets
        self.template_paths.append('./html') # Look last in the default 'files' folder
        super().__init__(self, widgets=widgets, *args, **kwargs)

    @abstractmethod
    def get_template_name(self):
        raise NotImplementedError

    def make_template(self):
        env = self.load_jinja_template()
        template = env.get_template(self.get_template_name())
        template.render(self.context)

    def load_jinja_template(self):
        loader = FileSystemLoader(self.template_paths)
        env = Environment(loader=loader)
        return env

    def load_css_file(self):
        css_file = self.__annotations__['css_file']
        if css_file is not None:
            with open(css_file, 'r') as file:
                css = file.read()
            style = etree.Element("style")
            style.text = css
            return style.tostring()
    
    def get_styles(self):
        return self.load_css_file()


    def load_js_file(self):
        js_file = self.__annotations__['js_file']
        if js_file is not None:
            with open(js_file, 'r') as file:
                js = file.read()
            script = etree.Element("script")
            script.text = js
            return script.tostring()
    
    def get_scripts(self):
        return self.load_js_file()

        
        

class TitleWithSingleItem(JinjaTemplateBuilder):
    css_file = './css/single-item-grid.css'

    def get_template_name(self):
        return 'title_with_single_widget.html'



