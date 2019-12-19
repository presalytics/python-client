import sass
import os
import presalytics.lib.plugins.reveal_theme


class OoxmlTheme(presalytics.lib.plugins.reveal_theme.RevealCustomTheme):
    __plugin_name__ = 'ooxml-theme'

    def to_style(self, config, **kwargs):
        base_path = os.path.join(os.path.dirname(__file__), 'scss')
        scss_file = os.path.join(base_path, 'overrides.tmpl')
        config.update({'path': base_path})
        with open(scss_file, 'r') as file:
            scss_template_string = file.read()
        scss_string = scss_template_string.format(**config)
        new_css = sass.compile(string=scss_string)
        style_string = "<style>\n{0}\n</style>".format(new_css)
        font_names = [config["headingFont"], config["bodyFont"]]
        links = self.get_fonts(font_names)
        return links + style_string
