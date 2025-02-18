from dataclasses import dataclass, field

from pygame.event import Event

from src.game._bird_element import BirdElement
from src.game._ground_element import GroundElement
from src.game._pipe_element import PipeElement


@dataclass(kw_only=True)
class StateDto:  # pylint: disable=C0103
    win_width: int
    win_height: int
    grounds: list[GroundElement]
    pipes: list[PipeElement]
    birds: list[BirdElement]
    level: int
    scoreboard: dict[str, int] = field(default_factory=dict)

    def scoreboard_set(self, key: str, val: int) -> None:
        self.scoreboard.setdefault(key, 0)
        self.scoreboard[key] = val

    def scoreboard_diff(self, key: str, diff_val: int) -> None:
        self.scoreboard.setdefault(key, 0)
        self.scoreboard[key] += diff_val


@dataclass(kw_only=True)
class CoordinatorSummaryDto:
    loser_bird_indexes: set[int] = field(default_factory=set)
    need_new_pipe: bool = False
    is_new_level: bool = False
    events: list[Event] = field(default_factory=list)
    game_is_started: bool = False  # INFO: don't need to reset this key in the reset method

    def reset(self) -> None:
        self.loser_bird_indexes = set()
        self.need_new_pipe = False
        self.is_new_level = False
        self.events = []
