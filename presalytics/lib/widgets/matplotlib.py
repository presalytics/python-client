import mpld3
import typing
import presalytics.story.components
import presalytics.story.outline
import presalytics.lib.exceptions
if typing.TYPE_CHECKING:
    from matplotlib.pyplot import Figure


class MatplotlibFigure(presalytics.story.components.WidgetBase):
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
