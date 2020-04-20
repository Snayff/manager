from __future__ import annotations

import attr
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type
from snecs.typedefs import EntityID

from scripts.constants import BIRTH_RATE

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


@attr.s(auto_attribs=True)
class Edict(ABC):
    # N.B. do not specify type as doing so makes it a instance variable and we need class variable
    owning_entity: int
    key = "not specified"
    name = "not specified"
    enact_description = "not specified"
    revoke_description = "not specified"
    affects = []

    @classmethod
    @abstractmethod
    def is_requirement_met(cls, entity: EntityID) -> bool:
        """
        Confirm if requirement for the edict is met.
        """
        raise NotImplementedError

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
    birth_reduction_rate = 0.12

    @classmethod
    def is_requirement_met(cls, entity: EntityID) -> bool:
        # no requirements, always true
        return True

    def enact(self) -> str:
        return f"Birthrate decreased by {str(self.birth_reduction_rate)}."

    def revoke(self) -> str:
        return f"Birthrate no longer decreased by {str(self.birth_reduction_rate)}."

    def apply(self, environment: Dict[str, Union[int, float]]):
        environment[BIRTH_RATE] = environment[BIRTH_RATE] * (1 - self.birth_reduction_rate)


