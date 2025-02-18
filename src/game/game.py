import pygame

from src.game._coordinator import Coordinator
from src.game._dto import StateDto
from src.game._window import Window
from src.game.dto import GameStartDto


class Game:
    def start(self, dto: GameStartDto) -> None:
        state = self._create_state(dto)
        window = Window(state)
        coordinator = Coordinator(state)

        clock = pygame.time.Clock()
        coordinator.initialize()

        while state.birds:
            clock.tick(30)
            coordinator.act()
            window.draw()

    @staticmethod
    def _create_state(dto: GameStartDto) -> StateDto:
        return StateDto(
            bird_init_count=dto.bird_init_count,
            bird_metas=dto.bird_metas,
            hook_after_frame=dto.hook_after_frame,
            hook_after_score=dto.hook_after_score,
            hook_after_lose=dto.hook_after_lose,
            win_width=600,
            win_height=800,
            grounds=[],
            pipes=[],
            birds=[],
            level=1,
        )


if __name__ == "__main__":
    Game().start(
        GameStartDto(
            bird_init_count=1, bird_metas={}, hook_after_frame=None, hook_after_score=None, hook_after_lose=None
        )
    )
