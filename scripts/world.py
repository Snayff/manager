from __future__ import annotations

import logging

import snecs
from typing import TYPE_CHECKING, Type, TypeVar
from snecs import Component, Query, new_entity
from snecs.typedefs import EntityID
from scripts import debug
from scripts.components import CastleStaff, Demesne, Details, Edicts, Hourglass, IsPlayerControlled, Knowledge, \
    Population, Resources
from scripts.constants import BIRTH_RATE, DAYS_IN_SEASON, DAYS_IN_YEAR, SEASONS_IN_YEAR
from scripts.demographics import Demographic
from scripts.edicts import Edict
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


def create_kingdom() -> EntityID:
    """
    Create a basic kingdom with empty components
    """
    default_components = [
        IsPlayerControlled(),
        CastleStaff([]),
        Hourglass(),
        Edicts(["conscription"]),
        Knowledge(),
        Resources()
    ]

    kingdom = create_entity(default_components)

    # update their knowledge so they have accurate info at the start
    update_entitys_knowledge(kingdom, "all")

    return kingdom


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


def get_all_demographics() -> Dict[str, Type[Demographic]]:
    """
    Get the base data for all races
    """
    return world_data.races


def get_demographic(race_key: str) -> Type[Demographic]:
    """
    Get the base data for a race
    """
    return world_data.races[race_key]


def get_edict(edict_key: str) -> Type[Edict]:
    """
    Get the base data for an edict
    """
    return world_data.edicts[edict_key]


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


def get_days_passed() -> int:
    """
    Get the number of days passed since world inception.
    """
    return world_data.days_passed


def get_modified_stat(entity: EntityID, stat: str, base_value: Union[int, float]) -> Union[int, float]:
    """
    Modifies a stat by all applicable edicts
    """
    edicts = get_entitys_component(entity, Edicts)
    environment = {stat: base_value}

    for edict in edicts.active_edicts:
        if BIRTH_RATE in edict.affects:
            edict.apply(environment)

    return environment[stat]


def get_land_size_modifier(size: str) -> float:
    """
    Get the numeric modifier value from the size string
    """
    return world_data.land_sizes[size]


def get_days_since(day: int) -> int:
    """
    Get the number of days since the day given
    """
    return world_data.days_passed - day


################################ SET - AMEND AN EXISTING SOMETHING ###############################

def set_days_passed(days_passed: int):
    """
    Set the amount of days passed
    """
    world_data.days_passed = days_passed


################################ CHECKS - RETURN BOOL ###############################

def can_afford_time_cost(entity: EntityID, hours_to_spend: float = 1.0):
    hourglass = get_entitys_component(entity, Hourglass)
    if hourglass.hours_available > hours_to_spend:
        return True
    else:
        return False


################################ ACTIONS - CHANGE STATE - RETURN NOTHING ###############################

def add_component(entity: EntityID, component: Component):
    """
    Add a component to the entity
    """
    snecs.add_component(entity, component)


def progress_days(days: int = 1):
    """
    Move time forwards by days
    """
    world_data.days_passed += days


def spend_daytime(entity: EntityID, hours_spent: float = 1):
    hourglass = get_entitys_component(entity, Hourglass)
    hourglass.hours_available = max(0.0, hourglass.hours_available - hours_spent)


def update_entitys_knowledge(entity: EntityID, new_knowledge: str):
    """
    Update an entity's knowledge to reflect the accurate and up to date information
    """
    knowledge = get_entitys_component(entity, Knowledge)
    current_day = get_days_passed()

    if new_knowledge == "resources" or new_knowledge == "all":
        resources = get_entitys_component(entity, Resources)

        knowledge.vittles = resources.vittles
        knowledge.wealth = resources.wealth
        knowledge.raw_materials = resources.raw_materials
        knowledge.refined_materials = resources.refined_materials
        knowledge.commodities = resources.commodities

        knowledge.resource_update_day = current_day

    elif new_knowledge == "demesne" or new_knowledge == "all":
        demesne = get_entitys_component(entity, Demesne)

        knowledge.demesne = demesne

        knowledge.demesne_update_day = current_day

    elif new_knowledge == "population" or new_knowledge == "all":
        population = get_entitys_component(entity, Population)

        knowledge.population = population

        knowledge.population_update_day = current_day

    else:
        logging.warning(f"Knowledge not updated as given unexpected key, '{new_knowledge}'.")
