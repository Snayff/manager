from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING, Type

import pygame

from scripts import state, ui, world
from scripts.components import Edicts, Hourglass, Population
from scripts.demographics import Demographic
from scripts.constants import BIRTH_RATE, DAYS_IN_YEAR, HOURS_IN_DAY, LINE_BREAK

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


def process_input(event: pygame.event.Event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            ui.swap_to_main_menu_screen()


def process_end_of_day() -> str:
    """
    Handle the transition of time. Returns string of updates
    """
    player_kingdom = world.get_player_kingdom()
    update_text = ""

    # births and deaths
    for kingdom, (population, ) in world.get_components([Population]):
        _update = ""
        for demographic in population:
            _update += demographic.name

            accrued_births = demographic.accrued_births
            accrued_deaths = demographic.accrued_deaths

            # get birth rate
            birth_rate = world.get_modified_stat(kingdom, BIRTH_RATE, demographic.birth_rate_in_year)

            accrued_births += birth_rate / DAYS_IN_YEAR
            accrued_deaths += demographic.amount / (demographic.lifespan * DAYS_IN_YEAR)

            # handle births
            if accrued_births >= 1:
                births = int(accrued_births)
                accrued_births -= births

                # add births
                demographic.amount += births * random.randint(demographic.min_brood, demographic.max_brood)
                _update += ", born: " + str(births)
            else:
                _update += ", born: 0"

            # update accrued births
            demographic.accrued_births = accrued_births

            # handle deaths of old age
            if accrued_deaths >= 1:
                deaths = int(accrued_deaths)
                accrued_deaths -= deaths

                # remove deaths
                demographic.amount -= deaths

                _update += ", died: " + str(deaths)
            else:
                _update += ", died: 0"

            # update accrued deaths
            demographic.accrued_deaths = accrued_deaths

        # log the change
        # N.B. not informing the player as they need to take actions to trigger updates
        name = world.get_name(kingdom)
        logging.debug(f"{name}'s end of turn: {_update}")


    # allocate available time
    hourglass = world.get_entitys_component(player_kingdom, Hourglass)
    hourglass.hours_available = HOURS_IN_DAY

    # manage movement of time
    world.progress_days(1)

    # save the game
    state.save_game(is_auto_save=True)

    # handle empty update
    if not update_text:
        update_text = "No news arrives."

    return update_text
