from __future__ import annotations

import attr
from abc import abstractmethod
from typing import TYPE_CHECKING, Type
from snecs.typedefs import EntityID
from scripts import world

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List

@attr.s
class Edict:
    name: str = attr.ib(default="not specified")

    @abstractmethod
    def enact(self, entity: EntityID):
        raise NotImplementedError

    @abstractmethod
    def revert(self, entity: EntityID):
        raise NotImplementedError


@attr.s
class Conscription(Edict):
    name = "conscription"

    def enact(self, entity: EntityID):
        birth_reduction_rate = 0.12

        from scripts.components import Population
        pop = world.get_entitys_component(entity, Population)

        for demo in pop:
            demo.birth_rate = demo.birth_rate - (demo.birth_rate * birth_reduction_rate)

