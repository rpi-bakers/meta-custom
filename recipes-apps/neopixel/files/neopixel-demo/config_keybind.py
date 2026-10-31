"""
Key bindings for NeoPixel demo.
"""

from led_strip import LedStrip
from typing import Callable

from led_pattern_rainbow import generate as rbw_generator
from led_pattern_random import generate as rdm_generator
from led_pattern_gradation import generate as grd_generator
from led_pattern_halloween import PatternType as Hw
from led_pattern_halloween import generate as hlw_generator

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
            "1": lambda: led.set_pattern(grd_generator),
            "2": lambda: led.set_pattern(rbw_generator),
            "3": lambda: led.set_pattern(rdm_generator),
            "4": lambda: led.set_pattern(hlw_generator, Hw.JACK_O_LANTERN),
            "5": lambda: led.set_pattern(hlw_generator, Hw.WITCH_PORTION),
            "6": lambda: led.set_pattern(hlw_generator, Hw.VAMPIRE_NIGHT),
            "7": lambda: led.set_pattern(hlw_generator, Hw.GHOSTLY_MOON),
            "8": lambda: led.set_pattern(hlw_generator, Hw.BLACK_CAT),
            "w": lambda: led.inc_led_on_num(1),
            "s": lambda: led.inc_led_on_num(-1),
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
            "p": lambda: led.inc_freq_count(1),
            ";": lambda: led.inc_freq_count(-1),
            "[": lambda: led.inc_led_count(1),
            "]": lambda: led.inc_led_count(-1),
        }

    ###############################################################################################
    # private
    ###############################################################################################
    @staticmethod
    def _quit_apps():
        print("quit LED control.")
        raise QuitRequested
