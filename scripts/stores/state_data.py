from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

import pygame

from scripts.constants import INITIALISING, GAME_FPS

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


class _StateDataStore:
    def __init__(self):
        self.current_game_state = INITIALISING
        self.previous_game_state = INITIALISING
        self.internal_clock = pygame.time.Clock()
        self.time: int = 1  # total time of actions taken

        logging.info(f"StateDataStore initialised.")


state_data = _StateDataStore()
