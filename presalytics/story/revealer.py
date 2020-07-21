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
import six
import sys
import urllib.parse
import presalytics
import presalytics.lib
import presalytics.lib.plugins
import presalytics.lib.plugins.base
import presalytics.lib.plugins.reveal
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
    Renders `presalytics.story.outline.StoryOutline` objects to 
    [reveal.js](https://github.com/hakimel/reveal.js/) presentations

    Parameters
    ----------
    story_outline : presalytics.story.outline.StoryOutline
        The presalytics StoryOutline to be rendered and presented
    
    Attributes
    -----------
    base : lxml.etree.Element
        An etree element containing the base html for each slide

    plugins : list of dict
        Plugin data that transform to html `<script>` and `<link>` tags through
        the rendering process

    plugin_mgr : presalytics.lib.plugins.base.PluginManager
        Sorts, validates, and renders plugins

    """
    base: lxml.etree.Element
    reveal_params: typing.Dict[str, typing.Any]

    __component_kind__ = 'revealer'

    def __init__(
            self,
            story_outline: 'StoryOutline',
            **kwargs):
        super(Revealer, self).__init__(story_outline, **kwargs)
        logger.info("Initializing story render for {}".format(story_outline.title))
        self.story_outline.validate()
        self.base = self._make_base()
        logger.info("Loading plugins")
        reveal_params = {}
        for key, val in kwargs.items():
            if key in presalytics.lib.plugins.reveal.RevealConfigPlugin.default_config.keys():
                reveal_params.update({key: val})
        if len(self.story_outline.pages) == 1:
            reveal_params.update({'controls': False})  # hide controls on single page story
        reveal_plugin_config = {
            'kind': 'script',
            'name': 'reveal',
            'config': {"reveal_params": reveal_params} if len(reveal_params.keys()) > 0 else {}
        }
        overrides_config = {
            'kind': 'style',
            'name': 'local',
            'config': {
                "css_file_id": "reveal_overrides"
            }
        }
        self.update_outline_from_instances()
        self.plugins = [reveal_plugin_config, overrides_config]
        self.get_component_implicit_plugins()
        outline_plugins = presalytics.lib.plugins.base.PluginManager.get_plugins_from_nested_dict(source_dict=self.story_outline.to_dict())
        self.plugins.extend(outline_plugins)
        self.plugin_mgr = presalytics.lib.plugins.base.PluginManager(self.plugins)
        logger.info("Revealer initilized.")

    def _make_base(self):
        base = lxml.etree.Element("div", attrib={
            "class": "reveal",
        })
        lxml.etree.SubElement(base, "div", attrib={"class": "slides"})
        try:
            client = self.get_client()
            website_token = client.token_util.token["access_token"]
            base.attrib['data-jwt'] = client.token_util.token["access_token"]
            base.attrib['data-jwt-refresh'] = client.token_util.token["refresh_token"]
            if presalytics.CONFIG.get("BROWSER_API_HOST", None):
                story_target = presalytics.CONFIG["BROWSER_API_HOST"] + "/story"
            else:
                story_target = client.story.api_client.configuration.host
            base.attrib['data-story-target'] = story_target
        except Exception as ex:
            logger.exception(ex, "Could not obtain access token from revealer component.")

        try:
            story_id = self.story_outline.story_id
            base.attrib['data-story-id'] = story_id
        except Exception:
            logger.info("Revealer could not extract story_id from outline.")
        return base
    
    def get_meta_tags(self, body=tuple()):
        """
        Security Note: If supplying a body, ensure that its already been stripped of unauthorized scripts. 
        """

        scripts = body.findall(".//script")

        srcs = []
        for script in scripts:
            src = script.get("src")
            if src:
                root = urllib.parse.urlparse(src).netloc
                if root:
                    srcs.append(root)
        allowed = ' '.join(set(srcs))

        tags = [
            '<meta charset="utf-8">',
            '<meta http-equiv="X-UA-Compatible" content="IE=edge">',
            '<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">',
        #    """<meta http-equiv="Content-Security-Policy" content="default-src 'self' https://*.presalytics.io; script-src 'self' https://*.presalytics.io {0};">""".format(allowed)
        ]
        return tags

    def package_as_standalone(self):
        """
        Render the story outline as a html document with only the 
        reveal.js presentation as conent

        Returns
        ----------
        A `str` containing a complete html document with the presentation
        """
        pres = self.render()
        body = E.BODY()
        body.append(pres)
        body = self.strip_unauthorized_scripts(body)
        for scripts in self.plugin_mgr.get_scripts():
            lxml_scripts = lxml.html.fragments_fromstring(scripts)
            for item in lxml_scripts:
                body.append(item)
        head = E.HEAD()
        for meta in self.get_meta_tags(body):
            lxml_meta = lxml.html.fragment_fromstring(meta)
            head.append(lxml_meta)
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

    def update_info(self):
        """
        Updates story metadata
        """
        info = self.story_outline.info
        info.date_modified = datetime.datetime.utcnow()

    def render(self):
        """
        Creates a reveal.js presenation html fragement

        Returns:
        ---------
        A `str` html fragment containing a reveal.js presentation
        """
        reveal_base = self.base
        for page in self.story_outline.pages:
            slides_container = reveal_base[0]
            slide = lxml.etree.SubElement(slides_container, "section")
            page_html = self.render_page(page)
            slide_fragment = lxml.html.fragment_fromstring(page_html)
            slide.append(slide_fragment)
        return reveal_base

    def render_page(self, page: 'Page') -> str:
        """
        Creates a reveal.js slide

        Returns
        ----------
        A `str` html framgment of the page
        """
        class_key = "page." + page.kind
        key = class_key + "." + page.name
        try:
            if presalytics.COMPONENTS.get_instance(key):
                page_instance = presalytics.COMPONENTS.get_instance(key)
            else:
                klass = presalytics.COMPONENTS.get(class_key)
                deserialize_method = getattr(klass, "deserialize", None)
                if callable(deserialize_method):
                    page_instance = deserialize_method(page, client_info=self.client_info)
                else:
                    message = 'Page component instance or class (kind) "{0}" unavailable in component registry'.format(key)
                    raise presalytics.lib.exceptions.MissingConfigException(message)
            page_html = page_instance.render()
        except Exception as ex:
            logger.exception(ex)
            t, v, tb = sys.exc_info()
            if not presalytics.CONFIG.get("DEBUG", False):
                page_html = presalytics.lib.exceptions.RenderExceptionHandler(ex, "page", traceback=tb).render_exception()
            else:
                six.reraise(t, v, tb)
        return page_html

    def present(self, files_path=None, debug=True, port=8082, host='127.0.0.1'):
        """
        Creates and opens the rendered story in the browser.  Story files are served by 
        a local flask server.  Not for production use.  Press Ctrl + C to close the server.

        Parameters
        ----------
        files_path : str
            filepath to a local folder that will work as root folder for a local flask
            server.  Defaults to the user's temporary files directory

        debug : str
            Defaults to True.  Indicates whether the flask server should be started
            in debug mode.
        
        port : str
            The network port to serve the story onto.  Defautls to 8082.
        
        host : str
            The host to for the local server.  Typically either localhost or the default gateway.
            Defaults to 127.0.0.1 (localhost).
        
        """
        logger.info("Building story rendering at http://{0}:{1}".format(host, port))
        if not files_path:
            files_path = tempfile.gettempdir()
        logger.info("Buidling standalone package for local rendering.")
        html = self.package_as_standalone().decode('utf-8')
        id = presalytics.story.util.to_title_case(self.story_outline.title)
        if id == '':
            id = 'blank'
        server = presalytics.story.server.LocalServer(host=host, debug=debug, port=port, root_path=files_path)
        pkg_templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib", "templates")
        shutil.copy(os.path.join(pkg_templates_dir, "favicon.ico"), os.path.join(files_path, "presalytics", "static"))
        html_file = os.path.join(files_path, "presalytics", "templates", id + '.html')
        with open(html_file, 'w') as file:
            file.write(html)
        address = "http://{}:{}/story/{}".format(host, port, id)
        logger.info("Opening browser tab...")
        presalytics.story.server.Browser(address).start()
        server.run()
