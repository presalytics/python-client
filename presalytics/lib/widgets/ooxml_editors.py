import typing
import marshal
import types
import lxml
import lxml.etree
import requests
import presalytics
import presalytics.lib.widgets.ooxml


def change_shape_color(xml: lxml.etree.Element, new_color_dict: typing.Dict):
    shapes = xml.findall('.//{*}sp')
    object_name = new_color_dict.get("object_name", None)
    color = new_color_dict.get("hex_color")
    new_fill = lxml.etree.Element("solidFill")
    lxml.etree.SubElement(new_fill, "srbgClr", {"val": color})
    fill_tags = [
        'noFill'
    ]
    if object_name:
        for shape in shapes:
            is_target = False
            nvprops = next(x for x in shapes if x.tag == "nvSpPr")
            if nvprops:
                name = nvprops.get("name")
                if name == object_name:
                    is_target = True
            if is_target:
                props = next(x for x in shapes if x.tag == "spPr")
                for child in props.iter():
                    if child.tag in fill_tags:
                        child.getparent().remove(child)
                props.SubElement(new_fill)
    else:
        for shape in shapes:
            props = next(x for x in shapes if x.tag == "spPr")
            for child in props.iter():
                if child.tag in fill_tags:
                    child.getparent().remove(child)
            props.SubElement(new_fill)


class OoxmlEditorWidget(presalytics.lib.widgets.ooxml.OoxmlWidgetBase):
    transform_function: typing.Callable[['OoxmlEditorWidget', lxml.etree.Element, typing.Dict], lxml.etree.Element]
   
    __component_kind__ = 'ooxml-xml-editor'

    def __init__(self,
                 name: str,
                 story_id: str,
                 ooxml_document_id: str,
                 endpoint_id,
                 transform_function=None,
                 transform_params=None,
                 **kwargs):
        self.story_id = story_id
        self.ooxml_id = ooxml_document_id
        self.name = name
        self.endpoint_map = presalytics.lib.widgets.ooxml.OoxmlEndpointMap(endpoint_id)
        # bind to current instance
        self.transform_function = types.MethodType(transform_function, self)
        self.transform_params = transform_params
        self.svg_html = self.update()
        self.outline_widget = self.serialize()

    def update_xml(self, xml_str) -> str:
        xml = lxml.etree.fromstring(xml_str)
        new_xml = self.transform_function(xml, self.transform_params)
        new_xml_str = lxml.etree.tostring(new_xml)
        return new_xml_str

    def update(self):
        client = presalytics.client.api.Client()
        auth_header = client.get_auth_header()
        xml_url = self.endpoint_map.get_xml_url(self.ooxml_id)
        xml_response = requests.get(xml_url, headers=auth_header)
        if xml_response.status_code != 200:
            raise presalytics.lib.exceptions.ApiException(default_exception=xml_response.content)
        new_xml = self.update_xml(xml_response.text)
        put_data = {
            "id": self.ooxml_id,
            "openOfficeXml": new_xml,
            "type": self.endpoint_map.endpoint_id

        }
        xml_update_response = requests.put(xml_url, put_data, headers=auth_header)
        if xml_response.status_code != 200:
            raise presalytics.lib.exceptions.ApiException(default_exception=xml_update_response.content)
        svg_data = self.get_svg(id)
        return svg_data

    @classmethod
    def deseriailize(cls, component, **kwargs):
        function_bytes = component.data["transform_function"]
        func = marshal.loads(function_bytes)
        return cls(component.name,
                   component.data["story_id"],
                   component.data["ooxml_document_id"],
                   component.data["endpoint_id"],
        )

    def serialize(self, **kwargs):
        data = {
            "story_id": self.story_id,
            "ooxml_id": self.ooxml_id,
            "endpoint_id": self.endpoint_map.endpoint_id
        }
        widget = presalytics.story.outline.Widget(
            name=self.name,
            data=data,
            kind=self.__component_kind__
        )
        return widget

