import pygame

from src.game._dto import StateDto
from src.game._utils import ASSETS_PATH


class Window:
    def __init__(self, state: StateDto) -> None:
        pygame.font.init()
        pygame.display.set_caption("Flappy Bird")
        self.state = state
        self.win = pygame.display.set_mode((self.state.win_width, self.state.win_height))
        self.bg_surface = pygame.transform.scale(pygame.image.load(ASSETS_PATH / "bg.png").convert_alpha(), (600, 900))
        self.stat_font = pygame.font.SysFont("comicsans", 50)

    def draw(self) -> None:
        self._draw_bg()

        for pipe in self.state.pipes:
            pipe.draw(self.win)

        for ground in self.state.grounds:
            ground.draw(self.win)

        for bird in self.state.birds:
            bird.draw(self.win)

        self._draw_scoreboard()
        pygame.display.update()

    def _draw_bg(self) -> None:
        self.win.blit(self.bg_surface, (0, 0))

    def _draw_scoreboard(self) -> None:
        for idx, (key, val) in enumerate(self.state.scoreboard.items()):
            label = self.stat_font.render(f"{key}: {val}", 1, (255, 255, 255))
            left_space = self.state.win_width - label.get_width() - 15
            top_space = (40 * idx) + 10
            self.win.blit(label, (left_space, top_space))
