import unittest
import os
import json
import lxml
import lxml.html
import lxml.etree
import base64
import io
import uuid
import presalytics.story.revealer
import presalytics.story.outline
import presalytics.lib.tools.component_tools
import presalytics.lib.widgets.ooxml_editors
import presalytics.lib.widgets.d3


class TestStory(unittest.TestCase):
    """
    Test module features thatr render stories to dashboards or other formats.

    Please note that these are integration tests, the development environment and
    `presaltytics.CONFIG` must be set up appropriately for these test execute 
    sucessfully.
    """
    def setUp(self):
        pass

    def test_deserailze_yaml(self):
        test_file = os.path.join(os.path.dirname(__file__), 'files', 'matplotlib-outline.yaml')
        outline = presalytics.story.outline.StoryOutline.import_yaml(test_file)
        self.assertTrue(isinstance(outline, presalytics.story.outline.StoryOutline))
        self.assertTrue(isinstance(outline.info, presalytics.story.outline.Info))
        self.assertTrue(isinstance(outline.pages[0], presalytics.story.outline.Page))
        self.assertTrue(isinstance(outline.pages[0].widgets[0], presalytics.story.outline.Widget))
        self.assertTrue(isinstance(outline.themes[0], presalytics.story.outline.Theme))
        self.assertEqual('Test-story', outline.title)

    def test_serialize_to_json(self):
        test_file = os.path.join(os.path.dirname(__file__), 'files', 'matplotlib-outline.yaml')
        outline = presalytics.story.outline.StoryOutline.import_yaml(test_file)
        json_str = outline.dump()
        new_dict = json.loads(json_str)
        self.assertEqual(new_dict["pages"][0]["widgets"][0]["data"]["temp"], "data")
        self.assertIsNotNone(json_str)

    def test_plugins(self):
        from presalytics import PLUGINS

    def test_create_outline_from_widget(self):
        import matplotlib.pyplot as plt
        import numpy as np
        
        x = np.random.rand(30)
        y = np.random.rand(30)
        z = np.random.rand(30)
        
        fig, ax = plt.subplots()

        ax.scatter(x, y, s=z*1000, alpha=0.5)

        wrapper = presalytics.lib.widgets.matplotlib.MatplotlibResponsiveFigure(fig, "BubbleChart")


        outline = presalytics.lib.tools.component_tools.create_outline_from_widget(wrapper)

        re_wrapper = presalytics.lib.widgets.matplotlib.MatplotlibResponsiveFigure.deserialize(outline.pages[0].widgets[0])

    

        self.assertIsInstance(outline, presalytics.story.outline.StoryOutline)
        self.assertIsInstance(re_wrapper, presalytics.lib.widgets.matplotlib.MatplotlibFigure)

        revealer = presalytics.story.revealer.Revealer(outline)

        self.assertGreaterEqual(len(revealer.plugin_mgr.dependency_map), 8)

        html_str = revealer.package_as_standalone().decode('utf-8')

        self.assertIsInstance(html_str, str)

    def test_render_page_exception(self):
        test_file = os.path.join(os.path.dirname(__file__), 'files', 'bad-outline.yaml')
        _debug = presalytics.CONFIG.pop("DEBUG", None)
        outline = presalytics.story.outline.StoryOutline.import_yaml(test_file)
        revealer = presalytics.story.revealer.Revealer(outline)
        html = revealer.package_as_standalone().decode('utf-8')
        self.assertTrue("Oops!" in html)
        if _debug:
            presalytics.CONFIG.update({"DEBUG": _debug})
    
    def text_replace_transform_test(self):
        test_file = os.path.join(os.path.dirname(__file__), 'files', 'ooxml_test_2.xml')
        test_element = lxml.etree.parse(test_file)
        params = {
            'beta': '66.02',
            'fit_quality': 'pretty good',
            'r_squared': '91.33%',
            'trend': 'positive'
        }

        replacer = presalytics.lib.widgets.ooxml_editors.TextReplace(params)

        updates = lxml.etree.tostring(replacer.execute(test_element)).decode('utf-8')

        for _, val in params.items():
            self.assertTrue(val in updates)

    def upload_from_json(self):
        from presalytics.client.presalytics_story import FileUpload

        test_file = os.path.join(os.path.dirname(__file__), 'files', 'bubblechart.pptx')
        with open(test_file, 'rb') as f:
            bin = f.read()
            content_length = len(bin)
            data = base64.b64encode(bin).decode('UTF-8')
            
        client = presalytics.Client()
        file = FileUpload(
            content_length=content_length,
            file_name="test.pptx",
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            file=str(data)
        )
        story = client.story.story_post_file_json(file_upload=file)
        from presalytics.client.presalytics_story import Story
        self.assertTrue(type(story) is Story)

    def d3(self):
        
        widget = presalytics.lib.widgets.d3.D3Widget(
            'test-widget',
            {
                'right_text': 'This is the right window',
                'left_text': 'This is the left window'
            },
            script_filename='d3-test.js',
            css_filename='fragment.css',
            html_filename='fragment.html'
        )
        widget.story_id = str(uuid.uuid4())
        w = widget.serialize()
        self.assertTrue(isinstance(w, presalytics.story.outline.Widget))
        new_widget = presalytics.lib.widgets.d3.D3Widget.deserialize(w)
        self.assertTrue(isinstance(new_widget, presalytics.lib.widgets.d3.D3Widget))

        html = widget.standalone_html()

        doc = lxml.html.document_fromstring(html)

        self.assertTrue(isinstance(doc, lxml.etree._Element))

        frame = lxml.html.fragment_fromstring(widget.to_html())

        self.assertTrue(isinstance(frame, lxml.etree._Element))

        # Uncomment to view test results

        # client = presalytics.Client()

        # outline = presalytics.lib.tools.component_tools.create_outline_from_widget(widget)

        # client.story.story_post({"outline": outline.dump()})

        
        


    def tearDown(self):
        pass
