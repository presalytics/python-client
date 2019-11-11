import lxml.html
from typing import Sequence
from importlib import import_module
from lxml import etree
from lxml.etree import Element
from datetime import datetime
from presalytics.story.outline import StoryOutline



class Revealer(object):
    """
    This class renders 'Story Outines' to reveal.js presentations
    """
    story_outline: StoryOutline
    base: Element
    links: Sequence[Element]


    def __init__(self, story_outline: StoryOutline):
        self.story_outline = story_outline
        self.story_outline.validate()
        self.base = self.make_base()
        self.links = self.make_links()
        self.extensions = self.story_outline.load_extensions()

    def make_base(self):
        base = etree.Element("div", class="reveal")
        base.subElement("div", class="slides")
        return base
    
    def make_links(self):
        css_base = etree.Element("link", rel="stylesheet", href="css/reveal.css")
        return css_base

    def package_as_standalone(self):
        pass

    def update_info(self):
        info = self.story_outline.info
        info.date_modified = datetime.now()
    
    def render(self):
        """
        This method returns a t
        """
        reveal_base = self.base()
        for page in self.story_outline.pages:
            slide = reveal_base.SubElement("div", class="slides")
            if page.use_templates:
                template_ext = [x for x in self.extensions if x.__class__.__name__ == page.template_name][0]
                
            else:
                pass

        return reveal_base
    
  


        

