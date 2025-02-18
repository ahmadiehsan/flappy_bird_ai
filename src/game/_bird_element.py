import pygame
from pygame import Surface
from pygame.event import Event

from src.game._i_element import IElement
from src.game._utils import ASSETS_PATH


class BirdElement(IElement):
    max_rotation = 25
    rotation_velocity = 20
    animation_time = 5

    def __init__(self, *, win_width: int, win_height: int) -> None:
        self.surfaces = [pygame.transform.scale2x(pygame.image.load(ASSETS_PATH / f"bird{i}.png")) for i in range(1, 4)]
        self.surface = self.surfaces[0]
        self.x_left = int(win_width / 2) - self.width
        self.y_top = int(win_height / 2) - int(self.height / 2)
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.velocity = 0
        self.surfaces_count = 0

    def move(self, events: list[Event]) -> None:
        self._move()
        self._jump(events)

    def draw(self, win: Surface) -> None:
        self.surfaces_count += 1

        # for animation of bird, loop through available images
        if self.surfaces_count <= self.animation_time:
            self.surface = self.surfaces[0]
        elif self.surfaces_count <= self.animation_time * 2:
            self.surface = self.surfaces[1]
        elif self.surfaces_count <= self.animation_time * 3:
            self.surface = self.surfaces[2]
        elif self.surfaces_count <= self.animation_time * 4:
            self.surface = self.surfaces[1]
        elif self.surfaces_count == self.animation_time * 4 + 1:
            self.surface = self.surfaces[0]
            self.surfaces_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.surface = self.surfaces[1]
            self.surfaces_count = self.animation_time * 2

        # tilt the bird
        rotated_image = pygame.transform.rotate(self.surface, self.tilt)
        new_rect = rotated_image.get_rect(center=self.surface.get_rect(topleft=(self.x_left, self.y_top)).center)

        # draw it
        win.blit(rotated_image, new_rect.topleft)

    def _move(self) -> None:
        self.tick_count += 1

        # for downward acceleration
        displacement = int(self.velocity * self.tick_count + 0.5 * 3 * self.tick_count**2)

        # terminal velocity
        if displacement >= 16:
            displacement = int((displacement / abs(displacement)) * 16)

        if displacement < 0:
            displacement -= 2

        self.y_top += displacement

        if displacement < 0:  # tilt up
            self.tilt = max(self.tilt, self.max_rotation)
        elif self.tilt > -90:
            self.tilt -= self.rotation_velocity

    def _jump(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.velocity = -10
                self.tick_count = 0
