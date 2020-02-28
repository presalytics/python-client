import os
import shutil
import pathlib
import unittest
import typing
import presalytics
import io
import lxml
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
        html = presalytics.Revealer(outline).package_as_standalone().decode('utf-8')
        self.assertIsInstance(html, str)

    def test_xml_widget(self):
        test_file = os.path.join(os.path.dirname(__file__), "files", "star.pptx")
        tmp_filename = os.path.join(os.path.dirname(__file__), os.path.basename(test_file))
        shutil.copyfile(test_file, tmp_filename)
        story = presalytics.create_story_from_ooxml_file(tmp_filename)
        outline = presalytics.StoryOutline.load(story.outline)
        old_widget = outline.pages[0].widgets[0]
        client = presalytics.Client()
        childs = client.ooxml_automation.documents_childobjects_get_id(old_widget.data["document_ooxml_id"])
        endpoint_map = presalytics.OoxmlEndpointMap.shape() 
        object_type = endpoint_map.get_object_type()
        info = next(x for x in childs if x.object_type == object_type)
        new_color = {
            "object_name": info.entity_name,
            "hex_color": "FF0000"
        }
        multiparams = {"transforms_list" : [
            {
                'name': 'ChangeShapeColor',
                'function_params': new_color
            },
            {
                'name': 'ReplaceText',
                'function_params': {
                    'test_text': "Test Passed!"
                }
            }
        ]}
        widget = presalytics.OoxmlEditorWidget(
            name="test-editor",
            story_id=story.id,
            object_ooxml_id=info.entity_id,
            endpoint_map=endpoint_map,
            transform_class=presalytics.MultiXmlTransform,
            transform_params=multiparams
        )
        outline.pages[0].widgets[0] = widget.outline_widget

        
        presalytics.COMPONENTS.register(widget)
        story.outline = outline.dump()
        client.story.story_id_put(story.id, story)
        html = presalytics.Revealer(outline).package_as_standalone().decode('utf-8')
        self.assertIsInstance(html, str)
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
        html = presalytics.Revealer(story_outline).package_as_standalone().decode('utf-8')
        self.assertIsInstance(html, str)

    def test_bytesio_upload(self):
        test_file = os.path.join(os.path.dirname(__file__), "files", "star.pptx")
        with open(test_file, 'rb') as f:
            _bytes = io.BytesIO(f.read())

        client = presalytics.Client()
        story = presalytics.story_post_file_bytes(client, _bytes, "testfile.pptx")
        from presalytics.client.presalytics_story.models.story import Story
        self.assertIsInstance(story, Story)

    def test_multixml(self):
        test_file = os.path.join(os.path.dirname(__file__), "files", "ooxml_test.xml")
        etree = lxml.etree.parse(test_file)
        multiparams = {"transforms_list" : [
            {
                'name': 'ChangeShapeColor',
                'function_params': {
                    "hex_color": "FF0000"
                }
            },
            {
                'name': 'ReplaceText',
                'function_params': {
                    'test_text': "Test Passed!"
                }
            }
        ]}
        inst  = presalytics.MultiXmlTransform(multiparams)
        new_lxml = inst.execute(etree.getroot())
        xml_string = lxml.etree.tostring(new_lxml).decode('utf-8')
        self.assertTrue("Test Passed!" in xml_string)
        self.assertTrue("FF0000" in xml_string)


    def tearDown(self):
        pass
