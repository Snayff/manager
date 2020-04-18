from __future__ import annotations

import logging
from abc import ABC
from typing import TYPE_CHECKING, Type, List
from snecs import RegisteredComponent

from scripts import utility
from scripts.constants import DAYS_IN_YEAR, MINUTES_IN_DAY

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict


################## CLASSES USED IN COMPONENTS ##############################
class ComponentElement:
    """
    Base class of any class that will be contained in a Component
    """
    def as_dict(self):
        """
        Return all members as a dict. Needs the
        """
        class_members = utility.get_members(self)
        _dict = {}

        for member in class_members:
            _dict[member] = getattr(self, member)

        return _dict

class Demographic(ComponentElement):
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


class Land(ComponentElement):
    """
    Details about a section of the world.
    """
    def __init__(self, land_data: Dict[str, str]):
        self.name: str = land_data["name"]
        self.terrain: str = land_data["terrain"]
        self.size: str = land_data["size"]


class StaffMember(ComponentElement):
    def __init__(self, name: str, role: str, skill: int):
        self.name: str = name
        self.role: str = role
        self.skill: int = skill


################ COMPONENTS ##########################

class Population(List[Demographic], RegisteredComponent):
    def serialize(self):
        _dict = {}
        for demo in self:
            _dict[demo.race] = demo.as_dict()

        return _dict

    @classmethod
    def deserialize(cls, serialized):
        return cls(*serialized)


class Details(RegisteredComponent):
    def __init__(self, name: str):
        self.kingdom_name = name

    def serialize(self):
        return self.kingdom_name

    @classmethod
    def deserialize(cls, serialized):
        return cls(*serialized)

class Demesne(List[Land], RegisteredComponent):
    def serialize(self):
        _dict = {}
        for land in self:
            _dict[land.name] = land.as_dict()

        return _dict

    @classmethod
    def deserialize(cls, serialized):
        return cls(*serialized)


class IsPlayerControlled(RegisteredComponent):
    __slots__ = ()

    def serialize(self):
        return True

    @classmethod
    def deserialize(cls, serialized):
        return cls(*serialized)


class CastleStaff(List[StaffMember], RegisteredComponent):
    def serialize(self):
        _dict = {}
        for staff_member in self:
            _dict[staff_member.name] = staff_member.as_dict()

        return _dict

    @classmethod
    def deserialize(cls, serialized):
        return cls(*serialized)


class Hourglass(RegisteredComponent):
    def __init__(self):
        self.minutes_available = MINUTES_IN_DAY

    def serialize(self):
        return self.minutes_available

    @classmethod
    def deserialize(cls, serialized):
        return cls(*serialized)
