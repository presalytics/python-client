import json
import presalytics.lib.plugins.base as ext
import presalytics.lib.plugins.jinja as jinja

class Mpld3NumpyToJson(json.JSONEncoder):
    """
    Simplified Numpy encoder that returns json that mpld3 will understand 
    """
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Mpld3Plugin(ext.ScriptPlugin, jinja.JinjaPluginMakerMixin):
    __plugin_name__ = 'mpld3'

    __dependencies__ = [
        {
            'kind': 'script',
            'name': 'external_scripts',
            'config': {
                'approved_scripts_key': 'd3v3'
            }
        },
        {
            'kind': 'script',
            'name': 'external_scripts',
            'config': {
                'approved_scripts_key': 'mpld3'
            }
        }
    ]

    template = '<script type="text/javascript">mpld3.draw_figure("{{ id|safe }}",{{ fig_json }});</script>'

    def to_script(self, config, **kwargs):
        fig_json = json.dumps(config["figure_dict"], cls=Mpld3NumpyToJson)
        render_config = {
            'id': config["id"],
            'fig_json': fig_json
        }
        return self.render(render_config)

