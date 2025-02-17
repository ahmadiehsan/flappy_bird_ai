import random
import sys

import pygame
from pygame.event import Event

from src.game._bird_element import BirdElement
from src.game._dto import StateDto
from src.game._ground_element import GroundElement
from src.game._pipe_element import PipeElement


class Coordinator:
    def __init__(self, state: StateDto) -> None:
        self.state = state

    def initialize(self) -> None:
        self.state.game_is_started = True
        self.state.scoreboard_diff("score", 0)
        self._updates()

    def act(self) -> None:
        events = pygame.event.get()
        self._exit(events)
        self._moves(events)
        self._collides()
        self._updates()

    def _exit(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.state.game_is_over = True
                pygame.quit()
                sys.exit()

    def _moves(self, events: list[Event]) -> None:
        for ground in self.state.grounds:
            ground.move(events)

        for pipe in self.state.pipes:
            pipe.move(events)

        for bird in self.state.birds:
            bird.move(events)

    def _collides(self) -> None:
        self._bird_pipe_collide()
        self._bird_ground_collide()
        self._bird_window_edges_collide()

    def _bird_pipe_collide(self) -> None:
        for bird in self.state.birds:
            for pipe in self.state.pipes:
                if bird.absolute_rect.colliderect(pipe.absolute_rect):
                    self.state.game_is_over = True
                    break

    def _bird_ground_collide(self) -> None:
        for bird in self.state.birds:
            for ground in self.state.grounds:
                if bird.absolute_rect.colliderect(ground.absolute_rect):
                    self.state.game_is_over = True
                    break

    def _bird_window_edges_collide(self) -> None:
        for bird in self.state.birds:
            if bird.top_lef_x < 0 or (bird.top_lef_x + bird.width) > self.state.win_width:
                self.state.game_is_over = True
                break

            if bird.top_lef_y < 0 or (bird.top_lef_y + bird.height) > self.state.win_height:
                self.state.game_is_over = True
                break

    def _updates(self) -> None:
        self._update_grounds()
        self._update_paired_pipes()
        self._update_birds()

    def _update_grounds(self) -> None:
        removes = [g for g in self.state.grounds if g.top_lef_x + g.width < 0]
        for remove in removes:
            self.state.grounds.remove(remove)

        try:
            last_element = self.state.grounds[-1]
            left_space = last_element.top_lef_x + last_element.width
        except IndexError:
            left_space = 0

        news = []
        while left_space < self.state.win_width:
            ground = GroundElement(left_space=left_space, win_height=self.state.win_height)
            news.append(ground)
            left_space = ground.top_lef_x + ground.width

        self.state.grounds.extend(news)

    def _update_paired_pipes(self) -> None:
        removes = [p for p in self.state.pipes if p.top_lef_x + p.width < 0]
        for remove in removes:
            self.state.pipes.remove(remove)

        try:
            need_new = self.state.pipes[-1].top_lef_x < self.state.birds[-1].top_lef_x
        except IndexError:
            need_new = True

        if not need_new:
            return

        left_space = (
            self.state.win_width if self.state.game_is_started else self.state.win_width - int(self.state.win_width / 3)
        )
        between_space = 200
        min_height = 40
        max_height = self.state.win_height - between_space - min_height
        pipe_1_height = random.randint(min_height, max_height)
        pipe_2_height = self.state.win_height - between_space - pipe_1_height
        news = [
            PipeElement(
                visible_height=pipe_1_height,
                left_space=left_space,
                win_height=self.state.win_height,
                is_upside_down=False,
            ),
            PipeElement(
                visible_height=pipe_2_height,
                left_space=left_space,
                win_height=self.state.win_height,
                is_upside_down=True,
            ),
        ]
        self.state.pipes.extend(news)
        self.state.level += 1
        self.state.scoreboard_diff("score", 1)

    def _update_birds(self) -> None:
        need_new = not bool(self.state.birds)
        if not need_new:
            return

        new_elements = [BirdElement(win_width=self.state.win_width, win_height=self.state.win_height)]
        self.state.birds.extend(new_elements)
