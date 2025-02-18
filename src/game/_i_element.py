from abc import ABC, abstractmethod

from pygame import Rect, Surface


class IElement(ABC):
    surface: Surface
    x_left: int
    y_top: int

    @abstractmethod
    def draw(self, win: Surface) -> None: ...

    @property
    def absolute_rect(self) -> Rect:
        return self.surface.get_rect(topleft=(self.x_left, self.y_top))

    @property
    def width(self) -> int:
        return self.surface.get_width()

    @property
    def height(self) -> int:
        return self.surface.get_height()

    @property
    def x_center(self) -> int:
        return self.x_left + int(self.width / 2)

    @property
    def x_right(self) -> int:
        return self.x_left + self.width

    @property
    def y_center(self) -> int:
        return self.y_top + int(self.height / 2)

    @property
    def y_bottom(self) -> int:
        return self.y_top + self.height
