import typing
import presalytics
import presalytics.lib.plugins.base
import presalytics.lib.exceptions

site_host = "https://presalytics.io"
try:
    site_host = presalytics.CONFIG.get("BROWSER_API_HOST", {}).get('SITE', "https://presalytics.io") #type: ignore
except (KeyError, AttributeError, ImportError, ModuleNotFoundError):
    pass


class AttrDict(dict):
    """ Dictionary subclass whose entries can be accessed by attributes
        (as well as normally).
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @staticmethod
    def from_nested_dict(data):
        """ Construct nested AttrDicts from nested dictionaries. """
        if not isinstance(data, dict):
            return data
        else:
            return AttrDict({key: AttrDict.from_nested_dict(data[key])
                            for key in data})

    def flatten(self) -> typing.Dict:
        return AttrDict._flatten(self, '', {})

    @staticmethod
    def _flatten(current, key, result) -> typing.Dict:
        if isinstance(current, dict):
            for k in current:
                new_key = "{0}.{1}".format(key, k) if len(key) > 0 else k
                AttrDict._flatten(current[k], new_key, result)
        else:
            result[key] = current
        return result


class ApprovedExternalLinks(presalytics.lib.plugins.base.StylePlugin):
    """
    `presalytics.lib.plugins.base.StylePlugin` subclass for converting a `presalytics.story.outline.Plugin` 
    config into an html `<link>` fragment.

    Attributes
    ----------
    attr_dict: presalytics.lib.plugins.external.AttrDict
        Performs nested lookups on the `STYLES_MAP`
    """
    __plugin_name__ = 'external_links'

    STYLES_MAP = {
        'c3': '{0}/static/vendor/c3/c3.min.css'.format(site_host),
        'reveal': {
            'base': '{0}/static/vendor/reveal/reveal.css'.format(site_host),
            'themes': {
                'beige': '{0}/static/vendor/reveal/theme/beige.css'.format(site_host),
                'black': '{0}/static/vendor/reveal/theme/black.css'.format(site_host),
                'blood': '{0}/static/vendor/reveal/theme/blood.css'.format(site_host),
                'league': '{0}/static/vendor/reveal/theme/league.css'.format(site_host),
                'moon': '{0}/static/vendor/reveal/theme/moon.css'.format(site_host),
                'night': '{0}/static/vendor/reveal/theme/night.css'.format(site_host),
                'serif': '{0}/static/vendor/reveal/theme/serif.css'.format(site_host),
                'simple': '{0}/static/vendor/reveal/theme/simple.css'.format(site_host),
                'sky': '{0}/static/vendor/reveal/theme/sky.min.css'.format(site_host),
                'solarized': '{0}/static/vendor/reveal/theme/solarized.css'.format(site_host),
                'white': '{0}/static/vendor/reveal/theme/white.css'.format(site_host)
            },
            'print': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/print/pdf.min.css',
            'toolbar': '{0}/static/css/toolbar.css'.format(site_host),
        },
        'preloaders' : '{0}/static/css/preloaders.css'.format(site_host),
        'bootstrap4': "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
        'font-awesome': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css',
        'bootstrap-table': 'https://unpkg.com/bootstrap-table@1.18.0/dist/bootstrap-table.min.css',
        'markdown-css': 'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css'
    
    }
    """
    Static nested dictionary containing links to external stylesheets that will be rendered alongside this plugin
    """

    def __init__(self, **kwargs):
        super(ApprovedExternalLinks, self).__init__(**kwargs)
        self.attr_dict = AttrDict(self.STYLES_MAP)


    def to_style(self, config, **kwargs):
        """
        Converts a dot-notation key for nested dictionaries (e.g., 'reveal.base') into a
        string contain an html fragement with `<link>` tag.  The dot-notation key 
        is pulled from the 'approved_styles_key' of the 'config' attrubte of subclass 
        of a `presalytics.story.outline.Plugin` object.
        """
        key = config['approved_styles_key']
        link = self.attr_dict.flatten()[key]
        if link is None:
            message = "Key {0} does not reference a link in the APPROVED_STYLES dictionary".format(key)
            raise presalytics.lib.exceptions.MissingConfigException(message)
        return '<link rel="stylesheet" href="{0}"/>'.format(link)


class ApprovedExternalScripts(presalytics.lib.plugins.base.ScriptPlugin):
    """
    `presalytics.lib.plugins.base.ScriptPlugin` subclass for converting a `presalytics.story.outline.Plugin` 
    config into an html `<script>` fragment.

    Attributes
    ----------
    attr_dict: presalytics.lib.plugins.external.AttrDict
        Performs nested lookups on the `SCRIPT_MAP`
    """
    __plugin_name__ = 'external_scripts'

    SCRIPT_MAP = {
        'c3': '{0}/static/vendor/c3/c3.min.js'.format(site_host),
        'd3': 'https://d3js.org/d3.v5.min.js',
        'd3v3': 'https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js',
        'reveal': {
            'base': '{0}/static/vendor/reveal/reveal.js'.format(site_host),
            # 'markdown': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/markdown/markdown.min.js',
            # 'highlight': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/highlight/highlight.min.js',
            # 'math': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/math/math.min.js',
            # 'zoom': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/zoom-js/zoom.min.js',
            # 'notes': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/notes/notes.min.js',
            # 'print': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/print-pdf/print-pdf.min.js',
            'toolbar': '{0}/static/js/toolbar.js'.format(site_host),
            'screenfull': '{0}/static/vendor/screenfull/screenfull.min.js'.format(site_host),

        },
        'mpld3': '{0}/static/mpld3/mpld3.min.js'.format(site_host),
        'ooxml': '{0}/static/js/ooxml.js'.format(site_host),
        'mpl-responsive': '{0}/static/js/mpl-responsive.js'.format(site_host),
        'events': '{0}/static/js/events.js'.format(site_host),
        'jquery': 'https://code.jquery.com/jquery-3.4.1.min.js',
        'popper': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js',
        'bootstrap4': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js',
        'bootstrap-table': 'https://unpkg.com/bootstrap-table@1.18.0/dist/bootstrap-table.min.js'
    }
    """
    Static nested dictionary containing links to external scripts that will be rendered alongside this plugin
    """

    def __init__(self, **kwargs):
        super(ApprovedExternalScripts, self).__init__(**kwargs)
        self.attr_dict = AttrDict(self.SCRIPT_MAP)


    def to_script(self, config, **kwargs):
        """
        Converts a dot-notation key for nested dictionaries (e.g., 'reveal.base') into a
        string containing an html fragement with `<script>` tags.  The dot-notation key 
        is pulled from the 'approved_styles_key' of the 'config' attrubte of subclass 
        of a `presalytics.story.outline.Plugin` object.
        """
        key = config['approved_scripts_key']
        link = self.attr_dict.flatten()[key]
        if link is None:
            message = "Key {0} does not reference a link in the APPROVED_SCRIPTS dictionary".format(key)
            raise presalytics.lib.exceptions.MissingConfigException(message)
        return '<script type="text/javascript" src="{0}"></script>'.format(link)
