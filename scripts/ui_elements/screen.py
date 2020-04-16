from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIPanel, UITextBox, UITextEntryLine
from pygame.rect import Rect

from scripts import ui
from scripts.constants import LINE_BREAK

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List, Callable
    from pygame_gui import UIManager
    from pygame_gui.core import UIElement


class Screen(ABC):
    # default values that dont need rect
    section_gap = 3
    line_height = 38

    # Top area
    header_x = 0
    header_y = 0
    
    header_height = 60
    post_header_y = header_height + header_y + section_gap

    # middle area selections
    section_start_x = 55
    button_x = section_start_x
    button_width = 152
    button_height = line_height
    option_text_x = section_start_x + (button_width - 3)  # 3 to have button touch on both sides
    info_x = section_start_x

    # bottom area
    choice_x = section_start_x
    choice_width = 200
    choice_height = 50

    def __init__(self, manager: UIManager, rect: Rect):
        self.manager: UIManager = manager
        self.rect: Rect = rect
        self.elements: Dict[str, UIElement] = {}
        self.options: Dict[str, Tuple[str, Callable]] = {
            "anteroom": ("Anteroom - Return", ui.swap_to_overview_screen)
        }
        
        # default values that need rect before they can be set
        self.header_width = rect.width
        self.option_text_width = rect.width - (self.option_text_x + self.section_start_x)  # account for gap on right
        self.max_section_height = rect.height - (self.post_header_y + self.choice_height + (self.section_gap * 3))
        self.half_max_section_height = self.max_section_height / 2
        self.choice_y = rect.height - self.choice_height - (self.section_gap * 2)
        self.info_width = rect.width - (self.info_x + self.section_start_x)  # account for gap on right
        
    def handle_event(self, event: pygame.event.Event):
        """
        Process events generated by this element.
        """
        object_id = event.ui_object_id.replace("options.", "")

        # options
        if object_id in self.options:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                prefix = self.options[object_id][0][:1]
                if prefix == "*":
                    logging.warning(f"Clicked {object_id}, which is not implemented. Took no action.")
                else:
                    self.options[object_id][1]()  # call the method

        if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            try:
                option = list(self.options)[int(event.text) - 1]  # -1 to offset from options starting at 1
                self.options[option][1]()  # call the method
            except KeyError:
                logging.warning(f"Key not found in options. Dodgy typing? ({event.text})")

            # clear text
            choice: UITextEntryLine = self.elements["choice"]
            choice.set_text("")
            choice.redraw()

    def kill(self):
        """
        Delete all elements from self.elements
        """
        elements = self.elements
        for name, element in elements.items():
            element.kill()
        self.elements = {}

    def create_info_section(self, x: int, y: int, width: int, height: int, text: str):
        """
        Create an information section on the screen. Called "info".
        """
        info_text = UITextBox(text, Rect((x, y), (width, height)), self.manager, False, 1)
        self.elements["info"] = info_text

    def create_option_section(self, button_x: int, text_x: int, y: int, button_width: int, button_height: int,
                                text_width: int, text_height: int):
        """
        Create an options section. Uses self.options. Creates a panel to contains buttons and text box. "options",
        [option_number] and "text".
        """
        # offsets for alignment
        offset_y = 0
        count = 1

        # to hold string from list
        options_text = ""

        # create panel to hold it all
        panel = UIPanel(Rect((button_x, y), (button_width + text_width, text_height)), 0, self.manager,
                        object_id="options")
        self.elements["panel"] = panel

        # loop options and extract text and id
        for _id, (text, _method) in self.options.items():
            options_text += text + LINE_BREAK + LINE_BREAK
            option_button = UIButton(Rect((button_x, y + offset_y), (button_width, button_height)),
                                     str(count), self.manager, object_id=_id, parent_element=panel)
            count += 1
            offset_y += button_height
            self.elements[_id] = option_button

        # add text to textbox
        options_text = UITextBox(options_text, Rect((text_x, y), (text_width, text_height)), self.manager, False, 1,
                                 parent_element=panel)
        self.elements["text"] = options_text

    def create_header(self, text: str):
        """
        Create the header section. Uses default settings. Called "header"
        """
        header = UILabel(Rect((self.header_x, self.header_y), (self.header_width, self.header_height)), text,
                         self.manager)
        self.elements["header"] = header

    def create_choice_field(self):
        """
        Create the choice input field. Uses default settings. Called "choice".
        """
        choice = UITextEntryLine(Rect((self.choice_x, self.choice_y), (self.choice_width, self.choice_height)),
                                 self.manager, object_id="overview_choice")
        choice.set_allowed_characters("numbers")
        self.elements["choice"] = choice
