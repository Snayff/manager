from __future__ import annotations

import logging
import sys
import traceback
import pygame
from scripts import state, ui, world
from scripts.constants import EXIT
from scripts.debug import create_profiler, disable_logging, disable_profiling, dump_profiling_data, initialise_logging


def main():
    """
    The entry for the game initialisation and game loop
    """
    # initialise logging
    initialise_logging()

    # initialise profiling
    profiler = create_profiler()

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
    ui.swap_to_main_menu_screen()

    while not state.get_current() == EXIT:

        # get info to support UI updates and handling events
        delta_time = state.get_delta_time()

        # process any deletions from last frame
        world.process_pending_deletions()

        # update based on input events
        for event in pygame.event.get():
            ui.process_ui_event(event)

        # allow the ui to respond to the progression of time
        ui.update(delta_time)

        # tick
        state.update_clock()

        # show the new state_data
        ui.draw()


if __name__ == "__main__":  # prevents being run from other modules
    main()
