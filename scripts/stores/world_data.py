from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from scripts.constants import AVERAGE, LARGE, SMALL
from scripts.demographics import Demographic, Goblin, Shoom
from scripts.edicts import Conscription, Edict

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


class _WorldDataStore:
    """
    Hold the world data
    """
    def __init__(self):
        # static values
        self.races: Dict[str, Type[Demographic]] = self._load_race_values()
        self.lands: Dict[str, Dict[str, str]] = self._load_land_values()
        self.land_sizes: Dict[str, float] = self._load_land_size_modifiers()
        self.edicts: Dict[str, Type[Edict]] = self._load_edicts()

        # volatile info
        self.days_passed: int = 1
        self.calendar: Dict[str, List] = {}

        logging.info(f"_WorldDataStore initialised.")

    ######################## LOAD VALUES ########################

    def _load_race_values(self) -> Dict[str, Type[Demographic]]:
        """
        Set the initial race values
        """
        races = {
            "goblin": Goblin,
            "shoom": Shoom
        }

        return races

    def _load_land_values(self) -> Dict[str, Dict[str, str]]:
        """
        Set the initial land values
        """
        lands = {
            "black_moors": {
                "key": "black_moors",
                "name": "Black Moors",
                "terrain": "grassland",
                "size": SMALL
            },
            "the_grove": {
                "key": "the_grove",
                "name": "The Grove",
                "terrain": "woods",
                "size": AVERAGE
            }
        }
        return lands

    def _load_edicts(self) -> Dict[str, Type[Edict]]:
        edicts = {
            "conscription": Conscription,

        }

        return edicts

    def _load_land_size_modifiers(self) -> Dict[str, float]:
        """
        Load the modifiers for each land size
        """
        sizes = {
            SMALL: 0.5,  # small worth half of average
            AVERAGE: 1.0,  # the default size
            LARGE: 2.0
        }
        return sizes


world_data = _WorldDataStore()
