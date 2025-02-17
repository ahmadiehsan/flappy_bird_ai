import pygame

from src.game._coordinator import Coordinator
from src.game._dto import StateDto
from src.game._window import Window


class Game:
    def __init__(self) -> None:
        self.state = self._create_state()
        self.window = Window(self.state)
        self.coordinator = Coordinator(self.state)

    def start(self) -> None:
        clock = pygame.time.Clock()
        self.coordinator.initialize()

        while not self.state.game_is_over:
            clock.tick(30)
            self.coordinator.act()
            self.window.draw()

    @staticmethod
    def _create_state() -> StateDto:
        return StateDto(
            win_width=600,
            win_height=800,
            grounds=[],
            pipes=[],
            birds=[],
            level=1,
            game_is_started=False,
            game_is_over=False,
        )


if __name__ == "__main__":
    Game().start()
