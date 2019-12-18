import os
import shutil
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
        tmp_dir = os.path.dirname(tmp_filename)
        shutil.copyfile(test_file, tmp_filename)
        outline = presalytics.create_story_from_ooxml_file(tmp_filename)
        os.remove(tmp_filename)
        shutil.copyfile(test_file, tmp_dir)
        widget_data = outline.pages[0].widgets[0]
        presalytics.OoxmlFileWidget.deseriailize(widget_data)
        presalytics.Revealer(outline).present()

    def tearDown(self):
        pass
