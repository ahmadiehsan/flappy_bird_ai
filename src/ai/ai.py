import re
from pathlib import Path

import neat
import pygame
from neat import DefaultGenome
from pygame.event import Event

from src.ai._dto import BirdMeta
from src.game.dto import GameStartDto
from src.game.game import Game
from src.shared_kernel.logger import logger
from src.shared_kernel.path import ROOT_PATH


class Ai:
    save_prefix = "neat-checkpoint-"
    save_path = ROOT_PATH / "output"
    config_file_path = ROOT_PATH / "configs" / "neat_feedforward.txt"

    def __init__(self) -> None:
        self.generation = 0
        self.game = Game()

    def start(self) -> None:
        population = self._load_or_create_population()
        self._add_reporters(population)
        self.generation = population.generation
        winner = population.run(self._eval_genomes, 200)
        logger.info("best genome: %s", winner)

    def _load_or_create_population(self) -> neat.Population:
        checkpoint_path = self._get_latest_checkpoint()

        if checkpoint_path:
            logger.info("restoring from checkpoint: %s", checkpoint_path)
            population = neat.Checkpointer.restore_checkpoint(str(checkpoint_path))
        else:
            config = self._load_config()
            population = neat.Population(config)

        return population

    def _get_latest_checkpoint(self) -> Path | None:
        checkpoints = {}

        for item in self.save_path.iterdir():
            if item.is_file():
                match = re.match(rf"{self.save_prefix}(\d+)", item.name)
                if match:
                    generation = int(match.group(1))
                    checkpoints[generation] = item

        if not checkpoints:
            return None

        return checkpoints[max(checkpoints)]

    def _load_config(self) -> neat.config.Config:
        return neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            self.config_file_path,
        )

    def _add_reporters(self, population: neat.Population) -> None:
        # add a stdout reporter to show progress in the terminal
        population.add_reporter(neat.StdOutReporter(show_species_detail=True))
        population.add_reporter(neat.StatisticsReporter())

        # add save reporter
        save_file_path = self.save_path / self.save_prefix
        population.add_reporter(neat.Checkpointer(generation_interval=5, filename_prefix=str(save_file_path)))

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

        if output[0] > 0:  # we use a relu activation function so result will be between 0 and infinity
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
