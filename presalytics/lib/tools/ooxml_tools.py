import datetime
import typing
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


def create_story_from_ooxml_file(filename: str,
                                 delegate_login=False,
                                 token=None) -> 'Story':
    story: 'Story'

    client = presalytics.Client(delegate_login=delegate_login, token=token)
    story = client.story.story_post_file(file=filename)
    outline = presalytics.StoryOutline.load(story.outline)
    for i in range(0, len(outline.pages)):
        page = outline.pages[i]
        for j in range(0, len(page.widgets)):
            widget = page.widgets[j]
            inst = presalytics.OoxmlFileWidget.deserialize(widget)
            presalytics.COMPONENTS.register(inst)
            outline.pages[i].widgets[j] = inst.serialize()
    story.outline = outline.dump()
    return story


def create_outline_from_ooxml_document(story: 'Story',
                                       ooxml_document: 'Document',
                                       title: str = None,
                                       description: str = None,
                                       themes: typing.Sequence['ThemeBase'] = None,
                                       delegate_login=False,
                                       token=None):

    info = presalytics.story.outline.Info(
        revision=0,
        date_created=datetime.datetime.now().isoformat(),
        date_modified=datetime.datetime.now().isoformat(),
        created_by=presalytics.CONFIG.get("USERNAME", ""),
        modified_by=presalytics.CONFIG.get("USERNAME", ""),
        revision_notes='Created by via "create_outline_from_ooxml_file" method'
    )

    if title:
        _title = title
    else:
        _title = ""

    if description:
        _description = description
    else:
        _description = ""

    pages = create_pages_from_ooxml_document(story, ooxml_document, delegate_login=delegate_login, token=token)

    if themes:
        _themes = themes
    else:
        ooxml_id = pages[0].widgets[0].data["document_ooxml_id"]
        _themes = [create_theme_from_ooxml_document(ooxml_id, delegate_login, token)]

    outline = presalytics.story.outline.StoryOutline(
        presalytics_story=presalytics.story.outline.get_current_spec_version(),
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
                                     delegate_login=False,
                                     token=None):
    pages = []
    client = presalytics.Client(delegate_login=delegate_login, token=token)
    child_objects = client.ooxml_automation.documents_childobjects_get_id(ooxml_document.id)
    document_type = client.ooxml_automation.documents_documenttype_typeid_get_type_id(ooxml_document.document_type_id)
    if document_type.file_extension == "pptx":
        slides_meta = [x for x in child_objects if x.object_type == "Slide.Slides"]
        ep_map = presalytics.OoxmlEndpointMap(presalytics.OoxmlEndpointMap.SLIDE)
        for slide in slides_meta:
            widget = presalytics.OoxmlFileWidget(
                filename=ooxml_document.filename,
                name=slide.entity_name,
                endpoint_map=ep_map,
                object_name=slide.entity_name,
                object_ooxml_id=slide.entity_id,
                document_ooxml_id=ooxml_document.id,
                story_id=story.id
            )
            widget_kind = "widget-page"
            widget_name = slide.entity_name
            widgets = [widget.serialize()]
            page = presalytics.story.outline.Page(
                kind=widget_kind,
                name=widget_name,
                widgets=widgets
            )
            pages.append(page)
    # TODO: insert excel chart handling here
    return pages


def create_theme_from_ooxml_document(document_id: str,
                                     delegate_login=False,
                                     token=None):
    client = presalytics.Client(delegate_login=delegate_login, token=token)
    child_objects = client.ooxml_automation.documents_childobjects_get_id(document_id)
    themes = [x for x in child_objects if x.object_type == "Theme.Themes"]
    if len(themes) > 1:
        slide_no = None
        for theme_data in themes:
            theme_info = client.ooxml_automation.theme_themes_get_id(theme_data.entity_id)
            parent_slide = client.ooxml_automation.slides_slides_get_id(theme_info.slide_id)
            if slide_no is None:
                slide_no = parent_slide.number
            else:
                if parent_slide.number < slide_no:
                    theme_meta = theme_info
                    if parent_slide.number == 0:
                        break
    else:
        theme_meta = client.ooxml_automation.theme_themes_get_id(themes[0].entity_id)
    theme = presalytics.lib.themes.ooxml.OoxmlTheme(theme_meta.name, theme_meta.id)
    return theme.serialize().to_dict()
