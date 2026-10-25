"""
LED color and pattern generation utilities.
"""

import math
import config_pattern as cfg

from enum import StrEnum

class PatternType(StrEnum):
    GRADATION = "GRADATION"
    RAINBOW = "RAINBOW"
    RANDOM = "RANDOM"

class LedPattern:
    """
    LED color and pattern generation utilities.
    """

    @staticmethod
    def validate_color(color, name) -> None:
        """
        Validate color.
        Args:
            color (tuple[int, int, int]): The color to validate.
            name (str): The name of the color to validate.
        """
        if not isinstance(color, (list, tuple)) or len(color) != 3:
            raise ValueError(f"{name} must contain exactly three RGB values")
        if any(
                not isinstance(channel, int)
                or isinstance(channel, bool)
                or not 0 <= channel <= 255
                for channel in color
        ):
            raise ValueError(f"{name} RGB values must be integers from 0 to 255")

    @staticmethod
    def validate_led_count(led_count) -> None:
        """
        Validate number of LEDs.
        Args:
            led_count (int): The number of LEDs to validate.
        """
        if not isinstance(led_count, int) or isinstance(led_count, bool) or led_count < 0:
            raise ValueError("led_on_num must be a non-negative integer")

    @staticmethod
    def adjust(
            pattern,
            elapsed_time:int,
            max_brightness:int,
            on_time:float,
            off_time:float,
            on_fade_rate:int,
            off_fade_rate:int) -> list[tuple[int,...]]:
        """
        Apply the repeating on/off cycle and fade envelope to an RGB pattern.

        Args:
            pattern: RGB colors, one per LED.
            elapsed_time (int): Time in seconds since the cycle began.
            max_brightness (int): Maximum output brightness as a percentage (0-100).
            on_time (float): Duration of the on phase in seconds.
            off_time (float): Duration of the off phase in seconds.
            on_fade_rate (int): Portion of the on phase used to fade in (0-100%).
            off_fade_rate (int): Portion of the off phase used to fade out (0-100%).

        Returns:
            A new RGB pattern scaled to the current brightness.
        """
        LedPattern._validate_pattern(pattern)
        LedPattern._validate_time(elapsed_time, "elapsed_time")
        LedPattern._validate_time(on_time, "on_time")
        LedPattern._validate_time(off_time, "off_time")

        for rate, name in (
                (max_brightness, "max_brightness"),
                (on_fade_rate, "on_fade_rate"),
                (off_fade_rate, "off_fade_rate"),
        ):
            if not isinstance(rate, int) or not math.isfinite(rate) or not 0 <= rate <= 100:
                raise ValueError(f"{name} must be between 0 and 100")

        if on_time == 0:
            return [(0, 0, 0) for _ in pattern]

        if off_time == 0:
            fade_in_time = on_time * on_fade_rate / 100
            brightness = (
                1.0
                if fade_in_time == 0
                else min(1.0, elapsed_time / fade_in_time)
            )

            brightness *= max_brightness / 100

            return [
                tuple(int(channel * brightness) for channel in color)
                for color in pattern
            ]

        cycle_time = on_time + off_time
        cycle_position = elapsed_time % cycle_time

        if cycle_position < on_time:
            fade_in_time = on_time * on_fade_rate / 100
            brightness = (
                1.0
                if fade_in_time == 0
                else min(1.0, cycle_position / fade_in_time)
            )
        else:
            fade_out_time = off_time * off_fade_rate / 100
            off_elapsed = cycle_position - on_time
            brightness = (
                0.0
                if fade_out_time == 0
                else max(0.0, 1.0 - off_elapsed / fade_out_time)
            )

        brightness *= max_brightness / 100

        adjusted_pattern = [
            tuple(int(channel * brightness) for channel in color)
            for color in pattern
        ]

        return adjusted_pattern

    ###############################################################################################
    # private
    ###############################################################################################
    @staticmethod
    def _validate_time(value, name):
        if not isinstance(value, float) or not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be a finite non-negative number")

    @staticmethod
    def _validate_pattern(pattern):
        if not isinstance(pattern, (list, tuple)):
            raise ValueError("pattern must be a list or tuple of RGB values")
        for index, color in enumerate(pattern):
            LedPattern.validate_color(color, f"pattern[{index}]")
