from __future__ import annotations

from typing import TYPE_CHECKING, Type

from pygame.rect import Rect
from pygame_gui import UIManager
from pygame_gui.elements import UITextBox, UILabel, UITextEntryLine, UIButton

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List

class OverviewScreen:
    def __init__(self, manager: UIManager, rect: Rect):
        self.elements = {}

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

        # options
        gap = "<br> <br>"
        options_text = ""
        options = [
            "Meet with your council.",
            "Host petitioners."
        ]
        offset_y = offset_y + line_height * 2
        _offset_y = offset_y  # for buttons
        count = 1

        for option in options:
            options_text += option + gap
            option_button = UIButton(Rect((start_x, start_y + _offset_y), (button_width, line_height)), str(count),
                                     manager)
            count += 1
            _offset_y += line_height

        options_height = rect.height - (offset_y + line_height * 3)
        options_text = UITextBox(options_text,
                                 Rect((start_x + button_width, start_y + offset_y), (text_width, options_height)),
                                 manager, False, 1)




        # choice
        choice = UITextEntryLine(Rect(((rect.width / 2) - (input_width / 2), -line_height * 2),
                                 (input_width, line_height * 2)),
                                 manager,
                                 anchors={
                                     "left": "left",
                                     "right": "left",
                                     "top": "bottom",
                                     "bottom": "bottom"
                                 })


