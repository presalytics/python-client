import typing
import time
import urllib.parse
import requests
import os
import datetime
import dateutil.parser
import lxml
import lxml.etree
import posixpath
import presalytics
import presalytics.client.api
import presalytics.story.components
import presalytics.client
import presalytics.lib.exceptions
import presalytics.story.outline
import presalytics.lib.util
import presalytics.lib.plugins.ooxml
if typing.TYPE_CHECKING:
    from presalytics.story.outline import StoryOutline, Page, Widget
    from presalytics.client.presalytics_story import Story as ApiStory


class OoxmlEndpointMap(object):
    """
    Mapping class that bridges Presalytics API Ooxml Automation service endpoints
    and component class that consume those endpoints (typically subclasses of 
    `presalytics.lib.widgets.ooxml.OoxmlWidgetBase`)

    The classmethods on this class are conveninece methods to help users 
    quickly inform their widget which endpoint their of a Ooxml Document their
    targets.

    Instance methods on this class are used by widget to generate urls and 
    lookup against object tree for target objects.

    Parameters
    ----------
    endpoint_id : str
        A unique string for identifying the object_type related to the enpoint
    
    baseurl : str
        For developer use. Allows this to generate urls for non-standard instances
        of the Ooxml Automation service.  Defaults to https://api.presalytics.io/ooxml-automation/

    Attributes
    ----------
    root_url : str
        the home url for the class instance.  Typically `http://api.presalytics.io/ooxml-automation/{object_type}`
    
    OBJECT_TYPE_MAP : str
        A mapping table for object_types and object tree lookup keys
    """
    _BASE_URL = "https://api.presalytics.io/ooxml-automation"
    _CHART = "Charts"
    _CONNECTION_SHAPE = "ConnectionShapes"
    _DOCUMENT = "Documents"
    _GROUP = "Groups"
    _IMAGE = "Images"
    _SHAPE = "Shapes"
    _SHAPETREE = "ShapeTrees"
    _SLIDE = "Slides"
    _TABLE = "Tables"
    _THEME = "Themes"

    def __init__(self, endpoint_id, baseurl: str = None):
        if endpoint_id not in OoxmlEndpointMap.__dict__.values():
            raise presalytics.lib.exceptions.ValidationError("{0} is not a valid endpoint ID".format(endpoint_id))
        self.endpoint_id = endpoint_id
        if not baseurl:
            self.baseurl = OoxmlEndpointMap._BASE_URL
            custom_hosts = presalytics.CONFIG.get("HOSTS", None)
            if custom_hosts:
                ooxml_host = custom_hosts.get("OOXML_AUTOMATION", None)
                if ooxml_host:
                    self.baseurl = ooxml_host
                
        else:
            self.baseurl = baseurl
        self.root_url = posixpath.join(self.baseurl, self.endpoint_id)
        self.OBJECT_TYPE_MAP = self._build_object_type_map()
    


    def _build_object_type_map(self):
        return {
            "Chart": [
                OoxmlEndpointMap._CHART,
            ],
            "Slide": [
                OoxmlEndpointMap._GROUP,
                OoxmlEndpointMap._SHAPE,
                OoxmlEndpointMap._SHAPETREE, 
                OoxmlEndpointMap._CONNECTION_SHAPE,
                OoxmlEndpointMap._SLIDE
            ],
            "Table": [
                OoxmlEndpointMap._TABLE
            ],
            "Theme": [
                OoxmlEndpointMap._THEME
            ],
            "Shared": [
                OoxmlEndpointMap._IMAGE
            ],
            "EMPTY": [
                OoxmlEndpointMap._DOCUMENT
            ]
        }
    
    def get_object_type(self):
        """
        Returns the Ooxml Automation service object type for this endpoint
        """
        for key, val in self.OBJECT_TYPE_MAP.items():
            for test_ep in val:
                if test_ep == self.endpoint_id:
                    if key == "EMPTY":
                        return self.endpoint_id
                    else:
                        return "{0}.{1}".format(key, self.endpoint_id)
        message = "Invalid EndpointMap configuration: {0} is not in OBJECT_TYPE_MAP".format(self.endpoint_id)
        raise presalytics.lib.exceptions.ValidationError(message)

    def get_id_url(self, id):
        """
        Returns a url to pull metadata from this Ooxml Automation service endpoint
        """
        return posixpath.join(self.root_url, id)

    def get_svg_url(self, id):
        """
        Returns a url to download an svg from this Ooxml Automation service endpoint
        """
        return posixpath.join(self.root_url, "Svg", id)

    def get_xml_url(self, id):
        """
        Returns a url to pull the Open Office Xml from this Ooxml Automation service endpoint
        """
        return posixpath.join(self.root_url, "OpenOfficeXml", id)

    @classmethod
    def connection_shape(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting ConnectionShape objects
        """
        return cls(OoxmlEndpointMap._CONNECTION_SHAPE, baseurl)

    @classmethod
    def chart(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting Chart objects
        """
        return cls(OoxmlEndpointMap._CHART, baseurl)

    @classmethod
    def document(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting Document objects
        """
        return cls(OoxmlEndpointMap._DOCUMENT, baseurl)
    
    @classmethod
    def group(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting Group objects
        """
        return cls(OoxmlEndpointMap._GROUP, baseurl)

    @classmethod
    def image(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting Image objects
        """
        return cls(OoxmlEndpointMap._IMAGE, baseurl)

    @classmethod
    def shape(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting Shape objects
        """
        return cls(OoxmlEndpointMap._SHAPE, baseurl)

    @classmethod
    def shapetree(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting ShapeTree objects
        """
        return cls(OoxmlEndpointMap._SHAPETREE, baseurl)

    @classmethod
    def slide(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting Slide objects
        """
        return cls(OoxmlEndpointMap._SLIDE, baseurl)

    @classmethod
    def table(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting Table objects
        """
        return cls(OoxmlEndpointMap._TABLE, baseurl)

    @classmethod
    def theme(cls, baseurl=None):
        """
        Factory method to create an `presalytics.lib.widgets.ooxml.OoxmlEndpointMap` instance
        targeting Theme objects
        """
        return cls(OoxmlEndpointMap._THEME, baseurl)


class OoxmlWidgetBase(presalytics.story.components.WidgetBase):
    """
    Base class for creating widgets from objects at endpoints in the 
    Presalytics API Ooxml Automation service.

    Parameters
    ----------
    name : str, optional
        The widget name.  If not provided, will be the `object_name` or `filename`

    story_id : str, optional
        The the id of the story in the Presalytics API Story service.  If not provided, 
        a new story will be created.  Do not supply if this object has not yet been created. 
    
    object_ooxml_id : str, optional
        The identifier of the Ooxml Automation service object bound the Story. Do not supply if this 
        object has not yet been created.

    endpoint_map : presalytics.lib.widgets.ooxml.OoxmlEndpointMap, optional
        Reference to the Presalytics API Ooxml Automation service endpoint and object type
        that for the object of interest

    Attributes
    ----------
    svg_html : str
        An html fragment containing the svg data
    """
    endpoint_map: OoxmlEndpointMap
    data: typing.Dict

    __plugins__ = [
        {
            'name': 'external_scripts',
            'kind': 'script',
            'config': {
                'approved_scripts_key': 'jquery'
            }
        },
        {
            'name': 'external_scripts',
            'kind': 'script',
            'config': {
                'approved_scripts_key': 'ooxml'
            }
        },
        {
            'name': 'external_links',
            'kind': 'style',
            'config': {
                'approved_styles_key': 'preloaders'
            }
        }
    ]

    def __init__(self, 
                 name,
                 story_id=None,
                 object_ooxml_id=None,
                 endpoint_map=None,
                 **kwargs):
        super(OoxmlWidgetBase, self).__init__(name, **kwargs)
        if object_ooxml_id:
            self.object_ooxml_id = object_ooxml_id
        if story_id:
            self.story_id = story_id
        if endpoint_map:
            self.endpoint_map = endpoint_map
        self.svg_html = None

    def create_container(self, **kwargs):
        """
        Wraps the Presalytics API Ooxml Automation service SVG endpoint in an `<iframe>` that
        will be rendered inside of a story
        """
        client = self.get_client()
        self.token = client.token_util.token["access_token"]
        svg_container_div = lxml.html.Element("div", {
            'class': 'svg-container',
            'data-jwt': self.token,
            'data-object-type': self.endpoint_map.endpoint_id,
            'data-object-id': self.object_ooxml_id
        })
        preloader_container_div = lxml.etree.SubElement(svg_container_div, "div", attrib={"class":"preloader-container"})
        preloader_row_div = lxml.etree.SubElement(preloader_container_div, "div", attrib={"class":"preloader-row"})
        preloader_file = os.path.join(os.path.dirname(__file__), "img", "preloader.svg")
        svg = lxml.html.parse(preloader_file)
        preloader_row_div.append(svg.getroot())
        empty_parent_div = lxml.html.Element("div", {
            'class': 'empty-parent bg-light'
        })
        empty_parent_div.append(svg_container_div)
        return lxml.html.tostring(empty_parent_div)


    def to_html(self, **kwargs):
        return self.svg_html

    def get_svg(self, id, timeout_iterator=0) -> str:
        """
        Get an svg-formatted version of the object from the Ooxml Automation service
        """
        svg_url = self.endpoint_map.get_svg_url(id)
        client = self.get_client()
        auth_header = client.get_auth_header()
        response = requests.get(svg_url, headers=auth_header)
        svg_data = response.text
        if response.status_code != 200:
            raise presalytics.lib.exceptions.ApiError(message=response.text, status_code=response.status_code)
        if response.text.startswith("Temp data"):
            if timeout_iterator > 5:
                raise presalytics.lib.exceptions.ApiError(message="Unable to download svg.  Please check for upstream processing errors.")
            else:
                time.sleep(2)
                svg_data = self.get_svg(id, timeout_iterator)
        return svg_data


class OoxmlFileWidget(OoxmlWidgetBase):
    """
    Builds a `widget` from a Presentation or Spreadsheet document

    This class interacts with the Presalytics API to extract SVG objects from
    Presentation and spreadsheet documents, identify them, and render them 
    into a story. The file is uploaded to Presalytics API Ooxml Automation service,
    which then processes the file and scans for objects in the file's object tree 
    (As seen in the 'Selection Pane' in PowerPoint) for objects matching the 'object_name'.
    When rendered, this widget retrieves an SVG of the identified object for rendering within 
    the story. 

    Please note that the Presalytics API Ooxml Automation object will be created overwritten 
    each time this widget is initialized, and replaced within the corresponding 
    `presalytics.story.outline.StoryOutline`.  For in-place editing of widgets Ooxml Automation objects 
    that are already bound to the `Story`, please see `presalytics.lib.widgets.ooxml_editors.OoxmlEditorWidget`

    Parameters
    ----------
    filename : str
        The local filepath a presentation or spreadsheet file containing
        the object to be rendered

    name : str, optional
        The widget name.  If not provided, attribute will be set as the `object_name` 
        or `filename`

    story_id : str, optional
        The the id of the story in the Presalytics API Story service.  If not provided, 
        a new story will be created.  Do not supply if this object has not yet been created. 
    
    object_ooxml_id : str, optional
        The identifier of the Ooxml Automation service object bound the Story. Do not supply if this 
        object has not yet been created.

    endpoint_map : presalytics.lib.widgets.ooxml.OoxmlEndpointMap, optional
        Reference to the Presalytics API Ooxml Automation service endpoint and object type
        that for the object of interest

    object_name : str, optional
        The name of the object in the file's object tree the will be rendered

    previous_ooxml_version : str, optional
        The id Ooxml Automation service document object that was previously used to 
        occupy this widget in the `presalytics.story.outline.StoryOutline`

    file_last_modified : str, optional
        The "last modified" date for the file at the `filename` path.  Used to ascertain
        whether file has been updated since the last time the widget was initialized, and
        correspondingly, whether the widget should be updated in the `presalytics.story.outline.StoryOutline`

    document_ooxml_id : str, optional
        The identifier for the parent "Document" object in the Ooxml Automation service for the object
        idenitifiable by a combinatation of `object_ooxml_id` and `endpoint_map`.
    
    """
    object_name: typing.Optional[str]
    ooxml_id: str
    file_last_modified: datetime.datetime
    previous_ooxml_version: typing.Dict[str, str]

    __component_kind__ = 'ooxml-file-object'

    def __init__(self,
                 filename,
                 name=None,
                 story_id=None,
                 object_ooxml_id=None,
                 endpoint_map=None,
                 object_name=None,
                 previous_ooxml_version={},
                 file_last_modified=None,
                 document_ooxml_id=None,
                 **kwargs):
        if object_name:
            self.object_name = object_name
        else:
            self.object_name = None
        if not name:
            if self.object_name:
                name = self.object_name
            else:
                name = filename
        super(OoxmlFileWidget, self).__init__(name, story_id, object_ooxml_id, endpoint_map, **kwargs)
        self.filename = os.path.basename(filename)
        if not self.endpoint_map:
            if filename.split(".")[-1] in ["pptx", "ppt"]:
                self.endpoint_map = OoxmlEndpointMap(OoxmlEndpointMap.SLIDE)
        self.previous_ooxml_version = previous_ooxml_version
        if file_last_modified:
            self.file_last_modified = file_last_modified.replace(tzinfo=datetime.timezone.utc)
        else:
            self.file_last_modified = datetime.datetime.utcnow()
        self.document_ooxml_id = document_ooxml_id
        self.update()
        self.svg_html = self.create_container(**kwargs)

    def update(self):
        """
        If the file is available locally, this renders that updated file and pushes
        the updated rendering data to the server
        """
        story: 'ApiStory'
        page: 'Page'
        widget: 'Widget'

        search_paths = list(set(presalytics.autodiscover_paths))
        if os.getcwd() not in search_paths:
            search_paths.append(os.getcwd())
        for path in search_paths:
            fpath = os.path.join(path, self.filename)
            if os.path.exists(fpath):
                # update only the file has been modified sine last time
                this_file_last_modified = datetime.datetime.utcfromtimestamp(os.path.getmtime(fpath)).astimezone(tz=datetime.timezone.utc)
                if self.file_last_modified is None or self.file_last_modified <= this_file_last_modified:
                    client = self.get_client()
                    story, status, headers = client.story.story_id_file_post_with_http_info(self.story_id, file=fpath, replace_existing=True, obsolete_id=self.document_ooxml_id)
                    if status >= 299:
                        raise presalytics.lib.exceptions.ApiError()
                    self.previous_ooxml_version = {
                        "document_ooxml_id": self.document_ooxml_id,
                        "object_ooxml_id": self.object_ooxml_id
                    }
                    new_outline = presalytics.story.outline.StoryOutline.load(story.outline)
                    for page in new_outline.pages:
                        found = False
                        for widget in page.widgets:
                            if widget.name == self.object_name:
                                self.document_ooxml_id = widget.data["document_ooxml_id"]
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        message = "Unable to find widget object name {0} in new story outline.  Has this widget been deleted?".format(self.object_name)
                        raise presalytics.lib.exceptions.ValidationError(message)

                    # Get object tree, compare to object name
                    child_tree = client.ooxml_automation.documents_childobjects_get_id(self.document_ooxml_id)
                    target_dto = None

                    try:
                        target_dto = next(x for x in child_tree if x.entity_name == self.object_name)
                    except StopIteration:
                        pass
                    # if name not in object or _object_name is none, get first item of type in end_point id
                    if not target_dto:
                        try:
                            target_dto = next(x for x in child_tree if x.object_type.split(".")[1] == self.endpoint_map.endpoint_id)
                        except StopIteration:
                            message = "Child tree of document {0} does not have a child object of type {1} or name {2}.".format(self.ooxml_id, self.endpoint_map.endpoint_id, self.object_name)
                            raise presalytics.lib.exceptions.InvalidConfigurationError(message)
                    # set widget parameters for recreation server-side (without file)
                    self.object_ooxml_id = target_dto.entity_id
                    self.file_last_modified = presalytics.lib.util.roundup_date_modified(this_file_last_modified)


    @classmethod
    def deserialize(cls, component, **kwargs):
        init_args = {
            "filename": component.data["filename"],
            "endpoint_map": OoxmlEndpointMap(component.data["endpoint_id"]),
            "object_name": component.data["object_name"],
            "name": component.name,
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
                    "file_last_modified": dateutil.parser.parse(component.data["file_last_modified"]).replace(tzinfo=datetime.timezone.utc)
                }
            )
        if "previous_ooxml_version" in component.data:
            init_args.update(
                {
                    "previous_ooxml_version": component.data["previous_ooxml_version"]
                }
            )
        if "story_id" in component.data:
            init_args.update(
                {
                    "story_id": component.data["story_id"]
                }
            )
        if len(kwargs.keys()) > 0:
            init_args.update(kwargs)
        return cls(**init_args)

    def serialize(self):
        self.update()
        data = {
            "filename": self.filename,
            "object_name": self.object_name,
            "endpoint_id": self.endpoint_map.endpoint_id,
            "document_ooxml_id": self.document_ooxml_id,
            "object_ooxml_id": self.object_ooxml_id,
            "story_id": self.story_id
        }
        if self.file_last_modified:
            data.update(
                {
                    "file_last_modified": self.file_last_modified.isoformat()
                }
            )
        if self.previous_ooxml_version:
            data.update(
                {
                    "previous_ooxml_version": self.previous_ooxml_version
                }
            )
        widget = presalytics.story.outline.Widget(
            name=self.name,
            kind=self.__component_kind__,
            data=data,
            plugins=None
        )
        return widget
