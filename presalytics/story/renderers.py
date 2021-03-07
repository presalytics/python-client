import lxml.html
import logging
import typing
import lxml
import lxml.html
import lxml.etree
import datetime
import six
import sys
import presalytics
import presalytics.lib
import presalytics.lib.plugins
import presalytics.lib.plugins.base
import presalytics.lib.plugins.reveal
import presalytics.lib.plugins.external
import presalytics.lib.templates
import presalytics.lib.templates.base
import presalytics.story.util
import presalytics.story.server
import presalytics.story.components
import presalytics.lib.exceptions
if typing.TYPE_CHECKING:
    from presalytics.story.outline import StoryOutline, Page


logger = logging.getLogger('presalytics.story.revealer')


class ClientSideRenderer(presalytics.story.components.Renderer):
    """
    Renders `presalytics.story.outline.StoryOutline` objects to
    [reveal.js](https://github.com/hakimel/reveal.js/) presentations

    Parameters
    ----------
    story_outline : presalytics.story.outline.StoryOutline
        The presalytics StoryOutline to be rendered and presented

    pages : `list[int]`
        A list of page numbers to render (starting at 0).  By default,
        all pages are rendered

    Attributes
    -----------

    plugins : list of dict
        Plugin data that transform to html `<script>` and `<link>` tags through
        the rendering process

    plugin_mgr : presalytics.lib.plugins.base.PluginManager
        Sorts, validates, and renders plugins

    """

    __component_kind__ = 'client_side'

    def __init__(
            self,
            story_outline: 'StoryOutline',
            pages: typing.List[int] = None,
            **kwargs):
        super(ClientSideRenderer, self).__init__(story_outline, **kwargs)
        self.story_outline.validate()
        if isinstance(pages, int):
            pages = [pages]
        elif not pages:
            pages = [p for p in range(0, len(self.story_outline.pages))]
        elif not isinstance(pages, list) or not isinstance(pages[0], int):
            raise presalytics.lib.exceptions.InvalidArgumentException(message='"pages" must be a list of integers')
        if len([p for p in pages if p >= len(self.story_outline.pages)]) > 0:
            raise presalytics.lib.exceptions.InvalidArgumentException(message='"pages" can only contain integers lower than the number of pages in the story')
        self.pages_to_render = pages
        self.update_outline_from_instances()
        self.plugins = []
        self.get_component_implicit_plugins()
        outline_plugins = presalytics.lib.plugins.base.PluginManager.get_plugins_from_nested_dict(source_dict=self.story_outline.to_dict())
        self.plugins.extend(outline_plugins)
        self.plugin_mgr = presalytics.lib.plugins.base.PluginManager(self.plugins)

    def package(self, base64=True) -> typing.Dict:
        """
        Prepares a story for rendering via a client-side application

        Returns
        ----------

        A dictionary of lists of html fragments with 3 keys: `pages`, `styles` and `scripts`
        """
        pages = self.render()
        scripts = self.plugin_mgr.get_scripts()
        styles = self.plugin_mgr.get_styles()
        if base64:
            pages = presalytics.lib.util.list_to_base64(pages)
            scripts = presalytics.lib.util.list_to_base64(scripts)
            styles = presalytics.lib.util.list_to_base64(styles)
        return {
            "pages": pages,
            "scripts": scripts,
            "styles": styles
        }

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
        A `list` of `str` html fragments for each page
        """
        slides = []
        for p in range(0, len(self.story_outline.pages)):
            if p in self.pages_to_render:
                page = self.story_outline.pages[p]
                page_html = self.render_page(page)
                slide_fragment = lxml.html.fragment_fromstring(page_html)
                slides.append(slide_fragment)
        return slides

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
            if not presalytics.settings.DEBUG:  # type: ignore[attr-defined]
                page_html = presalytics.lib.exceptions.RenderExceptionHandler(ex, "page", traceback=tb).render_exception()
            else:
                six.reraise(t, v, tb)
        return page_html
