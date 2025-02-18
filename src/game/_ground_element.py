import pygame
from pygame import Surface

from src.game._i_element import IElement
from src.game._utils import ASSETS_PATH


class GroundElement(IElement):
    def __init__(self, *, left_space: int, win_height: int) -> None:
        self.surface = pygame.transform.scale2x(pygame.image.load(ASSETS_PATH / "ground.png").convert_alpha())
        self.x_left = left_space
        self.y_top = win_height - int(win_height / 8)
        self.velocity = 5

    def move(self) -> None:
        self.x_left -= self.velocity

    def draw(self, win: Surface) -> None:
        win.blit(self.surface, (self.x_left, self.y_top))
