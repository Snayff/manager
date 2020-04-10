from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame.rect import Rect
from scripts.constants import BASE_WINDOW_HEIGHT, BASE_WINDOW_WIDTH
from scripts.stores.ui_data import ui_data

if TYPE_CHECKING:
    pass


def set_focused_element(element_name: str):
    """
    Set the element currently being used/interacted with
    """
    ui_data.focused_element_name = element_name
    ui_data.focused_element_changed = True


def show_overview_screen():
    """
    Show the overview screen, creating if necessary.
    """
    # is it init'd?
    if "overview" not in ui_data.elements:
        from scripts.ui_elements.overview import OverviewScreen
        overview = OverviewScreen(ui_data.gui, Rect((0, 0), (BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT)))
        ui_data.new_elements["overview"] = overview

    set_focused_element("overview")


def show_council_screen():
    """
    Show the Council screen, creating if necessary.
    """
    if "council" not in ui_data.elements:
        from scripts.ui_elements.council import CouncilScreen
        council = CouncilScreen(ui_data.gui, Rect((0, 0), (BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT)))
        ui_data.new_elements["council"] = council

    set_focused_element("council")


def draw():
    """
    Draw the UI.
    """
    main_surface = ui_data.main_surface

    # clear previous frame
    main_surface.fill((0, 0, 0))

    ui_data.gui.draw_ui(main_surface)

    # resize the surface to the desired resolution
    scaled_surface = pygame.transform.scale(main_surface, (ui_data.desired_width, ui_data.desired_height))
    ui_data.window.blit(scaled_surface, (0, 0))

    # update the display
    pygame.display.flip()  # make sure to do this as the last drawing element in a frame


def process_ui_event(event: pygame.event.Event):
    """
    Process input events
    """
    ui_data.gui.process_events(event)

    # make sure it is a pgui event
    if event.type == pygame.USEREVENT:
        elements = ui_data.elements

        for element in elements.values():
            element.handle_event(event)


def update(delta_time: float):
    """
    Update all ui_data elements
    """
    ui_data.gui.update(delta_time)

    # kill everything that isnt in the focused screen
    if ui_data.focused_element_changed:
        elements = ui_data.elements
        for name, element in elements.items():
            if name != ui_data.focused_element_name:
                element.kill()

    # copy newly created elements to the main element list
    if ui_data.new_elements:
        for key, value in ui_data.new_elements.items():
            ui_data.elements[key] = value

        # all copied, clear dict
        ui_data.new_elements = {}

