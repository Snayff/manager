from __future__ import annotations

import random
from typing import TYPE_CHECKING, Type

from scripts import world
from scripts.components import Demographic, Population
from scripts.constants import DAYS_IN_YEAR

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


def process_end_of_day():
    """
    Handle the transition of time.
    """
    for kingdom, (population, ) in world.get_components([Population]):
        for demographic in population:
            accrued_births = demographic.accrued_births
            accrued_deaths = demographic.accrued_deaths

            accrued_births += demographic.birth_rate_in_year / DAYS_IN_YEAR
            accrued_deaths += demographic.amount / (demographic.lifespan * DAYS_IN_YEAR)

            # handle births
            if accrued_births >= 1:
                births = int(accrued_births)
                accrued_births -= births

                # add births
                demographic.amount += births * random.randint(demographic.min_brood, demographic.max_brood)
                demographic.accrued_births = accrued_births

            # handle deaths of old age
            if accrued_deaths >= 1:
                deaths = int(accrued_deaths)
                accrued_deaths -= deaths

                # remove deaths
                demographic.amount -= deaths
                demographic.accrued_deaths = accrued_deaths

