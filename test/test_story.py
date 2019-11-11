import unittest
import os
import json
from presalytics.story.teller import Revealer
from presalytics.story.outline import StoryOutline, Info, Page, Widget, Theme
import yaml


class TestStory(unittest.TestCase):
    """
    Test module features thatr render stories to dashboards or 
    other formats
    """
    def setUp(self):
        pass
    
    def test_deserailze_yaml(self):
        test_file = os.path.join(os.path.dirname(__file__), 'files', 'matplotlib-outline.yaml')
        outline = StoryOutline.import_yaml(test_file)
        self.assertTrue(isinstance(outline, StoryOutline))
        self.assertTrue(isinstance(outline.info, Info))
        self.assertTrue(isinstance(outline.pages[0], Page))
        self.assertTrue(isinstance(outline.pages[0].widgets[0], Widget))
        self.assertTrue(isinstance(outline.themes[0], Theme))
        self.assertEqual('Test-story', outline.title)

    def test_serialize_to_json(self):
        test_file = os.path.join(os.path.dirname(__file__), 'files', 'matplotlib-outline.yaml')
        outline = StoryOutline.import_yaml(test_file)
        json_str = outline.dump()
        new_dict = json.loads(json_str)
        self.assertEqual(new_dict["pages"][0]["widgets"][0]["data"]["plotName"], "test_plt_1")
        self.assertIsNotNone(json_str)


    def test_render_matplotlib_plot(self):
        from test.files import test_plots
        test_file = os.path.join(os.path.dirname(__file__), 'files', 'matplotlib-outline.yaml')
        self.assertFalse(False)

        with open(test_plots) as file:
            outline = yaml.load(file, Loader=yaml.FullLoader)

        revealer = Revealer(outline).render()
    
    def tearDown(self):
        pass
