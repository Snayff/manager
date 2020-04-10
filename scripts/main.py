from __future__ import annotations

import cProfile
import datetime
import io
import logging
import pstats
import sys
import time
import traceback
import pygame
import snecs
from typing import TYPE_CHECKING, Type
from scripts import state, ui, world
from scripts.components import Demographic, Details, IsPlayerControlled, Land, Lands, Population
from scripts.constants import VERSION, EXIT

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


def main():
    """
    The entry for the game initialisation and game loop
    """
    # initialise logging
    initialise_logging()

    # initialise profiling
    # TODO - set to turn off for production builds
    profiler = create_profiler()

    initialise_game()

    # run the game
    try:
        game_loop()
    except Exception:
        logging.critical(f"Something went wrong and killed the game loop")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for line in tb_list:
            clean_line = line.replace("\n", "")
            logging.critical(f"{clean_line}")
        traceback.print_exc()

    # we've left the game loop so now close everything down
    disable_profiling(profiler)
    dump_profiling_data(profiler)
    disable_logging()

    # clean up pygame resources
    pygame.quit()

    # exit window and python
    raise SystemExit


def game_loop():
    """
    The core game loop, handling input, rendering and logic.
    """
    ui.show_overview_screen()

    while not state.get_current() == EXIT:

        # get info to support UI updates and handling events
        delta_time = state.get_delta_time()

        # process any deletions from last frame
        snecs.process_pending_deletions()

        # update based on input events
        for event in pygame.event.get():
            ui.process_ui_event(event)

        # allow everything to update in response to new state_data
        # processors.process_all(delta_time)
        ui.update(delta_time)
        state.update_clock()

        # show the new state_data
        ui.draw()


def initialise_game():
    components = [
        IsPlayerControlled(),
        Details("My Kingdom"),
        Population([Demographic("goblin", 100, 2)]),
        Lands([Land("homeland", "small", "muddy", [])])
    ]
    player_kingdom = world.create_entity(components)


def initialise_logging():
    """
    Configure logging

    Logging levels:
        CRITICAL - A serious error, indicating that may be unable to continue running.
        ERROR - A more serious problem, has not been able to perform some function.
        WARNING - An indication that something unexpected happened, but otherwise still working as expected.
        INFO - Confirmation that things are working as expected.
        DEBUG - Detailed information, typically of interest only when diagnosing problems

    File mode options:
        'r' - open for reading(default)
        'w' - open for writing, truncating the file first
        'x' - open for exclusive creation, failing if the file already exists
        'a' - open for writing, appending to the end of the file if it exists

    """

    log_file_name = "logs/game.log"
    log_level = logging.DEBUG
    file_mode = "w"

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # 8 adds space for 8 characters (# CRITICAL)
    log_format = "%(asctime)s| %(levelname)-8s| %(message)s"
    logging.basicConfig(filename=log_file_name, filemode=file_mode, level=log_level, format=log_format)

    # format into uk time
    logging.Formatter.converter = time.gmtime()


def create_profiler():
    """
    Create and enable the profiler
    """
    profiler = cProfile.Profile()
    profiler.enable()

    return profiler


def disable_logging():
    """
    Turn off current logging and clear logging resources
    """
    logging.shutdown()


def disable_profiling(profiler):
    """
    Turn off current profiling
    """
    profiler.disable()


def dump_profiling_data(profiler):
    """
    Dump data to a readable file
    """
    # dump the profiler stats
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.dump_stats("logs/profiling/profile.dump")

    # convert profiling to human readable format
    date_and_time = datetime.datetime.utcnow()
    out_stream = open("logs/profiling/" + date_and_time.strftime("%Y%m%d@%H%M") + "_" + VERSION + ".profile", "w")
    ps = pstats.Stats("logs/profiling/profile.dump", stream=out_stream)
    ps.strip_dirs().sort_stats("cumulative").print_stats()


if __name__ == "__main__":  # prevents being run from other modules
    main()
