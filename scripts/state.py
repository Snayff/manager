from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

import pygame

from scripts.constants import INITIALISING, GAME_FPS
from scripts.stores.state_data import state_data

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


def get_previous() -> int:
    """
    Get the previous game state_data
    """
    return state_data.previous_game_state


def get_internal_clock():
    """
    Get the internal clock
    """
    return state_data.internal_clock


def get_delta_time() -> float:
    """
    get delta time and set frame rate with .tick()
    """
    return state_data.internal_clock.tick(GAME_FPS) / 1000.0


def get_current() -> int:
    """
    Get the current game state_data
    """
    return state_data.current_game_state


def update_clock():
    """
    Tick the internal clock. Manages the frame rate.
    """
    # set frame rate
    state_data.internal_clock.tick(GAME_FPS)


def set_new(new_game_state: int):
    """
    Set the current game state_data
    """
    prev = state_data.previous_game_state

    state_data.previous_game_state = state_data.current_game_state
    state_data.current_game_state = new_game_state

    log_string = f"game_state updated from {prev} to {new_game_state}"
    logging.info(log_string)
