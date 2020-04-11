from __future__ import annotations

from typing import TYPE_CHECKING, Type

import pygame
from pygame_gui.elements import UIButton, UILabel, UITextBox

from scripts import world
from scripts.components import Details, IsPlayerControlled, Lands, Population
from scripts.constants import LINE_BREAK
from scripts.ui_elements.screen import Screen
from pygame.rect import Rect

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame_gui import UIManager


class CouncilScreen(Screen):
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)
        self.options["Something"] = ("something else", None)

        # get info text
        info_text = ""
        player_kingdom = world.get_player_kingdom()

        details = world.get_entitys_component(player_kingdom, Details)
        info_text += details.kingdom_name + LINE_BREAK

        population = world.get_entitys_component(player_kingdom, Population)
        for demo in population:
            info_text += demo.race + ": " + str(demo.amount) + "( " + str(demo.birth_rate) + " per year)" + \
                         LINE_BREAK

        lands = world.get_entitys_component(player_kingdom, Lands)
        for land in lands:
            info_text += land.name + ": " + land.size

        # create the screen
        self.create_header("Your Council")
        self.create_info_section(self.info_x, self.post_header_y, self.info_width, self.half_max_section_height,
                                 info_text)
        self.create_option_section(self.button_x, self.option_text_x, self.post_header_y + self.half_max_section_height,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field()

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

