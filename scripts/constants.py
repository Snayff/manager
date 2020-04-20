from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List

VERSION = "0.0.3"

SAVE_PATH = "saves/"
MAX_AUTOSAVES = 3

BASE_WINDOW_WIDTH = 1280
BASE_WINDOW_HEIGHT = 720
GAME_FPS = 60

EXIT = -1
INITIALISING = 0

LINE_BREAK = "<br>"

MINUTES_IN_DAY = 600
DAYS_IN_SEASON = 30
SEASONS_IN_YEAR = 4
DAYS_IN_YEAR = DAYS_IN_SEASON * SEASONS_IN_YEAR

BIRTH_RATE = "birth_rate"
