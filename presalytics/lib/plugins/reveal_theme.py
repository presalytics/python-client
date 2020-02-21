import os
import posixpath
import sass
import typing
import requests
import presalytics.lib.plugins.base


class RevealCustomTheme(presalytics.lib.plugins.base.StylePlugin):
    """
    Plugin to for customizing reveal.js settings for a given story

    This plugin's configuration dictionary keys and that load them in
    as variable to a _variables.scss file and compiles the scss using the
    sass python package. 

    See reveal.js' [Creating a Theme](https://github.com/hakimel/reveal.js/blob/8a54118f43b91030f3965088d5e1c1c7598a5cd3/css/theme/README.md)
    page for more information regarding configuration values.
    """
    __plugin_name__ = 'reveal_custom_theme'
    defaults: typing.Dict[str, str]

    fonts_base_url = 'https://fonts.googleapis.com/css?family={0}'
    """
    Google fonts base url for loading fonts via a `<link>` tag 
    """

    def to_style(self, config, **kwargs):
        """
        Returns compiled scss and links to download fonts
        """
        scss_variables = self.defaults
        scss_variables.update(config)
        scss_string = self.get_base_scss(scss_variables)
        new_css = sass.compile(string=scss_string)
        style_string = "<style>\n{0}\n</style>".format(new_css)
        links = self.get_fonts(config["fonts"])
        return links + style_string

    def get_fonts(self, fonts: typing.List[str]):
        """
        Creates `<link>` tags from font names
        """
        links = ""
        for font in fonts:
            link = self.get_font_link(font)
            if link:
                links = links + link + "\n"
        return links

    def get_font_link(self, font_name) -> typing.Optional[str]:
        """
        Tests whether a given font is available for download form google fonts.  Returns
        the link tag if available
        """
        test_url = self.fonts_base_url.format(font_name)
        r = requests.get(test_url)
        if r.status_code == 200:
            return '<link href="{0}" rel="stylesheet">'.format(test_url)
        else:
            return None

    def get_base_scss(self, scss_variables):
        """
        loads the reveal.js scss files into string to be compiled by the sass module
        """
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
    """
    Default reveal.js theme configuration for presalytics stories
    """
