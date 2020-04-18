from __future__ import annotations

import cProfile
import datetime
import io

import logging
import pstats
import time
from typing import TYPE_CHECKING, Type

from snecs import Component
from snecs.typedefs import EntityID

from scripts import world
from scripts.constants import VERSION

if TYPE_CHECKING:
    from typing import Union, Optional, Any, Tuple, Dict, List


def log_component_not_found(entity: EntityID, component: Type[Component]):
    """
    Use if component not found. Log the error as a warning in the format '{entity} tried to get {component} but it was
    not found.'
    """
    name = world.get_name(entity)
    logging.warning(f"'{name}'({entity}) tried to get {component.__name__}, but it was not found.")


def initialise_logging():
    """
    Configure logging

    Logging levels:
        CRITICAL - A serious error, indicating that may be unable to continue running.
        ERROR - A more serious problem, has not been able to perform some function.
        WARNING - An indication that something unexpected happened, but otherwise still working as expected.
        INFO - Confirmation that things are working as expected.
        DEBUG - Detailed information, typically of interest only when diagnosing problems

    File mode options:
        'r' - open for reading(default)
        'w' - open for writing, truncating the file first
        'x' - open for exclusive creation, failing if the file already exists
        'a' - open for writing, appending to the end of the file if it exists

    """

    log_file_name = "logs/game.log"
    log_level = logging.DEBUG
    file_mode = "w"

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # 8 adds space for 8 characters (# CRITICAL)
    log_format = "%(asctime)s| %(levelname)-8s| %(message)s"
    logging.basicConfig(filename=log_file_name, filemode=file_mode, level=log_level, format=log_format)

    # format into uk time
    logging.Formatter.converter = time.gmtime


def create_profiler():
    """
    Create and enable the profiler
    """
    profiler = cProfile.Profile()
    profiler.enable()

    return profiler


def disable_logging():
    """
    Turn off current logging and clear logging resources
    """
    logging.shutdown()


def disable_profiling(profiler):
    """
    Turn off current profiling
    """
    profiler.disable()


def dump_profiling_data(profiler):
    """
    Dump data to a readable file
    """
    # dump the profiler stats
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    ps.dump_stats("logs/profiling/profile.dump")

    # convert profiling to human readable format
    date_and_time = datetime.datetime.utcnow()
    out_stream = open("logs/profiling/" + date_and_time.strftime("%Y%m%d@%H%M") + "_" + VERSION + ".profile", "w")
    ps = pstats.Stats("logs/profiling/profile.dump", stream=out_stream)
    ps.strip_dirs().sort_stats("cumulative").print_stats()