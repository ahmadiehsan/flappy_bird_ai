from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import cast

from pygame.event import Event


@dataclass
class GameStartDto[TMeta]:  # pylint: disable=C0103
    bird_init_count: int
    bird_metas: list[TMeta]
    hook_on_new_frame: Callable[[TMeta], None] | None
    hook_on_new_level: Callable[[TMeta], None] | None
    hook_on_lose: Callable[[TMeta], None] | None
    hook_new_events: Callable[[TMeta, int, int, int], None] | None
    hook_select_event: Callable[[TMeta, Event], bool] | None
    hook_new_scoreboard_entries: Callable[[], dict[str, int]] | None

    def __post_init__(self) -> None:
        self._validate_bird_init_count()
        self._validate_bird_metas()

    def _validate_bird_init_count(self) -> None:
        if self.bird_init_count <= 0:
            err_msg = "bird init count is not valid"
            raise ValueError(err_msg)

    def _validate_bird_metas(self) -> None:
        if self.bird_metas and len(self.bird_metas) != self.bird_init_count:
            err_msg = "metas and birds are not equal"
            raise ValueError(err_msg)

    @cached_property
    def bird_metas_safe(self) -> list[TMeta]:
        return self.bird_metas if self.bird_metas else [cast("TMeta", i) for i in range(self.bird_init_count)]

    @cached_property
    def hook_on_new_frame_safe(self) -> Callable[[TMeta], None]:
        return self.hook_on_new_frame if self.hook_on_new_frame else lambda *args, **kwargs: None

    @cached_property
    def hook_on_new_level_safe(self) -> Callable[[TMeta], None]:
        return self.hook_on_new_level if self.hook_on_new_level else lambda *args, **kwargs: None

    @cached_property
    def hook_on_lose_safe(self) -> Callable[[TMeta], None]:
        return self.hook_on_lose if self.hook_on_lose else lambda *args, **kwargs: None

    @cached_property
    def hook_new_events_safe(self) -> Callable[[TMeta, int, int, int], None]:
        return self.hook_new_events if self.hook_new_events else lambda *args, **kwargs: None

    @cached_property
    def hook_select_event_safe(self) -> Callable[[TMeta, Event], bool]:
        return self.hook_select_event if self.hook_select_event else lambda *args, **kwargs: True

    @cached_property
    def hook_new_scoreboard_entries_safe(self) -> Callable[[], dict[str, int]]:
        return self.hook_new_scoreboard_entries if self.hook_new_scoreboard_entries else lambda *args, **kwargs: {}
