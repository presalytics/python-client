"""
Module helps serialize and deserialize presalytics story outlines to/from json and yaml source data.
Classes in this module acts are interfaces between story outlines and `component` objects
"""
import json
import numpy as np
import base64
import yaml
import inspect
import datetime
import dateutil.parser
import uuid
import abc
import typing
import sys
import os
import semantic_version
import jsonschema
from presalytics.story.util import to_camel_case, to_snake_case
from presalytics.lib.exceptions import ValidationError

class OutlineEncoder(json.JSONEncoder):
    """
    Json encoder for `presalytics.story.outline.OutlineBase` objects
    """
    def default(self, obj):
        """
        Override method for deserializing objects that inherit from 
        `presalytics.story.outline.OutlineBase`
        """
        if issubclass(obj.__class__, OutlineBase):
            return obj.to_dict()
        if isinstance(obj, datetime.datetime):
            return obj.replace(tzinfo=datetime.timezone.utc).isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        # Generalized numpy encoder/decoder -- for http transport
        # If input object is an ndarray it will be converted into a dict 
        # holding dtype, shape and the data, base64 encoded.
        if isinstance(obj, np.ndarray):
            if obj.flags['C_CONTIGUOUS']:
                obj_data = obj.data
            else:
                cont_obj = np.ascontiguousarray(obj)
                assert(cont_obj.flags['C_CONTIGUOUS'])
                obj_data = cont_obj.data
            data_b64 = base64.b64encode(obj_data).decode('utf-8')
            return dict(__ndarray__=data_b64,
                        dtype=str(obj.dtype),
                        shape=obj.shape)
        return json.JSONEncoder.default(self, obj)

def json_numpy_obj_hook(dct):
    """
    Decodes a previously encoded numpy ndarray with proper shape and dtype.
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'].encode('utf-8'))
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct


def get_current_spec_version():
    """
    Get the latest version of the story outline schema via reading foldernames in 
    the schemas subfolder of this file's directory
    """
    schema_dir = os.path.join(os.path.dirname(__file__), "schemas")
    major, minor, patch = None, None, None
    latest = None
    for _dir in os.listdir(schema_dir):
        if not latest: 
            latest = semantic_version.Version(_dir)
        elif latest < semantic_version.Version(_dir):
            latest = semantic_version.Version(_dir)
    return str(latest)

def load_schema(version_number):
    path = os.path.join(os.path.dirname(__file__), "schemas", version_number, "story-outline.schema.json")
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def load_latest_schema():
    version_number = get_current_spec_version()
    return load_schema(version_number)



class OutlineBase(abc.ABC):
    """
    Base object for building Story Outlines

    Includes methods for validiating, serializing, and deserializing outline classes
    """
    
    __annotations__: typing.Dict
    __required__: typing.Sequence[str]
    additional_properties: typing.Dict

    __required__ = []
    """
    A `list` of `str` objects representation attributes required to be to present
    in order for an instance to be deserialized.  Checked when the `validate` method is
    run
    """

    def __init__(self, **kwargs):
        if "additional_properties" in kwargs:
            self.additional_properties = kwargs["additional_properties"]
        else:
            self.additional_properties = kwargs

    def validate(self):
        """
        Ensures that the outline component has all required attributes.  Raises
        a `presalytics.lib.exceptions.ValidationError` if required attributes are 
        missing.  Reads the list of requried objects from the __required__ class
        variable
        """
        for key in self.__required__:
            if not hasattr(self, key):
                err_message = 'Could not load {0} object, source data missing "{1}" key'.format(self.__class__.__name__, key)
                raise ValidationError(err_message)


    @classmethod
    def deserialize(cls, json_obj: dict):
        """
        Serializes a `dict` into  class instance

        Parameters
        ----------
        json_obj : dict
            A dictionary containing attributes of the class
        
        Returns
        ----------
            A `class` instance
        """
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
    def load(cls, json_str: str):
        """
        Serializes a `str` into  class instance

        Parameters
        ----------
        json_str : str
            A dictionary containing attributes of the class
        
        Returns
        ----------
        A `class` instance
        """
        json_obj = json.loads(json_str)
        return cls.deserialize(json_obj)

    @classmethod
    def import_yaml(cls, yaml_file: str):
        """
        Serializes a yaml from a file into a class instance

        Parameters
        ----------
        yaml_file : str
            Filepath to the file with yaml representing that class
        
        Returns
        ----------
        A `class` instance
        """
        with open(yaml_file, 'r') as file:
            obj = yaml.unsafe_load(file) # use unsafe loader per: https://github.com/yaml/pyyaml/issues/286, Monitor for fix.
        return cls.deserialize(obj)

    def export_yaml(self, filename):
        """
        Dumps yaml-formatted text representing the class instance into a file

        Parameters
        ----------
        filename : str
            Filepath to the location where the yaml fiel shoudl be dumped
        """
        with open(filename, 'w') as file:
            yaml.dump(self.to_dict(), file)

    def dump(self):
        """
        Serialize the class instance to a stringified Json object

        Returns
        ---------
        A `str` object representing the class instance in json
        """
        return json.dumps(self, cls=OutlineEncoder)

    def to_dict(self):
        """
        Converts an instance to a `dict` object of attributes.
        Used for further serialization.

        Returns
        ----------
        A `dict` object containing instance attributes
        """
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
            ret_val = json.loads(json.dumps(val, cls=OutlineEncoder), encoding='utf-8', object_hook=json_numpy_obj_hook)
            ret[ret_key] = ret_val
        return ret


class Info(OutlineBase):
    """
    Carries metadata for a `presalytics.story.outline.StoryOutline`

    Attributes
    ----------
    revision : str
        The current revision number of the story outline
    
    date_created : datetime.datetime
        The creation date of the story in UTC 
    
    date_modified : datetime.dataime
        The last modified  date of the story in UTC 
    
    created_by : str
        The Presalytics API user id of the user that created the story
    
    modified_by : str
        The Presalytics API user id of the user that last modified the story
    
    revision_notes : str, optional
        Text explaining the changes made during that latest revision to the story
    
    """
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
                 story_id=None,
                 **kwargs):
        super(Info, self).__init__(**kwargs)
        self.revision = revision
        self.date_created = dateutil.parser.parse(date_created).replace(tzinfo=datetime.timezone.utc)
        self.date_modified = dateutil.parser.parse(date_modified).replace(tzinfo=datetime.timezone.utc)
        self.created_by = created_by
        self.modified_by = modified_by
        self.revision_notes = revision_notes

class Plugin(OutlineBase):
    """
    Represents at plugin to be incorporated in the story during rendering process.  The information
    contain in this object is passed to subclass of `presalytics.lib.plugins.base.PluginBase` found
    in the `presalytics.PLUGINS` registry. at render-time.

    Attributes
    ----------
    kind : str
        The kind of Plugin.  Usually either "style" for a `presalytics.lib.plugins.base.StylePlugin`
        or "script" for a `presalytics.lib.plugins.base.ScriptPlugin`

    name : str
        The name of the plugin.  A name must be unique within a 
        given `presalytics.PLUGINS` registry.

    config : dict
        The configiuration of the plugin.  The keys in this dictionary are unqiue to a given 
        plugin.
    """
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
    """
    A represenation of an analytic or graphic object to be rendered within a 
    `presalytics.story.outline.Page`. At render-time, the `presalytics.COMPONENTS`
    registry is queried for a matching class or instance. If found, the widget is
    rendered.

    Attributes
    ----------
    kind : str
        The kind of Widget. Typically corresponds to a class that inherits from 
        `presalytics.story.components.WidgetBase`

    name : str
        The name of the Widget.  Correpsonds to a local instance of 
        `presalytics.story.components.WidgetBase` loaded into `presalytics.COMPONENTS`

    data : dict
        Widget data required so the corresponding subclass of `presalytics.story.components.WidgetBase`
        can initialize and render
        
    plugins : list of presalytics.story.outline.Plugin
        A list of plugins that must be rendered alongside this widget
    """
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
    """
    A representation of a canvas on which `presalytics.story.outline.Widget` objects
    can be rendered. At render-time, the `presalytics.COMPONENTS`
    registry is queried for a matching class. If found, the page and its
    widgets are rendered.

    Attributes
    ----------
    kind : str
        The kind of Page. Typically corresponds to a class that inherits from 
        `presalytics.story.components.PageTemplateBase`

    name : str
        The name of the Page.  A name must be unique within a 
        given `presalytics.COMPONENTS` registry

    widgets : list of presalytics.story.outline.Widget
        Widgets that will be rendered along with the page        
        
    plugins : list of presalytics.story.outline.Plugin
        A list of plugins that must be rendered alongside this widget

    """
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
    """
    A container for story properties that persist accross all pages of story. At render-time, 
    the `presalytics.COMPONENTS` registry is queried for a matching class. If found, the theme is
    incorporated into the story.

    Attributes
    ----------
    kind : str
        The kind of Theme. Typically corresponds to a class that inherits from 
        `presalytics.story.components.ThemeBase`

    name : str
        The name of the Theme.  Corresponds to a local instance of 
        `presalytics.story.components.ThemeBase` loaded into `presalytics.COMPONENTS`

    data : dict
        Widget data required so the corresponding subclass of `presalytics.story.components.ThemeBase`
        can initialize and render
        
    plugins : A list of presalytics.story.outline.Plugin
        A list of plugins that must be rendered alongside this widget
    """
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
    """
    A StoryOutline contains instructions for a `presalytics.story.components.Renderer` 
    (e.g., `presalytics.story.revealer.Revealer`) to render an story into html.

    A story outline's `info`, `pages`, `widgets`, and `themes` are intended to be easily editable
    by both human users and machines via json serialization and deserialization, and the ecosystem
    of tools that can be used to edit json objects. Once a valid `StoryOutline` is
    built, it contains sufficient instructions for this library find the required components in the user's
    workspace and render theme.

    StoryOutlines are stored in the [Presalytics API Story Service](https://presalytics.io/docs/api-specifications/story/).
    The story service manages version history and user permissions for StoryOutlines.  For more information
    about how outlines are used, please see the [How It Works](https://presalytics.io/docs/how-it-works/)
    section of the website.

    Attributes
    ----------

    outline_version : str
        the version of that StoryOuline schema.
    
    info : presalytics.story.outline.Info
        Metadata about this StoryOutline
    
    pages : list of presalytics.story.outline.Page
        The pages that will be rendered in this story
    
    themes : list of presalytics.story.outline.Theme
        The themes that will underlie each `presalytics.story.outline.Page` in the StoryOutline
    
    title : str, optional
        A title for the story

    description: str, optional
        A description of the story
    
    story_id : str, optional
        The Presalytics API Story Id.  Automatically added once the story outline has been pushed to
        the server.

    """
    outline_version: str
    info: Info
    pages: typing.List[Page]
    description: str
    title: str
    themes: typing.List[Theme]
    story_id: str

    __required__ = [
        'outline_version',
        'info',
        'pages',
        'title',
    ]

    def __init__(self, info, pages, description, title, themes, plugins=None, story_id="empty", **kwargs):
        super(StoryOutline, self).__init__(**kwargs)
        self.outline_version = get_current_spec_version()
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
        self.story_id = story_id
        if not kwargs.get("validate", True):
            self.validate()

        def validate(self):
            super(StoryOutline, self).validate()
            jsonschema.validate(instance=self.to_dict(), schema=load_latest_schema())
        