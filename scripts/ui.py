from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pygame
from pygame.rect import Rect
from scripts.constants import BASE_WINDOW_HEIGHT, BASE_WINDOW_WIDTH
from scripts.stores.ui_data import ui_data

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

    #
    #
    #
    # focused_name = ui_data.focused_element_name
    #
    # # kill everything that isnt in the focused screen
    # if ui_data.focused_element_changed:
    #     old = ui_data.elements.pop(ui_data.focused_element)
    #
    #
    #
    #
    #     new_dict = {}
    #     elements = ui_data.elements
    #
    #     for name, element in elements.items():
    #         if name != focused_name:
    #             element.kill()
    #             logging.debug(f"Killed {name} element")
    #         else:
    #             new_dict = {name: element}
    #             logging.debug(f"Created new dict for {name}.")
    #
    #     # set elements to match focus screen
    #     if new_dict:
    #         ui_data.elements = new_dict
    #         logging.debug(f"Set elements to new dict ({new_dict}).")
    #
    #     # reset flag
    #     ui_data.focused_element_changed = False
    #



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

def swap_to_overview_screen():
    """
    Show the overview screen, creating if necessary.
    """
    delete_element_next_frame(ui_data.focused_element_name)

    from scripts.ui_elements.overview import OverviewScreen
    overview = OverviewScreen(ui_data.gui, Rect((0, 0), (BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT)))
    ui_data.new_elements["overview"] = overview

    set_focused_element("overview")


def swap_to_council_screen():
    """
    Show the Council screen, creating if necessary.
    """
    delete_element_next_frame(ui_data.focused_element_name)

    from scripts.ui_elements.council import CouncilScreen
    council = CouncilScreen(ui_data.gui, Rect((0, 0), (BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT)))
    ui_data.new_elements["council"] = council

    set_focused_element("council")
    logging.debug("Now showing Council Screen.")



