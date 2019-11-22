import json
import presalytics.lib.plugins.base as ext
import presalytics.lib.plugins.jinja as jinja


class Mpld3Plugin(ext.ScriptPlugin, jinja.JinjaPluginMakerMixin):
    __plugin_name__ = 'mpld3'

    __dependencies__ = [
        {
            'type': 'script',
            'name': 'external_scripts',
            'config': {
                'approved_scripts_key': 'reveal.base'
            }
        },
        {
            'type': 'script',
            'name': 'external_scripts',
            'config': {
                'approved_scripts_key': 'd3v3'
            }
        },
        {
            'type': 'script',
            'name': 'external_scripts',
            'config': {
                'approved_scripts_key': 'mpld3'
            }
        }
    ]

    template = '<script type="text/javascript">mpld3.draw_figure("{{ id|safe }}",{{ fig_json|tojson }});</script>'

    def to_script(self, config, **kwargs):
        render_config = {
            'id': config["id"],
            'fig_json': config["figure_dict"]
        }
        return self.render(render_config)
