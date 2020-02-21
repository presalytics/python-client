import jinja2
import presalytics.lib.exceptions
import typing


class JinjaPluginMakerMixin(object):
    """
    Mixin that helps plugins use Jinja2 python library for dynamically rendering 
    plugins based on the config dictionary.  Values from the `config` are pass 
    to the Jinja2 templating engine rendered into the html fragment via a 
    double-handlered placeholder (e.g., `{{ config_dict_key }}`)

    For more information on how to design a Jinja2 template, visit 
    https://jinja.palletsprojects.com

    Attributes
    ----------
    template : str
        the template property on a class that takes this mixin must 
        return a string with double-handlebarred placeholders

    Configuration Values
    ----------
    jinja_options : dict
        Options to be passed to the Jinja2 environment.  See a list of options on the 
        [Jinja2 API Page](https://jinja.palletsprojects.com/en/2.11.x/api/#jinja2.Environment)

    **kwargs : dict
        Other keyword arguments will be passed as variables to the Jinja2 rendering engine to that
        fill placeholders in the template
    """
    template: typing.Optional[str]
    template = None

    def __init__(self, *args, **kwargs):
        super(JinjaPluginMakerMixin, self).__init__(*args, *kwargs)

    def render(self, config: typing.Dict):
        """
        Loads the Configuration Value into the template and returns the filled out html fragment
        """
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
