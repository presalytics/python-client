
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


class D3Widget(presalytics.story.components.WidgetBase):
    """
    A `Widget` for rendering user-defined d3.js scripts

    This class allows users to load [d3.js](https://d3js.org/) objects
    into widgets in order to create custom and interactive widgets.
    User can define d3 scripts in a separate file and load them via `script_filename`
    parameter.

    Parameters
    ----------

    name : str
        the name of widget.  Must be unique within `presalytics.COMPONENTS`

    d3_data: dict
        Data that will be loaded into the script when run in the browser. Avaiable
        in the script as the `data` object.
    
    id: str, optional
        A unique identifier the widget.  Automatically generated when the
        widget is created or updated.

    story_id : str, optional
        The story_id of the parent story

    script64 : str. optional
        A base64-encoded string of the script's text.  Used for server-to-server
        transport over https

    script_filename: str, optional
        Required when updating the script text.  Read into the `script64` parameter
        via the `read_file` method

    html64 : str. optional
        A base64-encoded string of the html fragments's text.  Used for server-to-server
        transport over https

    html_filename: str, optional
        The name of file in the local directory with an html framement that should be rendered within the
        body (inside element `<div id="{{id}}" class="d3-container"></div>`) of the iframe containing the 
        d3 script

    css64 : str. optional
        A base64-encoded string of the css styles to apply to the d3 document.  Used for server-to-server
        transport over https.
    
    css_filename: str, optional
        A css file containing styles that will be applied to d3

        Note: Styles `html {width: 100%; height:100%;} body {width: 100%; height: 100%; margin: 0px;}`
        are applied by default if not css is provided


    


    Script Local Variables:
    ----------

    The following vairables are avialable to users when writing scripts:

    data: `javascript object`
        The data loaded into the script via `d3_data` parameter

    container: `html element`
        The first div in the body
    
    d3: `javascript object`
        The root d3 object for selecting, creating and editing elements on the DOM
        

    Security Note:
    ----------

    Scripts loaded via this widget are *Sandboxed*.  These script can only interact with
    dom elements defined in the widget script loaded via the `script_filename` parameter.
    Fetch and xhr actions are also disabled via a restrictive Content Security Policy.


    """
    __component_kind__ = 'd3'
    __plugins__ = [
        {
            'name': 'external_scripts',
            'kind': 'script',
            'config': {
                'approved_scripts_key': 'd3'
            }
        }
    ]

    def __init__(self, 
                 name: str, 
                 d3_data: typing.Dict,
                 id: str = None, 
                 story_id: str = None,
                 script64: str = None, 
                 script_filename: str = None, 
                 css64: str = None,
                 css_filename: str = None, 
                 html64: str = None,
                 html_filename: str = None,
                 *args, **kwargs):
        if not id:
            id = 'd3-' + str(uuid.uuid4())
        self.id = id
        self.d3_data = d3_data
        self.story_id = story_id
        super(D3Widget, self).__init__(name, *args, **kwargs)
        self.script_filename = script_filename
        self.script64 = self.read_file(script_filename)
        if not self.script64:
            self.script64 = script64
        if not self.script64:
            raise presalytics.lib.exceptions.InvalidConfigurationError("D3 Widget must be supplied either a script64 or script_filename keyword argument.")
        self.html64 = self.read_file(html_filename)
        self.html64 = self.html64 if self.html64 else html64
        self.css64 = self.read_file(css_filename)
        self.css64 = self.css64 if self.css64 else css64
        self.html_filename = html_filename
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
        if not self.story_id:
            message = "This object requires a valid story_id to render."
            raise presalytics.lib.exceptions.MissingConfigException(message=message)
        html = self.create_container()
        return html

    def create_container(self, **kwargs):
        """
        Wraps the D3 objects in an endpoint at the story API load via a sandboxed `<iframe>` that
        will be rendered
        """
        params = {
            "story_host": self.get_client(delegate_login=True).story.api_client.external_root_url,
            "id": self.id,
            "story_id": self.story_id,
        }
        source_url = "{story_host}/{story_id}/d3/{id}".format(**params)
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
            'sandbox': 'allow-forms allow-scripts'
        })
        empty_parent_div.append(frame)
        return lxml.html.tostring(empty_parent_div).decode('utf-8')

    @classmethod
    def deserialize(cls, outline, **kwargs):
        d3_data = outline.data.get("d3_data")
        story_id = outline.data.get("story_id", None)
        id = outline.data.get('id', None)
        data = outline.data.get('d3_data', None)
        script_filename = outline.data.get('script_filename', None)
        script64 = outline.data.get('script64', None)
        html_filename = outline.data.get('html_filename', None)
        html64 = outline.data.get('html64', None)
        css_filename = outline.data.get('css_filename', None)
        css64 = outline.data.get('css64', None)
        return cls(outline.name,
                   d3_data,
                   id=id,
                   story_id=story_id,
                   script64=script64,
                   script_filename=script_filename,
                   html64=html64,
                   html_filename=html_filename,
                   css64=css64,
                   css_filename=css_filename,
                   **kwargs)

    def serialize(self, **kwargs):
        data = {
            'd3_data': self.d3_data,
            'id': self.id,
            'story_id': self.story_id,
            'script_filename': self.script_filename,
            'script64': self.script64,
            'css64': self.css64,
            'html64': self.html64,
            'html_filename': self.html_filename,
            'css_filename': self.css_filename
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
                <script type="text/javascript" src="{{ d3_url }}"></script>
                <div id="{{ id }}" class="d3-container">{{ html_fragment }}</div>
                <script type="text/javascript">

                    var id = '{{id}}';

                    var data = JSON.parse('{{data|safe}}');

                    var container = document.getElementById(id);

                    {{script|safe}}
            
                </script>
            </body>
        </html>""")
        data = json.dumps(self.d3_data)  # dont use hyphens in data keys
        script = base64.b64decode(self.script64).decode('utf-8')  #type: ignore  #Required
        extra_css = base64.b64decode(self.css64).decode('utf-8') if self.css64 else D3Widget.DEFAULT_CSS  #type: ignore  
        html_fragment = base64.b64decode(self.html64).decode('utf-8') if self.html64 else None  #type: ignore   # disable nested iframes
        context = {
            "id": self.id,
            "d3_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('d3'),
            "data": data,
            "script": script,
            "css": extra_css,
            "html_fragment": html_fragment
        }
        return SIMPLE_HTML.render(**context)