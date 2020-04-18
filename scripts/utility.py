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
        if member[:2] != "__":
            members.append(member)

    return members
