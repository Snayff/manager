from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

import snecs
from snecs import Component, Query, new_entity
from snecs.typedefs import EntityID

from scripts import debug
from scripts.components import Details, IsPlayerControlled

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


_C = TypeVar("_C", bound=Component)


################################ CREATE - INIT OBJECT - RETURN NEW OBJECT ###############################
get_entitys_components = snecs.all_components
get_components = Query
has_component = snecs.has_component


def create_entity(components: List[Component] = None) -> EntityID:
    """
    Use each component in a list of components to create_entity an entity
    """
    if components is None:
        _components = []
    else:
        _components = components

    # create the entity
    entity = new_entity(_components)

    return entity


############################# GET - RETURN AN EXISTING SOMETHING ###########################

def get_player_kingdom() -> EntityID:
    """
    Get the player.
    """
    for entity, (flag,) in get_components([IsPlayerControlled]):
        return entity
    raise ValueError


def get_entitys_component(entity: EntityID, component: Type[_C]) -> _C:
    """
    Get an entity's component. Log if component not found.
    """
    if has_component(entity, component):
        return snecs.entity_component(entity, component)
    else:
        debug.log_component_not_found(entity, component)
        raise Exception


def get_name(entity: EntityID) -> str:
    """
    Get an entity's Identity component's name.
    """
    identity = get_entitys_component(entity, Details)
    if identity:
        name = identity.kingdom_name
    else:
        name = "not found"

    return name