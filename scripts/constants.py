from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List

VERSION = "0.4.0"

# save data
SAVE_PATH = "saves/"
MAX_AUTOSAVES = 3

# visual info
BASE_WINDOW_WIDTH = 1280
BASE_WINDOW_HEIGHT = 720
GAME_FPS = 60

# game states
EXIT = -1
INITIALISING = 0

# html codes
LINE_BREAK = "<br>"

# time/date values
HOURS_IN_DAY = 10.0
DAYS_IN_SEASON = 30
SEASONS_IN_YEAR = 4
DAYS_IN_YEAR = DAYS_IN_SEASON * SEASONS_IN_YEAR

# stats
BIRTH_RATE = "birth_rate"

# time costs
EDICT_COST = 1.5

# land size info
SMALL = "small"
AVERAGE = "average"
LARGE = "large"


