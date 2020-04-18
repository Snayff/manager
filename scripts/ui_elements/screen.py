from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIPanel, UITextBox, UITextEntryLine
from pygame.rect import Rect

from scripts import ui, world
from scripts.components import Hourglass
from scripts.constants import LINE_BREAK

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List, Callable
    from pygame_gui import UIManager
    from pygame_gui.core import UIElement


class Screen(ABC):
    """
    The base class for all screens. Provides methods for creating the main screen sections. Adds returning to the
    antechamber as an initial option. self.options must be overridden to remove this. Otherwise just add more options.
    """
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
    option_text_x = section_start_x + (button_width - section_gap)  # minus to have button touch on both sides
    info_x = section_start_x

    # bottom area
    choice_x = section_start_x
    choice_width = 200
    choice_height = 50
    hourglass_width = 300
    hourglass_height = choice_height

    def __init__(self, manager: UIManager, rect: Rect):
        self.manager: UIManager = manager
        self.rect: Rect = rect
        self.elements: Dict[str, UIElement] = {}
        self.options: Dict[str, Tuple[str, Callable]] = {
            "anteroom": ("Anteroom - Return", ui.swap_to_antechamber_screen)
        }
        self.showing = ""  # flag is set in setup

        # default values that need rect before they can be set
        self.header_width = rect.width
        self.option_text_width = rect.width - (self.option_text_x + self.section_start_x)  # account for gap on right
        self.max_section_height = rect.height - (self.post_header_y + self.choice_height + (self.section_gap * 3))
        self.half_max_section_height = self.max_section_height / 2
        self.choice_y = rect.height - self.choice_height - (self.section_gap * 2)
        self.hourglass_y = self.choice_y
        self.info_width = rect.width - (self.info_x + self.section_start_x)  # account for gap on right

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """
        Process events generated by this element. Must be overridden.
        """
        raise NotImplementedError


    def kill(self):
        """
        Delete all elements from self.elements and clear self.options.
        """
        elements = self.elements
        for name, element in elements.items():
            element.kill()
        self.elements = {}
        self.options = {}

    ############################ CREATE ##############################

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

    def create_choice_field(self, allowed_str: bool = False):
        """
        Create the choice input field. Uses default settings. Called "choice".
        """
        choice = UITextEntryLine(Rect((self.choice_x, self.choice_y), (self.choice_width, self.choice_height)),
                                 self.manager, object_id="choice")

        # prevent strings based on the arg
        if not allowed_str:
            choice.set_allowed_characters("numbers")

        self.elements["choice"] = choice

    def create_hourglass_display(self):
        """
        Create the display of how much time is left in the day
        """
        # get the text
        player_kingdom = world.get_player_kingdom()
        hourglass = world.get_entitys_component(player_kingdom, Hourglass)
        text = f"{str(hourglass.minutes_available)} minutes before sunset"

        # create the label
        rect = Rect((-self.hourglass_width - self.section_start_x, self.choice_y), (self.hourglass_width,
        self.hourglass_height))
        hourglass_display = UILabel(rect, text, self.manager, object_id="hourglass",
                                    anchors={
                                        "left": "right",
                                        "right": "right",
                                        "top": "top",
                                        "bottom": "bottom"
                                    })

        self.elements["hourglass"] = hourglass_display

    ############################ CHECKS ##############################

    def get_object_id(self, event: pygame.event.Event) -> str:
        """
        Strip unnecessary details from the event's ui_object_id and handle keyboard or mouse input to get object id
        """
        # get the id from either click or type
        object_id = ""
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            object_id = event.ui_object_id.replace("options.", "")
        elif event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.text.isnumeric():
                try:
                    object_id = list(self.options)[int(event.text) - 1]  # -1 to offset from options starting at 1
                except KeyError:
                    logging.warning(f"Key not found in options when getting object id. Dodgy typing? ({event.text})")

        return object_id


    def is_option_implemented(self, object_id: Union[str, int]) -> bool:
        """
        Confirm that the option selected is implemented
        """
        # check for a prefix indicating not implemented
        try:
            if object_id:
                prefix = self.options[object_id][0][:1]
                if prefix != "*":
                    return True
                else:
                    logging.warning(f"Selected {object_id}, which is not implemented. Took no action.")

        except KeyError:
            logging.warning(f"Key not found in options when getting prefix. Dodgy typing? ({object_id})")

        return False

    def call_options_function(self, object_id: str):
        """
        Call the option's function
        """
        self.options[object_id][1]()
