import random

import pygame
from pygame import Surface

from src.game._bird import Bird
from src.game._utils import ASSETS_PATH


class Pipe:
    image = pygame.transform.scale2x(pygame.image.load(ASSETS_PATH / "pipe.png").convert_alpha())
    gap = 200
    velocity = 5

    def __init__(self, x: int) -> None:
        self.x = x
        self.height = 0

        # where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        self.pipe_top = pygame.transform.flip(self.image, flip_x=False, flip_y=True)
        self.pipe_bottom = self.image

        self.passed = False
        self._set_height()

    def _set_height(self) -> None:
        """Set the height of the pipe, from the top of the screen."""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self) -> None:
        self.x -= self.velocity

    def draw(self, win: Surface) -> None:
        win.blit(self.pipe_top, (self.x, self.top))  # draw top
        win.blit(self.pipe_bottom, (self.x, self.bottom))  # draw bottom

    def collide(self, bird: Bird) -> bool:
        """Return if a point is colliding with the pipe."""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return bool(b_point or t_point)
