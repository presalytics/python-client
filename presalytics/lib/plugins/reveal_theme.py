import os
import posixpath
import sass
import typing
import requests
import presalytics.lib.plugins.base


class RevealCustomTheme(presalytics.lib.plugins.base.StylePlugin):
    __plugin_name__ = 'reveal_custom_theme'
    defaults: typing.Dict[str, str]

    fonts_base_url = 'https://fonts.googleapis.com/css?family={0}'

    def to_style(self, config, **kwargs):
        scss_variables = self.defaults
        scss_variables.update(config)
        scss_string = self.get_base_scss(scss_variables)
        new_css = sass.compile(string=scss_string)
        style_string = "<style>\n{0}\n</style>".format(new_css)
        links = self.get_fonts(config["fonts"])
        return links + style_string

    def get_fonts(self, fonts: typing.List[str]):
        links = ""
        for font in fonts:
            link = self.get_font_link(font)
            if link:
                links = links + link + "\n"
        return links

    def get_font_link(self, font_name) -> typing.Optional[str]:
        test_url = self.fonts_base_url.format(font_name)
        r = requests.get(test_url)
        if r.status_code == 200:
            return '<link href="{0}" rel="stylesheet">'.format(test_url)
        else:
            return None

    def get_base_scss(self, scss_variables):
        scss_folder = os.path.join(os.path.dirname(__file__), "scss")
        mixins_file = os.path.join(scss_folder, "reveal-mixins.scss")
        settings_file = os.path.join(scss_folder, "reveal-settings.scss")
        theme_file = os.path.join(scss_folder, "reveal-theme.scss")
        overrides_file = os.path.join(scss_folder, "overrides.scss.tmpl")

        with open(mixins_file, 'r') as m:
            mixins = m.read()

        with open(settings_file, 'r') as s:
            settings = s.read()

        with open(theme_file, 'r') as t:
            theme = t.read()

        with open(overrides_file, 'r') as o:
            overrides_template = o.read()

        overrides = overrides_template.format(**scss_variables)

        scss_string = "{0}\n{1}\n{2}\n{3}".format(mixins, settings, overrides, theme)
        return scss_string

    # Defaults to white theme parameters
    defaults = {
        # Background of the presentation
        "background_color": "#2b2b2b",

        # Primary/body text
        "main_font": 'Lato',
        "main_font_size": "inherit",
        "main_color": "#eee",

        # Vertical spacing between blocks of text
        "block_margin": "20px",

        # Headings
        "heading_margin": "0 0 $blockMargin 0",
        "heading_font": 'Lato',
        "heading_color": "#eee",
        "heading_line_height": "1.2",
        "heading_letter_spacing": "normal",
        "heading_text_transform": "none",
        "heading_text_shadow": "none",
        "heading_font_weight": "normal",

        "heading_one_text_shadow": "$headingTextShadow",
        "heading_one_size": "3.77em",
        "heading_two_size": "2.11em",
        "heading_three_size": "1.55em",
        "heading_four_size": "1.00em",

        "code_font": "monospace",

        # Links and actions
        "link_color": "#13DAEC",
        "linkColorHover": "lighten( $linkColor, 20% )",

        # Text selection
        "selection_background_color": "#FF5E99",
        "selection_color": "#fff"
    }
