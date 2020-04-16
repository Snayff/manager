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
        self.races = self._load_race_values()

        logging.info(f"_WorldDataStore initialised.")

    def _load_race_values(self):
        """
        Set the initial race values
        """
        races = {
            "goblin": {
                "race": "goblin",
                "homeworld": "G'rorrn",
                "amount": 100,
                "birth_rate": 2,
                "min_brood": 1,
                "max_brood": 2,
                "lifespan": 2
            },
            "shoom": {
                "race": "shoom",
                "homeworld": "Ee Arth",
                "amount": 20,
                "birth_rate": 0.2,
                "min_brood": 1,
                "max_brood": 1,
                "lifespan": 20
            }
        }

        return races


world_data = _WorldDataStore()
