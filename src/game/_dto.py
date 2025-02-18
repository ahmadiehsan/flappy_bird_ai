from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, cast

from pygame.event import Event

from src.game._bird_element import BirdElement
from src.game._ground_element import GroundElement
from src.game._pipe_element import PipeElement


@dataclass(kw_only=True)
class StateDto[TMeta]:  # pylint: disable=C0103
    bird_init_count: int
    bird_metas: list[TMeta]
    hook_after_frame: Callable[[TMeta], None] | None
    hook_after_level: Callable[[TMeta], None] | None
    hook_after_lose: Callable[[TMeta], None] | None
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

    @cached_property
    def bird_metas_safe(self) -> list[TMeta]:
        if not self.bird_metas:
            return [cast(TMeta, i) for i in range(len(self.birds))]

        return self.bird_metas

    @property
    def hook_after_frame_safe(self) -> Callable[[TMeta], None]:
        if not self.hook_after_frame:
            return self._null_func

        return self.hook_after_frame

    @property
    def hook_after_level_safe(self) -> Callable[[TMeta], None]:
        if not self.hook_after_level:
            return self._null_func

        return self.hook_after_level

    @property
    def hook_after_lose_safe(self) -> Callable[[TMeta], None]:
        if not self.hook_after_lose:
            return self._null_func

        return self.hook_after_lose

    @staticmethod
    def _null_func(*args: Any, **kwargs: Any) -> None:
        return


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
