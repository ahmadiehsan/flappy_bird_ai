import sys

import pygame

from src.game._base import Base
from src.game._bird import Bird
from src.game._game_data import GameData
from src.game._pipe import Pipe
from src.game._window import Window


class Game:
    def __init__(self) -> None:
        win_width = 600
        win_height = 800
        floor = 730
        self.window = Window(win_width, win_height)
        self.game_data = GameData(
            win_width=win_width,
            win_height=win_height,
            floor=floor,
            base=Base(floor),
            pipes=[Pipe(700)],
            bird=Bird(230, 350),
            score=0,
            loop=True,
        )

    def start(self) -> None:
        self._init_pygame()
        clock = pygame.time.Clock()

        while self.game_data.loop:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_data.loop = False
                    pygame.quit()
                    sys.exit()

            self._handle_base()
            self._handle_pipes()
            self._handle_bird()
            self.window.draw(self.game_data)

    @staticmethod
    def _init_pygame() -> None:
        pygame.font.init()
        pygame.display.set_caption("Flappy Bird")

    def _handle_base(self) -> None:
        self.game_data.base.move()

    def _handle_pipes(self) -> None:
        pipes_to_remove = []
        need_add_pipe = False

        for pipe in self.game_data.pipes:
            pipe.move()

            if pipe.collide(self.game_data.bird):
                self.game_data.loop = False

            if pipe.x + pipe.pipe_top.get_width() < 0:
                pipes_to_remove.append(pipe)

            if not pipe.passed and pipe.x < self.game_data.bird.x:
                pipe.passed = True
                need_add_pipe = True

        if need_add_pipe:
            self.game_data.score += 1
            self.game_data.pipes.append(Pipe(self.game_data.win_width))

        for pipe_to_remove in pipes_to_remove:
            self.game_data.pipes.remove(pipe_to_remove)

    def _handle_bird(self) -> None:
        if (
            self.game_data.bird.y + self.game_data.bird.image.get_height() - 10 >= self.game_data.floor
            or self.game_data.bird.y < -50
        ):
            self.game_data.loop = False


if __name__ == "__main__":
    Game().start()
