from __future__ import annotations

import attr
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type
from snecs.typedefs import EntityID
from scripts import utility, world
from scripts.constants import BIRTH_RATE, LINE_BREAK

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


@attr.s(auto_attribs=True)
class Edict(ABC):
    # N.B. do not specify type as doing so makes it a instance variable and we need class variable
    owning_entity: int
    key = "not specified"  # internal key used
    name = "not specified"  # name shown
    enact_description = "not specified"  # desc shown when turned on
    revoke_description = "not specified"  # desc shown when turned off
    affects = []  # stats affected
    init_days_per_land = 0  # days required per land

    # instance vars
    day_changed: int = 0  # the day it was enacted or revoked

    @classmethod
    @abstractmethod
    def is_requirement_met(cls, entity: EntityID) -> bool:
        """
        Confirm if requirement for the edict is met.
        """
        raise NotImplementedError

    @classmethod
    def get_ramp_up_duration(cls, entity: EntityID):
        from scripts.components import Demesne
        demesne = world.get_entitys_component(entity, Demesne)
        num_lands = len(demesne)
        mod = 0

        # get all size modifiers
        for land in demesne:
            mod += world.get_land_size_modifier(land.size)

        # avg times time needed
        duration = (num_lands / mod) * cls.init_days_per_land

        return duration

    @abstractmethod
    def enact(self) -> str:
        """
        Process any effects triggered from enacting
        """
        pass

    @abstractmethod
    def revoke(self) -> str:
        """
        Process any effects triggered from revoking
        """
        pass

    @abstractmethod
    def apply(self, environment: Dict[str, Union[int, float]]):
        """
        Apply the edict's modifiers
        """
        raise NotImplementedError


@attr.s(auto_attribs=True)
class Conscription(Edict):
    key = "conscription"
    name = "Conscription"
    enact_description = "Put their bodies to work in our service."
    revoke_description = "Return them to the fields and homes."
    affects = [BIRTH_RATE]
    init_days_per_land = 2

    # class specific vars
    birth_reduction_rate = 0.12


    @classmethod
    def is_requirement_met(cls, entity: EntityID) -> bool:
        # no requirements, always true
        return True

    def enact(self) -> str:
        # set day enacted
        self.day_changed = world.get_current_date()[0]

        # build confirmation message
        duration = self.get_ramp_up_duration(self.owning_entity)
        msg = f"Conscription will need {duration} days to take full effect. At that point:" + LINE_BREAK
        msg += f"Birthrate decreased by: {str(self.birth_reduction_rate)}."

        return msg

    def revoke(self) -> str:
        # update day changed
        self.day_changed = world.get_current_date()[0]

        duration = self.get_ramp_up_duration(self.owning_entity)
        msg = f"Conscription will take {duration} days to take full effect. At that point:" + LINE_BREAK
        msg += f"Birthrate will no longer be decreased by: {str(self.birth_reduction_rate)}."

        return msg

    def apply(self, environment: Dict[str, Union[int, float]]):
        ramp_duration = self.get_ramp_up_duration(self.owning_entity)
        days_since = world.get_days_since(self.day_changed)

        # handle divide by 0
        if days_since > 0:
            ramp_up_mod = min(1 - (days_since / ramp_duration), 1.0)
        else:
            ramp_up_mod = 0

        # modify base rate by amount of ramp up completed
        modified_birth_rate = utility.lerp(0, self.birth_reduction_rate, ramp_up_mod)

        new_birth_rate = environment[BIRTH_RATE] * (1 - modified_birth_rate)
        environment[BIRTH_RATE] = new_birth_rate

