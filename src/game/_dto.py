from dataclasses import dataclass, field

from src.game._bird_element import BirdElement
from src.game._ground_element import GroundElement
from src.game._pipe_element import PipeElement


@dataclass(kw_only=True)
class StateDto:
    win_width: int
    win_height: int
    grounds: list[GroundElement]
    pipes: list[PipeElement]
    birds: list[BirdElement]
    level: int
    game_is_started: bool
    game_is_over: bool
    scoreboard: dict[str, int] = field(default_factory=dict)

    def scoreboard_diff(self, key: str, diff_val: int) -> None:
        self.scoreboard.setdefault(key, 0)
        self.scoreboard[key] += diff_val
