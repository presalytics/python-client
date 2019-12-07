import datetime
import typing
import presalytics.story.outline
import presalytics.client.api
import presalytics.lib.widgets.ooxml
import presalytics.lib.themes.ooxml

if typing.TYPE_CHECKING:
    from presalytics_story.models import Story
    from presalytics_ooxml_automation import Document
    from presalytics.story.components import ThemeBase


def create_story_from_ooxml_file(filename: str) -> 'Story':
    story: 'Story'

    client = presalytics.Client()
    story = client.story.story_post_file(filename)
    outline = presalytics.StoryOutline.deserialize(story.outline)
    for i in range(0, len(outline.pages)):
        page = outline.pages[i]
        for j in range(0, len(page.widgets)):
            widget = page.widgets[j]
            inst = presalytics.OoxmlFileWidget.deseriailize(widget)
            presalytics.COMPONENTS.register(inst)
            outline.pages[i].widgets[j] = inst.serialize()
    return story


def create_outline_from_ooxml_document(story: 'Story',
                                       ooxml_document: 'Document',
                                       title: str = None,
                                       description: str = None,
                                       themes: typing.Sequence['ThemeBase'] = None):

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

    pages = create_pages_from_ooxml_document(story, ooxml_document)

    if themes:
        _themes = themes
    else:
        first_widget = pages[0].widget.data["ooxml_id"]
        _themes = create_theme_from_ooxml_document(first_widget.outline_widget.data["ooxml_id"])

    outline = presalytics.story.outline.StoryOutline(
        presalytics_story=presalytics.story.outline.get_current_spec_version(),
        info=info,
        pages=pages,
        description=_description,
        title=_title,
        themes=_themes,
        plugins={}
    )
    return outline


def create_pages_from_ooxml_document(story: 'Story', ooxml_document: 'Document'):
    pages = []
    client = presalytics.Client()
    child_objects = client.ooxml_automation.documents_childobjects_get_id(ooxml_document.id)
    document_type = client.ooxml_automation.documents_documenttype_get_id(ooxml_document.document_type_id)
    if document_type.file_extension == "pptx":
        slides_meta = [x for x in child_objects if x.type == "Slides.Slide"]
        ep_map = presalytics.OoxmlEndpointMap(presalytics.OoxmlEndpointMap.SLIDE)
        for slide in slides_meta:
            widget = presalytics.OoxmlFileWidget(
                filename=ooxml_document.filename,
                name=slide.name,
                endpoint_map=ep_map,
                object_name=slide.name
            )
            page = {
                "kind": "widget-page",
                "name": "page-{}".format(slide.name),
                "widgets": [widget.serialize()]
            }
            pages.append(page)
    # TODO: insert excel chart handling here
    return pages


def create_theme_from_ooxml_document(document_id: str):
    client = presalytics.Client()
    document = client.ooxml_automation.documents_get_id(document_id)
    ooxml_theme = client.ooxml_automation.theme_themes_get_id(document.theme_id)
    theme_name = ooxml_theme.name
    theme = presalytics.lib.themes.ooxml.OoxmlTheme(theme_name, ooxml_theme.id)
    return theme
