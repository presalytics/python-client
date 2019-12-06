import datetime
import typing
import presalytics.story.outline
import presalytics.client.api
import presalytics.lib.widgets.ooxml
import presalytics.lib.themes.ooxml
if typing.TYPE_CHECKING:
    from presalytics.story.components import ThemeBase


def create_outline_from_ooxml_file(filename: str,
                                   title: str = None,
                                   description: str = None,
                                   themes: typing.Sequence['ThemeBase'] = None
                                   ) -> presalytics.story.outline.StoryOutline:
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
        _title = filename

    if description:
        _description = description
    else:
        _description = ""
    pages = create_pages_from_document(filename)

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


def create_pages_from_document(filename):
    pages = []
    client = presalytics.client.api.Client()
    document, status, headers = client.ooxml_automation.documents_post_with_http_info(filename)
    child_objects = client.ooxml_automation.documents_childobjects_get_id(document.id)
    if document.document_type == "pptx":
        slides_meta = [x for x in child_objects if x.type == "Slides.Slide"]
        endpoint = presalytics.lib.widgets.ooxml.OoxmlEndpointMap.SLIDE
        for slide in slides_meta:
            widget = presalytics.lib.widgets.ooxml.OoxmlFileWidget(filename, endpoint_id=endpoint, object_name=slide.name)
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
