import logging
import time
from typing import (
    Literal,
    List,
    Union,
)

import pyautogui

__all__ = [
    # Classes
    'Game',

    # Exceptions
    'UnknownKeyError',
    'SongIsEmptyError',
]
LOGGER = logging.getLogger(__name__)

# Typing
_T_KEY = Literal['w', 'a', 's', 'd', '#', '_']
_T_SONG = List[_T_KEY]
_T_NUMBER = Union[int, float]


class UnknownKeyError(Exception):
    ...


class SongIsEmptyError(Exception):
    ...


class Game:
    def __init__(self, song: _T_SONG, mouse_press_time: _T_NUMBER):
        self._original_song = song.copy()
        self._song = self._original_song.copy()
        self._mouse_press_time = mouse_press_time

    def refresh_song(self) -> None:
        self._song = self._original_song.copy()
        LOGGER.info('Song refreshed')

    def press_next_key(self) -> None:
        key_to_press = self._song.pop(0)

        if key_to_press == '#':
            pyautogui.mouseDown(button='left')
            pyautogui.mouseDown(button='right')
            if self._mouse_press_time > 0:
                time.sleep(self._mouse_press_time)
            pyautogui.mouseUp(button='left')
            pyautogui.mouseUp(button='right')
        elif key_to_press == '_':
            pyautogui.press('space')
        elif key_to_press in 'wasd':
            pyautogui.press(key_to_press)
        else:
            raise UnknownKeyError(f'Unknown key in song: {key_to_press}')
        LOGGER.debug(f'Key pressed: {key_to_press}')

        # Check if song ended
        if not self._song:
            raise SongIsEmptyError

    @staticmethod
    def end_performance() -> None:
        LOGGER.info('Ending performance ...')
        pyautogui.keyDown('e')
        time.sleep(2)
        pyautogui.keyUp('e')
        LOGGER.info('Performance ended')

    @staticmethod
    def start_performance() -> None:
        LOGGER.info('Starting performance ...')
        pyautogui.press('e')
        LOGGER.info('Performance started')
