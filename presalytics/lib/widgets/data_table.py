
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
import presalytics.story.outline

if typing.TYPE_CHECKING:
    pass


logger = logging.getLogger(__name__)


class DataTableWidget(presalytics.story.components.WidgetBase):
    """
    A `Widget` for rendering data tables, implemented over the top of bootstrap-table.
    For security reasons, data tables are loaded via a sandboxed iframe that points
    to an endpoint in the Presalytics Story API.

    This class allows users to load [bootstrap-table](https://bootstrap-table.com) objects
    into widgets in order to create responsive data tables directly off a simple data object.

    Parameters
    ----------

    name : str
        the name of widget.  Must be unique within `presalytics.COMPONENTS`

    data: dict
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
    __component_kind__ = 'data-table'
 

    def __init__(self, 
                 name: str,
                 table_data: typing.Dict,
                 css64: str = None,
                 css_filename: str = None, 
                 *args,
                 **kwargs):
        self.table_data = table_data
        super(DataTableWidget, self).__init__(name, *args, **kwargs)
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
        table_data = outline.data.get("table_data")
        return cls(outline.name,
                   table_data=table_data,
                    **kwargs)

    def serialize(self, **kwargs):
        data = {
            'table_data': self.table_data,
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
        background-color: #f8f9fa !important;
    }

    .data-table-container {
        border: none !important;
        display: table;
        width: 100%;
    }

    .data-table-container tbody {
        background-color: #fff;
    }

    .data-table-container thead {
        background-color: #199ec7;
        color: white;
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
                <link href="{{bootstrap4_css_url}}" rel="stylesheet"/>
                <link href="{{font_awesome_url}}" rel="stylesheet"/>
                <link href="{{bootstrap_table_css_url}}" rel="stylesheet"/>
                <script type="text/javascript" src="{{ events_url }}"></script>
                <div id="table" class="data-table-container"></div>
                <script type="text/javascript" src="{{ jquery_url }}"></script>
                <script type="text/javascript" src="{{ popper_url }}"></script>  
                <script type="text/javascript" src="{{ bootstrap4_js_url }}"></script>  
                <script type="text/javascript" src="{{ boostrap_table_js_url }}"></script>  
                <script type="text/javascript">
                    $(document).ready(function() {
                        var data = JSON.parse('{{data|safe}}');
                        $("#table").bootstrapTable(data);
                    });
                </script>
            </body>
        </html>""")
        data = json.dumps(self.table_data, cls=presalytics.story.outline.OutlineEncoder)  # dont use hyphens in data keys
        extra_css = base64.b64decode(self.css64).decode('utf-8') if self.css64 else DataTableWidget.DEFAULT_CSS  #type: ignore  
        context = {
            "bootstrap4_css_url": presalytics.lib.plugins.external.ApprovedExternalLinks().attr_dict.flatten().get('bootstrap4'),
            "font_awesome_url": presalytics.lib.plugins.external.ApprovedExternalLinks().attr_dict.flatten().get('font-awesome'),
            "bootstrap_table_css_url": presalytics.lib.plugins.external.ApprovedExternalLinks().attr_dict.flatten().get('bootstrap-table'),
            "jquery_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('jquery'),
            "popper_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('popper'),
            "boostrap_table_js_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('bootstrap-table'),
            "d3_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('d3'),
            "events_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('events'),
            "data": data,
            "css": extra_css
        }
        return SIMPLE_HTML.render(**context)
