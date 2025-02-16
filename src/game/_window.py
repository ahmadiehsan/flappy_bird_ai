import pygame

from src.game._game_data import GameData
from src.game._utils import ASSETS_PATH


class Window:
    def __init__(self, win_width: int, win_height: int) -> None:
        pygame.font.init()
        pygame.display.set_caption("Flappy Bird")
        self.win = pygame.display.set_mode((win_width, win_height))
        self.bg_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH / "bg.png").convert_alpha(), (600, 900))
        self.stat_font = pygame.font.SysFont("comicsans", 50)

    def draw(self, game_data: GameData) -> None:
        self.win.blit(self.bg_img, (0, 0))

        for pipe in game_data.pipes:
            pipe.draw(self.win)

        game_data.base.draw(self.win)
        game_data.bird.draw(self.win)

        score_label = self.stat_font.render("Score: " + str(game_data.score), 1, (255, 255, 255))
        self.win.blit(score_label, (self.win.get_width() - score_label.get_width() - 15, 10))

        pygame.display.update()
