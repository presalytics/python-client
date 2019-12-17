import typing
import time
import urllib.parse
import requests
import os
import datetime
import dateutil.parser
import presalytics
import presalytics.client.api
import presalytics.story.components
import presalytics.client
import presalytics.lib.exceptions
import presalytics.story.outline
import presalytics.lib.util


class OoxmlEndpointMap(object):
    BASE_URL = "https://api.presalytics.io/ooxml-automation"

    CHART = "Charts"
    CONNECTION_SHAPE = "ConnectionShapes"
    DOCUMENT = "Documents"
    GROUP = "Groups"
    IMAGE = "Images"
    SHAPE = "Shapes"
    SHAPETREE = "ShapeTrees"
    SLIDE = "Slides"
    TABLE = "Tables"
    THEME = "Themes"

    def __init__(self, endpoint, baseurl: str = None):
        if endpoint not in OoxmlEndpointMap.__dict__.values():
            raise presalytics.lib.exceptions.ValidationError("{0} is not a valid endpoint ID".format(endpoint))
        self.endpoint_id = endpoint
        if not baseurl:
            custom_hosts = presalytics.CONFIG.get("HOSTS", None)
            if custom_hosts:
                ooxml_host = custom_hosts.get("OOXML_AUTOMATION", None)
                if ooxml_host:
                    self.baseurl = ooxml_host
            if not self.baseurl:
                self.baseurl = OoxmlEndpointMap.BASE_URL
        else:
            self.baseurl = baseurl
        self.root_url = urllib.parse.urljoin(self.baseurl, self.endpoint_id)

    def get_id_url(self, id):
        return os.path.join(self.root_url, id)

    def get_svg_url(self, id):
        return os.path.join(self.root_url, "Svg", id)
    
    def get_xml_url(self, id):
        return os.path.join(self.root_url, "OpenOfficeXml" + id)


class OoxmlWidgetBase(presalytics.story.components.WidgetBase):
    endpoint_map: OoxmlEndpointMap
    data: typing.Dict

    __plugins__ = [
        {
            'name': 'external_scripts',
            'kind': 'script',
            'config': {
                'approved_scripts_key': 'ooxml'
            }
        }
    ]

    def to_html(self, **kwargs):
        return self.svg_html

    def get_svg(self, id, timeout_iterator=0) -> str:
        svg_url = self.endpoint_map.get_svg_url(id)
        client = presalytics.client.api.Client()
        auth_header = client.get_auth_header()
        response = requests.get(svg_url, headers=auth_header)
        svg_data = response.text
        if response.status_code != 200:
            raise presalytics.lib.exceptions.ApiException(default_exception=response.content)
        if response.text.startswith("Temp data"):
            if timeout_iterator > 5:
                raise presalytics.lib.exceptions.ApiException()
            else:
                time.sleep(2)
                svg_data = self.get_svg(id, timeout_iterator)
        return svg_data


class OoxmlEditorWidget(OoxmlWidgetBase):
    __component_kind__ = 'ooxml-xml-editor'

    def __init__(self, name: str, story_id: str, ooxml_id: str, endpoint_map, data):
        self.story_id = story_id
        self.ooxml_id = ooxml_id
        self.name = name
        self.endpoint_map = endpoint_map
        self.svg_html = self.update(data)
        self.outline_widget = self.serialize()

    def update(self, data: typing.Dict) -> str:
        client = presalytics.client.api.Client()
        auth_header = client.get_auth_header()
        xml_url = self.endpoint_map.get_xml_url(self.ooxml_id)
        xml_response = requests.get(xml_url, headers=auth_header)
        if xml_response.status_code != 200:
            raise presalytics.lib.exceptions.ApiException(default_exception=xml_response.content)
        new_xml = self.update_xml(xml_response.text, data)
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
        return cls(component.name,
                   component.data["story_id"],
                   component.data["ooxml_id"],
                   component.data["endpoint_id"])

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

    def update_xml(self, old_xml: str, data: typing.Dict):
        raise NotImplementedError


class OoxmlFileWidget(OoxmlWidgetBase):
    object_name: typing.Optional[str]
    ooxml_id: str
    file_last_modified: datetime.datetime
    previous_versions: typing.Dict[str, str]

    __component_kind__ = 'ooxml-file-object'

    def __init__(self,
                 filename,
                 name=None,
                 endpoint_map=None,
                 object_name=None,
                 previous_ooxml_version={},
                 file_last_modified=None,
                 document_ooxml_id=None,
                 object_ooxml_id=None):
        self.filename = filename
        if endpoint_map:
            self.endpoint_map = endpoint_map
        else:
            if filename.split(".")[-1] in ["pptx", "ppt"]:
                self.endpoint_map = OoxmlEndpointMap(OoxmlEndpointMap.SLIDE)
        if object_name:
            self.object_name = object_name
        else:
            self.object_name = None
        if name:
            self.name = name
        else:
            if self.object_name:
                self.name = self.object_name
            else:
                self.name = filename
        self.prevision_ooxml_version = previous_ooxml_version
        self.file_last_modified = file_last_modified
        self.document_ooxml_id = document_ooxml_id
        self.object_ooxml_id = object_ooxml_id
        self.update()
        self.svg_html = self.get_svg(self.object_ooxml_id)

    def update(self):
        # if the file exists locally and has been modified or is new, update attributes ooxml_object_id and ooxml_document_id (i.e., reupload) -store data in prevision version
        search_paths = presalytics.autodiscover_paths
        search_paths.append(os.getcwd())
        for path in search_paths:
            if os.path.exists(self.filename):
                # update only the file has been modified sine last time
                this_file_last_modified = datetime.datetime.utcfromtimestamp(os.path.getmtime(self.filename))
                if self.file_last_modified is None or self.file_last_modified <= this_file_last_modified:
                    client = presalytics.client.api.Client()
                    document, status, headers = client.ooxml_automation.documents_post(filename)
                    if status >= 299:
                        raise presalytics.lib.exceptions.ApiError()
                    self.document_ooxml_id = document.id
                    # Get object tree, compare to object name
                    child_tree = client.ooxml_automation.documents_childobjects_get_id(self.document_ooxml_id)
                    target_dto = None

                    try:
                        target_dto = next(x for x in child_tree if x.name == self.object_name)
                    except StopIteration:
                        pass
                    # if name not in object or _object_name is none, get first item of type in end_point id
                    if not target_dto:
                        try:
                            target_dto = next(x for x in child_tree if x.type == self.endpoint_map.endpoint_id)
                        except StopIteration:
                            message = "Child tree of document {0} does not have a child object of type {1} or name {2}.".format(self.ooxml_id, self.endpoint_map.endpoint_id, self.object_name)
                            raise presalytics.lib.exceptions.InvalidConfigurationError(message)
                    # set widget parameters for recreation server-side (without file)
                    self.object_ooxml_id = target_dto.id
                    self.file_last_modified = presalytics.lib.util.roundup_date_modified(this_file_last_modified)

    @classmethod
    def deserialize(cls, component, **kwargs):
        init_args = {
            "filename": component.data["filename"],
            "endpoint_map": OoxmlEndpointMap(component.data["endpoint_id"]),
            "object_name": component.data["object_name"],
            "name": component.name
        }
        if "document_ooxml_id" in component.data:
            init_args.update(
                {
                    "document_ooxml_id": component.data["document_ooxml_id"]
                }
            )
            if "object_ooxml_id" in component.data:
                init_args.update(
                    {
                        "object_ooxml_id": component.data["object_ooxml_id"]
                    }
                )
            if "file_last_modified" in component.data:
                init_args.update(
                    {
                        "file_last_modified": dateutil.parser.parse(component.data["file_last_modified"])
                    }
                )
            if "previous_ooxml_version" in component.data:
                init_args.update(
                    {
                        "prevision_ooxml_version": component.data["previous_ooxml_version"]
                    }
                )
            return cls(**init_args)

    def serialize(self, **kwargs):
        self.update()
        data = {
            "filename": self.filename,
            "object_name": self.object_name,
            "endpoint_id": self.endpoint_map.endpoint_id,
            "document_ooxml_id": self.document_ooxml_id,
            "object_ooxml_id": self.object_ooxml_id
        }
        if self.file_last_modified:
            data.append(
                {
                    "file_last_modified": self.file_last_modifed.isoformat()
                }
            )
        widget = presalytics.story.outline.Widget(
            name=self.name,
            kind=self.__component_kind__,
            data=data,
            plugins=None
        )
        return widget
