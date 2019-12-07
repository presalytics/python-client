import os
import unittest
import presalytics


class TestComponents(unittest.TestCase):
    """
    Test module features thatr render stories to dashboards or other formats
    """
    def setUp(self):
        pass

    def test_render_matplotlib_plot(self):
        test_file = os.path.join(os.path.dirname(__file__), 'files', 'matplotlib-outline.yaml')
        outline = presalytics.StoryOutline.import_yaml(test_file)
        presalytics.Revealer(outline).present(files_path='/tmp')

    def test_xml_widget(self):
        pass

    def test_file_widget(self):
        test_file = os.path.join(os.path.dirname(__file__), "files", "star.pptx")
        outline = presalytics.create_story_from_ooxml_file(test_file)
        presalytics.Revealer(outline).present()

    def tearDown(self):
        pass
