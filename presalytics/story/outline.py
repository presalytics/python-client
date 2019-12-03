"""
Module helps serialize and deserialize presalytics story outlines to/from json yaml.
Allow downstream modules work seemlessly with json data

Note: this module leverage type-checking at runtime, and may cause ciruclar references
if you are incorporating type hints on presaltyics objects in modules that import this file.
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
from presalytics.story.util import to_camel_case, to_snake_case
from presalytics.lib.exceptions import ValidationError


class OutlineEncoder(json.JSONEncoder):
    def default(self, obj):
        if issubclass(obj.__class__, OutlineBase):
            return obj.to_dict()
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, uuid.uuid4):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class OutlineBase(abc.ABC):
    __client_ver__: str
    __annotations__: typing.Dict
    __required__: typing.Sequence[str]

    __required__ = []

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            key_name = to_snake_case(key)
            val = self.deserialize_child(key_name, val)
            setattr(self, key_name, val)
        self.validate()

    def validate(self):
        for key in self.__required__:
            if not hasattr(self, key):
                err_message = 'Could not load {0} object, source data missing "{1}" key'.format(self.__class__.__name__, key)
                raise ValidationError(err_message)

    def deserialize_child(self, key_name, val):
        if key_name in self.__annotations__:
            sub_type = self.__annotations__[key_name]
            if inspect.isclass(sub_type) and not issubclass(sub_type, str):
                if issubclass(sub_type, OutlineBase):
                    val = sub_type(**val)
                if issubclass(sub_type, typing.Sequence):
                    try:
                        list_type = sub_type.__args__[0]
                        if issubclass(list_type, OutlineBase):
                            for x in range(0, len(val)):
                                val[x] = list_type(**val[x])
                    except TypeError:
                        pass
                if issubclass(sub_type, typing.Dict):
                    try:
                        val_type = sub_type.__args__[1]
                        if issubclass(val_type, OutlineBase):
                            for child_key, child_val in val.items():
                                updated_val = val_type({child_key, child_val})
                                val.update(child_key, updated_val)
                    except TypeError:
                        pass
                if issubclass(sub_type, datetime.datetime):
                    val = dateutil.parser.parse(val)
                if issubclass(sub_type, uuid.UUID):
                    val = uuid.UUID(val)
        return val

    @classmethod
    def deserialize(cls, json_obj):
        return cls(**json_obj)

    @classmethod
    def load(cls, json_str):
        return json.JSONDecoder(object_hook=cls.deserialize).decode(json)

    @classmethod
    def import_yaml(cls, yaml_file):
        with open(yaml_file, 'r') as file:
            obj = yaml.safe_load(file)
        return cls.deserialize(obj)

    def dump(self):
        return json.dumps(self, cls=OutlineEncoder)

    def to_dict(self):
        ret = {}
        for key, val in self.__dict__.items():
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


class Widget(OutlineBase):
    name: str
    kind: str
    data: typing.Dict[str, str]
    plugins: typing.Sequence[str]
    additional_properties: typing.Dict[str, str]

    __required__ = [
        'name',
        'data'
    ]


class Page(OutlineBase):
    name: str
    kind: str
    widgets: typing.Sequence[Widget]
    additional_properties: typing.Dict[str, str]
    plugins: typing.List[typing.Dict]

    __required__ = [
        'name'
    ]


class Theme(OutlineBase):
    name: str
    module_name: str
    additional_properties: typing.Dict[str, str]

    __required__ = [
        'name'
    ]


class Plugin(OutlineBase):
    type: str
    name: str
    config: typing.Dict

    __required__ = [
        'type',
        'config',
        'name'
    ]


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
