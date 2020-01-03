import typing
import presalytics
import presalytics.lib.plugins.base
import presalytics.lib.exceptions

site_host = "https://presalytics.io"
try:
    from config import PRESALYTICS
    site_host = PRESALYTICS["HOSTS"]["SITE"]
except (KeyError, AttributeError, ImportError, ModuleNotFoundError):
    pass

script_map = {
    'd3': 'https://cdnjs.cloudflare.com/ajax/libs/d3/5.12.0/d3.min.js',
    'd3v3': 'https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js',
    'reveal': {
        'base': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/js/reveal.min.js',
        'marked': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/markdown/marked.js',
        'markdown': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/markdown/markdown.min.js',
        'highlight': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/highlight/highlight.min.js',
        'math': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/math/math.min.js',
        'zoom': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/zoom-js/zoom.min.js',
        'notes': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/notes/notes.min.js',
        'print': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/plugin/print-pdf/print-pdf.min.js'

    },
    'mpld3': '{0}/static/mpld3/mpld3.min.js'.format(site_host),
    'ooxml': '{0}/static/ooxml/ooxml.js'.format(site_host)
}


styles_map = {
    'reveal': {
        'base': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/reveal.min.css',
        'themes': {
            'beige': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/beige.min.css',
            'black': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/black.min.css',
            'blood': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/blood.min.css',
            'league': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/league.min.css',
            'moon': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/moon.min.css',
            'night': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/night.min.css',
            'serif': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/serif.min.css',
            'simple': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/simple.min.css',
            'sky': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/sky.min.css',
            'solarized': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/solarized.min.css',
            'white': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/theme/white.min.css'
        },
        'print': 'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.6.0/css/print/pdf.min.css'
    }
}


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


ALLOWED_SCRIPTS = AttrDict(script_map)


ALLOWED_STYLES = AttrDict(styles_map)


class ApprovedExternalLinks(presalytics.lib.plugins.base.StylePlugin):
    __plugin_name__ = 'external_links'

    def to_style(self, config, **kwargs):
        key = config['approved_styles_key']
        link = ALLOWED_STYLES.flatten()[key]
        if link is None:
            message = "Key {0} does not reference a link in the APPROVED_LINKS dictionary".format(key)
            raise presalytics.lib.exceptions.MissingConfigException(message)
        return '<link rel="stylesheet" href="{0}"/>'.format(link)


class ApprovedExternalScripts(presalytics.lib.plugins.base.ScriptPlugin):
    __plugin_name__ = 'external_scripts'

    def to_script(self, config, **kwargs):
        key = config['approved_scripts_key']
        link = ALLOWED_SCRIPTS.flatten()[key]
        if link is None:
            message = "Key {0} does not reference a link in the APPROVED_SCRIPTS dictionary".format(key)
            raise presalytics.lib.exceptions.MissingConfigException(message)
        return '<script type="text/javascript" src="{0}"></script>'.format(link)
