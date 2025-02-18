from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class GameStartDto[TMeta]:  # pylint: disable=C0103
    bird_init_count: int
    bird_metas: list[TMeta]
    hook_after_frame: Callable[[TMeta], None] | None
    hook_after_level: Callable[[TMeta], None] | None
    hook_after_lose: Callable[[TMeta], None] | None

    def __post_init__(self) -> None:
        if self.bird_metas and len(self.bird_metas) != self.bird_init_count:
            err_msg = "metas and birds are not equal"
            raise ValueError(err_msg)
