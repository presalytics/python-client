"""
Module helps serialize and deserialize presalytics story outlines to/from json yaml.
Allow downstream modules work seemlessly with json data

Note: this module leverage type-checking at runtime, and may cause ciruclar references
if you are incorporating type hints on presalytics objects in modules that import this file.
The problem is solved using the TYPE_CHECKING boolean in the python's typing package.
"""
import json
import yaml
import inspect
import datetime
import dateutil.parser
import uuid
import abc
import typing
import sys
from presalytics.story.util import to_camel_case, to_snake_case
from presalytics.lib.exceptions import ValidationError


class OutlineEncoder(json.JSONEncoder):
    def default(self, obj):
        if issubclass(obj.__class__, OutlineBase):
            return obj.to_dict()
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def get_current_spec_version():
    return '0.1.1'


class OutlineBase(abc.ABC):
    __client_ver__: str
    __annotations__: typing.Dict
    __required__: typing.Sequence[str]
    additional_properties: typing.Dict

    __required__ = []

    def __init__(self, **kwargs):
        if "additional_properties" in kwargs:
            self.additional_properties = kwargs["additional_properties"]
        else:
            self.additional_properties = kwargs

    def validate(self):
        for key in self.__required__:
            if not hasattr(self, key):
                err_message = 'Could not load {0} object, source data missing "{1}" key'.format(self.__class__.__name__, key)
                raise ValidationError(err_message)

    @classmethod
    def deserialize(cls, json_obj):
        if type(json_obj) == cls:
            return json_obj
        updated_obj = {}
        for key, val in json_obj.items():
            new_key = to_snake_case(key)
            updated_obj.update({new_key: val})
        for req in inspect.getargspec(cls).args:
            if req not in updated_obj and req != 'self':
                updated_obj.update({req: None})
        return cls(**updated_obj)

    @classmethod
    def load(cls, json_str):
        json_obj = json.loads(json_str)
        return cls.deserialize(json_obj)

    @classmethod
    def import_yaml(cls, yaml_file):
        with open(yaml_file, 'r') as file:
            obj = yaml.safe_load(file)
        return cls.deserialize(obj)

    def export_yaml(self, filename):
        with open(filename, 'w') as file:
            yaml.dump(self.to_dict(), file)

    def dump(self):
        return json.dumps(self, cls=OutlineEncoder)

    def to_dict(self):
        ret = {}
        for key, val in self.__dict__.items():
            if key not in self.__required__:
                if isinstance(val, list):
                    if len(val) == 0:
                        continue
                if isinstance(val, dict):
                    if len(val.items()) == 0:
                        continue
            ret_key = "{}".format(to_camel_case(key))
            ret_val = json.loads(json.dumps(val, cls=OutlineEncoder), encoding='utf-8')
            ret[ret_key] = ret_val
        return ret


class Info(OutlineBase):
    revision: str
    date_created: datetime.datetime
    date_modified: datetime.datetime
    created_by: str
    modified_by: str
    revision_notes: str

    def __init__(self,
                 revision,
                 date_created,
                 date_modified,
                 created_by,
                 modified_by,
                 revision_notes,
                 **kwargs):
        super(Info, self).__init__(**kwargs)
        self.revision = revision
        self.date_created = dateutil.parser.parse(date_created)
        self.date_modified = dateutil.parser.parse(date_modified)
        self.created_by = created_by
        self.modified_by = modified_by
        self.revision_notes = revision_notes


class Plugin(OutlineBase):
    kind: str
    name: str
    config: typing.Dict

    __required__ = [
        'kind',
        'config',
        'name'
    ]

    def __init__(self, kind, name, config, **kwargs):
        super(Plugin, self).__init__(**kwargs)
        self.kind = kind
        self.name = name
        self.config = config


class Widget(OutlineBase):
    name: str
    kind: str
    data: typing.Dict[str, str]
    plugins: typing.Sequence

    __required__ = [
        'name',
        'data'
    ]

    def __init__(self, name, kind, data, plugins=None, **kwargs):
        super(Widget, self).__init__(**kwargs)
        self.name = name
        self.kind = kind
        if data:
            self.data = data
        else:
            self.data = {}
        if plugins:
            self.plugins = [Plugin.deserialize(x) for x in plugins]
        else:
            self.plugins = []


class Page(OutlineBase):
    name: str
    kind: str
    widgets: typing.Sequence[Widget]
    plugins: typing.List[Plugin]

    __required__ = [
        'name',
        'kind'
    ]

    def __init__(self, name, kind, widgets, plugins=None, **kwargs):
        super(Page, self).__init__(**kwargs)
        self.name = name
        self.kind = kind
        if widgets:
            self.widgets = [Widget.deserialize(x) for x in widgets]
        else:
            self.widgets = []
        if plugins:
            self.plugins = [Plugin.deserialize(x) for x in plugins]
        else:
            self.plugins = []


class Theme(OutlineBase):
    name: str
    kind: str
    data: typing.Dict
    plugins: typing.List[Plugin]

    __required__ = [
        'name'
    ]

    def __init__(self, name, kind, data, plugins=None, **kwargs):
        super(Theme, self).__init__(**kwargs)
        self.name = name
        self.kind = kind
        if data:
            self.data = data
        else:
            self.data = {}
        if plugins:
            self.plugins = [Plugin.deserialize(x) for x in plugins]
        else:
            self.plugins = []


class StoryOutline(OutlineBase):
    presalytics_story: str
    info: Info
    pages: typing.Sequence[Page]
    description: str
    title: str
    themes: typing.Sequence[Theme]

    __required__ = [
        'presalytics_story',
        'info',
        'pages',
        'title'
    ]

    def __init__(self, presalytics_story, info, pages, description, title, themes, plugins=None, **kwargs):
        super(StoryOutline, self).__init__(**kwargs)
        self.presalytics_story = presalytics_story
        self.info = Info.deserialize(info)
        self.pages = [Page.deserialize(x) for x in pages]
        if description:
            self.description = description
        else:
            self.description = ""
        if title:
            self.title = title
        else:
            self.title = ""
        if themes:
            self.themes = [Theme.deserialize(x) for x in themes]
        else:
            self.themes = []
        if plugins:
            self.plugins = [Plugin.deserialize(x) for x in plugins]
        else:
            self.plugins = []
