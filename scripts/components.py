from __future__ import annotations

import attr
from typing import TYPE_CHECKING, List
from snecs import RegisteredComponent
from scripts.constants import HOURS_IN_DAY
from scripts.demographics import Demographic
from scripts.edicts import Edict

if TYPE_CHECKING:
    pass


################## CLASSES USED IN COMPONENTS ##############################

@attr.s(auto_attribs=True)
class Land:
    """
    Details about a section of the world.
    """
    key: str
    name: str
    terrain: str
    size: str


@attr.s(auto_attribs=True)
class StaffMember:
    key: str
    name: str
    role: str
    skill: int


################ COMPONENTS ##########################

class Population(List[Demographic], RegisteredComponent):
    def serialize(self):
        _dict = {}
        for demo in self:
            _dict[demo.key] = attr.asdict(demo)

        return _dict

    @classmethod
    def deserialize(cls, serialized):
        demo_list = []

        for key, demo_values in serialized.items():
            from scripts import world
            demo = world.get_demographic(key)

            demo_list.append(demo(**demo_values))

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
            _dict[land.key] = attr.asdict(land)

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
        return IsPlayerControlled()


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
    def __init__(self, hours_available: float = HOURS_IN_DAY):
        self.hours_available: float = hours_available

    def serialize(self):
        return self.hours_available

    @classmethod
    def deserialize(cls, serialized):
        return Hourglass(serialized)


class Edicts(RegisteredComponent):
    """
    List of known and active edicts
    """
    def __init__(self, known_edicts: List[str] = None, active_edicts: List[Edict] = None):
        if known_edicts is None:
            known_edicts = []
        if active_edicts is None:
            active_edicts = []
        self.known_edicts: List[str] = known_edicts
        self.active_edicts: List[Edict] = active_edicts

    def serialize(self):
        known_dict = {}
        active_dict = {}
        for edict_name in self.known_edicts:
            known_dict[edict_name] = edict_name

        for edict in self.active_edicts:
            active_dict[edict.name] = attr.asdict(edict)

        _dict = {
            "known_edicts": known_dict,
            "active_edicts": active_dict
        }

        return _dict

    @classmethod
    def deserialize(cls, serialized):
        known_edicts = []
        active_edicts = []

        for key, inner_dict in serialized.items():
            if key == "known_edicts":
                for edict_name in inner_dict.values():
                    known_edicts.append(edict_name)
            elif key == "active_edicts":
                for _key, edict_values in inner_dict.items():
                    from scripts import world
                    edict = world.get_edict(_key)
                    active_edicts.append(edict(**edict_values))

        return Edicts(known_edicts, active_edicts)


class Resources(RegisteredComponent):
    """
    A Kingdom's resources.
    """
    def __init__(self, vittles: int = 0, wealth: int = 0, raw_materials: int = 0, refined_materials: int = 0,
            commodities: int = 0):
        self.vittles = vittles  # used to eat and drink
        self.wealth = wealth  # used to buy stuff
        self.raw_materials = raw_materials  # used to build basic stuff
        self.refined_materials = refined_materials  # used to build better stuff
        self.commodities = commodities  # used to trade

    def serialize(self):
        return self.vittles, self.wealth, self.raw_materials, self.refined_materials, self.commodities

    @classmethod
    def deserialize(cls, serialized):
        return Resources(**serialized)
