import os
import typing
import presalytics.lib.plugins.base
import presalytics.lib.exceptions

css_path = os.path.join(os.path.dirname(__file__), "css")

local_styles_map = {
    "single_item_grid": os.path.join(css_path, "single-item-grid.css")
}


class LocalStylesPlugin(presalytics.lib.plugins.base.StylePlugin):
    __plugin_name__ = 'local'

    def to_style(self, config, **kwargs):
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
            file_path = local_styles_map[id]
        with open(file_path, 'r') as f:
            style_data = f.read()
        tag = "<style>{0}</style>".format(style_data)
        return tag
