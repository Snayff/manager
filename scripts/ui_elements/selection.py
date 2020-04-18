from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

import pygame
import pygame_gui
from scripts import ui, world
from scripts.components import Demographic, Details, Land, Demesne, Population
from scripts.constants import LINE_BREAK
from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame.rect import Rect
    from pygame_gui import UIManager

class SelectionScreen(Screen):
    """
    Handle selection of race and location
    """
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)

        self.showing = ""  # flag to determine what action happens on press
        self.options = {}  # remove goto council
        self.header_text = "On the other side of the Rift"

        self.setup_select_race()

    def handle_event(self, event: pygame.event.Event):
        """
        Handle events
        """
        # get the id
        object_id = self.get_object_id(event)

        # doesnt need object id
        if self.showing == "name":
            self.select_name(event.text)
            ui.swap_to_antechamber_screen()

        # if we selected a dodgy option, do nothing
        if not self.is_option_implemented(object_id):
            return None

        # possible options, in reverse order to prevent selection being applicable to more than one
        if self.showing == "race":
            self.select_race(object_id)
            self.setup_select_land()
        elif self.showing == "land":
            self.select_land(object_id)
            self.setup_select_kingdom_name()

    ############################ SETUP ##############################

    def setup_select_race(self):
        """
        Set up the screen for selection race
        """
        # clear existing elements
        self.kill()

        # set the flag
        self.showing = "race"

        info_text = "You open your eyes and blink into the uneven, unexpected light of the new world. Not sure who " \
                    "else survived the journey through the Rift you look around." + LINE_BREAK

        # get races
        races = world.get_all_race_data()
        for key, race in races.items():
            self.options[key] = (f"{str(race['amount'])} {race['name']}s from {race['homeworld']}.", None)

        # create the screen
        self.create_header(self.header_text)
        self.create_info_section(self.info_x, self.post_header_y, self.info_width, self.half_max_section_height,
                                 info_text)
        self.create_option_section(self.button_x, self.option_text_x,
                                   self.post_header_y + self.half_max_section_height,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field(allowed_str=False)

    def setup_select_land(self):
        """
        Set up the screen for showing land
        """
        # clear existing elements
        self.kill()

        # set the flag
        self.showing = "land"

        info_text = "You remember. Clearly, and painfully. But there is no time to mourn, we must move on from this" \
                    " desolate place" + LINE_BREAK

        # create lands
        lands = world.get_all_land_data()
        for key, land in lands.items():
            self.options[key] = (f"The {land['size']} {land['terrain']} place known as {land['name']}.", None)

        # create the screen
        self.create_header(self.header_text)
        self.create_info_section(self.info_x, self.post_header_y, self.info_width, self.half_max_section_height,
                                 info_text)
        self.create_option_section(self.button_x, self.option_text_x,
                                   self.post_header_y + self.half_max_section_height,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field(allowed_str=False)

    def setup_select_kingdom_name(self):
        """
        Set up the screen for showing name
        """
        # clear existing elements
        self.kill()

        # set the flag
        self.showing = "name"

        info_text = "You and yours have arrived. Is that despair you feel, or merely tiredness? Despite your doubt," \
                    " your people look to you for direction. Perhaps we should start with a name. " + LINE_BREAK

        # create the screen
        self.create_header(self.header_text)
        self.create_info_section(self.info_x, self.post_header_y, self.info_width, self.half_max_section_height,
                                 info_text)

        self.create_choice_field(allowed_num=False)

    ############################ CHOICES ##############################

    def select_race(self, race_name: str):
        """
        Add the race component to the player
        """
        player_kingdom = world.get_player_kingdom()
        race_data = world.get_race_data(race_name)
        world.add_component(player_kingdom, Population([Demographic(race_data)]))

    def select_land(self, land_name: str):
        """
        Add the land component to the player
        """
        player_kingdom = world.get_player_kingdom()
        land_data = world.get_land_data(land_name)
        world.add_component(player_kingdom, Demesne([Land(land_data)]))

    def select_name(self, kingdom_name: str):
        """
        Add the race component to the player
        """
        player_kingdom = world.get_player_kingdom()
        world.add_component(player_kingdom, Details(kingdom_name))

