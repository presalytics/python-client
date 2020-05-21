import typing
import presalytics
import presalytics.client.auth
import presalytics.story.components
import presalytics.story.outline
import presalytics.story.util
import presalytics.client.presalytics_ooxml_automation.models


class OoxmlTheme(presalytics.story.components.ThemeBase):
    """
    TODO: Review whether this class is obsolete
    """
    name: str
    ooxml_id: str
    plugin_config: typing.Dict
    always_refresh: bool

    __component_kind__ = 'ooxml-theme'

    def __init__(self, 
                 name, 
                 ooxml_theme_id, 
                 plugin_config=None, 
                 always_refresh=False,
                 client_info={},
                 **kwargs):
        super(OoxmlTheme, self).__init__(**kwargs)
        self.name = name
        self.ooxml_id = ooxml_theme_id
        self.always_refresh = always_refresh
        self.client_kwargs = client_info
        if not plugin_config or self.always_refresh:
            if not plugin_config:
                self.plugin_config = {}
            self.get_configuration()

    def get_configuration(self):
        client = presalytics.Client(**self.client_kwargs)
        theme = client.ooxml_automation.theme_themes_details_get_id(self.ooxml_id)
        extra_params = ['dateCreated', 'dateModified', 'userCreated', 'userModified', 'id', 'themeId']
        colors = {k: v for k, v in theme.colors.to_dict().items() if k not in extra_params}
        fonts = {k: v for k, v in theme.fonts.to_dict().items() if k not in extra_params}
        slide_details = client.ooxml_automation.slides_slides_details_get_id(theme.slide_id)
        color_map_dict = slide_details.slide_master.to_dict()["color_map"]
        color_types = client.ooxml_automation.shared_colortypes_get()

        mapped_colors = {
            "background1": self.map_color_type("background1", color_map_dict, colors, color_types),
            "background2": self.map_color_type("background2", color_map_dict, colors, color_types),
            "text1": self.map_color_type("text1", color_map_dict, colors, color_types),
            "text2": self.map_color_type("text2", color_map_dict, colors, color_types)
        }
        color_params = {k: v for k, v in colors.items() if k not in extra_params}
        color_params.update(mapped_colors)
        params = {k: v for k, v in color_params.items() if k not in extra_params}
        params.update(fonts)

        self.plugin_config = params
    

    def map_color_type(
            self,
            color_map_name: str,
            color_map: typing.Dict,
            theme_colors: typing.Dict,
            color_types_list=None) -> str:
        if not color_types_list:
            client = presalytics.Client(**self.client_kwargs)
            color_types_list = client.ooxml_automation.shared_colortypes_get()
        color_id = color_map[color_map_name]
        color_name = next(x.name for x in color_types_list if x.type_id == color_id)
        key = color_name[0].lower() + color_name[1:]
        color = theme_colors.get(key, None)
        return color

    def serialize(self):
        plugin = presalytics.story.outline.Plugin(
            kind='style',
            name='ooxml-theme',
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
