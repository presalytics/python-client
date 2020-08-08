import sass
import os
import posixpath
import string
import typing
import presalytics.lib.plugins.reveal_theme
import presalytics.story.util


class OoxmlTheme(presalytics.lib.plugins.reveal_theme.RevealCustomTheme):
    """
    This class takes theme data from an Presalytics API Ooxml Automation service Theme object
    and feeds those values into the `presalytics.lib.plugins.reveal_theme.RevealCustomTheme`
    """
    __plugin_name__ = 'ooxml-theme'

    def to_style(self, config, **kwargs):
        base_path = os.path.join(os.path.dirname(__file__), 'scss')
        if os.name == "nt":
            import_path = posixpath.join(*base_path.split('\\'))
        else:
            import_path = base_path
        scss_file = os.path.join(base_path, 'overrides.tmpl')
        config.update({'path': import_path})
        with open(scss_file, 'r') as file:
            scss_template_string = file.read()
        config = self.config_to_camelCase(config)
        scss_string = scss_template_string.format(**config)
        new_css = sass.compile(string=scss_string)
        style_string = "<style>\n{0}\n</style>".format(new_css)
        font_names = [config["headingFont"], config["bodyFont"]]
        links = self.get_fonts(font_names)
        return links + style_string
    
    def config_to_camelCase(self, config: typing.Dict) -> typing.Dict:
        new_dict = dict()
        for key, val in config.items():
            new_dict.update({
                presalytics.story.util.to_camel_case(key): val
            })
        return new_dict

