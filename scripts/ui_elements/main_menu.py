from __future__ import annotations

import os
from typing import TYPE_CHECKING, Type
from scripts import state, ui
from scripts.components import CastleStaff, Edicts, Hourglass, IsPlayerControlled
from scripts.constants import EXIT, SAVE_PATH
from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame.rect import Rect
    from pygame_gui import UIManager
    import pygame


class MainMenuScreen(Screen):
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)

        self.setup_main_menu()

    def handle_event(self, event: pygame.event.Event):
        """
        Handle events
        """
        # get the id
        object_id = self.get_object_id(event)

        # if we selected a dodgy option, do nothing
        if not self.is_option_implemented(object_id):
            return None

        if self.showing == "main_menu":
            self.call_options_function(object_id)
        elif self.showing == "load":
            self.init_load_game(object_id)


    def setup_main_menu(self):
        """
        Show the default screen layout
        """
        # clear existing elements
        self.kill()

        # set the flag
        self.showing = "main_menu"

        # set options
        self.options = {
            "new_game": ("New game", self.init_new_game),
            "init_load_game": ("Load game", self.setup_load_game),
            "settings": ("* Settings", None),
            "exit_game": ("Exit game", self.exit_game)
        }

        # create the screen
        self.create_option_section(self.button_x, self.option_text_x,
                                   self.post_header_y,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field(allowed_str=False)

    def setup_load_game(self):
        """
        Show all save files
        """
        # clear existing elements
        self.kill()

        # set the flag
        self.showing = "load"

        self.options = {
            "cancel": ("Go Back", self.setup_main_menu),
        }

        # get all save files as options
        for filename in os.listdir(os.getcwd() + "/" + SAVE_PATH):
            filename = filename.replace(".json", "")
            self.options[filename] = (filename, None)

        # create the screen
        self.create_option_section(self.button_x, self.option_text_x,
                                   self.post_header_y,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field(allowed_str=False)

    def init_new_game(self):
        """
        Create new game data and swap to selection screen
        """
        # create the player entity
        components = [
            IsPlayerControlled(),
            CastleStaff([]),
            Hourglass(),
            Edicts(["conscription"])
        ]
        from scripts import world
        player_kingdom = world.create_entity(components)

        ui.swap_to_selection_screen()

    def init_load_game(self, filename: str):
        """
        Load the game data for the selected filename, and swap to antechamber screen
        """
        state.load_game(filename)

        ui.swap_to_antechamber_screen()

    def exit_game(self):
        """
        Change the game state to EXIT
        """
        state.set_new(EXIT)
