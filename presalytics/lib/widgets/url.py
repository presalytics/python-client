
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
    A `Widget` for rendering urls in an iframe.  Allows users
    load 3rd party site and applications natively within a presalytics
    story.

    Parameters
    ----------

    name : str
        the name of widget.  Must be unique within `presalytics.COMPONENTS`

    url: str
        The url to be loaded in the `<iframe>`.  For secutriy reasons, it must be https.

    """
    __component_kind__ = 'url'

    def __init__(self, 
                 name: str,
                 url: str,
                 *args,
                 **kwargs):
        self.url = url
        super(UrlWidget, self).__init__(name, *args, **kwargs)


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
            'sandbox': 'allow-scripts allow-forms allow-popups allow-popups-to-escape-sandbox'
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
