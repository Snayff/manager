from __future__ import annotations

import logging
from abc import ABC
from typing import TYPE_CHECKING, Type, List

import attr
from snecs import RegisteredComponent

from scripts import utility
from scripts.constants import DAYS_IN_YEAR, MINUTES_IN_DAY

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict


################## CLASSES USED IN COMPONENTS ##############################
# @attr.s
# class Test:
#     x = attr.ib()
#
# test = Test(x=1)

# class ComponentElement:
#     """
#     Base class of any class that will be contained in a Component
#     """
#     def as_dict(self):
#         """
#         Return all members as a dict. Needs the
#         """
#         class_members = utility.get_members(self)
#         _dict = {}
#
#         for member in class_members:
#             _dict[member] = getattr(self, member)
#
#         return _dict
@attr.s
class Demographic:
    """
    Details about a section of the population.
    """
    name: str = attr.ib()
    homeworld: str = attr.ib()
    amount: int = attr.ib()
    birth_rate: float = attr.ib()
    min_brood: int = attr.ib()
    max_brood: int = attr.ib()
    lifespan: float = attr.ib()

    accrued_deaths: float = attr.ib(default=0.0)
    accrued_births: float = attr.ib(default=0.0)

    @property
    def birth_rate_in_year(self) -> float:
        """
        How many will approximately be born in a year.
        """
        return (self.birth_rate * self.amount) * (max(self.max_brood - self.min_brood, 1))


@attr.s
class Land:
    """
    Details about a section of the world.
    """
    name: str = attr.ib()
    terrain: str = attr.ib()
    size: str = attr.ib()


@attr.s
class StaffMember:
    name: str = attr.ib()
    role: str = attr.ib()
    skill: int = attr.ib()


################ COMPONENTS ##########################

class Population(List[Demographic], RegisteredComponent):
    def serialize(self):
        _dict = {}
        for demo in self:
            _dict[demo.name] = attr.asdict(demo)

        return _dict

    @classmethod
    def deserialize(cls, serialized):
        demo_list = []

        for key, demo in serialized.items():
            demo_list.append(Demographic(**demo))

        return Population(demo_list)


class Details(RegisteredComponent):
    def __init__(self, name: str):
        self.kingdom_name = name

    def serialize(self):
        return self.kingdom_name

    @classmethod
    def deserialize(cls, serialized):
        return Details(serialized)

class Demesne(List[Land], RegisteredComponent):
    def serialize(self):
        _dict = {}
        for land in self:
            _dict[land.name] = attr.asdict(land)

        return _dict

    @classmethod
    def deserialize(cls, serialized):
        land_list = []
        for key, land in serialized.items():
            land_list.append(Land(**land))
        return Demesne(land_list)


class IsPlayerControlled(RegisteredComponent):
    __slots__ = ()

    def serialize(self):
        return True

    @classmethod
    def deserialize(cls, serialized):
        return ()


class CastleStaff(List[StaffMember], RegisteredComponent):
    def serialize(self):
        _dict = {}
        for staff_member in self:
            _dict[staff_member.name] = attr.asdict(staff_member)

        return _dict

    @classmethod
    def deserialize(cls, serialized):
        staff_list = []
        for key, staff_member in serialized.items():
            staff_list.append(StaffMember(**staff_member))
        return CastleStaff(staff_list)


class Hourglass(RegisteredComponent):
    def __init__(self, minutes_available: int = MINUTES_IN_DAY):
        self.minutes_available = minutes_available

    def serialize(self):
        return self.minutes_available

    @classmethod
    def deserialize(cls, serialized):
        return Hourglass(serialized)

