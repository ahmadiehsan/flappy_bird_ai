from abc import ABC, abstractmethod

from pygame import Rect, Surface
from pygame.event import Event


class IElement(ABC):
    surface: Surface
    top_lef_x: int
    top_lef_y: int

    @abstractmethod
    def move(self, events: list[Event]) -> None: ...

    @abstractmethod
    def draw(self, win: Surface) -> None: ...

    @property
    def absolute_rect(self) -> Rect:
        return self.surface.get_rect(topleft=(self.top_lef_x, self.top_lef_y))

    @property
    def width(self) -> int:
        return self.surface.get_width()

    @property
    def height(self) -> int:
        return self.surface.get_height()
