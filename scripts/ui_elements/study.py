from __future__ import annotations

from typing import TYPE_CHECKING, Type
from scripts import ui, world
from scripts.components import Edicts
from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame_gui import UIManager
    from pygame.rect import Rect
    from pygame.event import Event

class StudyScreen(Screen):
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)

        self.header_text = "Your Private Study"

        self.setup_default_screen()



    def handle_event(self, event: Event):
        """
        Handle events
        """
        # get the id
        object_id = self.get_object_id(event)

        # check if the message window has been dismissed
        if "message_window" in object_id:
            # refresh the screen
            self.setup_default_screen()

        #  ensure we didnt select a dodgy option
        if self.is_option_implemented(object_id):
            if self.showing == "study":
                if object_id == "antechamber":
                    self.call_options_function(object_id)

                # if the second element of the tuple (possible) is True
                elif self.options[object_id][1]:
                    # add the edict
                    self.toggle_edict(object_id)

    def setup_default_screen(self):
        """
        Show the default screen layout
        """
        # clear existing elements
        self.kill()

        # set the flag
        self.showing = "study"

        # clear options
        self.options = {
            "antechamber": ui.Option("Anteroom - Return", ui.swap_to_antechamber_screen),
        }

        # get possible edicts and set as options
        player_kingdom = world.get_player_kingdom()
        edicts = world.get_entitys_component(player_kingdom, Edicts)
        for edict_name in edicts.known_edicts:
            edict = world.get_edict(edict_name)

            # is it active?
            if edict in edicts.active_edicts:
                possible = True
                prefix = "Revoke "
                description = edict.revoke_description
            elif edict.is_requirement_met(player_kingdom):
                # not active but possible
                possible = True
                prefix = "Enact "
                description = edict.enact_description
            else:
                possible = False
                prefix = "[Requirement not met]"
                description = edict.enact_description

            self.options[edict_name] = ui.Option(prefix + edict_name + " - " + description, possible, )

        # create the info text
        info_text = "You rifle through your scattered parchments, hearing the crack of old vellum with each wave of "\
                    "your arm. It is time to continue work on your vision."

        # create the screen
        self.create_header(self.header_text)
        self.create_info_section(self.info_x, self.post_header_y, self.info_width, self.half_max_section_height,
                                 info_text)
        self.create_option_section(self.button_x, self.option_text_x,
                                   self.post_header_y + self.half_max_section_height,
                                   self.button_width, self.button_height, self.option_text_width,
                                   self.half_max_section_height)
        self.create_choice_field(allowed_str=False)

    def toggle_edict(self, edict_name):
        """
        Enact or revoke an edict.
        """
        player_kingdom = world.get_player_kingdom()
        edicts = world.get_entitys_component(player_kingdom, Edicts)
        edict = world.get_edict(edict_name)
        edict = edict(owning_entity=player_kingdom)  # This is throwing an unexpected arg error but is right.

        if edict in edicts.active_edicts:
            msg = edict.revoke()
            outcome = "rescinded"
            edicts.active_edicts.remove(edict)
        else:
            msg = edict.enact()
            edicts.active_edicts.append(edict)
            outcome = "proclaimed"

        self.create_message(msg, "Edict " + outcome)
