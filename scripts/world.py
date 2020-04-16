from __future__ import annotations

import snecs
from typing import TYPE_CHECKING, Type, TypeVar
from snecs import Component, Query, new_entity
from snecs.typedefs import EntityID
from scripts import debug
from scripts.components import Details, IsPlayerControlled
from scripts.constants import DAYS_IN_SEASON, SEASONS_IN_YEAR
from scripts.stores.world_data import world_data

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


def get_all_race_data() -> Dict[str, Dict[str, Union[int, str]]]:
    """
    Get the base data for all races
    """
    return world_data.races


def get_race_data(race_name: str) -> Dict[str, Union[int, str]]:
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


################################ ACTIONS - CHANGE STATE - RETURN NOTHING ###############################

def add_component(entity: EntityID, component: Component):
    """
    Add a component to the entity
    """
    snecs.add_component(entity, component)


def pass_time(days: int = 0, seasons: int = 0, years: int = 0):
    """
    Move time forwards by days, seasons and or years
    """
    seasons_to_add = 0
    years_to_add = 0

    # add days to the calendar
    if days > 0:
        seasons_to_add = (days + world_data.day) / DAYS_IN_SEASON
        if seasons_to_add > 1:
            # get the remainder and convert to days
            new_day_value = (seasons_to_add % 1) * 100
            world_data.day = new_day_value
        else:
            world_data.day += days

    # add seasons to the calendar
    seasons_to_add = int(seasons_to_add)  # remove the decimals
    if seasons + seasons_to_add > 0:
        years_to_add = (seasons + seasons_to_add + world_data.season) / SEASONS_IN_YEAR
        if years_to_add > 1:
            new_season_value = (years_to_add % 1) * 100
            world_data.season = new_season_value
        else:
            world_data.season += seasons

    # add years to the calendar
    years_to_add = int(years_to_add)  # remove the decimals
    if years + years_to_add > 0:
        world_data.year += years + years_to_add
