import mpld3
import jinja2
import typing
import json
import presalytics.story.components
import presalytics.story.outline
import presalytics.lib.exceptions
import presalytics.lib.constants
import presalytics.lib.plugins.matplotlib
import presalytics.lib.plugins.external
if typing.TYPE_CHECKING:
    from matplotlib.pyplot import Figure


class MatplotlibFigure(presalytics.story.components.WidgetBase):
    """
    A `Widget` for rendering `matplotlib.pyplot.Figure` instances in stories

    This class acts as wrapper class for matplotlib figures, allowing their packaging into
    `presalytics.story.outline.Widget` objects and serialization to json.  At render-time, 
    the figure is converted to a d3.js object via the [mpld3](https://mpld3.github.io/)
    package.

    Parameters
    ----------

    figure : `matplotlib.pyplot.Figure`
        the figure to create the widget from

    name : str
        the name of widget.  Must be unique within `presalytics.COMPONENTS`

    Attributes
    ----------
    figure_dict : dict
        A `dict` containing json-serializable data for reconstituting the
        `matplotlib.pyplot.Figure` object.

    figure_id : str
        A unique identifier used to render the that figure into a d3.js object
    """
    __component_kind__ = 'matplotlib_figure'
    additional_properties: typing.Dict

    def __init__(self, figure: 'Figure', name: str, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fig = figure
        self.name = name
        self.figure_dict = None
        if self.fig:
            self.figure_dict = mpld3.fig_to_dict(figure)
        else:
            figure_dict = kwargs.pop("figure_dict", None)
            if figure_dict:
                self.figure_dict = figure_dict
        if self.figure_dict is None:
            message = "MatplotlibFigure requires a figure_dict attribute.  Please supply either a valid figure_dict or matplotlib.pyplot.Figure object to __init__"
            raise presalytics.lib.exceptions.ValidationError(message)
        self.figure_id = self.figure_dict["id"]
        self.additional_properties = {}
        for key, val in kwargs.items():
            self.additional_properties[key] = val
        self.outline_widget = self.serialize()

    def to_html(self):
        return '<div id="{0}" class="mpld3"></div>'.format(self.figure_id)

    @classmethod
    def deserialize(cls, outline, **kwargs):
        figure_dict = outline.data.get("figure_dict")
        return cls(None, outline.name, figure_dict=figure_dict, **outline.additional_properties)

    def serialize(self, **kwargs):
        data = {
            'figure_dict': self.figure_dict,
            'id': self.figure_id
        }
        plugin_obj = presalytics.story.outline.Plugin(
            name='mpld3',
            kind='script',
            config=data
        )
        return presalytics.story.outline.Widget(
            name=self.name,
            kind=self.__component_kind__,
            plugins=[plugin_obj.to_dict()],
            data=data,
            additional_properties=self.additional_properties
        )


class MatplotlibResponsiveFigure(MatplotlibFigure):
    """
    A `Widget` for rendering `matplotlib.pyplot.Figure` instances in stories

    This class acts as wrapper class for matplotlib figures, allowing their packaging into
    `presalytics.story.outline.Widget` objects and serialization to json.  At render-time, 
    the figure is converted to a d3.js object via the [mpld3](https://mpld3.github.io/)
    package.

    This class also depends on the static plugin

    Parameters
    ----------

    figure : `matplotlib.pyplot.Figure`
        the figure to create the widget from

    name : str
        the name of widget.  Must be unique within `presalytics.COMPONENTS`

    story_id : str, optional
        The story of thet

    Attributes
    ----------
    figure_dict : dict
        A `dict` containing json-serializable data for reconstituting the
        `matplotlib.pyplot.Figure` object.

    figure_id : str
        A unique identifier used to render the that figure into a d3.js object
    """

    additional_properties: typing.Dict
    __component_kind__ = 'matplotlib-responsive'

    __plugins__ = [
        {
            'name': 'external_scripts',
            'kind': 'script',
            'config': {
                'approved_scripts_key': 'mpl-responsive'
            }
        },
        {
            'name': 'external_links',
            'kind': 'style',
            'config': {
                'approved_styles_key': 'preloaders'
            }
        }
    ] #type: ignore

    def __init__(self, figure: 'Figure', name: str, story_id: str = "empty", *args, **kwargs):
        try:
            self.story_host = presalytics.CONFIG["HOSTS"]["STORY"]
        except (KeyError, AttributeError):
            self.story_host = presalytics.lib.constants.HOST
        self.story_id = story_id
        super(MatplotlibResponsiveFigure, self).__init__(figure, name, *args, **kwargs)

        
    def to_html(self):
        if not self.story_id:
            message = "This object requires a valid story_id to render."
            raise presalytics.lib.exceptions.MissingConfigException(message=message)
        html = self.create_container()
        return html


    def create_container(self, **kwargs):
        """
        Wraps the Matplotlib Figure in a SVG endpoint load via `<iframe>` that
        will be rendered inside of a story and rescaled to give repsonsive effect
        """
        client = self.get_client()
        self.token = client.token_util.token["access_token"]
        params = {
            "story_host": self.story_host,
            "figure_id": self.figure_id,
            "story_id": self.story_id
        }
        source_url = "{story_host}/story/{story_id}/matplotlib-responsive/{figure_id}/".format(**params)
        svg_container_div = lxml.html.Element("div", {
            'class': 'matplotlib-responsive-container',
            'data-jwt': self.token,
            'data-source-url': source_url
        })
        preloader_container_div = lxml.etree.SubElement(svg_container_div, "div", attrib={"class":"preloader-container"})
        preloader_row_div = lxml.etree.SubElement(preloader_container_div, "div", attrib={"class":"preloader-row"})
        preloader_file = os.path.join(os.path.dirname(__file__), "img", "preloader.svg")
        svg = lxml.html.parse(preloader_file)
        preloader_row_div.append(svg.getroot())
        empty_parent_div = lxml.html.Element("div", {
            'class': 'empty-parent bg-light'
        })
        empty_parent_div.append(svg_container_div)
        return lxml.html.tostring(empty_parent_div)


    @classmethod
    def deserialize(cls, outline, **kwargs):
        figure_dict = outline.data.get("figure_dict")
        story_id = outline.data.get("story_id", None)
        return cls(None, 
                   outline.name,
                   story_id,
                   figure_dict=figure_dict,
                   **outline.additional_properties)

    def serialize(self, **kwargs):
        data = {
            'figure_dict': self.figure_dict,
            'id': self.figure_id,
            'story_id': self.story_id
        }
        return presalytics.story.outline.Widget(
            name=self.name,
            kind=self.__component_kind__,
            data=data,
            additional_properties=self.additional_properties
        )

    def standalone_html(self) -> str:
        SIMPLE_HTML = jinja2.Template("""<!DOCTYPE html>
        <html>
            <head>
                <style>
                {{ extra_css }}
                </style>
            </head>
            <body>
                <script type="text/javascript" src="{{ d3_url }}"></script>
                <script type="text/javascript" src="{{ mpld3_url }}"></script>
                <div id={{ figid }}></div>
                <script type="text/javascript">

                !function(mpld3){
                    {{ extra_js }}
                    mpld3.draw_figure({{ figid }}, {{ figure_json }});
                }(mpld3);
                </script>
            </body>
        </html>""")
        figure_json = json.dumps(self.figure_dict, cls=presalytics.lib.plugins.matplotlib.Mpld3NumpyToJson)
        context = {
            "d3_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('d3v3'),
            "mpld3_url": presalytics.lib.plugins.external.ApprovedExternalScripts().attr_dict.flatten().get('mpld3'),
            "figid": self.figure_id,
            "figure_json": figure_json
        }
        return SIMPLE_HTML.render(**context)