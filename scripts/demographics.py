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
    name: str = "not specified"
    homeworld: str = "not specified"
    amount: int = 0
    birth_rate: float = 0
    min_brood: int = 0
    max_brood: int = 0
    lifespan: float = 0

    accrued_deaths: float = 0.0
    accrued_births: float = 0.0

    @property
    def birth_rate_in_year(self) -> float:
        """
        How many, approximately, will be born in a year. Variance caused by min and max brood size.
        """
        return (self.birth_rate * self.amount) * (max(self.max_brood - self.min_brood, 1))


@attr.s(auto_attribs=True)
class Goblin(Demographic):
    name: str = "Goblin"
    homeworld: str = "G'rorrn"
    amount: int = 100
    birth_rate: float = 2
    min_brood: int = 1
    max_brood: int = 4
    lifespan: float = 10


@attr.s(auto_attribs=True)
class Shoom(Demographic):
    name: str = "Shoom"
    homeworld: str = "Ee Arth"
    amount: int = 20
    birth_rate: float = 0.2
    min_brood: int = 1
    max_brood: int = 1
    lifespan: float = 100
