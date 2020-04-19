from __future__ import annotations

import snecs
from typing import TYPE_CHECKING, Type, TypeVar
from snecs import Component, Query, new_entity
from snecs.typedefs import EntityID
from scripts import debug
from scripts.components import Details, IsPlayerControlled
from scripts.constants import DAYS_IN_SEASON, DAYS_IN_YEAR, SEASONS_IN_YEAR
from scripts.demographics import Demographic
from scripts.stores.world_data import world_data

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


_C = TypeVar("_C", bound=Component)
get_entitys_components = snecs.all_components
get_components = Query
has_component = snecs.has_component
serialise = snecs.serialize_world
deserialise = snecs.deserialize_world
process_pending_deletions = snecs.process_pending_deletions
move_world = snecs.ecs.move_world


################################ CREATE - INIT OBJECT - RETURN NEW OBJECT ###############################

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


def get_all_race_data() -> Dict[str, Type[Demographic]]:
    """
    Get the base data for all races
    """
    return world_data.races


def get_demographic(race_name: str) -> Type[Demographic]:
    """
    Get the base data for a race
    """
    return world_data.races[race_name]


def get_all_land_data() -> Dict[str, Dict[str, str]]:
    """
    Get the base data for all lands
    """
    return world_data.lands


def get_land_data(land_name: str) -> Dict[str, str]:
    """
    Get the base data for a land
    """
    return world_data.lands[land_name]


def get_current_date() -> Tuple[int, int, int]:
    """
    Get the current day, season, year
    """
    total_days = world_data.days_passed

    current_year, days_passed_in_year = divmod(total_days, DAYS_IN_YEAR)
    current_season, current_day = divmod(days_passed_in_year, DAYS_IN_SEASON)

    # add one to season and year so they dont show as 0
    current_season += 1
    current_year += 1

    return current_day, current_season, current_year


################################ SET - AMEND AN EXISTING SOMETHING ###############################

def set_days_passed(days_passed: int):
    """
    Set the amount of days passed
    """
    world_data.days_passed = days_passed


################################ ACTIONS - CHANGE STATE - RETURN NOTHING ###############################

def add_component(entity: EntityID, component: Component):
    """
    Add a component to the entity
    """
    snecs.add_component(entity, component)


def pass_days(days: int = 1):
    """
    Move time forwards by days
    """
    world_data.days_passed += days
