from __future__ import annotations

import json
import logging
import os
from typing import TYPE_CHECKING

from scripts import world
from scripts.constants import GAME_FPS, MAX_AUTOSAVES, SAVE_PATH
from scripts.stores.state_data import state_data
from scripts.stores.world_data import world_data

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


def save_game(is_auto_save: bool = False):
    """
    Serialise the game data to a file
    """
    # get the info needed
    full_save_path = os.getcwd() + "/" + SAVE_PATH
    save = {}
    save["days_passed"] = world_data.days_passed
    save["world"] = world.serialise()

    # get date for filename
    date = world.get_current_date()
    player_kingdom = world.get_player_kingdom()
    name = world.get_name(player_kingdom)
    name = name.replace(" ", "_")  # clean name
    filename = f"{name}_{date[0]}_{date[1]}_{date[2]}"

    # manage autosaves
    if is_auto_save:
        # add prefix
        filename = "autosave_" + filename

        # clear old autosaves
        existing_autosaves = []
        for _filename in os.listdir(full_save_path):
            if f"autosave_{name}" in _filename:
                existing_autosaves.append(_filename)
        while len(existing_autosaves) > MAX_AUTOSAVES - 1:  # -1 to handle the offset
            _filename = existing_autosaves.pop(0)
            os.remove(full_save_path + "/" + _filename)




    # write to json
    with open(SAVE_PATH + filename + ".json", "w") as file:
        json.dump(save, file, indent=4)


def load_game(filename: str):
    """
    Deserialise the game data from a file. Filename does not include path to save folder.
    """
    # read from json
    with open(SAVE_PATH + filename + ".json", "r") as file:
        save = json.load(file)

    # deserialise data
    world.set_days_passed(save["days_passed"])
    new_world = world.deserialise(save["world"])

    # set the data as the default world
    world.move_world(new_world)


