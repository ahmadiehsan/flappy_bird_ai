import pygame
from pygame import Mask, Surface

from src.game._utils import ASSETS_PATH


class Bird:
    def __init__(self, x: int, y: int) -> None:
        self.images = [pygame.transform.scale2x(pygame.image.load(ASSETS_PATH / f"bird{i}.png")) for i in range(1, 4)]
        self.max_rotation = 25
        self.rotation_velocity = 20
        self.animation_time = 5
        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.images[0]

    def jump(self) -> None:
        self.velocity = -10
        self.tick_count = 0
        self.height = self.y

    def move(self) -> None:
        self.tick_count += 1

        # for downward acceleration
        displacement = int(self.velocity * self.tick_count + 0.5 * 3 * self.tick_count**2)

        # terminal velocity
        if displacement >= 16:
            displacement = int((displacement / abs(displacement)) * 16)

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            self.tilt = max(self.tilt, self.max_rotation)
        elif self.tilt > -90:
            self.tilt -= self.rotation_velocity

    def draw(self, win: Surface) -> None:
        self.image_count += 1

        # For animation of bird, loop through three images
        if self.image_count <= self.animation_time:
            self.image = self.images[0]
        elif self.image_count <= self.animation_time * 2:
            self.image = self.images[1]
        elif self.image_count <= self.animation_time * 3:
            self.image = self.images[2]
        elif self.image_count <= self.animation_time * 4:
            self.image = self.images[1]
        elif self.image_count == self.animation_time * 4 + 1:
            self.image = self.images[0]
            self.image_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.image = self.images[1]
            self.image_count = self.animation_time * 2

        # tilt the bird
        self._blit_rotate_center(win, self.image, (self.x, self.y), self.tilt)

    def get_mask(self) -> Mask:
        """Get the mask for the current image of the bird."""
        return pygame.mask.from_surface(self.image)

    @staticmethod
    def _blit_rotate_center(win: Surface, image: Surface, top_left: tuple[int, int], angle: int) -> None:
        """Rotate an image and blit it to the window."""
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
        win.blit(rotated_image, new_rect.topleft)
