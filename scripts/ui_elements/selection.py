from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

import pygame
import pygame_gui
from pygame.rect import Rect
from pygame_gui import UIManager

from scripts import world
from scripts.components import Demographic, Population
from scripts.constants import LINE_BREAK
from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


class SelectionScreen(Screen):
    """
    Handle selection of race and location
    """
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)

        self.selecting = ""  # flag to determine what action happens on press
        self.options = {}  # remove goto council
        self.header_text = "On the other side of the Rift"

        self.setup_select_race()

    def handle_event(self, event: pygame.event.Event):
        # N.B. no call to super.

        object_id = event.ui_object_id.replace("options.", "")

        # options
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            prefix = self.options[object_id][0][:1]
            if prefix == "*":
                logging.warning(f"Clicked {object_id}, which is not implemented. Took no action.")
            else:
                if self.selecting == "race":
                    self.add_race(object_id)
                    self.setup_select_land()
                elif self.selecting == "land":
                    self.add_land(object_id)

    ############################ SETUP ##############################

    def setup_select_race(self):
        """
        Set up the screen for selection race
        """
        # clear existing elements
        self.kill()

        # set the flag
        self.selecting = "race"

        info_text = "You open your eyes and blink into the uneven, unexpected light of the new world. Not sure who " \
                    "else survived the journey through the Rift you look around."+ LINE_BREAK

        # get races
        races = world.get_all_race_data()
        for name, race in races.items():
            self.options[name] = (f"{str(race['amount'])} {name}s from {race['homeworld']}.", None)

        # create the screen
        self.create_header(self.header_text)
        self.create_info_section(self.info_x, self.post_header_y, self.info_width, self.half_max_section_height,
                                 info_text)
        self.create_option_section(self.button_x, self.option_text_x,
                                   self.post_header_y + self.half_max_section_height,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field()

    def setup_select_land(self):
        """
        Set up the screen for selection race
        """
        # clear existing elements
        self.kill()

        # set the flag
        self.selecting = "land"

        info_text = "You remember. Clearly, and painfully. But there is no time to mourn, we must move on from this" \
                    " desolate place" + LINE_BREAK

        # create lands
        self.options["north"] = (f"To the north is scrub.", None)
        self.options["south"] = (f"To the south is more scrub.", None)

        # create the screen
        self.create_header(self.header_text)
        self.create_info_section(self.info_x, self.post_header_y, self.info_width, self.half_max_section_height,
                                 info_text)
        self.create_option_section(self.button_x, self.option_text_x,
                                   self.post_header_y + self.half_max_section_height,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field()

    ############################ CHOICES ##############################

    def add_race(self, race_name: str):
        """
        Add the race component to the player"""
        player_kingdom = world.get_player_kingdom()
        race_data = world.get_race_data(race_name)
        world.add_component(player_kingdom, Population([Demographic(race_data)]))

        # Details("My Kingdom"),
        # Population([Demographic("Goblin", 100, 2, 1, 2)]),
        # Lands([Land("The Homeland", "small", "muddy", []), Land("Black Moor", "average", "grass", [])]),
        # CastleStaff([])

