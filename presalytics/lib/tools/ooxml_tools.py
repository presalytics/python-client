import datetime
import typing
import logging
import presalytics
import presalytics.story.outline
import presalytics.client.api
import presalytics.lib.widgets.ooxml
import presalytics.lib.themes.ooxml

if typing.TYPE_CHECKING:
    from presalytics.client.presalytics_story import Story
    from presalytics.client.presalytics_ooxml_automation import Document
    from presalytics.story.components import ThemeBase
    from presalytics.story.outline import StoryOutline


logger = logging.getLogger(__name__)


def add_ooxml_document_to_story(story_id, new_document_filepath, replace_id=None, username=None, password=None):
    """
    Utility method for asscoiating a new Document in the Presalytics API Ooxml Automation service
    with a Story.  

    Parameters
    ----------
    story_id: str
        The Presalytics API Story service Id for for the story

    new_document_filepath str
        The local filepath to the document tha you want to associate with the story

    replace_id: str, option
        If you want to replace a document, this the documents Ooxml Automation service Id  
        
        Passing this value will also update the references to Ooxml Automation
        service Document object in the Story Outline.  This is a good option if you have
        not made significant changes to the new version of the document.  Widgets may 
        fail to render if more than minor changes are made to the object tree.

    username: str, option
        Presalytics API username.  Defaults to workspace username.

    password: str, option
        Presalytics API password. 
    """

    client = presalytics.client.api.Client(username=username, password=password)
    if story_id == "empty" or not story_id:
        message = "The story_id must not be empty"
        raise presalytics.lib.exceptions.InvalidArgumentException(message)
    replace = True if replace_id else False
    story = client.story.story_id_file_post(story_id, file=new_document_filepath, replace_existing=replace, obsolete_id=replace_id)

def create_story_from_ooxml_file(filename: str, client_info={}) -> 'Story':
    """
    Utility Method for building stories into the Presalytics API directly from a Presentation or Spreadsheet file. 

    Parameters
    ----------
    filename : str
        A string contain the local path to a presenation or spreadsheet object.

    client_info : dict, optional
        A dictionary containing arguments that will be unpacked and passed to a `presalytics.client.api.Client` object on intialization. 
        This dictionary can include the `token`, `cache_tokens`, `delegate_login` values.  See `presalytics.client.api.Client` for more information.

    Returns:
    ----------
    A `presalytics.client.presalytics_story.models.story.Story` containing information about the Story object in the Presalytics API

    """

    story: 'Story'
    logger.info("Starting presalytics tool: create_story_from_ooxml_file")
    logger.info("Intializing presalytics client.")
    
    client = presalytics.Client(**client_info)
    logger.info("Sending file to presalytics server for document processing and base story creation")
    story = client.story.story_post_file(file=filename)
    logger.info("Creating local instances of file widgets")
    outline = presalytics.StoryOutline.load(story.outline)
    for i in range(0, len(outline.pages)):
        page = outline.pages[i]
        for j in range(0, len(page.widgets)):
            widget = page.widgets[j]
            logger.info('Creating OoxmlFileWidget with name "{}"'.format(widget.name))
            inst = presalytics.OoxmlFileWidget.deserialize(widget, **client_info)
            presalytics.COMPONENTS.register(inst)
            logger.info('Rewriting outline with widget: "{}"'.format(widget.name))
            outline.pages[i].widgets[j] = inst.serialize()
    story.outline = outline.dump()
    return story


def create_outline_from_ooxml_document(story_api: 'Story',
                                       ooxml_document: 'Document',
                                       title: str = None,
                                       description: str = None,
                                       themes: typing.Sequence['ThemeBase'] = None,
                                       client_info={}):
    """
    Utility Method for generating a story from a presenation or spreadsheet file

    This method encapsulates a standard workflow for interating the the Presalytics
    API into a single function.  This method takes known `presalytics.client.presalytics_ooxml_automation.models.document.Document`
    with a known `presalytics.client.presalytics_story.models.story.Story`.  This method returns a `presalytics.story.outline.StoryOutline`
    that can be used to replace with existing `presalytics.story.outline.StoryOutline` on the story if the user warrants it.
    

    Parameters
    ----------
    story_api : presalytics.client.presalytics_story.models.story.Story
        The represenation for the Presalytics API instance that will recieve a new associate with the  **ooxml_document**

    ooxml_document : presalytics.client.presalytics_ooxml_automation.models.document.Document 
        the new ooxml_document will be associated with the story.  The outline will be generated from this object

    title : str, optional
        If not provided, the story will take on the title of the `presalytics.client.presalytics_ooxml_automation.models.document.Document` object

    description : str, optional
        If not provided, the story description will initialize as the empty string
    
    themes : list of presalytics.story.components.ThemeBase, optional
        A list of the themes to added to the returned `presalytics.story.outline.StoryOutline`
    
    client_info : dict, optional
        A dictionary containing arguments that will be unpacked and passed to a `presalytics.client.api.Client` object on intialization. 
        This dictionary can include the `token`, `cache_tokens`, `delegate_login` values.  See `presalytics.client.api.Client` for more information.

    Returns
    ----------
    A `presalytics.story.outline.StoryOutline` for the user to optionally serialize and append to the story in downstream operations

    """
    info = presalytics.story.outline.Info(
        revision=0,
        date_created=datetime.datetime.utcnow().isoformat(),
        date_modified=datetime.datetime.utcnow().isoformat(),
        created_by=presalytics.CONFIG.get("USERNAME", ""),
        modified_by=presalytics.CONFIG.get("USERNAME", ""),
        revision_notes='Created by via "create_outline_from_ooxml_file" method'
    )

    if description:
        _description = description
    else:
        _description = ""
    try:
        pages = create_pages_from_ooxml_document(story_api, ooxml_document, client_info=client_info)
    except Exception as ex:
        logger.error("Error adding pages to outline", exc_info=True)
        pages = []
    try:
        if themes:
            _themes = themes
        else:
            ooxml_id = pages[0].widgets[0].data["document_ooxml_id"]
            _themes = [create_theme_from_ooxml_document(ooxml_id, client_info=client_info)]
    except Exception:
        logger.error("Unable to add theme to ooxml_story", exc_info=True)
        _themes = []
    
    if title:
        _title = title
    else:
        _title = pages[0].widgets[0].name

    outline = presalytics.story.outline.StoryOutline(
        info=info,
        pages=pages,
        description=_description,
        title=_title,
        themes=_themes,
        plugins=[]
    )
    return outline


def create_pages_from_ooxml_document(story: 'Story', 
                                     ooxml_document: 'Document',
                                     client_info={}):
    """
    Utility Method for building stories into the Presalytics API directly from a Presenation or Spreadsheet file. 

    Parameters
    ----------
    story : presalytics.client.presalytics_story.models.story.Story
        Representation for Presalytics API Story object

    ooxml_document: presalytics.client.presalytics_ooxml_automation.models.document.Document
        The ooxml_document on the story that you want to create pages from

    client_info : dict, optional
        A dictionary containing arguments that will be unpacked and passed to a `presalytics.client.api.Client` object on intialization. 
        This dictionary can include the `token`, `cache_tokens`, `delegate_login` values.  See `presalytics.client.api.Client` for more information.

    Returns:
    ----------
    A list of `presalytics.story.outline.Page` objects representing the slides, pages and charts in the source document

    """
    pages = []
    order = []
    pages_unordered = []
    client = presalytics.Client(**client_info)
    child_objects = client.ooxml_automation.documents_childobjects_get_id(ooxml_document.id)
    document_type = client.ooxml_automation.documents_documenttype_typeid_get_type_id(ooxml_document.document_type_id)
    if document_type.file_extension == "pptx":
        slides_meta = [x for x in child_objects if x.object_type == "Slide.Slides"]
        ep_map = presalytics.OoxmlEndpointMap.slide()
        for slide in slides_meta:
            try:
                widget = presalytics.OoxmlFileWidget(
                    filename=ooxml_document.filename,
                    name=slide.entity_name,
                    endpoint_map=ep_map,
                    object_name=slide.entity_name,
                    object_ooxml_id=slide.entity_id,
                    document_ooxml_id=ooxml_document.id,
                    story_id=story.id,
                    client_info=client_info
                )
                widget_kind = "widget-page"
                widget_name = slide.entity_name
                widgets = [widget.serialize()]
                page = presalytics.story.outline.Page(
                    kind=widget_kind,
                    name=widget_name,
                    widgets=widgets
                )

                this_slide_meta = client.ooxml_automation.slides_slides_get_id(slide.entity_id)
                order.append(this_slide_meta.number -1)
                pages_unordered.append(page)
            except:
                logger.error("Unable to add widget {0} to outline ooxml document {1}".format(slide.entity_name, ooxml_document.id))
    # TODO: insert excel chart handling here
    for j in range(0, len(order)):
        idx = order.index(j)
        pages.append(pages_unordered[idx])    
    return pages

def create_theme_from_ooxml_document(document_id: str, client_info={}):
    """
    Creates a `presalytics.story.outline.Theme` object from an Presalytics API ooxml_document object

    Parameters:
    ----------
    document_id: str
        A string containing a uuid that corresponds to a document in the Ooxml Automation service of the Presalytics API

    client_info : dict, optional
        A dictionary containing arguments that will be unpacked and passed to a `presalytics.client.api.Client` object on intialization. 
        This dictionary can include the `token`, `cache_tokens`, `delegate_login` values.  See `presalytics.client.api.Client` for more information.

    Returns:
    ----------
    A `presalytics.story.outline.Theme` object with formats extracted from the ooxml_document

    """
    client = presalytics.Client(**client_info)
    child_objects = client.ooxml_automation.documents_childobjects_get_id(document_id)
    themes = [x for x in child_objects if x.object_type == "Theme.Themes"]
    if len(themes) > 1:
        slide_no = None
        for theme_data in themes:
            theme_info = client.ooxml_automation.theme_themes_get_id(theme_data.entity_id)
            parent_slide = client.ooxml_automation.slides_slides_get_id(theme_info.slide_id)
            if slide_no is None:
                slide_no = parent_slide.number
                theme_meta = theme_info
            else:
                if parent_slide.number < slide_no:
                    theme_meta = theme_info
                    if parent_slide.number == 0:
                        break
    else:
        theme_meta = client.ooxml_automation.theme_themes_get_id(themes[0].entity_id)
    theme = presalytics.lib.themes.ooxml.OoxmlTheme(
        theme_meta.name, 
        theme_meta.id, 
        client_info=client_info
    )
    return theme.serialize().to_dict()

def get_mime_type_from_filename(client: presalytics.Client, filename) -> typing.Optional[str]:
    """
    Determines the mimetype from a file's type extension

    Parameters:
    ----------
    client : presalytics.client.api.Client
        A client object for making api calls
    
    filename : str
        A filename against which the method can lookup mimetypes

    Returns:
    ----------
    A string containing a mimetype to attach to file uploads

    """
    doc_types = client.ooxml_automation.documents_documenttype_get()
    file_extension = filename.split(".")[-1]
    try:
        return next(x.mime_type for x in doc_types if x.file_extension == file_extension)
    except StopIteration:
        return None
        