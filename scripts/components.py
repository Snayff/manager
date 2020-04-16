from __future__ import annotations

from typing import TYPE_CHECKING, Type, List
from snecs import RegisteredComponent

from scripts.constants import DAYS_IN_YEAR

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict


################## CLASSES USED IN COMPONENTS ##############################
class Demographic:
    def __init__(self, race: str, amount: int = 1, birth_rate: int = 1, min_brood_size: int = 1,
            max_brood_size: int = 1, lifespan: int = 1):
        self.race = race
        self.amount = amount

        # birth
        self.birth_rate = birth_rate  # number of births per couple, per year
        self.accrued_births: float = 0.0  # to hold the amounts less than 1
        self.min_brood_size = min_brood_size  # how many babies born at once
        self.max_brood_size = max_brood_size

        # death
        self.lifespan = lifespan
        self.accrued_deaths: float = 0.0  # to hold the amounts less than 1

    @property
    def birth_rate_in_year(self):
        """
        How many will approximately be born in a year.
        """
        return (self.birth_rate * self.amount) * (max(self.max_brood_size - self.min_brood_size, 1))


class Land:
    def __init__(self, name: str, size: str, terrain: str, buildings: List[str]):
        self.name = name
        self.terrain = terrain
        self.size = size
        self.buildings = buildings


class StaffMember:
    def __init__(self, name: str, role: str, skill: int):
        self.name = name
        self.role = role
        self.skill = skill


################ COMPONENTS ##########################

class Population(List[Demographic], RegisteredComponent):
    pass


class Details(RegisteredComponent):
    def __init__(self, name: str):
        self.kingdom_name = name


class Lands(List[Land], RegisteredComponent):
    pass


class IsPlayerControlled(RegisteredComponent):
    __slots__ = ()


class CastleStaff(List[StaffMember], RegisteredComponent):
    pass
