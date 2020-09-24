
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


class ChartWidget(presalytics.story.components.WidgetBase):
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
    __component_kind__ = 'chart'

    def __init__(self, 
                 name: str,
                 id: str,
                 chart_data: typing.Dict,
                 *args,
                 **kwargs):
        if not id:
            id = 'chart-' + str(uuid.uuid4())
        self.id = id
        self.chart_data = chart_data
        super(ChartWidget, self).__init__(name, *args, **kwargs)


    def to_html(self, data=None, **kwargs) -> str:
        """
        Renders the sandboxed iframe with will contain the d3 script widget
        """
        html = self.create_container()
        return html

    def create_container(self, **kwargs):
        """
        Wraps the D3 objects in an endpoint at the story API load via a sandboxed `<iframe>` that
        will be rendered
        """
        story_host = self.get_client(delegate_login=True).story.api_client.external_root_url
        source_url = "{0}/cache/{1}".format(story_host, self.nonce)
        empty_parent_div = lxml.html.Element("div", {
            'class': 'empty-parent bg-light',
            'style': 'height: 100%; width: 100%, display: block; text-align: left;'
        })
        frame = lxml.html.Element("iframe", {
            'src': source_url,
            'frameborder': "0",
            'scrolling': "auto",
            'class': 'd3-responsive-frame',
            'style': 'max-height: none; max-width: none; height:100%; width: 100%;',
            'sandbox': 'allow-scripts'
        })
        empty_parent_div.append(frame)
        return lxml.html.tostring(empty_parent_div).decode('utf-8')

    @classmethod
    def deserialize(cls, outline, **kwargs):
        chart_data = outline.data.get("chart_data")
        story_id = outline.data.get("story_id", None)
        id = outline.data.get('id', None)
        return cls(outline.name,
                   id=id,
                   chart_data=chart_data,
                   story_id=story_id,
                    **kwargs)

    def serialize(self, **kwargs):
        data = {
            'chart_data': self.chart_data,
            'id': self.id,
            'story_id': self.story_id,
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

    def create_subdocument(self, **kwargs):
        return self.standalone_html()


    def standalone_html(self) -> str:
        """
        Returns string with an html document containing that d3 widget

        Loaded via the Story API d3 endpoint
        """
        SIMPLE_HTML = jinja2.Template("""<!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                {{ css }}
                </style>
            </head>
            <body>
                <link href="{{c3_styles_url}}" rel="stylesheet"/>
                <script type="text/javascript" src="{{ d3_url }}"></script>
                <script type="text/javascript" src="{{ c3_script_url }}"></script>  
                <div id="{{ id }}" class="chart-container"></div>
                <script type="text/javascript">
                    document.addEventListener("DOMContentLoaded", function(event) { 
                        var id = '{{id}}';

                        var data = JSON.parse('{{data|safe}}');

                        var container = document.getElementById(id);

                        c3.generate(data);
                    
                    });
                </script>
            </body>
        </html>""")
        data = json.dumps(self.chart_data)  # dont use hyphens in data keys
        extra_css = base64.b64decode(self.css64).decode('utf-8') if self.css64 else ChartWidget.DEFAULT_CSS  #type: ignore  
        context = {
            "id": self.id,
            "c3_styles_url": presalytics.lib.plugins.external.ApprovedExternalLinks().attr_dict.flatten().get('c3'),
            "c3_script_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('c3'),
            "d3_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('d3'),
            "data": data,
            "css": extra_css
        }
        return SIMPLE_HTML.render(**context)