from __future__ import annotations

import attr
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type
from scripts import world

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


@attr.s(auto_attribs=True)
class Edict(ABC):
    owning_entity: int
    name: str = "not specified"
    enact_description: str = "not specified"
    revoke_description: str = "not specified"
    affects: List[str] = []

    @abstractmethod
    def is_requirement_met(self) -> bool:
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
    def apply(self) -> str:
        """
        Apply the edict's modifiers
        """
        raise NotImplementedError


@attr.s(auto_attribs=True)
class Conscription(Edict):
    name: str = "conscription"
    enact_description: str = "Put their bodies to work in our service."
    revoke_description: str = "Return them to the fields and their homes."
    affects: List[str] = ["birth_rate"]
    birth_reduction_rate: float = 0.12

    def is_requirement_met(self) -> bool:
        # no requirements, always true
        return True

    def enact(self) -> str:
        return f"Birthrate decreased by {str(self.birth_reduction_rate)}."

    def revoke(self) -> str:
        pass

    def apply(self):
        # TODO - this needs to be integrated
        birth_reduction_rate = 0.12

        from scripts.components import Population
        pop = world.get_entitys_component(self.owning_entity, Population)

        for demo in pop:
            demo.birth_rate = demo.birth_rate - (demo.birth_rate * birth_reduction_rate)

