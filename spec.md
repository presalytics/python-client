# presalytics

Presalytics python client
https://presalytics.io

# Client
```python
Client(self, delegate_login=False, token=None, cache_tokens=True, username=None, password=None, **kwargs)
```
Main PresalyticsClient base object
## exchange_token
```python
Client.exchange_token(self, original_token, audience=None)
```
Requires developer account and authorized client credentials
# PluginBase
```python
PluginBase(self, **kwargs)
```

A plugin converts a dictionary of configuration values into an html script.
Typically plugins are are used as reable mapping classes to add script tags to
to a rendered html body.

Attributes:
----------

__plugin_kind__: str
    The __plugin_kind__ is a static string that uniquely identifies this plugin to classes
    the render story outlines (e.g., presalytics.story.revealer.Revealer).


## get_tag
```python
PluginBase.get_tag(self, config:Dict[str, Any], **kwargs) -> str
```

Generic method to be implemented by all inheriting classes. Allow plugin
to be render without knowledge of the underlying plugin kind.

Parameters:
----------

config: Dict
    A set configuration values for the plugin.  Required keys should be
    specified by the docstring of the inheriting classes.
    Can be implemented via a mypy_extensions.TypedDict object if warranted.
    The presalytics.story.outline.Plugin's config element should be passed
    as this value to render the script.

Returns:
----------

A string carrying a html script that can be embedded in a html document


# ApprovedExternalLinks
```python
ApprovedExternalLinks(self, **kwargs)
```

# ApprovedExternalScripts
```python
ApprovedExternalScripts(self, **kwargs)
```

# JinjaPluginMakerMixin
```python
JinjaPluginMakerMixin(self, *args, **kwargs)
```

# LocalStylesPlugin
```python
LocalStylesPlugin(self, **kwargs)
```

# Mpld3Plugin
```python
Mpld3Plugin(self, **kwargs)
```

## template
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
# OoxmlTheme
```python
OoxmlTheme(self, **kwargs)
```

# RevealConfigPlugin
```python
RevealConfigPlugin(self, **kwargs)
```

## default_config
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
    d = {}
    for k, v in iterable:
        d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)
## template
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
# RevealCustomTheme
```python
RevealCustomTheme(self, **kwargs)
```

## defaults
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
    d = {}
    for k, v in iterable:
        d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)
## fonts_base_url
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
# JinjaTemplateBuilder
```python
JinjaTemplateBuilder(self, page:'Page', **kwargs) -> None
```

## get_template_name
```python
JinjaTemplateBuilder.get_template_name(self)
```

Requires subclasses have either a "__template___" property or override this method

# MatplotlibFigure
```python
MatplotlibFigure(self, figure:'Figure', name:str, *args, **kwargs)
```

# OoxmlFileWidget
```python
OoxmlFileWidget(self, filename, name=None, endpoint_map=None, object_name=None, previous_ooxml_version={}, file_last_modified=None, document_ooxml_id=None, story_id=None, object_ooxml_id=None, **kwargs)
```

## update
```python
OoxmlFileWidget.update(self)
```

If the file is available locally, this renders that updated file and pushes
the updated rendering data to the server

# OoxmlEndpointMap
```python
OoxmlEndpointMap(self, endpoint, baseurl:str=None)
```

## BASE_URL
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## CHART
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## CONNECTION_SHAPE
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## DOCUMENT
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## GROUP
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## IMAGE
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## SHAPE
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## SHAPETREE
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## SLIDE
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## TABLE
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
## THEME
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
# StoryOutline
```python
StoryOutline(self, presalytics_story, info, pages, description, title, themes, plugins=None, **kwargs)
```

# Revealer
```python
Revealer(self, story_outline:'StoryOutline', **kwargs)
```

This class renders 'Story Outines' to reveal.js presentations

## render
```python
Revealer.render(self)
```

This method returns a t

# WidgetBase
```python
WidgetBase(self, name, *args, **kwargs) -> None
```

Inherit from this base class to create widget components that can be rendered to html via the
presalytics.story.revealer.Revealer class.  This component also need to build a method
that allows the widget to be serialzed into a presalytics.story.outline.Widget object.

Parameters:
----------
widget: Widget
    A presalytics.story.outline.Widget object use for initialized the component class.

Attributes:
----------
outline_widget: Widget
    A presalytics.story.outline.Widget object

css: List[str]
    A list of keys in dot notation that point to links in the ALLOWED_STYLES dictionary
    in the presalytics.lib.templates.base module.

js: List[str]
    A list of keys in dot notation that point to links in the ALLOWED_SCRIPTS dictionary
    in the presalytics.lib.templates.base module.

## to_html
```python
WidgetBase.to_html(self, data:Dict=None, **kwargs) -> str
```

Returns valid html that renders the widget in a broswer.

Parameters:
----------
data: Dict
    The data parameter is a dictionary should contain the minimum amount of that is required to
    successfully render the object.  As the widget is update, data control how the disply of
    information changes.
**kwargs:
    Optional keyword arguments can be used in subclass to modify the behavior of the to_html function.
    these keyword arguments should be geinvariant through successive updates to the chart.  For example,
    keycloak argument should control the styling of the widget, which should not change as the data in
    the object (e.g., a chart) is updated.  Keyword arguments are loaded via additional_properties
    parameter in in the presalytics.story.outline.Widget object.

Returns
----------
A string of containing an html fragment that will be loaded into a template in successive operations

## serialize
```python
WidgetBase.serialize(self, **kwargs) -> 'Widget'
```

Creates presalytics.story.outline.Widget object from instance data. This widget should
have the correct name, data and additional_properties so the same widget can be reconstituted
via the to_html method, given the same set of data.

Typically, this method will call an update method that run a local script with updates this
Widget's data Dictionary prior being loading into the Widget outline object for serialization.

Parameters:
----------
**kwargs:
    Optional keyword arguments can be used in subclass to modify the behavior of the to_html function.
    these keyword arguments should be be invariant through successive updates to the chart. Overrides
    for this widgets default additional_properties shoudl be loaded via these keyword argments.


## deserialize
```python
WidgetBase.deserialize(widget:'Widget', **kwargs) -> 'WidgetBase'
```

Creates an instance of the widget from the data object in the presalytics.story.outline.Widget
object. This method exists to ensure widgets can be portable across environments.  To clarify,
widgets built on the client-side via the __init__ method can be reconstructed server-side via
the deserialize method.  This allows decoupling of the widget generation/updating of data and
the rendering of the widget in a UI.  Renderers (e.g., presalytics.story.revealer.Revealer object)
need not know about how the data get updated, but can update the graphic with data generated by
the widget when the serialize method is called.

Parameters:
----------

widget: Widget
    A prealytics.story.outline.Widget object

Returns:
----------

An instance the widget class

# PageTemplateBase
```python
PageTemplateBase(self, page:'Page', **kwargs) -> None
```

Inherit from this base class to render templates to html via the
presalytics.story.revealer.Revealer class.

Parameters:
----------
page: Page
    A presalytics.story.outline.Page object for instalizing the class

Attributes:
----------
outline_page: Page
    A presalytics.story.outline.Page object

widgets: List[WidgetComponentBase]
    A list widget that will be loaded into templates and rendered via placeholders.
    These widgets must have a "to_html(self, data, **kwargs)" method.

css: List[str]
    A list of keys in dot notation that point to links in the ALLOWED_STYLES dictionary
    in the presalytics.lib.templates.base module.

js: List[str]
    A list of keys in dot notation that point to links in the ALLOWED_SCRIPTS dictionary
    in the presalytics.lib.templates.base module.

## render
```python
PageTemplateBase.render(self, **kwargs) -> str
```

Returns valid html that renders the template in a broswer with data loaded from widgets.

Parameters:
----------
widgets: Sequence[WidgetComponentBase]
    List of widget instances a one to many different class that inhereit from the WidgetComponentBase
    abstract class. Defaults tot he widget list that the class as initilazed with.

**kwargs:
    Optional keyword arguments can be used in subclass to modify the behavior of the to_html function.
    these keyword arguments should be geinvariant through successive updates to the chart.  For example,
    keycloak argument should control the styling of the widget, which should not change as the data in
    the object (e.g., a chart) is updated.  Keyword arguments are loaded via additional_properties
    parameter in in the presalytics.story.outline.Widget object.

Returns
----------
A string of containing an html fragment that will be loaded into a template in successive operations

## load_widget
```python
PageTemplateBase.load_widget(self, widget:'Widget')
```

Converts a presalytics.story.outline.Widget object to a subclass of WidgetComponentBase
via a presalytics.story.loaders.WidgetLoaderBase object.

## get_page_widgets
```python
PageTemplateBase.get_page_widgets(self, page:'Page')
```

Converts the widgets within a presaltytics.story.outline.Page object to a list
of widgets subclassed from WidgetComponentBase

# Renderer
```python
Renderer(self, **kwargs)
```

# ThemeBase
```python
ThemeBase(self, **kwargs)
```

Themes are containers for plugins should be rendered once
across the entire document.  The init method should configure
parameters with get passed to plugins via serialization and
deserialization.

# create_theme_from_ooxml_document
```python
create_theme_from_ooxml_document(document_id:str, client_info={})
```

# create_pages_from_ooxml_document
```python
create_pages_from_ooxml_document(story:'Story', ooxml_document:'Document', client_info={})
```

# create_story_from_ooxml_file
```python
create_story_from_ooxml_file(filename:str, client_info={}) -> 'Story'
```

# create_outline_from_ooxml_document
```python
create_outline_from_ooxml_document(story:'Story', ooxml_document:'Document', title:str=None, description:str=None, themes:Sequence[_ForwardRef('ThemeBase')]=None, client_info={})
```

# get_mime_type_from_filename
```python
get_mime_type_from_filename(client:presalytics.client.api.Client, filename) -> Union[str, NoneType]
```

# story_post_file_bytes
```python
story_post_file_bytes(client:'Client', binary_obj:'BytesIO', filename:str, mime_type:str=None)
```

# OoxmlEditorWidget
```python
OoxmlEditorWidget(self, name:str, story_id:str, object_ooxml_id:str, endpoint_id, transform_class=None, transform_params=None, **kwargs)
```

# XmlTransformBase
```python
XmlTransformBase(self, function_params:Dict, *args, **kwargs)
```

# ChangeShapeColor
```python
ChangeShapeColor(self, function_params:Dict, *args, **kwargs)
```

