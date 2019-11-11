import json
import yaml
import inspect
from datetime import datetime
from importlib import import_module
import re
from dateutil.parser import parse as dateparse
from uuid import uuid4, UUID
from abc import ABC
from typing import Sequence, Dict
from typing_extensions import Literal
from presalytics.lib.exceptions import ValidationError
from presalytics.story.extension_base import ExtensionBase


class OutlineEncoder(json.JSONEncoder):
    def default(self, obj):
        if issubclass(obj.__class__, OutlineBase):
            return obj.to_dict()
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, uuid4):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def to_snake_case(camel_case_str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_title_case(name_string):
    components = name_string.split('_')
    return ''.join(x[0].upper() + x[1:] for x in components)


class OutlineBase(ABC):
    __client_ver__: str
    __annotations__: Dict
    __required__: Sequence[str]
    
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
                err_message = "Could not load {0} object, source data missing {1} key".format(self.__class__.__name__, key)
                raise ValidationError(err_message)

    def deserialize_child(self, key_name, val):
        if key_name in self.__annotations__:
            sub_type = self.__annotations__[key_name]
            if inspect.isclass(sub_type):
                if issubclass(sub_type, OutlineBase):
                    val = sub_type(**val)
                if issubclass(sub_type, Sequence):
                    list_type = sub_type.__args__[0]
                    if issubclass(list_type, OutlineBase):
                        for x in range(0, len(val)):
                            val[x] = list_type(**val[x])
                if issubclass(sub_type, Dict):
                    val_type = sub_type.__args__[1]
                    if issubclass(val_type, OutlineBase):
                        for child_key, child_val in val.items():
                            updated_val = val_type({child_key, child_val})
                            val.update(child_key, updated_val)
                if issubclass(sub_type, datetime):
                    val = dateparse(val)
                if issubclass(sub_type, UUID):
                    val = UUID(val)
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
            # if type(val) == str:
            #     "{}".format(val)
            ret_val = json.loads(json.dumps(val, cls=OutlineEncoder))
            ret[ret_key] = ret_val
        return ret



class Info(OutlineBase):
    revision: str
    date_created: datetime
    date_modified: datetime
    created_by: str
    modified_by: str
    revision_notes: str


class Widget(OutlineBase):
    name: str
    data: Dict[str, str]
    additional_properties: Dict

    __required__ = [
        'name',
        'data'
    ]


class Page(OutlineBase):
    use_template: bool
    template_name: str
    widgets: Sequence[Widget]
    additional_properties: Dict



class Theme(OutlineBase):
    name: str
    module_name: str
    additional_properties: Dict

    __required__ = [
        'name'
    ]


class Extension(OutlineBase):
    type: Literal["widget", "theme", "template", "x-*"]
    module_name: str
    name: str

    __required__ = [
        'type',
        'name'
    ]



class StoryOutline(OutlineBase):
    presalytics_story: str
    info: Info
    pages: Sequence[Page]
    description: str
    title: str
    themes: Sequence[Theme]
    extensions: Sequence[Extension]

    __required__ = [
        'presalytics_story',
        'info',
        'pages',
        'title'
    ]

    def load_extensions(self) -> Sequence[ExtensionBase]:
        loaded_extensions = []
        for extension in self.extensions:
            if extension.module_name is not None:
                import_module(extension.module_name)
            if not extension.type in Extension.__annotations__['type'].__values__ or extension.type[2:] != "x-":
                message = "Unknown extension type {}.  Must be type widget, theme, tempalte, or x-*".format(extension.type)
                raise ValidationError(message)
            ext_class = globals()[extension.name]
            if not issubclass(ext_class, ExtensionBase):
                message = "Extension {} must be a subclass of presalytics.story.ExtensionBase".format(extension.name)
                raise ValidationError(message)
            loaded_extensions.append(ext_class)
        return loaded_extensions
            
            
            

