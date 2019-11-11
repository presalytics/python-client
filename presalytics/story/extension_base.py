from abc import ABC, abstractmethod
from typing import Dict, TypeVar, Sequence
from presalytics.story.components import WidgetComponent, WidgetPlaceholder

class ExtensionBase(ABC):
    __extension_type__: str
    """
    Base class for authoring extensions
    """

    @abstractmethod
    def make(self):
        raise NotImplementedError

    

class WidgetExtensionBase(ExtensionBase):
    """
    Base class for creating custom widgets that render to html objects
    """
    __extension_type__ = 'widget'

    def __init__(self, data: Dict[str, str]):
        self.data = data
    
    def make(self):
        return self.make_widget()

    @abstractmethod
    def make_widget(self) -> WidgetComponent:
        raise NotImplementedError

WidgetComponentClass = TypeVar('WidgetComponentClass', bound=WidgetComponent)

class TemplateExtensionBase(ExtensionBase):
    __extension_type__ = 'template'
    widgets = Sequence[WidgetComponentClass]

    def __init__(self, widgets: Sequence[WidgetComponentClass]) -> None:
        self.widgets = widgets

    def make(self):
        return self.make_template()

    @abstractmethod
    def make_template(self):
        raise NotImplementedError

    def get_styles(self):
        """
        Override as needed with an html style tag (as string)
        """
        return None

    def get_scripts(self):
        """
        Override as needed with an html script tag (as string)
        """
        return None


class ThemeExtensionBase(ExtensionBase):
    __extension_type__ = 'theme'

    def make(self):
        return self.make_theme()

    @abstractmethod
    def make_theme(self):
        raise NotImplementedError
    
