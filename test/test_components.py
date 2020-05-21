import os
import shutil
import pathlib
import unittest
import typing
import presalytics
import io
import lxml
from presalytics.client.api import get_client
if typing.TYPE_CHECKING:
    from presalytics.client.presalytics_story import Story, OoxmlDocument
    from presalytics.client.presalytics_ooxml_automation.models import ChartChartDataDTO, TableTableDataDTO


class TestComponents(unittest.TestCase):
    """
    Test module features thatr render stories to dashboards or other formats
    """

    def test_render_matploytlib_plot(self):
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
        client_info = get_client().get_client_info()
        story = presalytics.create_story_from_ooxml_file(tmp_filename, client_info=client_info)
        outline = presalytics.StoryOutline.load(story.outline)
        old_widget = outline.pages[0].widgets[0]
        childs = get_client().ooxml_automation.documents_childobjects_get_id(old_widget.data["document_ooxml_id"])
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
                'name': 'TextReplace',
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
        get_client().story.story_id_put(story.id, story)
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

        story = presalytics.story_post_file_bytes(get_client(), _bytes, "testfile.pptx")
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
                'name': 'TextReplace',
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

    def test_chart_update(self):
        story: "Story"
        story_detailed: "Story"
        document: "OoxmlDocument"

        test_file = os.path.join(os.path.dirname(__file__), "files", "bubblechart.pptx")
        story = get_client().story.story_post_file(file=[test_file])
        story_detailed = get_client().story.story_id_get(story.id, include_relationships=True)
        document = story_detailed.ooxml_documents[0]
        object_tree = get_client().ooxml_automation.documents_childobjects_get_id(document.ooxml_automation_id)
        endpoint_map = presalytics.OoxmlEndpointMap.chart() 
        object_type = endpoint_map.get_object_type()
        chart_id = next(entity.entity_id for entity in object_tree if entity.object_type == object_type)
        updater = presalytics.lib.widgets.ooxml.ChartUpdaterWidget('updater', story.id, chart_id)

        dto = updater.get_dto()
        dummySeriesName = "TestSeries1"
        data = [
            [1,2,5,None],
            [None,None,4,5],
            [9,3,8,None],
            [None,None,3,6]
        ]
        
        
        dto.data_points = data
        series = dto.series_names
        series[0] = dummySeriesName
        dto.series_names = series

        df = updater.get_dataframe()
        updater.put_dataframe(df)

        html = updater.to_html()

        self.assertTrue(len(html) > 0)

        widget = updater.serialize()

        self.assertTrue(isinstance(widget, presalytics.story.outline.Widget))

        inst = presalytics.lib.widgets.ooxml.ChartUpdaterWidget.deserialize(widget)

        self.assertTrue(isinstance(inst, presalytics.lib.widgets.ooxml.ChartUpdaterWidget))

    def test_table_update(self):
        story: "Story"
        story_detailed: "Story"
        document: "OoxmlDocument"
        dto: "TableTableDataDTO"

        test_file = os.path.join(os.path.dirname(__file__), "files", "table.pptx")
        story = get_client().story.story_post_file(file=[test_file])
        story_detailed = get_client().story.story_id_get(story.id, include_relationships=True)
        document = story_detailed.ooxml_documents[0]
        object_tree = get_client().ooxml_automation.documents_childobjects_get_id(document.ooxml_automation_id)
        endpoint_map = presalytics.OoxmlEndpointMap.table() 
        object_type = endpoint_map.get_object_type()
        table_id = next(entity.entity_id for entity in object_tree if entity.object_type == object_type)
        updater = presalytics.lib.widgets.ooxml.TableUpdaterWidget('updater', story.id, table_id)

        dto = updater.get_dto()
        dummyEntryName = "CR6!XD?"

        dto.table_data[2][2] = dummyEntryName


        updater.update_from_dto(dto)
        # updater.get_svg_file()
        # client.download_file(story.id, document.ooxml_automation_id)
        self.assertTrue(dummyEntryName in updater.get_svg(updater.table_id))

    def tearDown(self):
        pass
