import pygame
from pygame import Surface

from src.game._i_element import IElement
from src.game._utils import ASSETS_PATH


class PipeElement(IElement):
    transparent_gap = 15

    def __init__(self, *, visible_height: int, left_space: int, win_height: int, is_upside_down: bool) -> None:
        surface = pygame.transform.scale2x(pygame.image.load(ASSETS_PATH / "pipe.png").convert_alpha())

        self.is_upside_down = is_upside_down

        if not is_upside_down:
            self.surface = surface
        else:
            self.surface = pygame.transform.flip(surface, flip_x=False, flip_y=True)

        self.x_left = left_space

        if not is_upside_down:
            self.y_top = win_height - visible_height + self.transparent_gap
        else:
            self.y_top = visible_height - self.height + self.transparent_gap

        self.velocity = 5

    def move(self) -> None:
        self.x_left -= self.velocity

    def draw(self, win: Surface) -> None:
        win.blit(self.surface, (self.x_left, self.y_top))
