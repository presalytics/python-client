
import typing
import base64
import uuid
import logging
import jinja2
import json
import os
import lxml
import lxml.html
import markdown
import mdx_gfm
import presalytics
import presalytics.lib.exceptions


if typing.TYPE_CHECKING:
    pass


logger = logging.getLogger(__name__)


class MarkdownWidget(presalytics.story.components.WidgetBase):
    """
    A `Widget` for rendering markdown to html objects.

    This implementation uses [Github-flavored Markdown](https://github.github.com/gfm/).

    Parameters
    ----------

    name : str
        the name of widget.  Must be unique within `presalytics.COMPONENTS`

    markdown_text: str
        A string of markdown text to be converted to html via the `to_html` method

    css64 : str. optional
        A base64-encoded string of the css styles to apply to the d3 document.  Used for server-to-server
        transport over https.
    
    css_filename: str, optional
        A css file containing styles that will be applied to d3

        Note: Styles `html {width: 100%; height:100%;} body {width: 100%; height: 100%; margin: 0px;}`
        are applied by default if not css is provided


    Attributes
    -----------

    md: `markdown.Markdown`
        A markdown renderer. By default this rendered loads `py-gfm`'s
        `mdx_gfm.GithubFlavoredMarkdownExtension` to extend the renderer

    """
    __component_kind__ = 'markdown'
    __plugins__ = [
        {
            'name': 'external_links',
            'kind': 'style',
            'config': {
                'approved_styles_key': 'markdown-css'
            }
        }
    ]

    def __init__(self, 
                 name: str,
                 markdown_text: str,
                 css64: str = None,
                 css_filename: str = None, 
                 *args,
                 **kwargs):
        self.markdown_text = markdown_text
        self.md = markdown.Markdown(extensions=[mdx_gfm.GithubFlavoredMarkdownExtension()])
        super(MarkdownWidget, self).__init__(name, *args, **kwargs)
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
        html = self.md.convert(self.markdown_text)
        return html

    @classmethod
    def deserialize(cls, outline, **kwargs):
        markdown_text = outline.data.get("markdown_text")
        return cls(outline.name,
                   markdown_text=markdown_text,
                   **kwargs)

    def serialize(self, **kwargs):
        data = {
            'markdown_text': self.markdown_text,
        }
        return presalytics.story.outline.Widget(
            name=self.name,
            kind=self.__component_kind__,
            data=data,
        )
    
    @classmethod
    def from_file(cls, name, filepath: str, **kwargs):
        """
        Loads `markdown_text` via a file, rather than a string object.  
        `filepath` can be relative or absolute.
        """
        with open(filepath, 'r') as f:
            markdown_text = f.read()
        return cls(name, markdown_text, **kwargs)
