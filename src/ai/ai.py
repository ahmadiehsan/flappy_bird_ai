import logging

import neat
import pygame
from neat import DefaultGenome
from pygame.event import Event

from src.ai._dto import BirdMeta
from src.game.dto import GameStartDto
from src.game.game import Game
from src.shared_kernel.path import ROOT_PATH


class Ai:
    def __init__(self) -> None:
        self.generation = 0
        self.game = Game()

    def start(self) -> None:
        config = self._load_config()

        # create the population, which is the top-level object for a NEAT run
        population = neat.Population(config)

        # add a stdout reporter to show progress in the terminal
        population.add_reporter(neat.StdOutReporter(show_species_detail=True))
        population.add_reporter(neat.StatisticsReporter())

        # run for up to 50 generations.
        winner = population.run(self._eval_genomes, 50)

        # show final stats
        logging.info("best genome: %s", winner)

    @staticmethod
    def _load_config() -> neat.config.Config:
        config_file = ROOT_PATH / "configs" / "feedforward.txt"
        return neat.config.Config(
            neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file
        )

    def _eval_genomes(self, genomes: list[tuple[int, DefaultGenome]], config: neat.config.Config) -> None:
        metas = []  # list holding the genome itself, the neural network associated with the genome
        for _, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            metas.append(BirdMeta(network=network, genome=genome))

        self.game.start(
            GameStartDto(
                bird_init_count=len(metas),
                bird_metas=metas,
                hook_on_new_frame=self._hook_on_new_frame,
                hook_on_new_level=self._hook_on_new_level,
                hook_on_lose=self._hook_on_lose,
                hook_new_events=self._hook_new_events,
                hook_select_event=self._hook_select_event,
                hook_new_scoreboard_entries=self._hook_new_scoreboard_entries,
            )
        )

        self.generation += 1

    @staticmethod
    def _hook_on_new_frame(meta: BirdMeta) -> None:
        meta.genome.fitness += 0.1

    @staticmethod
    def _hook_on_new_level(meta: BirdMeta) -> None:
        meta.genome.fitness += 5

    @staticmethod
    def _hook_on_lose(meta: BirdMeta) -> None:
        meta.genome.fitness -= 1

    @staticmethod
    def _hook_new_events(meta: BirdMeta, bird_y_center: int, top_pipe_y_bottom: int, bottom_pipe_y_top: int) -> None:
        # send bird location and top/bottom pipe location and determine from the network whether to jump or not
        output = meta.network.activate((bird_y_center, top_pipe_y_bottom, bottom_pipe_y_top))

        if output[0] > 0:  # we use a tanh activation function so result will be between -1 and 1
            pygame.event.post(Event(pygame.KEYDOWN, key=pygame.K_UP, ai_generated=True, meta_id=id(meta)))

    @staticmethod
    def _hook_select_event(meta: BirdMeta, event: Event) -> bool:
        is_ai_generated = getattr(event, "ai_generated", False)
        is_related_to_meta = id(meta) == getattr(event, "meta_id", None)
        return is_ai_generated and is_related_to_meta

    def _hook_new_scoreboard_entries(self) -> dict[str, int]:
        return {"generation": self.generation}


if __name__ == "__main__":
    Ai().start()
