from __future__ import annotations

from typing import TYPE_CHECKING, Type

import pygame
import pygame_gui
from pygame.rect import Rect
from pygame_gui.elements import UITextBox, UILabel, UITextEntryLine, UIButton

from scripts import ui
from scripts.ui_elements.screen import Screen

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame_gui import UIManager


class OverviewScreen(Screen):
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)
        self.options = {
            "council": ("Meet with your council", ui.show_council_screen),
            # "*Host petitioners",
            # "*Search for new lands",
            # "*Proclaim an edict",
            # "*Military action",
            # "*Demand construction",
            # "*Instruct diplomats",
            # "*Spy Network",
            # "*End the day"
        }

        # positioning
        start_y = 10
        offset_y = 0
        start_x = 50
        button_width = 150
        input_width = 200
        text_width = rect.width - ((start_x + button_width) * 2)
        line_height = 40

        # header
        intro = UILabel(Rect((start_x, start_y + offset_y), (rect.width, line_height)), "Overview Screen",
                        manager)
        self.elements["intro"] = intro

        # options
        gap = "<br> <br>"
        options_text = ""

        # offsets for alignment
        offset_y = offset_y + line_height * 2
        _offset_y = offset_y  # for buttons
        count = 1

        # loop options and extract text and id
        for _id, (text, _method) in self.options.items():
            options_text += text + gap
            option_button = UIButton(Rect((start_x, start_y + _offset_y), (button_width, line_height)), str(count),
                                     manager, object_id=_id)
            count += 1
            _offset_y += line_height
            self.elements[_id] = option_button

        # add text to textbox
        options_height = rect.height - (offset_y + line_height * 3)
        options_text = UITextBox(options_text,
                                 Rect((start_x + button_width, start_y + offset_y), (text_width, options_height)),
                                 manager, False, 1)
        self.elements["text_box"] = options_text

        # create choice box
        choice = UITextEntryLine(Rect(((rect.width / 2) - (input_width / 2), -line_height * 2),
                                 (input_width, line_height * 2)), manager,
                                 anchors={
                                     "left": "left",
                                     "right": "left",
                                     "top": "bottom",
                                     "bottom": "bottom"
                                 }, object_id="overview_choice")
        self.elements["choice"] = choice

    def handle_event(self, event: pygame.event.Event):
        """
        Handle events created by this UI widget
        """
        object_id = event.ui_object_id

        # options
        if object_id in self.options:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                self.options[object_id][1]()  # call the method

