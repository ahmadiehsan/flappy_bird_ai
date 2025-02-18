from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class GameStartDto[TMeta]:  # pylint: disable=C0103
    bird_init_count: int
    bird_metas: dict[str, TMeta]
    hook_after_frame: Callable[[dict[str, TMeta], str], None] | None
    hook_after_score: Callable[[dict[str, TMeta], str, int], None] | None
    hook_after_lose: Callable[[dict[str, TMeta], str], None] | None

    def __post_init__(self) -> None:
        if self.bird_metas and len(self.bird_metas) != self.bird_init_count:
            err_msg = "metas and birds are not equal"
            raise ValueError(err_msg)
