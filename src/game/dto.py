from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import cast

from pygame.event import Event


@dataclass
class GameStartDto[TMeta]:  # pylint: disable=C0103
    bird_init_count: int
    bird_metas: list[TMeta]
    hook_filter_events: Callable[[list[Event]], list[Event]] | None
    hook_new_frame: Callable[[TMeta], None] | None
    hook_new_level: Callable[[TMeta], None] | None
    hook_lose: Callable[[TMeta], None] | None

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
        return self.bird_metas if self.bird_metas else [cast(TMeta, i) for i in range(self.bird_init_count)]

    @cached_property
    def hook_filter_events_safe(self) -> Callable[[list[Event]], list[Event]]:
        return self.hook_filter_events if self.hook_filter_events else lambda events: events

    @cached_property
    def hook_new_frame_safe(self) -> Callable[[TMeta], None]:
        return self.hook_new_frame if self.hook_new_frame else lambda *args, **kwargs: None

    @cached_property
    def hook_new_level_safe(self) -> Callable[[TMeta], None]:
        return self.hook_new_level if self.hook_new_level else lambda *args, **kwargs: None

    @cached_property
    def hook_lose_safe(self) -> Callable[[TMeta], None]:
        return self.hook_lose if self.hook_lose else lambda *args, **kwargs: None
