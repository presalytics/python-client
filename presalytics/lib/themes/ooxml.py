import typing
import presalytics
import presalytics.story.components
import presalytics.story.outline


class OoxmlTheme(presalytics.story.components.ThemeBase):
    name: str
    ooxml_id: str
    plugin_config: typing.Dict
    always_refresh: bool

    __component_kind__ = 'ooxml-theme'

    def __init__(self, name, ooxml_theme_id, plugin_config=None, always_refresh=False, **kwargs):
        super(OoxmlTheme, self).__init__(**kwargs)
        self.name = name
        self.ooxml_id = ooxml_theme_id
        self.always_refresh = always_refresh
        if not plugin_config or self.always_refresh:
            if not plugin_config:
                self.plugin_config = {}
            self.get_configuration()

    def get_configuration(self):
        client = presalytics.Client()
        theme = client.ooxml_automation.theme_themes_details_get_id(self.ooxml_id)
        colors = theme.colors
        fonts = theme.fonts
        slide_details = client.ooxml_automation.slides_slides_details_get_id(theme.slide_id)
        colormaps = slide_details.slide_master["color_maps"]
        mapped_colors = {
            "background1": "$" + colormaps["background1"],
            "background2": "$" + colormaps["background2"],
            "text1": "$" + colormaps["text1"],
            "text2": "$" + colormaps["text2"]
        }
        params = colors
        params.update(fonts)
        params.update(mapped_colors)
        self.plugin_config = params

    def serialize(self):
        plugin = presalytics.story.outline.Plugin(
            kind='ooxml-theme',
            name=self.name,
            config=self.plugin_config
        )
        data = {
            "ooxml_theme_id": self.ooxml_id,
            "always_refresh": self.always_refresh,
        }
        theme = presalytics.story.outline.Theme(
            kind=self.__component_kind__,
            name=self.name,
            data=data,
            plugins=[plugin]
        )
        return theme

    @classmethod
    def deseriailize(cls, component, **kwargs):
        plugin_config = component.plugins[0].config
        return cls(
            name=component.name,
            ooxml_theme_id=component.data["ooxml_theme_id"],
            plugin_config=plugin_config,
            always_refresh=component.data["always_refresh"],
            **kwargs
        )
