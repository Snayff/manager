from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


class _WorldDataStore:
    """
    Hold the world data
    """
    def __init__(self):
        self.races: Dict[str, Dict[str, Union[int, str]]] = self._load_race_values()
        self.lands: Dict[str, Dict[str, str]] = self._load_land_values()

        self.days_passed: int = 1

        logging.info(f"_WorldDataStore initialised.")

    ######################## LOAD VALUES ########################

    def _load_race_values(self) -> Dict[str, Dict[str, Union[int, str]]]:
        """
        Set the initial race values
        """
        races = {
            "goblin": {
                "name": "Goblin",
                "homeworld": "G'rorrn",
                "amount": 100,
                "birth_rate": 2,
                "min_brood": 1,
                "max_brood": 2,
                "lifespan": 2
            },
            "shoom": {
                "name": "Shoom",
                "homeworld": "Ee Arth",
                "amount": 20,
                "birth_rate": 0.2,
                "min_brood": 1,
                "max_brood": 1,
                "lifespan": 20
            }
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


world_data = _WorldDataStore()
