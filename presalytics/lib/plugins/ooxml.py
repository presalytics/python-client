import sass
import os
import presalytics.lib.plugins.reveal_theme


class OoxmlTheme(presalytics.lib.plugins.reveal_theme.RevealCustomTheme):
    __plugin_name__ = 'ooxml-theme'

    def to_style(self, config, **kwargs):
        scss_file = os.path.join(os.path.dirname(__file__), 'scss', 'ooxml-theme.scss')
        with open(scss_file, 'r') as file:
            scss_template_string = file.read()
        scss_string = scss_template_string.format(**config)
        new_css = sass.compile(string=scss_string)
        style_string = "<style>\n{0}\n</style>".format(new_css)
        links = self.get_fonts(config["fonts"])
        return links + style_string
