from __future__ import annotations

from typing import TYPE_CHECKING, Type
from pygame.rect import Rect
from scripts import processors, ui
from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame_gui import UIManager


class OverviewScreen(Screen):
    """
    Initial screen for player. Show main options.
    """
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)
        self.options = {
            "council": ("Council Room - Meet with your council", ui.swap_to_council_screen),
            "host": ("*Throne Room - Host petitioners", None),
            "search": ("*Cartographer's Display - Search for new lands", None),
            "edict": ("*Study - Proclaim an edict", None),
            "military": ("*Cartographer's Display - Military action", None),
            "construction": ("*Rookery - Demand construction", None),
            "diplomats": ("*Rookery - Instruct diplomats", None),
            "spy": ("*Rookery - Spy Network", None),
            "end_day": ("Chambers - End the day", processors.process_end_of_day)
        }
        # TODO - combine duplicate instructions

        # create the screen
        self.create_header("Anteroom")
        self.create_option_section(self.button_x, self.option_text_x, self.post_header_y, self.button_width,
                                   self.button_height, self.option_text_width, self.max_section_height)
        self.create_choice_field()

