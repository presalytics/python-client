import os
import shutil
import lxml.html
import webbrowser
import logging
import collections
import typing
import tempfile
import lxml
import lxml.html
import lxml.etree
import lxml.html.builder as E
import datetime
import presalytics
import presalytics.lib
import presalytics.lib.plugins
import presalytics.lib.plugins.base
import presalytics.lib.templates
import presalytics.lib.templates.base
import presalytics.story.util
import presalytics.story.server
import presalytics.story.components
import presalytics.lib.exceptions
if typing.TYPE_CHECKING:
    from presalytics.story.outline import StoryOutline, Page, Plugin
    from presalytics.story.components import PageTemplateBase, ComponentBase, WidgetBase, ThemeBase


logger = logging.getLogger('presalytics.story.revealer')


class Revealer(presalytics.story.components.Renderer):
    """
    This class renders 'Story Outines' to reveal.js presentations
    """
    story_outline: 'StoryOutline'
    base: lxml.etree.Element
    links: typing.Sequence[lxml.etree.Element]
    plugins: typing.List[typing.Dict]

    __component_kind__ = 'revealer'

    def __init__(
            self,
            story_outline: 'StoryOutline',
            **kwargs):
        
        self.story_outline = story_outline
        logger.info("Initializing story render for {}".format(story_outline.title))
        self.story_outline.validate()
        self.base = self.make_base()
        logger.info("Loading plugins")
        reveal_plugin_config = {
            'kind': 'script',
            'name': 'reveal',
            'config': {}
        }
        self.update_outline_from_instances()
        self.plugins = [reveal_plugin_config]
        self.get_component_implicit_plugins()
        outline_plugins = presalytics.lib.plugins.base.PluginManager.get_plugins_from_nested_dict(story_outline.to_dict())
        self.plugins.extend(outline_plugins)
        self.plugin_mgr = presalytics.lib.plugins.base.PluginManager(self.plugins)
        logger.info("Revealer initilized.")

    @classmethod
    def deserialize(cls, component: 'StoryOutline', **kwargs):
        return cls(component, **kwargs)

    def serialize(self) -> 'StoryOutline':
        self.update_outline_from_instances()
        return self.story_outline

    def update_outline_from_instances(self, sub_dict: typing.Dict = None):
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
                                                self.set_outline_data_from_instance(inst)
                if isinstance(val, dict):
                    if len(val.keys()) > 0:
                        self.update_outline_from_instances(val)
                if isinstance(val, list):
                    for list_item in val:
                        if isinstance(list_item, dict):
                            self.update_outline_from_instances(list_item)

    def get_component_implicit_plugins(self, sub_dict: typing.Dict = None):
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

    def set_outline_data_from_instance(self, inst: 'ComponentBase'):
        if inst.__component_type__ == 'widget':
            self.set_widget_outline_data(inst)
        if inst.__component_type__ == 'page':
            self.set_page_outline_data(inst)
        if inst.__component_type__ == 'theme':
            self.set_theme_outline_data(inst)

    def set_theme_outline_data(self, inst: 'ThemeBase'):
        theme_index = None
        for t in range(0, len(self.story_outline.themes)):
            if inst.name == self.story_outline.themes[t].name:
                theme_index = t
            if theme_index:
                break
        theme_outline = inst.serialize()
        if theme_index:
            self.story_outline.themes[theme_index] = theme_outline    

    def set_page_outline_data(self, inst: 'PageTemplateBase'):
        page_index = None
        for p in range(0, len(self.story_outline.pages)):
            if inst.name == self.story_outline.pages[p].name:
                page_index = p
            if page_index:
                break
        page_outline = inst.serialize()
        if page_index:
            self.story_outline.pages[page_index] = page_outline


    def set_widget_outline_data(self, inst: 'WidgetBase'):
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
        if isinstance(page_index, int) and isinstance(widget_index, int):
            self.story_outline.pages[page_index].widgets[widget_index] = w_outline  

    def update_outline(self):
        raise NotImplementedError

    def make_base(self):
        base = lxml.etree.Element("div", attrib={"class": "reveal"})
        lxml.etree.SubElement(base, "div", attrib={"class": "slides"})
        return base

    def package_as_standalone(self):
        pres = self.render()
        body = E.BODY()
        body.append(pres)
        body = self.strip_unauthorized_scripts(body)
        for scripts in self.plugin_mgr.get_scripts():
            lxml_scripts = lxml.html.fragments_fromstring(scripts)
            for item in lxml_scripts:
                body.append(item)
        head = E.HEAD()
        for link in self.plugin_mgr.get_styles():
            lxml_links = lxml.html.fragments_fromstring(link)
            for item in lxml_links:
                head.append(item)
        head = self.strip_unauthorized_scripts(head)
        html = E.HTML(
            head,
            body
        )
        return lxml.html.tostring(html, pretty_print=True)

    # def render_plugin(self, plugin):
    #     plugin_type = plugin['type']
    #     plugin_config = plugin['config']
    #     plugin_class = self.plugin_loader.load(plugin_type)
    #     script_string = plugin_class().to_string(plugin_config)
    #     return lxml.html.fragment_fromstring(script_string)

    def strip_unauthorized_scripts(self, body):
        allowed_scripts = presalytics.lib.plugins.external.ALLOWED_SCRIPTS.flatten().values()
        script_elements = body.findall(".//script")
        for ele in script_elements:
            try:
                link = ele.get("src")
            except KeyError:
                ele.getparent().remove(ele)
            if link not in allowed_scripts:
                ele.getparent().remove(ele)
        return body

    def update_info(self):
        info = self.story_outline.info
        info.date_modified = datetime.datetime.now()

    def render(self):
        """
        This method returns a t
        """
        reveal_base = self.base
        for page in self.story_outline.pages:
            slide = lxml.etree.SubElement(reveal_base, "section")
            page_html = self.render_page(page)
            slide_fragment = lxml.html.fragment_fromstring(page_html)
            slide.append(slide_fragment)
        return reveal_base

    def render_page(self, page: 'Page') -> str:
        class_key = "page." + page.kind
        key = class_key + "." + page.name
        if presalytics.COMPONENTS.get_instance(key):
            page_instance = presalytics.COMPONENTS.get_instance(key)
        else:
            klass = presalytics.COMPONENTS.get(class_key)
            deserialize_method = getattr(klass, "deserialize", None)
            if callable(deserialize_method):
                page_instance = deserialize_method(page)
            else:
                message = 'Page component instance or class (kind) "{0}" unavailable in component registry'.format(key)
                raise presalytics.lib.exceptions.MissingConfigException(message)
        return page_instance.render()

    @staticmethod
    def make_local_folders(files_path=None):
        if files_path is None:
            files_path = os.getcwd()
        if not os.path.exists(files_path):
            os.mkdir(files_path)
        templates_path = os.path.join(files_path, "templates")
        if not os.path.exists(templates_path):
            os.mkdir(templates_path)
        static_files_path = os.path.join(files_path, "static")
        if not os.path.exists(static_files_path):
            os.mkdir(static_files_path)
        css_path = os.path.join(static_files_path, "css")
        if not os.path.exists(css_path):
            os.mkdir(css_path)
        js_path = os.path.join(static_files_path, "js")
        if not os.path.exists(js_path):
            os.mkdir(js_path)
        theme_path = os.path.join(css_path, "theme")
        if not os.path.exists(theme_path):
            os.mkdir(theme_path)

    def present(self, files_path=None, debug=True, port=8082, host='127.0.0.1'):
        logger.info("Building story rendering at http://{0}:{1}".format(host, port))
        if not files_path:
            files_path = tempfile.gettempdir()
        logger.info("Buidling standalone package for local rendering.")
        html = self.package_as_standalone().decode('utf-8')
        id = presalytics.story.util.to_title_case(self.story_outline.title)
        if id == '':
            id = 'blank'
        self.make_local_folders(files_path)
        template_folder = os.path.dirname(presalytics.lib.templates.base .__file__)
        shutil.copy(os.path.join(template_folder, "favicon.ico"), os.path.join(files_path, "static"))
        html_file = os.path.join(files_path, "templates", id + '.html')
        with open(html_file, 'w') as file:
            file.write(html)
        address = "http://{}:{}/story/{}".format(host, port, id)
        logger.info("Opening browser tab...")
        presalytics.story.server.Browser(address).start()
        presalytics.story.server.LocalServer(host=host, debug=debug, port=port, root_path=files_path).run()
