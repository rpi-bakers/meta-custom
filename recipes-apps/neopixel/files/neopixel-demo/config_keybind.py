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

    def __init__(self, led: LedStrip, pattern="gradation"):
        """
        init class.
        """
        self._led = led
        self._patterns = {
            "gradation": (grd_generator, "DEFAULT"),
            "rainbow": (rbw_generator, "DEFAULT"),
            "random": (rdm_generator, "DEFAULT"),
            "halloween_jack_o_lantern": (hlw_generator, Hw.JACK_O_LANTERN),
            "halloween_witch_portion": (hlw_generator, Hw.WITCH_PORTION),
            "halloween_vampire_night": (hlw_generator, Hw.VAMPIRE_NIGHT),
            "halloween_ghostly_moon": (hlw_generator, Hw.GHOSTLY_MOON),
            "halloween_black_cat": (hlw_generator, Hw.BLACK_CAT),
        }
        self.pattern = "gradation"
        self._select_pattern(pattern)
        self.functions: dict[str, Callable[[], None]] = {
            "q": lambda: self._quit_apps(),
            "1": lambda: self._select_pattern("gradation"),
            "2": lambda: self._select_pattern("rainbow"),
            "3": lambda: self._select_pattern("random"),
            "4": lambda: self._select_pattern("halloween_jack_o_lantern"),
            "5": lambda: self._select_pattern("halloween_witch_portion"),
            "6": lambda: self._select_pattern("halloween_vampire_night"),
            "7": lambda: self._select_pattern("halloween_ghostly_moon"),
            "8": lambda: self._select_pattern("halloween_black_cat"),
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
    def _select_pattern(self, pattern):
        generator, pattern_type = self._patterns[pattern]
        self._led.set_pattern(generator, pattern_type)
        self.pattern = pattern

    @staticmethod
    def _quit_apps():
        print("quit LED control.")
        raise QuitRequested
