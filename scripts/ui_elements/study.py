from __future__ import annotations

from typing import TYPE_CHECKING, Type

from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame_gui import UIManager
    from pygame.rect import Rect

class StudyScreen(Screen):
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)
        self.options = {
        }