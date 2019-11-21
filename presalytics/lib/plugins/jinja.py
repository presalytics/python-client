import jinja2
import presalytics.lib.exceptions
import typing


class JinjaPluginMakerMixin(object):
    template: typing.Optional[str]
    template = None

    def __init__(self, *args, **kwargs):
        super(JinjaPluginMakerMixin, self).__init__(*args, *kwargs)

    def render(self, config: typing.Dict):
        template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(self.get_template())
        return template.render(config)

    def get_template(self) -> str:
        if not self.template:
            raise presalytics.lib.exceptions.ValidationError("Plugins the use the JinjaPluginMakerMixin must have a defiined template attribute.")
        else:
            return self.template
