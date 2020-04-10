from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from snecs import Component
from snecs.typedefs import EntityID

from scripts import world

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


def log_component_not_found(entity: EntityID, component: Type[Component]):
    """
    Use if component not found. Log the error as a warning in the format '{entity} tried to get {component} but it was
    not found.'
    """
    name = world.get_name(entity)
    logging.warning(f"'{name}'({entity}) tried to get {component.__name__}, but it was not found.")

