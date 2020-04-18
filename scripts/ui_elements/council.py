from __future__ import annotations

from typing import TYPE_CHECKING, Type

import pygame

from scripts import world
from scripts.components import CastleStaff, Details, IsPlayerControlled, Demesne, Population
from scripts.constants import LINE_BREAK
from scripts.ui_elements.screen import Screen
from pygame.rect import Rect

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame_gui import UIManager


class CouncilScreen(Screen):
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)
        self.options["hire"] = ("* View the Rolls - Hire Staff", None)

        # prep to build info text
        info_text = ""
        player_kingdom = world.get_player_kingdom()

        # current date and kingdom name
        details = world.get_entitys_component(player_kingdom, Details)
        date = world.get_current_date()
        info_text += f"It is the {str(date[0])} day, in the {str(date[1])} season, of the {str(date[2])} year in " \
                     f"{details.kingdom_name}..." + LINE_BREAK

        # new section: subjects
        info_text += LINE_BREAK + LINE_BREAK
        info_text += "-- Subjects --" + LINE_BREAK

        population = world.get_entitys_component(player_kingdom, Population)
        pop_text = ""
        for demo in population:
            pop_text += demo.name + ": " + str(demo.amount) + " (" + str(demo.birth_rate_in_year) + " per year), "
        info_text += pop_text

        # new section: land
        info_text += LINE_BREAK + LINE_BREAK
        info_text += "-- Demesne --" + LINE_BREAK
        lands = world.get_entitys_component(player_kingdom, Demesne)
        land_text = ""
        for land in lands:
            land_text += land.name + ": " + land.size + ", "
        info_text += land_text

        # new section: staff
        info_text += LINE_BREAK + LINE_BREAK
        info_text += "-- Staff --" + LINE_BREAK

        # add staff info
        staff = world.get_entitys_component(player_kingdom, CastleStaff)
        for member in staff:
            info_text += member.name + ", your " + member.role + "."

        # create the screen
        self.create_header("Your Council")
        self.create_info_section(self.info_x, self.post_header_y, self.info_width, self.half_max_section_height,
                                 info_text)
        self.create_option_section(self.button_x, self.option_text_x,
                                   self.post_header_y + self.half_max_section_height,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field(allowed_str=False)
        self.create_hourglass_display()


    def handle_event(self, event: pygame.event.Event):
        # get the id
        object_id = self.get_object_id(event)

        # if we selected a dodgy option, do nothing
        if not self.is_option_implemented(object_id):
            return None

        self.call_options_function(object_id)
