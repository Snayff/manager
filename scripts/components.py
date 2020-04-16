from __future__ import annotations

from typing import TYPE_CHECKING, Type, List
from snecs import RegisteredComponent

from scripts.constants import DAYS_IN_YEAR

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict


################## CLASSES USED IN COMPONENTS ##############################
class Demographic:
    """
    Details about a section of the population.
    """
    def __init__(self, race_data: Dict[str, Union[int, str]]):
        self.race: str = race_data["name"]
        self.amount: int = race_data["amount"]

        # birth
        self.birth_rate: float = race_data["birth_rate"]  # number of births per couple, per year
        self.accrued_births: float = 0.0  # to hold the amounts less than 1
        self.min_brood: int = race_data["min_brood"]  # how many babies born at once
        self.max_brood: int = race_data["max_brood"]

        # death
        self.lifespan: int = race_data["lifespan"]
        self.accrued_deaths: float = 0.0  # to hold the amounts less than 1

    @property
    def birth_rate_in_year(self) -> float:
        """
        How many will approximately be born in a year.
        """
        return (self.birth_rate * self.amount) * (max(self.max_brood - self.min_brood, 1))


class Land:
    """
    Details about a section of the world.
    """
    def __init__(self, land_data: Dict[str, Union[int, str]]):
        self.name = land_data["name"]
        self.terrain = land_data["terrain"]
        self.size = land_data["size"]


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
