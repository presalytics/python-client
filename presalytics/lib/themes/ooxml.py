import typing
import presalytics
import presalytics.client.auth
import presalytics.story.components
import presalytics.story.outline
import presalytics.client.presalytics_ooxml_automation.models


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
        if presalytics.CONFIG.get("DELEGATE_LOGIN", False):
            token = presalytics.client.auth.TokenUtil().token
            client = presalytics.Client(
                delegate_login=True,
                token=token
            )
        else:
            client = presalytics.Client()
        theme = client.ooxml_automation.theme_themes_details_get_id(self.ooxml_id)
        colors = theme.colors
        fonts = theme.fonts
        slide_details = client.ooxml_automation.slides_slides_details_get_id(theme.slide_id)
        color_map_dict = slide_details.slide_master["colorMap"]
        color_types = client.ooxml_automation.shared_colortypes_get()

        mapped_colors = {
            "background1": OoxmlTheme.map_color_type("background1", color_map_dict, color_types),
            "background2": OoxmlTheme.map_color_type("background2", color_map_dict, color_types),
            "text1": OoxmlTheme.map_color_type("text1", color_map_dict, color_types),
            "text2": OoxmlTheme.map_color_type("text2", color_map_dict, color_types)
        }
        params = colors
        params.update(fonts)
        params.update(mapped_colors)
        self.plugin_config = params
    
    @staticmethod
    def map_color_type(
            color_map_name: str,
            color_map: typing.Dict,
            color_types_list=None) -> str:
        if not color_types_list:
            if presalytics.CONFIG.get("DELEGATE_LOGIN", False):
                token = presalytics.client.auth.TokenUtil().token
                client = presalytics.Client(
                    delegate_login=True,
                    token=token
                )
            else:
                client = presalytics.Client()
            color_types_list = client.ooxml_automation.shared_colortypes_get()
        color_id = color_map[color_map_name]
        color_name = [x.name for x in color_types_list if x.type_id == color_id][0]
        color = color_map.get(color_name, None)
        return color

            


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
