import random
import sys

import pygame

from src.game._bird_element import BirdElement
from src.game._dto import CoordinatorSummaryDto, StateDto
from src.game._ground_element import GroundElement
from src.game._pipe_element import PipeElement


class Coordinator:
    def __init__(self, state: StateDto) -> None:
        self.state = state
        self.summary = CoordinatorSummaryDto()

    def initialize(self) -> None:
        self._add_new_elements()
        self._update_scores()
        self.summary.game_is_started = True

    def act(self) -> None:
        self._track_events()
        self._exit()
        self._move_elements()
        self._collide_elements()
        self._add_new_elements()
        self._update_scores()
        self._garbage_collect_elements()
        self.summary.reset()

    def _track_events(self) -> None:
        self.summary.events = pygame.event.get()

    def _exit(self) -> None:
        for event in self.summary.events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def _move_elements(self) -> None:
        for ground in self.state.grounds:
            ground.move(self.summary.events)

        for pipe in self.state.pipes:
            pipe.move(self.summary.events)

        for bird in self.state.birds:
            bird.move(self.summary.events)

    def _collide_elements(self) -> None:
        self._bird_pipe_collide()
        self._bird_ground_collide()
        self._bird_window_edges_collide()

    def _bird_pipe_collide(self) -> None:
        for bird in self.state.birds:
            for pipe in self.state.pipes:
                if bird.absolute_rect.colliderect(pipe.absolute_rect):
                    self.summary.loser_birds.add(bird)
                    break

    def _bird_ground_collide(self) -> None:
        for bird in self.state.birds:
            for ground in self.state.grounds:
                if bird.absolute_rect.colliderect(ground.absolute_rect):
                    self.summary.loser_birds.add(bird)
                    break

    def _bird_window_edges_collide(self) -> None:
        for bird in self.state.birds:
            if (
                bird.top_lef_x < 0
                or (bird.top_lef_x + bird.width) > self.state.win_width
                or bird.top_lef_y < 0
                or (bird.top_lef_y + bird.height) > self.state.win_height
            ):
                self.summary.loser_birds.add(bird)

    def _add_new_elements(self) -> None:
        self._add_new_grounds()
        self._add_new_paired_pipes()
        self._add_new_birds()

    def _add_new_grounds(self) -> None:
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

    def _add_new_paired_pipes(self) -> None:
        try:
            self.summary.need_new_pipe = self.state.pipes[-1].top_lef_x < self.state.birds[-1].top_lef_x
        except IndexError:
            self.summary.need_new_pipe = True

        if not self.summary.need_new_pipe:
            return

        if self.summary.game_is_started:
            left_space = self.state.win_width
        else:
            left_space = self.state.win_width - int(self.state.win_width / 10)

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

    def _add_new_birds(self) -> None:
        if self.summary.game_is_started:
            return

        news: list[BirdElement] = []
        while len(news) < self.state.bird_init_count:
            bird = BirdElement(win_width=self.state.win_width, win_height=self.state.win_height)
            news.append(bird)

        self.state.birds.extend(news)

    def _update_scores(self) -> None:
        if not self.summary.game_is_started:
            self.state.scoreboard_set("score", 0)
            self.state.scoreboard_set("birds", len(self.state.birds))
            return

        if self.summary.need_new_pipe:
            self.state.level += 1
            self.summary.score_update_amount = 1

        self.state.scoreboard_diff("score", self.summary.score_update_amount)
        self.state.scoreboard_set("birds", len(self.state.birds))

    def _garbage_collect_elements(self) -> None:
        self._garbage_collect_grounds()
        self._garbage_collect_pipes()
        self._garbage_collect_birds()

    def _garbage_collect_grounds(self) -> None:
        indexes = [i for i, g in enumerate(self.state.grounds) if g.top_lef_x + g.width < 0]
        for index in indexes:
            del self.state.grounds[index]

    def _garbage_collect_pipes(self) -> None:
        indexes = [i for i, p in enumerate(self.state.pipes) if p.top_lef_x + p.width < 0]
        for index in indexes:
            del self.state.pipes[index]

    def _garbage_collect_birds(self) -> None:
        if self.state.bird_metas:
            has_meta = True
            iterate_on = zip(self.state.birds, self.state.bird_metas, strict=True)
        else:
            has_meta = False
            iterate_on = zip(self.state.birds, [str(i) for i in range(len(self.state.birds))], strict=True)

        for bird_idx, (bird, meta_id) in enumerate(iterate_on):
            if bird in self.summary.loser_birds:
                del self.state.birds[bird_idx]

                if has_meta:
                    del self.state.bird_metas[meta_id]

                self.state.hook_after_lose_safe(self.state.bird_metas, meta_id)
            else:
                self.state.hook_after_frame_safe(self.state.bird_metas, meta_id)

            if self.summary.score_update_amount:
                self.state.hook_after_score_safe(self.state.bird_metas, meta_id, self.summary.score_update_amount)
