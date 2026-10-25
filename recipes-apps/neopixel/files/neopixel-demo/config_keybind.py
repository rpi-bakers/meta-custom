"""
Key bindings for NeoPixel demo.
"""
from led_pattern import PatternType

from led_strip import LedStrip
from typing import Callable

class QuitRequested(Exception):
    """Raised when the user presses q."""

class ConfigKeyBind:
    """
    key bindings for NeoPixel demo.
    """

    def __init__(self, led: LedStrip):
        """
        init class.
        """
        self._led = led
        self.functions: dict[str, Callable[[], None]] = {
            "q": lambda: self._quit_apps(),
            "1": lambda: led.set_pattern(PatternType.GRADATION),
            "2": lambda: led.set_pattern(PatternType.RAINBOW),
            "3": lambda: led.set_pattern(PatternType.RANDOM),
            "w": lambda: self._inc_led_on_num(1),
            "s": lambda: self._inc_led_on_num(-1),
            "e": lambda: led.change_parameter("max_brightness", 1),
            "d": lambda: led.change_parameter("max_brightness", -1),
            "r": lambda: led.change_parameter("on_time", 1),
            "f": lambda: led.change_parameter("on_time", -1),
            "t": lambda: led.change_parameter("off_time", 1),
            "g": lambda: led.change_parameter("off_time", -1),
            "y": lambda: led.change_parameter("fade_in_rate", 1),
            "h": lambda: led.change_parameter("fade_in_rate", -1),
            "u": lambda: led.change_parameter("fade_out_rate", 1),
            "j": lambda: led.change_parameter("fade_out_rate", -1),
            "i": lambda: led.change_parameter("interval_sec", 1),
            "k": lambda: led.change_parameter("interval_sec", -1),
            "o": lambda: led.change_parameter("start_position", 1),
            "l": lambda: led.change_parameter("start_position", -1),
            "[": lambda: self._inc_led_count(1),
            "]": lambda: self._inc_led_count(-1),
        }

    ###############################################################################################
    # private
    ###############################################################################################
    def _inc_led_on_num(self, direction):
        """
        If led_on_num is changed, need to update pattern.
        """
        self._led.change_parameter("led_on_num", direction)
        self._led.set_pattern(self._led.pattern_type)

    def _inc_led_count(self, direction):
        """
        If led_count is changed, NeoPixel_SPI needs to be reinitialized.
        """
        self._led.change_parameter("led_count", direction)
        self._led.clear()
        self._led.pixels = self._led.init_neopixel_spi()

    def _quit_apps(self):
        raise QuitRequested
