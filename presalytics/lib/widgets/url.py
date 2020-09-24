
import typing
import base64
import uuid
import logging
import jinja2
import json
import os
import lxml
import lxml.html
import presalytics
import presalytics.lib.exceptions

if typing.TYPE_CHECKING:
    pass


logger = logging.getLogger(__name__)


class UrlWidget(presalytics.story.components.WidgetBase):
    """
    A `Widget` for rendering chart objects, implemented over the top of c3.js.
    For security reasons, charts are loaded via a sandboxed iframe that points
    to an endpoint in the Presalytics Story API.

    This class allows users to load [c3.js](https://c3js.org/) objects
    into widgets in order load charts directly off a simple data object.

    Parameters
    ----------

    name : str
        the name of widget.  Must be unique within `presalytics.COMPONENTS`

    data: dict
        Data that will be loaded into the `c3.generate()` method.  Please go
        to [c3js.org](https://c3js.org/gettingstarted.html) for more information 
        on how to configure this object.

    story_id : str, optional
        The story_id of the parent story

    """
    __component_kind__ = 'url'

    def __init__(self, 
                 name: str,
                 url: str,
                 *args,
                 **kwargs):
        self.url = url
        super(ChartWidget, self).__init__(name, *args, **kwargs)


    def to_html(self, data=None, **kwargs) -> str:
        """
        Renders url to a sandboxed iframe 
        """
        return self.create_container()

    def create_container(self, **kwargs):
        """
        Wraps the D3 objects in an endpoint at the story API load via a sandboxed `<iframe>` that
        will be rendered
        """

        empty_parent_div = lxml.html.Element("div", {
            'class': 'empty-parent bg-light',
            'style': 'height: 100%; width: 100%, display: block; text-align: left;'
        })
        frame = lxml.html.Element("iframe", {
            'src': self.url,
            'frameborder': "0",
            'scrolling': "auto",
            'class': 'd3-responsive-frame',
            'style': 'max-height: none; max-width: none; height:100%; width: 100%;',
            'sandbox': 'allow-scripts allow-forms allow-popups allow-popups-to-escape-sandbox allow-same-origin'
        })
        empty_parent_div.append(frame)
        return lxml.html.tostring(empty_parent_div).decode('utf-8')

    @classmethod
    def deserialize(cls, outline, **kwargs):
        return cls(outline.name,
                   outline.data.get('url'),
                    **kwargs)

    def serialize(self, **kwargs):
        data = {
            'url': self.url
        }
        return presalytics.story.outline.Widget(
            name=self.name,
            kind=self.__component_kind__,
            data=data,
        )

    DEFAULT_CSS = """
    html {
        height: 100%;
        width: 100%;
    }
    body {
        height: 100%;
        width: 100%;
        margin: 0px;
    }
    """
