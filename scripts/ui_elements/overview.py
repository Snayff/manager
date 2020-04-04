from __future__ import annotations

from typing import TYPE_CHECKING, Type

from pygame.rect import Rect
from pygame_gui import UIManager
from pygame_gui.elements import UITextBox

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List

class OverviewScreen:
    def __init__(self, manager: UIManager):
        self._elements = {}

        intro = UITextBox("Welcome to whatever this is.", Rect((20, 10), (500, 100)), manager, False, 1)

