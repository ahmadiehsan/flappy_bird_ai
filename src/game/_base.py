import pygame
from pygame import Surface

from src.game._utils import ASSETS_PATH


class Base:
    def __init__(self, y: int) -> None:
        self.image = pygame.transform.scale2x(pygame.image.load(ASSETS_PATH / "base.png").convert_alpha())
        self.velocity = 5
        self.width = self.image.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self) -> None:
        self.x1 -= self.velocity
        self.x2 -= self.velocity
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win: Surface) -> None:
        win.blit(self.image, (self.x1, self.y))
        win.blit(self.image, (self.x2, self.y))
