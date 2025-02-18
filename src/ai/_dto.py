from dataclasses import dataclass

import neat
from neat import DefaultGenome


@dataclass(kw_only=True)
class BirdMeta:
    network: neat.nn.FeedForwardNetwork
    genome: DefaultGenome
