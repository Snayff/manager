from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pygame
from pygame.rect import Rect
from scripts.constants import BASE_WINDOW_HEIGHT, BASE_WINDOW_WIDTH
from scripts.stores.ui_data import ui_data
from scripts.ui_elements.main_menu import MainMenuScreen

if TYPE_CHECKING:
    pass


######################## CORE FUNCTIONALITY - NEEDED TO RUN ###############################

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

    # delete all items
    if ui_data.element_keys_to_delete:
        for key in ui_data.element_keys_to_delete:
            element = ui_data.elements.pop(key)
            element.kill()
            logging.debug(f"Killed {key} element")
        # clear list
        ui_data.element_keys_to_delete = []

    # copy newly created elements to the main element list
    if ui_data.new_elements:
        for key, value in ui_data.new_elements.items():
            ui_data.elements[key] = value
            logging.debug(f"Moved {key} from new_elements to elements.")

        # all copied, clear dict
        ui_data.new_elements = {}


######################## ALTER - CHANGE EXISTING ELEMENTS ###############################

def set_focused_element(element_name: str):
    """
    Set the element currently being used/interacted with
    """
    ui_data.focused_element_name = element_name
    logging.debug(f"Set {element_name} as focused element.")


def delete_element_next_frame(element_name: str):
    """
    Add element name to the list of keys to be deleted next frame.
    """
    if element_name != "":
        ui_data.element_keys_to_delete.append(element_name)
        logging.debug(f"Added {element_name} to delete list.")


######################## NAVIGATION - MOVING AROUND SCREENS ###############################

def swap_to_antechamber_screen():
    """
    Show the antechamber screen
    """
    delete_element_next_frame(ui_data.focused_element_name)

    from scripts.ui_elements.antechamber import AntechamberScreen
    screen = AntechamberScreen(ui_data.gui, Rect((0, 0), (BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT)))
    ui_data.new_elements["antechamber"] = screen

    set_focused_element("antechamber")


def swap_to_council_screen():
    """
    Show the Council screen
    """
    delete_element_next_frame(ui_data.focused_element_name)

    from scripts.ui_elements.council import CouncilScreen
    screen = CouncilScreen(ui_data.gui, Rect((0, 0), (BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT)))
    ui_data.new_elements["council"] = screen

    set_focused_element("council")
    logging.debug("Now showing Council Screen.")


def swap_to_selection_screen():
    """
    Show the selection screen
    """
    delete_element_next_frame(ui_data.focused_element_name)

    from scripts.ui_elements.selection import SelectionScreen
    screen = SelectionScreen(ui_data.gui, Rect((0, 0), (BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT)))
    ui_data.new_elements["selection"] = screen

    set_focused_element("selection")
    logging.debug("Now showing Selection Screen.")


def swap_to_main_menu_screen():
    """
    Show the main menu screen
    """
    delete_element_next_frame(ui_data.focused_element_name)

    screen = MainMenuScreen(ui_data.gui, Rect((0, 0), (BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT)))
    ui_data.new_elements["main_menu"] = screen

    set_focused_element("main_menu")
    logging.debug("Now showing Main Menu Screen.")

