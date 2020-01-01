import os
import shutil
import pathlib
import unittest
import typing
import presalytics
if typing.TYPE_CHECKING:
    from presalytics.client.presalytics_story import Story


class TestComponents(unittest.TestCase):
    """
    Test module features thatr render stories to dashboards or other formats
    """
    def setUp(self):
        pass

    def test_render_matplotlib_plot(self):
        presalytics.autodiscover_paths.append('test/files')
        presalytics.COMPONENTS = presalytics.story.components.ComponentRegistry(autodiscover_paths=presalytics.autodiscover_paths)
        test_file = os.path.join(os.path.dirname(__file__), 'files', 'matplotlib-outline.yaml')
        outline = presalytics.StoryOutline.import_yaml(test_file)
        presalytics.Revealer(outline).present(files_path='/tmp')

    def test_xml_widget(self):
        story: Story

        test_file = os.path.join(os.path.dirname(__file__), "files", "star.pptx")
        tmp_filename = os.path.join(os.path.dirname(__file__), os.path.basename(test_file))
        shutil.copyfile(test_file, tmp_filename)
        story = presalytics.create_story_from_ooxml_file(tmp_filename)
        outline = presalytics.StoryOutline.load(story.outline)
        old_widget = outline.pages[0].widgets[0]
        client = presalytics.Client()
        childs = client.ooxml_automation.documents_childobjects_get_id(old_widget.data["document_ooxml_id"])
        object_type = presalytics.OoxmlEndpointMap.shape().get_object_type()
        info = next(x for x in childs if x.object_type == object_type)
        new_color = {
            "object_name": info.entity_name,
            "hex_color": "FFFFFF"
        }
        widget = presalytics.OoxmlEditorWidget(
            name="test-editor",
            story_id=story.id,
            object_ooxml_id=info.entity_id,
            endpoint_id=info.object_type.split(".")[1],
            transform_class=presalytics.ChangeShapeColor,
            transform_params=new_color
        )
        outline.pages[0].widgets[0] = widget.outline_widget
        presalytics.COMPONENTS.register(widget)
        presalytics.Revealer(outline).present()
        os.remove(tmp_filename)

    def test_file_widget(self):
        test_file = os.path.join(os.path.dirname(__file__), "files", "star.pptx")
        tmp_filename = os.path.join(os.path.dirname(__file__), os.path.basename(test_file))
        shutil.copyfile(test_file, tmp_filename)
        story = presalytics.create_story_from_ooxml_file(tmp_filename)
        pathlib.Path(tmp_filename).touch()
        story_outline = presalytics.StoryOutline.load(story.outline)
        widget_data = story_outline.pages[0].widgets[0]
        presalytics.OoxmlFileWidget.deserialize(widget_data)
        presalytics.Revealer(story_outline).present()

    def tearDown(self):
        pass
