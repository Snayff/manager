from __future__ import annotations

from typing import TYPE_CHECKING, Type, List
from snecs import RegisteredComponent

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict


class Demographic:
    def __init__(self, race: str, amount: int = 1, birth_rate: int = 1):
        self.birth_rate = birth_rate
        self.amount = amount
        self.race = race


class Land:
    def __init__(self, name: str, size: str, terrain: str, buildings: List[str]):
        self.name = name
        self.terrain = terrain
        self.size = size
        self.buildings = buildings


class Population(List[Demographic], RegisteredComponent):
    pass


class Details(RegisteredComponent):
    def __init__(self, name: str):
        self.kingdom_name = name


class Lands(List[Land], RegisteredComponent):
    pass


class IsPlayerControlled(RegisteredComponent):
    __slots__ = ()
