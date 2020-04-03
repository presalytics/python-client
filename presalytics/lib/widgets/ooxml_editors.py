import typing
import types
import logging
import json
import lxml
import lxml.etree
import abc
import re
import requests
import collections
import presalytics
import presalytics.lib.registry
import presalytics.lib.exceptions
import presalytics.lib.widgets.ooxml


logger = logging.getLogger(__name__)


class XmlTransformBase(abc.ABC):
    """
    Base class for writing Open Office Xml tranform functions to be implemented
    by `presalytics.lib.widgets.ooxml_editors.OoxmlEditorWidget`
    
    *For more information about Open Office Xml Schema that underlies 
    .pptx and .xlsx files, see http://officeopenxml.com/

    *For more information on how to lxml to write transforms, consult https://lxml.de/

    Parameters
    ----------
    function_params : dict
        A dictionary containing variables that will be used when the `transform_function`
        is executed
    """
    __xml_transform_kind__ = 'XmlTransform'

    def __init__(self, function_params: typing.Dict, *args, **kwargs):
        self.function_params = function_params

    @abc.abstractmethod
    def transform_function(self, lxml_element: lxml.etree.Element, params: typing.Dict) -> lxml.etree.Element:
        """
        Modifies Open Office Xml via transforming `lxml.etree.Element` using a params `dict` containing
        variables. Must be overridden in subclasses.
        """
        pass
    

    def execute(self, lxml_element: lxml.etree.Element):
        """
        Called by widget classes (e.g., `presalytics.lib.widgets.ooxml_editors.OoxmlEditorWidget`) to 
        perform the updates prescribed in the `transform_function`
        """
        return self.transform_function(lxml_element, self.function_params)


class ChangeShapeColor(XmlTransformBase):
    """
    Changes the color of a set of [Open Office Xml Shapes](http://officeopenxml.com/drwShape.php)
    
    Function Parameters Dictionary
    ----------
    hex_color : str
        The six-digit hexadecimal-format color string (e.g., ffa500 for orange).  See
        https://www.color-hex.com/ for an example color calculator

    object_name : str, optional
        The object tree name of the target shape.  If not supplied, all descendent shapes will
        have their color changed.      
    """
    __xml_transform_name__ = "ChangeShapeColor"

    @staticmethod
    def replace_color_on_target_shape(shape_xml: lxml.etree.Element, new_color: str) -> lxml.etree.Element:
        """
        Changes the color of an [Open Office Xml Shape](http://officeopenxml.com/drwShape.php)
        """
        new_fill = lxml.etree.Element("solidFill")
        lxml.etree.SubElement(new_fill, "srbgClr", {"val": new_color})
        fill_tags = [
            'noFill',
            'blipFill',
            'gradFill',
            'pattFill',
            'solidFill'
        ]
        props = shape_xml.find('.//{*}spPr')
        for child in props.getchildren():
            if any(re.search('{*}' + r, child.tag) for r in fill_tags):
                current_nsmap = child.nsmap
                current_index = props.index(child)
                current_prefix = child.prefix
                current_ns = current_nsmap.get(current_prefix, None)
                new_fill = lxml.etree.Element(lxml.etree.QName(current_ns, "solidFill"), nsmap=current_nsmap)
                lxml.etree.SubElement(new_fill, lxml.etree.QName(current_ns, "srgbClr"), {"val": new_color}, nsmap=current_nsmap)
                child.getparent().remove(child)
                props.insert(current_index, new_fill)
        return shape_xml

    def transform_function(self, lxml_element, params):
        """
        Changes the color of an [Open Office Xml Shape](http://officeopenxml.com/drwShape.php)

        Parameters
        -----------
        lxml_element : lxml.etree.Element
            An element containing as least one an `<sp>` element

        params : dict
            See the `Function Parameters Dictionary` for required entries
        """
        
        if re.match('{.*}sp', lxml_element.tag):
            shapes = [lxml_element]
        else:
            shapes = lxml_element.findall('.//{*}sp')
        object_name = params.get("object_name", None)
        color = params.get("hex_color")
        if object_name:
            for shape in shapes:
                is_target = False
                nvprops = shape.find('.//{*}nvSpPr')
                if len(nvprops) > 0:
                    name = nvprops.find('.//*[@name]').get("name")
                    if name == object_name:
                        is_target = True
                if is_target:
                    shape = ChangeShapeColor.replace_color_on_target_shape(shape, color)
        else:
            for shape in shapes:
                shape = ChangeShapeColor.replace_color_on_target_shape(shape, color)
        return lxml_element

class TextReplace(XmlTransformBase):
    """
    Replaces text in a template built into an Office Office Xml object that has 
    been uploaded to the Presalytics Ooxml Automation service.  Text to be should
    be in the format of a "template tag", which is a string enclosed in handlebars
    as such: '{{template_tag}}'

    Function Parameters Dictionary
    ----------

    A dictionary that maps template tags to the new strings that will replace the
    tags in the rendered widget.  The the dictionary keys should not be enclosed in handlebars.
    """
    __xml_transform_name__ = "TextReplace"

    class TextElementInfo(object):
        """
        Holds metadata for a list of `<t>` tags from an Office Open Xml document. 
        """
        def __init__(self, element: lxml.etree.Element, start_position: int):
            self.element = element
            self.text = "" if not element.text else element.text
            self.length = len(self.text)
            self.start_position = start_position
            self.end_position = self.start_position + self.length - 1

    class TextList(object):
        """
        Class for managing a list of `TextElementInfo` objects
        """
        _list: typing.List['TextReplace.TextElementInfo']

        def __init__(self):
            self._list = []

        def append(self, text_element_info):
            if isinstance(text_element_info, globals()['TextReplace'].TextElementInfo):
                self._list.append(text_element_info)
            else:
                raise presalytics.lib.exceptions.InvalidArgumentException(message="Argument must be an instance of class 'TextElementInfo'")
        
        def set_text(self, index, new_string):
            self._list[index].text = new_string
            self._list[index].element.text = new_string

        def get_text(self, index):
            return self._list[index].text

        def get_plaintext_string(self):
            ret = ""
            for item in self._list:
                ret += item.text
            return ret

        def get_position(self, match_string):
            return self.get_plaintext_string().find(match_string)

        def get_list_index_of_position(self, position: int):
            for item in self._list:
                if item.start_position <= position and item.end_position >= position:
                    return self.get_index(item)
            raise presalytics.lib.exceptions.InvalidArgumentException(message="Position {} out of range".format(position))
        
        def get_index(self, text_element_info: 'TextReplace.TextElementInfo'):
            for i in range(len(self._list)):
                if self._list[i] == text_element_info:
                    return i
            raise presalytics.lib.exceptions.InvalidArgumentException(message="Supplied argument on in self._list")
        
        def set_text_to_empty_string(self, index):
            self._list[index].text = ""
            self._list[index].element.text = ""

        def set_start_to_new_value(self, index, new_value):
            start_text, remainder = self._list[index].text.split("{{", 1)
            end = ""
            if "}}" in remainder:
                end = remainder.split("}}", 1)[1]
            new_text = "{0}{1}{2}".format(start_text, new_value, end)
            self._list[index].text = new_text
            self._list[index].element.text = new_text

        def truncate_end(self, index):
            end_text = self._list[index].text.split("}}", 1)[-1]
            self._list[index].text = end_text
            self._list[index].element.text = end_text

        def plaintext_string_list(self):
            return [x.text for x in self._list]

        def reset(self):
            for i in range(0, len(self._list)):
                start_position = 0 if i == 0 else self._list[i-1].end_position + 1
                self._list[i] = TextReplace.TextElementInfo(self._list[i].element, start_position)


            
    def replace_handlebars(self, info_list, params):
        """
        Method that finds template tags and replaces them 
        """
        for key, val in params.items():
            match_key = "{{" + key + "}}"
            match_start_position =  info_list.get_position(match_key)
            if match_start_position > -1:
                match_end_position = match_start_position + len(match_key) - 1
                match_start_index = info_list.get_list_index_of_position(match_start_position)
                match_end_index = info_list.get_list_index_of_position(match_end_position)
                if match_start_index < match_end_index:
                    info_list.truncate_end(match_end_index)
                for i in range(match_start_index + 1, match_end_index):
                    info_list.set_text_to_empty_string(i)
                info_list.set_start_to_new_value(match_start_index, val)
                info_list.reset()
                self.replace_handlebars(info_list, params)


    def transform_function(self, lxml_element, params):
        """
        Replaces template tags located {{inside_handlebars}} that match keys in the
        `params` dict with values from the `params` dict. 

        This method searches for match for plain text strings, so that if template
        tags are split across xml `<t>` elements, they are still identified and replaced. 

        Parameters
        -----------
        lxml_element : lxml.etree.Element
            An element containing as least one an `<t>` element

        params : dict
            A dictionary that maps template tags (no handlebars) to their respective
            replacement values.
        """
        text_list = lxml_element.findall('.//{*}t')
        info_list = TextReplace.TextList()
        position = 0
        for tag in text_list:
            info = self.TextElementInfo(tag, position)
            position = info.end_position + 1
            info_list.append(info)
        self.replace_handlebars(info_list, params)
        return lxml_element


class XmlTransformRegistry(presalytics.lib.registry.RegistryBase):
    """
    Registry for XmlTransform Classes.  Read by `presalytics.lib.widgets.ooxml_editors.MultiXmlTransform`
    and `presalytics.lib.widgets.ooxml_editors.OoxmlEditorWidget` so XmlTransformBase subclasses
    can be deserialized at run-time without a loaded instance in `locals()`.
    """
    def __init__(self):
        include_paths = presalytics.COMPONENTS.autodiscover_paths # todo: Change this line -does not exist at timport time.
        reserved_names = presalytics.COMPONENTS.reserved_names
        super(XmlTransformRegistry, self).__init__(autodiscover_paths=include_paths, reserved_names=reserved_names)

    def get_name(self, klass):
        return getattr(klass, "__xml_transform_name__", None)

    def get_type(self, klass):
        return getattr(klass, "__xml_transform_kind__", None)


XML_TRANSFORM_REGISTRY = None
"""
Static instance of `presalytics.lib.widgets.ooxml_editors.XmlTransformRegistry`. 

Should not be used directly by consuming classes. Only initialized if a consuming 
class or method calls the `presalytics.lib.widgets.ooxml_editors.get_transform_registry`.  This is done
for performance reasons since there's no need to build this registry at import-time if its never 
used in a workspace.
"""

def get_transform_registry():
    """
    Initalizes and retreives `presalytics.lib.widgets.ooxml_editors.XML_TRANSFORM_REGISTRY`
    """
    global XML_TRANSFORM_REGISTRY
    if not XML_TRANSFORM_REGISTRY:
        XML_TRANSFORM_REGISTRY = XmlTransformRegistry()
    return XML_TRANSFORM_REGISTRY



class MultiXmlTransform(XmlTransformBase):
    """
    This class allow users to run mutiple transforms on multiple targets in a single widget.  `MultiXmlTransform`
    wraps multiple subclasses of `presalytics.lib.widgets.ooxml_editors.XmlTransformBase`, creates instances of
    them, and feeds them into an `presalytics.lib.widgets.ooxml_editors.OoxmlEditorWidget` instance.  To do this,
    the `presalytics.lib.widgets.ooxml_editors.XmlTransformBase` subclasses must be loaded into the 
    `presalytics.lib.widgets.ooxml_editors.XML_TRANSFORM_REGISTRY` when called.

    The function parameters for the 

    Parameters
    ----------
    fail_quietly: bool, optional
        Defaults to false.  Indicates whether an exception should be raised when a subclass specified
        in the function parameters cannot not be found in the `presalytics.lib.widgets.ooxml_editors.XML_TRANSFORM_REGISTRY`
        instance. 
        

    Function Parameters Dictionary
    ----------
    transforms_list: list of dict
        A list of dictionaries, with each item in the list consiting of a dictionary of two entries.  
        The entries are as follows:
         
         * name: [str]
            The name of the the subclass of `presalytics.lib.widgets.ooxml_editors.XmlTransformBase` that
            will be that will be initialized
         
         * function_params: [dict]
            The `params` that will be the loaded into the instance's `transform_function` 
    """
    transform_instances: typing.List[XmlTransformBase]

    __xml_transform_name__ = "MultiXmlTransform"

    def __init__(self, transforms: typing.Dict[str, typing.List[typing.Dict[str, typing.Any]]], fail_quietly=True, **kwargs):
        super(MultiXmlTransform, self).__init__(transforms, **kwargs)
        transforms_list = transforms.get("transforms_list", None)
        self.fail_quietly = fail_quietly
        self.transform_instances = []
        self.transform_registry = get_transform_registry()
        for _transform in transforms_list: #type: ignore
            key = "XmlTransform." + _transform["name"]
            transform_class = self.transform_registry.get(key)
            if not transform_class:
                message = "Could not find XmlTransform with name '{}'".format(_transform["name"])
                if self.fail_quietly:
                    logging.info(message)
                else:
                    raise self.transform_registry.raise_error(message) #noqa
            else:
                inst = transform_class(_transform["function_params"])
                self.transform_instances.append(inst)

    def transform_function(self, lxml_element, params):
        for inst in self.transform_instances:
            lxml_element = inst.execute(lxml_element)
        return lxml_element    


class OoxmlEditorWidget(presalytics.lib.widgets.ooxml.OoxmlWidgetBase):
    """
    Edits a `widget` from a Presentation or Spreadsheet document and renders 
    the edited widget.

    This class interacts with the Presalytics API to extract SVG objects from
    Presentation and spreadsheet documents, from Presaltytics Ooxml Automation
    service objects that have already been loaded into the API.  This class requires
    that users supply `transform_function` by subclassing 
    `presalytics.lib.widgets.ooxml_editors.XmlTransformBase`, and an optional set of 
    parameters to act as variables in the transform function.

    Parameters
    ----------
    filename : str
        The local filepath a presentation or spreadsheet file containing
        the object to be rendered

    name : str
        The widget name.  If not provided, attribute will be set as the `object_name` 
        or `filename`

    story_id : str
        The the id of the story in the Presalytics API Story service.  If not provided, 
        a new story will be created.  Do not supply if this object has not yet been created. 
    
    object_ooxml_id : str
        The identifier of the Ooxml Automation service object bound the Story. Do not supply if this 
        object has not yet been created.

    endpoint_map : presalytics.lib.widgets.ooxml.OoxmlEndpointMap
        Reference to the Presalytics API Ooxml Automation service endpoint and object type
        that for the object of interest

    tranform_class : subclass of presalytics.lib.widgets.ooxml_editors.XmlTransformBase
        A class containing a `transform_function` method that transforms Open Office Xml via
        an `lxml.etree.Element` instance

    transform_params : dict, optional
        A dictionary of parameters that will be passed to the `transform_class`'s `transform_function`
        as variables to modify the underlying OpenOfficeXml 
    
    """
    transform: XmlTransformBase

    __component_kind__ = 'ooxml-xml-editor'

    def __init__(self,
                 name: str,
                 story_id,
                 object_ooxml_id,
                 endpoint_map,
                 transform_class,
                 transform_params={},
                 **kwargs):
        super(OoxmlEditorWidget, self).__init__(name, story_id=story_id, object_ooxml_id=object_ooxml_id, endpoint_map=endpoint_map, **kwargs)
        self.name = name
        self.transform = transform_class(transform_params)
        self.update()
        self.svg_html = self.create_container(**self.client_info)
        self.outline_widget = self.serialize()

    def update_xml(self, xml_str) -> str:
        """
        Runs the `transform_function` Open Office Xml data downloaded via the Presalytics API
        """
        xml = lxml.etree.fromstring(xml_str)
        new_xml = self.transform.execute(xml)
        new_xml_str = lxml.etree.tostring(new_xml)
        return new_xml_str

    def update(self):
        """
        Update the widget, include changes to the Xml
        """
        client = self.get_client()
        headers = client.get_auth_header()
        headers.update(client.get_request_id_header())
        if self.transform:
            xml_url = self.endpoint_map.get_xml_url(self.object_ooxml_id)
            xml_response = requests.get(xml_url + "?updated=false", headers=headers)
            if xml_response.status_code != 200:
                raise presalytics.lib.exceptions.ApiError(message=xml_response.text)
            dto = xml_response.json()
            new_xml = self.update_xml(dto["openOfficeXml"])
            dto["openOfficeXml"] = new_xml.decode('utf-8')
            xml_update_response = requests.put(xml_url, json=dto, headers=headers)
            if xml_response.status_code != 200:
                raise presalytics.lib.exceptions.ApiError(message=xml_update_response.content)

    @classmethod
    def deserialize(cls, component, **kwargs):
        endpoint_map = presalytics.lib.widgets.ooxml.OoxmlEndpointMap(component.data["endpoint_id"])
        class_key = "XmlTransform." + component.data.get("transform_class", "")
        transform_class = get_transform_registry().get(class_key)
        transform_params = component.data.get("transform_params", {})
        return cls(component.name,
                   component.data["story_id"],
                   component.data["object_ooxml_id"],
                   endpoint_map,
                   transform_class=transform_class,
                   transform_params=transform_params,
                   **kwargs)

    def serialize(self, **kwargs):
        data = {
            "story_id": self.story_id,
            "object_ooxml_id": self.object_ooxml_id,
            "endpoint_id": self.endpoint_map.endpoint_id,
            "transform_class": self.transform.__xml_transform_name__,
            "transform_params": self.transform.function_params
        }
        widget = presalytics.story.outline.Widget(
            name=self.name,
            data=data,
            kind=self.__component_kind__
        )
        return widget
