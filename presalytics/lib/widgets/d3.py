
import typing
import base64
import uuid
import logging
import jinja2
import json
import os
import presalytics
import presalytics.lib.exceptions

if typing.TYPE_CHECKING:
    pass


logger = logging.getLogger(__name__)


class D3Widget(presalytics.story.components.WidgetBase):
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
                 script_filename: str = None, *args, **kwargs):
        if not id:
            id = 'd3-' + str(uuid.uuid4())
        self.id = id
        self.d3_data = d3_data
        self.story_id = story_id
        super(D3Widget, self).__init__(name, *args, **kwargs)
        self.script_filename = script_filename
        if script_filename:
            self.script64 = self.read_file(script_filename)
        else:
            if script64:
                self.script64 = script64
            else:
                raise presalytics.lib.exceptions.InvalidConfigurationError("D3 Widget must be supplied either a script64 or script_filename keyword argument.")
        
    def read_file(self, filename) -> str:

        search_paths = list(set(presalytics.autodiscover_paths))
        data64 = None
        if os.getcwd() not in search_paths:
            search_paths.append(os.getcwd())
        for path in search_paths:
            fpath = os.path.join(path, filename)
            if os.path.exists(fpath):
                with open(fpath, 'rb') as f:
                    data = f.read()
                    data64 = base64.b64encode(data)
                break
        if not data64:
            logger.info("File {0} could not be found".format(filename))
        return data64.decode('utf-8')  #type: ignore

    def to_html(self, data=None, **kwargs) -> str:
        if not self.story_id:
            message = "This object requires a valid story_id to render."
            raise presalytics.lib.exceptions.MissingConfigException(message=message)
        html = self.create_container()
        return html

    def create_container(self, **kwargs):
        """
        Wraps the D3 objects in an endpoint at the story API load via a sandboxed `<iframe>` that
        will be rendered inside of a story and rescaled to give repsonsive effect
        """
        params = {
            "site_host": self.get_client(delegate_login=True).story.api_client.configuration.host,
            "figure_id": self.id,
            "story_id": self.story_id
        }
        source_url = "{site_host}/story/{story_id}/d3/{id}".format(**params)
        empty_parent_div = lxml.html.Element("div", {
            'class': 'empty-parent bg-light',
            'style': 'height: 100%; width: 100%, display: block; text-align: left;'
        })
        frame = lxml.html.Element("iframe", {
            'src': source_url,
            'frameborder': "0",
            'scrolling': "auto",
            'class': 'd3-responsive-frame',
            'style': 'max-height: none; max-width: none; height:1005; width: 100%;',
            'sandbox': 'allow-forms allow-scripts'
        })
        empty_parent_div.append(frame)
        return lxml.html.tostring(empty_parent_div).decode('utf-8')

    @classmethod
    def deserialize(cls, outline, **kwargs):
        data = outline.data.get("data")
        story_id = outline.data.get("story_id", None)
        id = outline.data.get('id', None)
        data = outline.data.get('d3_data', None)
        filename = outline.data.get('filename', None)
        script64 = outline.data.get('script64', None)
        return cls(outline.name,
                   d3_data,
                   id=id,
                   story_id=story_id,
                   script64=script64,
                   script_filename=filename,
                   **kwargs)

    def serialize(self, **kwargs):
        data = {
            'd3_data': self.d3_data,
            'id': self.id,
            'story_id': self.story_id,
            'filename': self.script_filename,
            'script64': self.script64
        }
        return presalytics.story.outline.Widget(
            name=self.name,
            kind=self.__component_kind__,
            data=data,
        )


    def standalone_html(self) -> str:
        SIMPLE_HTML = jinja2.Template("""<!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                {{ extra_css }}
                </style>
            </head>
            <body>
                <script type="text/javascript" src="{{ d3_url }}"></script>
                <div id="{{ id }}"></div>
                <script type="text/javascript">

                    var id = {{id}}

                    var data = {{data}}

                    {{script}}
            
                </script>
            </body>
        </html>""")
        data = json.dumps(self.d3_data)
        script = base64.b64decode(self.script64).decode('utf-8')
        context = {
            "id": self.id,
            "d3_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('d3'),
            "data": data,
            "script": script
        }
        return SIMPLE_HTML.render(**context)

