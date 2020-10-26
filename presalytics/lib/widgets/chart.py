
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

    chart_data: dict
        Data that will be loaded into the `c3.generate()` method.  Please go
        to [c3js.org](https://c3js.org/gettingstarted.html) for more information 
        on how to configure this object.

    css64 : str. optional
        A base64-encoded string of the css styles to apply to the d3 document.  Used for server-to-server
        transport over https.
    
    css_filename: str, optional
        A css file containing styles that will be applied to d3

        Note: Styles `html {width: 100%; height:100%;} body {width: 100%; height: 100%; margin: 0px;}`
        are applied by default if not css is provided
    """
    __component_kind__ = 'chart'

    def __init__(self, 
                 name: str,
                 chart_data: typing.Dict,
                 css64: str = None,
                 css_filename: str = None,
                 *args,
                 **kwargs):
        self.chart_data = chart_data
        super(ChartWidget, self).__init__(name, *args, **kwargs)
        self.add_bind_to()
        self.css64 = self.read_file(css_filename)
        self.css64 = self.css64 if self.css64 else css64
        self.css_filename = css_filename

    def read_file(self, filename) -> typing.Optional[str]:
        """
        Find a file named `filename` and return its base64-ecoded content
        """
        data64 = None
        if filename:
            search_paths = list(set(presalytics.autodiscover_paths))
            if os.getcwd() not in search_paths:
                search_paths.append(os.getcwd())
            for path in search_paths:
                fpath = os.path.join(path, filename)
                if os.path.exists(fpath):
                    with open(fpath, 'rb') as f:
                        data = f.read()
                        data64 = base64.b64encode(data).decode('utf-8')  #type: ignore
                    break
            if not data64:
                logger.debug("File {0} could not be found".format(filename))
        return data64

    def add_bind_to(self):
        if 'bindto' not in self.chart_data.keys():
            self.chart_data['bindto'] = '#chart'


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
            'sandbox': 'allow-scripts allow-same-origin'
        })
        empty_parent_div.append(frame)
        return lxml.html.tostring(empty_parent_div).decode('utf-8')

    @classmethod
    def deserialize(cls, outline, **kwargs):
        chart_data = outline.data.get("chart_data")
        return cls(outline.name,
                   chart_data=chart_data,
                   **kwargs)

    def serialize(self, **kwargs):
        data = {
            'chart_data': self.chart_data,
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

    .c3-axis-y text,
    .c3-axis-x text,
    .c3-axis-y2 text
    {
        font-size: 1rem;
    }

    .c3-legend-item {
        font-size: 20px;
    }

    #chart {
        margin: 20px;
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
                <script type="text/javascript" src="{{ events_url }}"></script>
                <div id="chart" class="chart-container"></div>
                <script type="text/javascript">

                    document.addEventListener("DOMContentLoaded", (event) => { 
                        var data = JSON.parse('{{data|safe}}');

                        var aspectRatio = data.aspectRatio || 0.5625; // 16:9 AR

                        var chart = c3.generate(data);
                        var timeout;

                        var c3Resize = () => {
                            clearTimeout(timeout);
                            timeout = setTimeout( () => {
                                timeout = null;
                                var width = document.querySelector('#chart').offsetWidth;
                                var newHeight = width * aspectRatio;
                                chart.resize({height: newHeight});
                                chart.internal.selectChart.style('max-height', 'none');
                            }, 500);
                            
                        }

                        const observer = new ResizeObserver(c3Resize);

                        observer.observe(document.querySelector('body'));

                        c3Resize();
                    });
                </script>
            </body>
        </html>""")
        data = json.dumps(self.chart_data)  # dont use hyphens in data keys
        extra_css = base64.b64decode(self.css64).decode('utf-8') if self.css64 else ChartWidget.DEFAULT_CSS  #type: ignore  
        context = {
            "c3_styles_url": presalytics.lib.plugins.external.ApprovedExternalLinks().attr_dict.flatten().get('c3'),
            "c3_script_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('c3'),
            "d3_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('d3'),
            "events_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('events'),
            "data": data,
            "css": extra_css
        }
        return SIMPLE_HTML.render(**context)