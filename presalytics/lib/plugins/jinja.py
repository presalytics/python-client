import jinja2
import presalytics.lib.exceptions
import typing


class JinjaPluginMakerMixin(object):
    template: typing.Optional[str]
    template = None

    def __init__(self, *args, **kwargs):
        super(JinjaPluginMakerMixin, self).__init__(*args, *kwargs)

    def render(self, config: typing.Dict):
        options = {
            "loader": jinja2.BaseLoader()
        }
        if config.get("jinja_options", None):
            options.update(config.pop("jinja_options"))
        template = jinja2.Environment(**options).from_string(self.get_template())
        return template.render(config)

    def get_template(self) -> str:
        if not self.template:
            raise presalytics.lib.exceptions.ValidationError("Plugins the use the JinjaPluginMakerMixin must have a defiined template attribute.")
        else:
            return self.template
