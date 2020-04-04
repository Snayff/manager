from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

import pygame
from pygame_gui import UIManager
from scripts.constants import BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT
from scripts.ui_elements.overview import OverviewScreen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


class _UIManager:
    """
    Manage the UI, such as windows, resource bars etc
    """

    def __init__(self):
        self.debug_font = None

        # first action needs to be to init pygame.
        pygame.init()

        #  set the display
        self._desired_width = BASE_WINDOW_WIDTH
        self._desired_height = BASE_WINDOW_HEIGHT
        self._screen_scaling_mod_x = self._desired_width // BASE_WINDOW_WIDTH
        self._screen_scaling_mod_y = self._desired_height // BASE_WINDOW_HEIGHT
        self._window: pygame.display = pygame.display.set_mode((self._desired_width, self._desired_height))
        self._main_surface: pygame.Surface = pygame.Surface((BASE_WINDOW_WIDTH,
                                                            BASE_WINDOW_HEIGHT), pygame.SRCALPHA)
        # hold ref to all current elements
        self._elements = {}

        # now that the display is configured  init the pygame_gui
        self._gui = UIManager((BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT), "themes.json")

        # process config
        pygame.display.set_caption("TBC - Manager")

        logging.info(f"UIManager initialised.")

        overview = OverviewScreen(self._gui)

    def update(self, delta_time: float):
        """
        Update all ui_manager elements
        """
        self._gui.update(delta_time)

    def process_ui_events(self, event):
        """
        Process input events
        """
        self._gui.process_events(event)

        # make sure it is a pgui event
        if event.type == pygame.USEREVENT:
            elements = self._elements

            for element in elements.values():
                element.handle_events(event)

    def draw(self):
        """
        Draw the UI.
        """
        main_surface = self._main_surface

        # clear previous frame
        main_surface.fill((0, 0, 0))

        self._gui.draw_ui(main_surface)

        # resize the surface to the desired resolution
        scaled_surface = pygame.transform.scale(main_surface, (self._desired_width, self._desired_height))
        self._window.blit(scaled_surface, (0, 0))

        # update the display
        pygame.display.flip()  # make sure to do this as the last drawing element in a frame


ui = _UIManager()
