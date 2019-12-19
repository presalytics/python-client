import os
import shutil
import pathlib
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
