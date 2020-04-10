from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Type

import pygame

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List, Callable
    from pygame_gui import UIManager
    from pygame.rect import Rect
    from pygame_gui.core import UIElement


class Screen(ABC):
    def __init__(self, manager: UIManager, rect: Rect):
        self.manager: UIManager = manager
        self.rect: Rect = rect
        self.elements: Dict[str, UIElement] = {}
        self.options: Dict[str, Tuple[str, Callable]] = {}

    def handle_event(self, event: pygame.event.Event):
        pass

    def kill(self):
        elements = self.elements
        for name, element in elements.items():
            element.kill()
        self.elements = {}
