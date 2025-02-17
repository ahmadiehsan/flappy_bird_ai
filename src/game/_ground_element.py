import pygame
from pygame import Surface
from pygame.event import Event

from src.game._i_element import IElement
from src.game._utils import ASSETS_PATH


class GroundElement(IElement):
    def __init__(self, *, left_space: int, win_height: int) -> None:
        self.surface = pygame.transform.scale2x(pygame.image.load(ASSETS_PATH / "ground.png").convert_alpha())
        self.top_lef_x = left_space
        self.top_lef_y = win_height - int(win_height / 8)
        self.velocity = 5

    def move(self, events: list[Event]) -> None:  # noqa: ARG002
        self.top_lef_x -= self.velocity

    def draw(self, win: Surface) -> None:
        win.blit(self.surface, (self.top_lef_x, self.top_lef_y))
