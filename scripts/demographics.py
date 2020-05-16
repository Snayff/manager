from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Type

import attr

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


@attr.s(auto_attribs=True)
class Demographic(ABC):
    """
    Details about a section of the population.
    """
    # N.B. do not specify type as doing so makes it a instance variable and we need class variable
    key = "not specified"
    name = "not specified"
    homeworld = "not specified"
    initial_amount = 0
    birth_rate = 0  # how many births per year
    min_brood = 0
    max_brood = 0
    lifespan = 0

    # instance vars
    amount: int = 0
    accrued_deaths: float = 0.0
    accrued_births: float = 0.0

    @property
    def birth_rate_in_year(self) -> int:
        """
        How many, approximately, will be born in a year. Variance caused by min and max brood size.
        """
        birth_rate_in_year = (self.birth_rate * self.amount) * (max((self.max_brood + self.min_brood) / 2, 1))
        return int(birth_rate_in_year)


@attr.s(auto_attribs=True)
class Goblin(Demographic):
    key = "goblin"
    name = "Goblin"
    homeworld = "G'rorrn"
    initial_amount = 100
    birth_rate = 2
    min_brood = 1
    max_brood = 4
    lifespan = 10

    amount: int = initial_amount


@attr.s(auto_attribs=True)
class Shoom(Demographic):
    key = "shoom"
    name = "Shoom"
    homeworld = "Ee Arth"
    initial_amount = 20
    birth_rate = 0.2
    min_brood = 1
    max_brood = 1
    lifespan = 100

    amount: int = initial_amount


@attr.s(auto_attribs=True)
class Pan(Demographic):
    key = "pan"
    name = "Pan"
    homeworld = "TBC"
    initial_amount = 30
    birth_rate = 0.6
    min_brood = 1
    max_brood = 2
    lifespan = 60

    amount: int = initial_amount
