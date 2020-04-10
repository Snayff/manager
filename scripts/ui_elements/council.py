from __future__ import annotations

from typing import TYPE_CHECKING, Type

from pygame_gui.elements import UIButton, UILabel, UITextBox

from scripts import world
from scripts.components import Details, IsPlayerControlled, Lands, Population
from scripts.ui_elements.screen import Screen
from pygame.rect import Rect

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List
    from pygame_gui import UIManager


class CouncilScreen(Screen):
    def __init__(self, manager: UIManager, rect: Rect):
        super().__init__(manager, rect)
        self.options = {
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
        intro = UILabel(Rect((start_x, start_y + offset_y), (rect.width, line_height)), "Council Screen",
                        manager)
        self.elements["intro"] = intro

        # options
        gap = "<br> <br>"
        options_text = ""

        # offsets for alignment
        offset_y = offset_y + line_height * 2
        _offset_y = offset_y  # for buttons
        count = 1

        # create info
        info_text = ""
        player_kingdom = world.get_player_kingdom()

        details = world.get_entitys_component(player_kingdom, Details)
        info_text += details.kingdom_name + gap

        population = world.get_entitys_component(player_kingdom, Population)
        for demo in population:
            info_text += demo.race + ": " + str(demo.amount) + "( " + str(demo.birth_rate) + " per year)" +\
                         gap

        lands = world.get_entitys_component(player_kingdom, Lands)
        for land in lands:
            info_text += land.name + ": " + land.size

        info_height = rect.height - (offset_y + line_height * 3)
        info_text = UITextBox(info_text, Rect((start_x + button_width, start_y + offset_y), (text_width, info_height)),
                              manager, False, 1)

        # # loop options and extract text and id
        # for _id, (text, _method) in self.options.items():
        #     options_text += text + gap
        #     option_button = UIButton(Rect((start_x, start_y + _offset_y), (button_width, line_height)), str(count),
        #                              manager, object_id=_id)
        #     count += 1
        #     _offset_y += line_height
        #     self.elements[_id] = option_button
        #
        # # add text to textbox
        # options_height = rect.height - (offset_y + line_height * 3)
        # options_text = UITextBox(options_text,
        #                          Rect((start_x + button_width, start_y + offset_y), (text_width, options_height)),
        #                          manager, False, 1)

