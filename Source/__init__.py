import os

from .ConfigReader import ConfigReader
from .Game import (
    Game,
    UnknownKeyError,
    SongIsEmptyError,
)
from .ScreenShot import ScreenShot

__all__ = [
    # Classes
    'ConfigReader',
    'ScreenShot',
    'Game',

    # Exceptions
    'UnknownKeyError',
    'SongIsEmptyError',

    # Functions
    'clear_console',
]


def clear_console() -> None:
    os.system('cls || clear')
