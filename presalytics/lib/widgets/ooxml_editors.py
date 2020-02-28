import typing
import types
import logging
import json
import lxml
import lxml.etree
import abc
import re
import requests
import pystache
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
    Replaces text in an ooxml Element
    """
    __xml_transform_name__ = "ReplaceText"
    def transform_function(self, lxml_element, params):
        """
        Replaces the text inside 

        Parameters
        -----------
        lxml_element : lxml.etree.Element
            An element containing as least one an `<sp>` element

        params : dict
            See the `Function Parameters Dictionary` for required entries
        """
        text_list = lxml_element.findall('.//{*}t')
        for t in text_list:
            t.text = pystache.render(t.text, params)
        return lxml_element


class XmlTransformRegistry(presalytics.lib.registry.RegistryBase):
    """
    Registry for XmlTransform Classes
    """
    def __init__(self):
        include_paths = presalytics.COMPONENTS.autodiscover_paths
        super(XmlTransformRegistry, self).__init__(autodiscover_paths=include_paths)

    def get_name(self, klass):
        return getattr(klass, "__xml_transform_name__", None)

    def get_type(self, klass):
        return getattr(klass, "__xml_transform_kind__", None)


XML_TRANSFORM_REGISTRY = XmlTransformRegistry()


class MultiXmlTransform(XmlTransformBase):
    """
    This class allow users to run mutiple transforms on multiple targets in a single widget
    """
    transform_instances: typing.List[XmlTransformBase]

    __xml_transform_name__ = "MultiXmlTransform"

    def __init__(self, transforms: typing.Dict[str, typing.List[typing.Dict[str, typing.Any]]], fail_quietly=True, **kwargs):
        super(MultiXmlTransform, self).__init__(transforms, **kwargs)
        transforms_list = transforms.get("transforms_list", None)
        self.fail_quietly = fail_quietly
        self.transform_instances = []
        
        self.transform_registry = XML_TRANSFORM_REGISTRY
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
        self.svg_data = self.update()
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
        auth_header = client.get_auth_header()
        if self.transform:
            xml_url = self.endpoint_map.get_xml_url(self.object_ooxml_id)
            xml_response = requests.get(xml_url, headers=auth_header)
            if xml_response.status_code != 200:
                raise presalytics.lib.exceptions.ApiError(message=xml_response.text)
            dto = xml_response.json()
            new_xml = self.update_xml(dto["openOfficeXml"])
            dto["openOfficeXml"] = new_xml.decode('utf-8')
            xml_update_response = requests.put(xml_url, json=dto, headers=auth_header)
            if xml_response.status_code != 200:
                raise presalytics.lib.exceptions.ApiError(message=xml_update_response.content)
        svg_data = self.get_svg(self.object_ooxml_id)
        return svg_data

    @classmethod
    def deserialize(cls, component, **kwargs):
        endpoint_map = presalytics.lib.widgets.ooxml.OoxmlEndpointMap(component.data["endpoint_id"])
        class_key = "XmlTransform." + component.data.get("transform_class", "")
        transform_class = XML_TRANSFORM_REGISTRY.get(class_key)
        transform_params = component.data.get("transform_params", {})
        return cls(component.name,
                   component.data["story_id"],
                   component.data["object_ooxml_id"],
                   endpoint_map,
                   transform_class=transform_class,
                   transform_params=transform_params
                   )

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
