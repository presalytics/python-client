import unittest
import os
import json
import presalytics.story.revealer
import presalytics.story.outline
import presalytics.lib.tools.component_tools

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

        client = presalytics.Client()

        story = client.story.story_post(outline.dump())
        
        outline = presalytics.story.outline.StoryOutline.load(story.outline)

        re_wrapper = presalytics.lib.widgets.matplotlib.MatplotlibResponsiveFigure.deserialize(outline.pages[0].widgets[0])

    

        self.assertIsInstance(outline, presalytics.story.outline.StoryOutline)
        self.assertIsInstance(re_wrapper, presalytics.lib.widgets.matplotlib.MatplotlibFigure)

        revealer = presalytics.story.revealer.Revealer(outline)

        self.assertEqual(len(revealer.plugin_mgr.dependency_map), 6)

        html_str = revealer.package_as_standalone().decode('utf-8')

        self.assertIsInstance(html_str, str)

    def tearDown(self):
        pass
