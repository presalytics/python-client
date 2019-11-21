import mpld3
import typing
import presalytics.story.components
import presalytics.story.outline
import presalytics.lib.exceptions
from matplotlib import pyplot as plot


class MatplotlibPyplot(presalytics.story.components.WidgetBase):
    __component_kind__ = 'matplotlib_pyplot'
    additional_properties: typing.Dict

    def __init__(self, plt: plot, name: str, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.plt = plt
        self.name = name
        if self.plt:
            self.plot_dict = mpld3.fig_to_dict(self.plt.figure())
        else:
            plot_dict = kwargs.pop("plot_dict", None)
            if plot_dict:
                self.plot_dict = plot_dict
        if self.plot_dict is None:
            message = "MatplotlibPyplot requires a plot_dict attribute.  Please supply either a valid plot_dict or matplotlib.pyplot object to __init__"
            raise presalytics.lib.exceptions.ValidationError(message)
        self.plot_id = self.plot_dict["id"]
        self.additional_properties = {}
        for key, val in kwargs.items():
            self.additional_properties[key] = val
        self.outline_widget = self.serialize()

    def to_html(self):
        return '<div id={0} class="mpld3"></div>'.format(self.plot_id)

    @classmethod
    def deserialize(cls, outline, **kwargs):
        plot_dict = outline.data.get("plot_dict")
        return cls(None, outline.name, plot_dict=plot_dict, **outline.additional_properties)

    def serialize(self, **kwargs):
        data = {
            'plot_dict': self.plot_dict,
            'id': self.plot_id
        }
        plugin_obj = presalytics.story.outline.Plugin(
            name='mpld3',
            type='script',
            config=data
        )
        return presalytics.story.outline.Widget(
            name=self.name,
            kind=self.__component_kind__,
            plugins=[plugin_obj],
            data=data,
            additional_properties=self.additional_properties
        )
