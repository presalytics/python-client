import typing
import datetime
import presalytics.story.components
import presalytics.story.outline
if typing.TYPE_CHECKING:
    from presalytics.story.components import WidgetBase, PageTemplateBase
    from presalytics.story.outline import StoryOutline, Info, Page, Widget, Theme


def create_outline_from_widget(widget: 'WidgetBase',
                               page_name: str = None,
                               title: str = None,
                               description: str = None) -> 'StoryOutline':
    """
    Creates a `presalytics.story.outline.StoryOutline` from a subclass of 
    `presalytics.story.components.WidgetBase`.  Useful for quickstarts, demos, and 
    rapidly sharing content without having to manaully build a `StoryOutline`.

    Parameters
    ----------

    widget : subclass of presalytics.story.components.WidgetBase
        The widget component that you want to build the story from

    page_name : str, optional
        The name you want to give the `presalytics.story.outline.Page` in the outline.
        Defaults to the name of the supplied `widget`

    title : str, optional
        The title of the `presalytics.story.outline.StoryOutline`.  Defaults to
        `page_name`.

    description : str, optional
        The description of the story.  Autopopulated if unassigned.

    """
    info = presalytics.story.outline.Info(
        revision="0",
        date_created=datetime.datetime.now().astimezone(datetime.timezone.utc).isoformat(),
        date_modified=datetime.datetime.now().astimezone(datetime.timezone.utc).isoformat(),
        created_by=presalytics.CONFIG["USERNAME"],
        modified_by=presalytics.CONFIG["USERNAME"],
        revision_notes="Created by 'create_outline_from_widget' method"
    )

    outline_widget = widget.serialize()
    if not page_name:
        page_name = outline_widget.name

    page = presalytics.story.outline.Page(
        name=page_name,
        kind="widget-page",
        widgets=[outline_widget]
    )
    if not description:
        description = "{0} with {1} created by 'create_outline_from_widget' method".format(page_name, outline_widget.name)

    if not title:
        title = page_name

    outline = presalytics.story.outline.StoryOutline(
        info=info,
        pages=[page],
        description=description,
        title=title,
        themes=[]
    )

    return outline

def create_outline_from_page(page: 'PageTemplateBase',
                             title: str = None,
                             description: str = None) -> 'StoryOutline':
    """
    Creates a `presalytics.story.outline.StoryOutline` from a subclass of 
    `presalytics.story.components.PageTemplateBase`.  Useful for quick starts, demos, and 
    rapidly sharing content without having to manaully build a `StoryOutline`.

    Parameters
    ----------

    page : subclass of presalytics.story.components.PageTemplateBase
        The Page component that you want to build the story from

    title : str, optional
        The title of the `presalytics.story.outline.StoryOutline`.  Defaults to
        the name of the page.

    description : str, optional
        The description of the story.  Autopopulated if unassigned.

    """
    info = presalytics.story.outline.Info(
        revision="0",
        date_created=datetime.datetime.now().astimezone(datetime.timezone.utc).isoformat(),
        date_modified=datetime.datetime.now().astimezone(datetime.timezone.utc).isoformat(),
        created_by=presalytics.CONFIG["USERNAME"],
        modified_by=presalytics.CONFIG["USERNAME"],
        revision_notes="Created by 'create_outline_from_page' method"
    )

    page_outline = page.serialize()

    if not description:
        description = "{0} created by 'create_outline_from_page' method".format(page_outline.name)

    if not title:
        title = page_outline.name

    outline = presalytics.story.outline.StoryOutline(
        info=info,
        pages=[page],
        description=description,
        title=title,
        themes=[]
    )

    return outline