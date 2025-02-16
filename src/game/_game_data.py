from dataclasses import dataclass

from src.game._base import Base
from src.game._bird import Bird
from src.game._pipe import Pipe


@dataclass(kw_only=True)
class GameData:
    win_width: int
    win_height: int
    floor: int
    base: Base
    pipes: list[Pipe]
    bird: Bird
    score: int
    loop: bool
