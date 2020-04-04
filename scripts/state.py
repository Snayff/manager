from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

import pygame

from scripts.constants import INITIALISING, GAME_FPS

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


class _StateManager:
    def __init__(self):
        self.current_game_state = INITIALISING
        self.previous_game_state = INITIALISING
        self.internal_clock = pygame.time.Clock()
        self.time: int = 1  # total time of actions taken

    def get_previous(self) -> int:
        """
        Get the previous game state
        """
        return self.previous_game_state

    def get_internal_clock(self):
        """
        Get the internal clock
        """
        return self.internal_clock

    def get_delta_time(self) -> float:
        """
        get delta time and set frame rate with .tick()
        """
        return self.internal_clock.tick(GAME_FPS) / 1000.0

    def get_current(self) -> int:
        """
        Get the current game state
        """
        return self.current_game_state

    def update_clock(self):
        """
        Tick the internal clock. Manages the frame rate.
        """
        # set frame rate
        self.internal_clock.tick(GAME_FPS)

    def set_new(self, new_game_state: int):
        """
        Set the current game state
        """
        prev = self.previous_game_state

        self.previous_game_state = self.current_game_state
        self.current_game_state = new_game_state

        log_string = f"game_state updated from {prev} to {new_game_state}"
        logging.info(log_string)


state = _StateManager()
