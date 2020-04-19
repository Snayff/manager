from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

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
        self.edicts: Dict[str, Type[Edict]] = self._load_edicts()

        # volatile info
        self.days_passed: int = 1

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
                "name": "Black Moors",
                "terrain": "grassland",
                "size": "small"
            },
            "the_grove": {
                "name": "The Grove",
                "terrain": "woods",
                "size": "medium"
            }
        }
        return lands

    def _load_edicts(self) -> Dict[str, Type[Edict]]:
        edicts = {
            "conscription": Conscription,

        }

        return edicts


world_data = _WorldDataStore()
