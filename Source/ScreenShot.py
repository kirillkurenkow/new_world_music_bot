import logging
from typing import Tuple

from PIL import ImageGrab
from PIL.Image import Image
from PIL.PyAccess import PyAccess

__all__ = ['ScreenShot']
LOGGER = logging.getLogger(__name__)

# Typing
_T_SCREENSHOT_BOX = Tuple[int, int, int, int]


class ScreenShot:
    def __init__(self, box: _T_SCREENSHOT_BOX):
        self.__screenshot = self.__get_screenshot(box)

    @staticmethod
    def __get_screenshot(box: _T_SCREENSHOT_BOX) -> Image:
        screenshot = ImageGrab.grab(bbox=box)
        return screenshot

    @property
    def have_black_pixel(self) -> bool:
        loaded_screenshot: PyAccess = self.__screenshot.load()  # noqa
        for x in range(self.__screenshot.width):
            for y in range(self.__screenshot.height):
                color = loaded_screenshot[x, y]
                if color == (11, 11, 11):
                    return True
        return False
