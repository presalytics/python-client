import typing
import types
import json
import lxml
import lxml.etree
import abc
import re
import requests
import presalytics
import presalytics.lib.widgets.ooxml


class XmlTransformBase(abc.ABC):
    def __init__(self, function_params: typing.Dict, *args, **kwargs):
        self.function_params = function_params

    @abc.abstractmethod
    def transform_function(self, lxml_element: lxml.etree.Element, params: typing.Dict) -> lxml.etree.Element:
        pass

    def execute(self, lxml_element: lxml.etree.Element):
        return self.transform_function(lxml_element, self.function_params)


class ChangeShapeColor(XmlTransformBase):
    @staticmethod
    def replace_color_on_target_shape(shape_xml: lxml.etree.Element, new_color: str) -> lxml.etree.Element:
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


class OoxmlEditorWidget(presalytics.lib.widgets.ooxml.OoxmlWidgetBase):
    transform: XmlTransformBase

    __component_kind__ = 'ooxml-xml-editor'

    def __init__(self,
                 name: str,
                 story_id: str,
                 object_ooxml_id: str,
                 endpoint_id,
                 transform_class=None,
                 transform_params=None,
                 **kwargs):
        super(OoxmlEditorWidget, self).__init__(**kwargs)    
        self.story_id = story_id
        self.object_ooxml_id = object_ooxml_id
        self.name = name
        self.endpoint_map = presalytics.lib.widgets.ooxml.OoxmlEndpointMap(endpoint_id)
        self.transform = transform_class(transform_params)
        self.svg_html = self.update()
        self.outline_widget = self.serialize()

    def update_xml(self, xml_str) -> str:
        xml = lxml.etree.fromstring(xml_str)
        new_xml = self.transform.execute(xml)
        new_xml_str = lxml.etree.tostring(new_xml)
        return new_xml_str

    def update(self):
        client = presalytics.client.api.Client(
            delegate_login=self.delegate_login,
            token=self.token,
            cache_tokens=self.cache_tokens
        )
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
    def deseriailize(cls, component, **kwargs):
        return cls(component.name,
                   component.data["story_id"],
                   component.data["object_ooxml_id"],
                   component.data["endpoint_id"]
                   )

    def serialize(self, **kwargs):
        data = {
            "story_id": self.story_id,
            "object_ooxml_id": self.object_ooxml_id,
            "endpoint_id": self.endpoint_map.endpoint_id
        }
        widget = presalytics.story.outline.Widget(
            name=self.name,
            data=data,
            kind=self.__component_kind__
        )
        return widget
