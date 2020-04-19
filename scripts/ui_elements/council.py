from __future__ import annotations

from typing import TYPE_CHECKING, Type

from snecs.typedefs import EntityID

from scripts import ui, world
from scripts.components import CastleStaff, Details, Edicts, IsPlayerControlled, Demesne, Population
from scripts.constants import LINE_BREAK
from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame_gui import UIManager
    from pygame.rect import Rect
    from pygame.event import Event


class CouncilScreen(Screen):
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)

        self.header_text = "Your Council Chambers"

        self.setup_default_screen()



    def handle_event(self, event: Event):
        # get the id
        object_id = self.get_object_id(event)

        # check if the message window has been dismissed
        if "message_window" in object_id:
            # refresh the screen
            self.setup_default_screen()

        # ensure we didnt select a dodgy option
        if self.is_option_implemented(object_id):
            self.call_options_function(object_id)


    def setup_default_screen(self):
        self.options = {
            "antechamber": ("Anteroom - Return", ui.swap_to_antechamber_screen),
            "hire": ("* View the Rolls - Hire Staff", None)
        }

        # prep to build info text
        info_text = ""
        player_kingdom = world.get_player_kingdom()

        # current date and kingdom name
        info_text += self.get_intro_section_text(player_kingdom)

        # new section: subjects
        info_text += LINE_BREAK + LINE_BREAK
        info_text += self.get_population_section_text(player_kingdom)

        # new section: land
        info_text += LINE_BREAK + LINE_BREAK
        info_text += self.get_demesne_section_text(player_kingdom)

        # new section: staff
        info_text += LINE_BREAK + LINE_BREAK
        info_text += self.get_staff_section_text(player_kingdom)

        # new section: active edicts
        info_text += LINE_BREAK + LINE_BREAK
        info_text += self.get_edict_section_text(player_kingdom)

        # create the screen
        self.create_header(self.header_text)
        self.create_info_section(self.info_x, self.post_header_y, self.info_width, self.half_max_section_height,
                                 info_text)
        self.create_option_section(self.button_x, self.option_text_x,
                                   self.post_header_y + self.half_max_section_height,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field(allowed_str=False)
        self.create_hourglass_display()

    def get_intro_section_text(self, player_kingdom: EntityID) -> str:
        """
        Get the current date and kingdom name
        """

        details = world.get_entitys_component(player_kingdom, Details)
        date = world.get_current_date()
        info_text = f"It is the {str(date[0])} day, in the {str(date[1])} season, of the {str(date[2])} year in "\
                    f"{details.kingdom_name}..." + LINE_BREAK

        return info_text

    def get_population_section_text(self, player_kingdom: EntityID) -> str:
        """
        Get the population info
        """
        population = world.get_entitys_component(player_kingdom, Population)
        info_text = "-- Subjects --" + LINE_BREAK
        for demo in population:
            info_text += demo.name + ": " + str(demo.amount) + " (" + str(demo.birth_rate_in_year) + " per year), "
        return info_text

    def get_demesne_section_text(self, player_kingdom: EntityID) -> str:
        """
        Get the land info
        """
        lands = world.get_entitys_component(player_kingdom, Demesne)
        info_text = "-- Demesne --" + LINE_BREAK
        for land in lands:
            info_text += land.name + ": " + land.size + ", "
        return info_text

    def get_staff_section_text(self, player_kingdom: EntityID) -> str:
        """
        Get the staff info
        """
        info_text = "-- Staff --" + LINE_BREAK
        staff = world.get_entitys_component(player_kingdom, CastleStaff)
        for member in staff:
            info_text += member.name + ", your " + member.role + "."
        return info_text

    def get_edict_section_text(self, player_kingdom: EntityID) -> str:
        """
        Get the edict info
        """
        info_text = "-- Active Edicts --" + LINE_BREAK
        edicts = world.get_entitys_component(player_kingdom, Edicts)
        for edict in edicts.active_edicts:
            info_text += edict.name
        return info_text
