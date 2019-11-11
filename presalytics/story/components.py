from abc import ABC, abstractmethod

class ComponentBase(ABC):
    __component_type__: str

    @abstractmethod
    def to_string(self):
        """
        Returns component as string of html data.
        """
        raise NotImplementedError


class WidgetComponent(ComponentBase):
    __component_type__ = 'widget'

class WidgetPlaceholder(WidgetComponent):
    __component_type__ = 'placeholder'

    def to_string(self):
        return "{{ placeholder }}"