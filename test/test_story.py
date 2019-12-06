import unittest
import os
import json
import presalytics.story.revealer
import presalytics.story.outline


class TestStory(unittest.TestCase):
    """
    Test module features thatr render stories to dashboards or other formats
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

    def tearDown(self):
        pass
