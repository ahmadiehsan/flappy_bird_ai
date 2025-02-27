import random
import sys

import pygame

from src.game._bird_element import BirdElement
from src.game._dto import CoordinatorSummaryDto, StateDto
from src.game._ground_element import GroundElement
from src.game._pipe_element import PipeElement
from src.game.dto import GameStartDto


class Coordinator:
    def __init__(self, state: StateDto, start_dto: GameStartDto) -> None:
        self.state = state
        self.start_dto = start_dto
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
        for idx, bird in enumerate(self.state.birds):
            meta = self.start_dto.bird_metas_safe[idx]
            top_pipe_y_bottom, bottom_pipe_y_top = self._get_upcoming_pipes_y(bird)
            self.start_dto.hook_new_events_safe(meta, bird.y_center, top_pipe_y_bottom, bottom_pipe_y_top)

        self.summary.events = pygame.event.get()

    def _get_upcoming_pipes_y(self, bird: BirdElement) -> tuple[int, int]:
        top_pipe = next((p for p in self.state.pipes if p.x_right > bird.x_left and p.is_upside_down), None)
        bottom_pipe = next((p for p in self.state.pipes if p.x_right > bird.x_left and not p.is_upside_down), None)

        top_pipe_y_bottom = top_pipe.y_bottom if top_pipe else 0
        bottom_pipe_y_top = bottom_pipe.y_top if bottom_pipe else self.state.win_height

        return top_pipe_y_bottom, bottom_pipe_y_top

    def _exit(self) -> None:
        for event in self.summary.events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def _move_elements(self) -> None:
        self._move_grounds()
        self._move_pipes()
        self._move_birds()

    def _move_grounds(self) -> None:
        for ground in self.state.grounds:
            ground.move()

    def _move_pipes(self) -> None:
        for pipe in self.state.pipes:
            pipe.move()

    def _move_birds(self) -> None:
        for idx, bird in enumerate(self.state.birds):
            bird.move()

            for event in self.summary.events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    meta = self.start_dto.bird_metas_safe[idx]

                    if self.start_dto.hook_select_event_safe(meta, event):
                        bird.jump()

    def _collide_elements(self) -> None:
        self._bird_pipe_collide()
        self._bird_ground_collide()
        self._bird_window_edges_collide()

    def _bird_pipe_collide(self) -> None:
        for idx, bird in enumerate(self.state.birds):
            for pipe in self.state.pipes:
                if bird.absolute_rect.colliderect(pipe.absolute_rect):
                    self.summary.loser_bird_indexes.add(idx)
                    break

    def _bird_ground_collide(self) -> None:
        for idx, bird in enumerate(self.state.birds):
            for ground in self.state.grounds:
                if bird.absolute_rect.colliderect(ground.absolute_rect):
                    self.summary.loser_bird_indexes.add(idx)
                    break

    def _bird_window_edges_collide(self) -> None:
        for idx, bird in enumerate(self.state.birds):
            if (
                bird.x_left < 0
                or bird.x_right > self.state.win_width
                or bird.y_top < 0
                or bird.y_bottom > self.state.win_height
            ):
                self.summary.loser_bird_indexes.add(idx)

    def _add_new_elements(self) -> None:
        self._add_new_grounds()
        self._add_new_paired_pipes()
        self._add_new_birds()

    def _add_new_grounds(self) -> None:
        try:
            last_element = self.state.grounds[-1]
            left_space = last_element.x_right
        except IndexError:
            left_space = 0

        news = []
        while left_space < self.state.win_width:
            ground = GroundElement(left_space=left_space, win_height=self.state.win_height)
            news.append(ground)
            left_space = ground.x_right

        self.state.grounds.extend(news)

    def _add_new_paired_pipes(self) -> None:
        try:
            need_new_pipe = self.state.pipes[-1].x_left < self.state.birds[-1].x_left
        except IndexError:
            need_new_pipe = True

        self.summary.need_new_pipe = need_new_pipe
        if not need_new_pipe:
            return

        if self.summary.game_is_started:
            left_space = self.state.win_width
        else:
            left_space = self.state.win_width - int(self.state.win_width / 10)

        between_space = max(150, 250 - (self.state.level * 3))  # Decreases as the level goes up
        min_height = 90
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
        while len(news) < self.start_dto.bird_init_count:
            bird = BirdElement(win_width=self.state.win_width, win_height=self.state.win_height)
            news.append(bird)

        self.state.birds.extend(news)

    def _update_scores(self) -> None:
        if not self.summary.game_is_started:
            self.state.scoreboard_set("level", 1)
            self.state.scoreboard_set("score", 0)
            self.state.scoreboard_set("birds", len(self.state.birds))
            return

        if self.summary.need_new_pipe:
            self.state.level += 1
            self.summary.is_new_level = True
            self.state.scoreboard_diff("level", 1)
            self.state.scoreboard_diff("score", 10)

        self.state.scoreboard_set("birds", len(self.state.birds))

        new_entries = self.start_dto.hook_new_scoreboard_entries_safe()
        for key, val in new_entries.items():
            self.state.scoreboard_set(key, val)

    def _garbage_collect_elements(self) -> None:
        self._garbage_collect_grounds()
        self._garbage_collect_pipes()
        self._garbage_collect_birds()

    def _garbage_collect_grounds(self) -> None:
        indexes = [i for i, g in enumerate(self.state.grounds) if g.x_right < 0]
        for idx in sorted(indexes, reverse=True):
            del self.state.grounds[idx]

    def _garbage_collect_pipes(self) -> None:
        indexes = [i for i, p in enumerate(self.state.pipes) if p.x_right < 0]
        for idx in sorted(indexes, reverse=True):
            del self.state.pipes[idx]

    def _garbage_collect_birds(self) -> None:
        for loser_idx in sorted(self.summary.loser_bird_indexes, reverse=True):
            meta = self.start_dto.bird_metas_safe[loser_idx]
            del self.state.birds[loser_idx]
            self.start_dto.hook_on_lose_safe(meta)
            del self.start_dto.bird_metas_safe[loser_idx]

        for alive_idx in range(len(self.state.birds)):
            meta = self.start_dto.bird_metas_safe[alive_idx]
            self.start_dto.hook_on_new_frame_safe(meta)

            if self.summary.is_new_level:
                self.start_dto.hook_on_new_level_safe(meta)
