import os
import typing
import presalytics.lib.plugins.base
import presalytics.lib.exceptions

css_path = os.path.join(os.path.dirname(__file__), "css")

class LocalStylesPlugin(presalytics.lib.plugins.base.StylePlugin):
    """
    Plugin incorporate styles from a css stylesheet in a local filepath
    """
    __plugin_name__ = 'local'

    LOCAL_STYLES_MAP = {
        "single_item_grid": os.path.join(css_path, "single-item-grid.css"),
        "flex_row": os.path.join(css_path, "flex-row.css"),
        "light_grey": os.path.join(css_path, "light-grey.css"),
        "responsive_title": os.path.join(css_path, "responsive-title.css"),
        "reveal_overrides": os.path.join(css_path, "reveal-overrides-base.css")
    }
    """
    Dictionary containing a map configuration keys to css files that are 
    member of the Presalytics Python Library manifest
    """

    def to_style(self, config, **kwargs):
        """
        Renders a css stylesheet as an inline style tag in a story

        Parameters
        ----------
        config : dict
            A dictionary containing either a "css_file_path" key, which points
            to a local file path, or a "css_file_id" refers to a css file included
            in the Presalytics Python Library's manifest 
        """
        id = config.get("css_file_id", None)
        if not id:
            file_path = config.get("css_file_path", None)
            if not file_path:
                message = 'Plugin requires "css_file_id" or "css_file_path" in its configuration dictionary'
                raise presalytics.lib.exceptions.MissingConfigException(message)
            if not os.path.exists(file_path):
                message = 'Path {0} in plugin configuration does not exist'.format(file_path)
                raise presalytics.lib.exceptions.MissingConfigException(message)
        else:
            file_path = LocalStylesPlugin.LOCAL_STYLES_MAP[id]
        with open(file_path, 'r') as f:
            style_data = f.read()
        tag = "<style>{0}</style>".format(style_data)
        return tag
