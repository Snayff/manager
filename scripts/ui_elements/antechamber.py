from __future__ import annotations

from typing import TYPE_CHECKING, Type
from scripts import processors, ui
from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame_gui import UIManager, UI_BUTTON_PRESSED
    from pygame.rect import Rect
    from pygame.event import Event


class AntechamberScreen(Screen):
    """
    Initial screen for player. Show main options.
    """
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)

        self.setup_default_screen()

    def handle_event(self, event: Event):
        """
        Handle input events
        """
        # get the id
        object_id = self.get_object_id(event)

        # buttons presses
        if event.user_type == UI_BUTTON_PRESSED:
            #  ensure we didnt select a dodgy option
            if self.is_option_implemented(object_id):
                self.call_options_function(object_id)

    def setup_default_screen(self):
        """
        Set up the default screen
        """
        # clear existing elements
        self.kill()

        # set the flag
        self.showing = "antechamber"

        self.options = {
            "council": ui.Option("Council Room - Meet with your council", ui.swap_to_council_screen),
            "host": ui.Option("*Throne Room - Host petitioners", None),
            "search": ui.Option("*Cartographer's Display - Search for new lands", None),
            "edict": ui.Option("Study - Proclaim an edict", ui.swap_to_study_screen),
            "military": ui.Option("*Cartographer's Display - Military action", None),
            "construction": ui.Option("*Rookery - Demand construction", None),
            "diplomats": ui.Option("*Rookery - Instruct diplomats", None),
            "spy": ui.Option("*Rookery - Spy Network", None),
            "end_day": ui.Option("Chambers - End the day", self.end_day)
        }
        # TODO - combine duplicate instructions

        # create the screen
        self.create_header("Antechamber")
        self.create_option_section(self.button_x, self.option_text_x, self.post_header_y, self.button_width,
                                   self.button_height, self.option_text_width, self.max_section_height)
        self.create_choice_field(allowed_str=False)
        self.create_hourglass_display()

    def end_day(self):
        """
        Trigger the processors and refresh the screen
        """
        processors.process_end_of_day()
        self.setup_default_screen()
