import pygame

from src.game._coordinator import Coordinator
from src.game._dto import StateDto
from src.game._window import Window
from src.game.dto import GameStartDto


class Game:
    def start(self, dto: GameStartDto) -> None:
        state = self._create_state()
        window = Window(state)
        coordinator = Coordinator(state, dto)

        clock = pygame.time.Clock()
        coordinator.initialize()

        while state.birds:
            clock.tick(30)
            coordinator.act()
            window.draw()

    @staticmethod
    def _create_state() -> StateDto:
        return StateDto(win_width=600, win_height=800, grounds=[], pipes=[], birds=[], level=1)


if __name__ == "__main__":
    Game().start(
        GameStartDto(
            bird_init_count=1,
            bird_metas=[],
            hook_filter_events=None,
            hook_new_frame=None,
            hook_new_level=None,
            hook_lose=None,
            hook_new_events=None,
        )
    )
