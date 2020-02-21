import os
import sass
import typing
import presalytics.lib.exceptions
import presalytics.lib.plugins.base

class ScssPlugin(presalytics.lib.plugins.base.StylePlugin):
    """
    Compiles scss from files and a `dict` of variables and loads
    them into a script tag

    *Note: Any `<script>` tags nested into the resultant style tag will
    be removed at render-time by a `presalytics.story.components.Renderer`.
    These script tags will not make it to the browser.

    Configuration Values
    ----------
    filenames : list of str
        A list of scss filenames that will get compiled to css if
        all files are present

    rendered_css : str, optional
        If the files are not present, this string will be placed in the
        resultant style tag

    variables : dict, optional
        Scss variables to include. Dictionary keys should be prefixed with a
        `$` to indicate that they are scss variable names.  
    """
    __plugin_name__ = "scss_files"

    def __init__(self, **kwargs):
        super(ScssPlugin, self).__init__(**kwargs)

    def _files_are_local(self, filenames):
        for fname in filenames:
            if not os.path.exists(fname):
                return False
        return True

    def _create_variables_string(self, variables):
        _vars = ""
        for key, val in variables.items():
            _vars = _vars + key + ": " + val + "; "
        return _vars

    def _load_files_to_string(self, filenames):
        scss_string = ""
        for fname in filenames:
            with open(fname, 'r') as f:
                addl_scss = f.read()
            scss_string = scss_string + addl_scss
        return scss_string

    def make_css(self, filenames: typing.List[str], variables: typing.Dict[str, str]):
        """
        Compiles the scss in filenames to an html fragment using variables 
        
        Returns
        ----------
        A `<style>` tag html fragment in a string
        """
        _scss = self._create_variables_string(variables) + self._load_files_to_string(filenames)
        return sass.compile(string=_scss)

    def to_style(self, config, **kwargs):
        """
        Renders a config containing `Configuration Values` to a style tag
        """
        filenames = config.get("filenames", None)
        if not filenames:
            raise presalytics.lib.exceptions.MissingConfigException("Filenames are required in the config.")
        variables = config.get("variables", {})
        if self._files_are_local(filenames):
            rendered_css = self.make_css(filenames, variables)
        elif config.get("rendered_css", None):
            rendered_css = config.get("rendered_css")
        else:
            raise presalytics.lib.exceptions.MissingConfigException("A file referenced by this plugin could not be found.")
        return "<style>{0}</style>".format(rendered_css)


    @classmethod
    def configure(cls, filenames: typing.List[str], variables: typing.Dict = {}, old_css: str = None) -> typing.Dict:
        """
        Call this method when serializing a subclass of `presalytics.story.components.ComponentBase` 
        to generate a configuration for the plugin with a valid `rendered_css` entry
        """
        inst = cls()
        if not filenames:
            raise presalytics.lib.exceptions.MissingConfigException("Filenames are required in the config.")
        if inst._files_are_local(filenames):
            rendered_css = inst.make_css(filenames, variables)
        elif old_css:
            rendered_css = old_css
        else:
            raise presalytics.lib.exceptions.MissingConfigException("A file referenced by this plugin could not be found.")
        ret = {
            "name": inst.__plugin_name__,
            "kind": inst.__plugin_kind__,
            "config": {
                "filenames": filenames,
                "variables": variables,
                "rendered_css": rendered_css
            }
        }
        return ret

