from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


def get_members(cls: Union[Any, Type[Any]]) -> List[str]:
    """
    Get a class' members, excluding special methods e.g. anything prefixed with '__'. If passed a class returns
    class attributes only. If passed an instances returns all members of that instance.
    """
    members = []

    for member in cls.__dict__.keys():
        # check it is not a dunder method
        if member[:2] != "__":
            # check it isnt a method or function
            if not hasattr(member, "__call__"):
                members.append(member)

    return members


def lerp(initial_value: float, target_value: float, lerp_fraction: float) -> float:
    """
    Linear interpolation between initial and target by amount. Fraction clamped between 0 and 1.
    """
    clamped_lerp_fraction = clamp(lerp_fraction, 0, 1)

    if clamped_lerp_fraction >= 0.99:
        return target_value
    else:
        return initial_value * (1 - clamped_lerp_fraction) + target_value * clamped_lerp_fraction


def clamp(value, min_value, max_value):
    """
    Return the value, clamped between min and max.
    """
    return max(min_value, min(value, max_value))