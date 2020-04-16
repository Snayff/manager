from __future__ import annotations

import logging
from typing import TYPE_CHECKING
import pygame
from pygame_gui import UIManager
from scripts.constants import BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT
from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


class _UIDataStore:
    """
    Manage the UI, such as windows, resource bars etc
    """

    def __init__(self):
        # first action needs to be to init pygame.
        pygame.init()

        #  set the display
        self.desired_width = BASE_WINDOW_WIDTH
        self.desired_height = BASE_WINDOW_HEIGHT
        self._screen_scaling_mod_x = self.desired_width // BASE_WINDOW_WIDTH
        self._screen_scaling_mod_y = self.desired_height // BASE_WINDOW_HEIGHT
        self.window: pygame.display = pygame.display.set_mode((self.desired_width, self.desired_height))
        self.main_surface: pygame.Surface = pygame.Surface((BASE_WINDOW_WIDTH,
                                                            BASE_WINDOW_HEIGHT), pygame.SRCALPHA)

        # hold ref to all current elements
        self.elements: Dict[str, Screen] = {}
        self.new_elements: Dict[str, Screen] = {}
        self.focused_element_name: str = ""
        self.element_keys_to_delete: List[Optional[str]] = []

        # now that the display is configured  init the pygame_gui
        self.gui = UIManager((BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT), "../../themes.json")

        # process config
        pygame.display.set_caption("Kingdom Manager")

        logging.info(f"_UIDataStore initialised.")


ui_data = _UIDataStore()
