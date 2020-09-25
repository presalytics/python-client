
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
                 markdown_text: str = None,
                 *args,
                 **kwargs):
        self.markdown_text = markdown_text
        self.md = markdown.Markdown(extensions=[mdx_gfm.GithubFlavoredMarkdownExtension()])
        super(MarkdownWidget, self).__init__(name, *args, **kwargs)


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
