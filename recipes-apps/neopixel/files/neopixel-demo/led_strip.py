"""
LED strip controller
"""

import math
import board
import neopixel_spi
import led_pattern_gradation

from led_pattern import LedPattern

# parameter name        step,   min, max
PARAMS_RANGE = {
    "led_count":        (1,       1, 300),
    "led_on_num":       (1,       1, 300),
    "pattern_freq":     (1,       1, 50),
    "max_brightness":   (1,       0, 100),
    "on_time":          (0.1,   0.0, 10.0),
    "off_time":         (0.1,   0.0, 10.0),
    "fade_in_rate":     (1,       0, 100),
    "fade_out_rate":    (1,       0, 100),
    "interval_sec":     (0.01, 0.01, 10.0),
    "start_position":   (1,       0, None),
}

class LedStrip:
    """
    Led strip controller class.
    """
    def __init__(
            self,
            led_count,
            led_on_num,
            start_position,
            max_brightness,
            on_time,
            off_time,
            fade_in_rate,
            fade_out_rate,
            interval_sec,
            pattern_freq
    ):
        """
        Initialize LedStrip object.
        Args:
            led_count (int): number of LEDs
            led_on_num (int): number of LEDs light on
            start_position (int): start position
            max_brightness (int): maximum brightness
            on_time (float): start time
            off_time (float): stop time
            fade_in_rate (int): fade in rate
            fade_out_rate (int): fade out rate
            interval_sec (float): cycle time
            pattern_freq (int): pattern frequency
        """

        if not isinstance(led_count, int) or isinstance(led_count, bool) or led_count <= 0:
            raise ValueError("led_count must be a positive integer")
        if not isinstance(start_position, int) or isinstance(start_position, bool):
            raise ValueError("start_position must be an integer")
        if not 0 <= start_position < led_count:
            raise ValueError("start_position must be a valid LED index")
        if (
            not isinstance(interval_sec, (int, float))
            or isinstance(interval_sec, bool)
            or not math.isfinite(interval_sec)
        ):
            raise ValueError("interval_sec must be a finite number")

        self.led_count = led_count
        self.led_on_num = led_on_num
        self.pattern_type = "DEFAULT"
        self.max_brightness = max_brightness
        self.on_time = on_time
        self.off_time = off_time
        self.fade_in_rate = fade_in_rate
        self.fade_out_rate = fade_out_rate
        self.interval_sec = interval_sec
        self.direction = 1
        self.start_position = start_position
        self.last_step_count = 0
        self.spi = board.SPI()
        self.parameter_ranges = PARAMS_RANGE
        self.pixels = self.init_neopixel_spi()
        self.pattern_freq = pattern_freq
        self.pattern = led_pattern_gradation.generate(led_on_num, pattern_freq)
        self.generator = led_pattern_gradation.generate
        self.clear()

    def init_neopixel_spi(self) -> neopixel_spi.NeoPixel_SPI:
        """
        Initialize NeoPixel SPI object.
        Note:
            If led_count is changed, NeoPixel_SPI needs to be reinitialized.
        """
        pixels = neopixel_spi.NeoPixel_SPI(
        spi = self.spi,                 # The SPI bus to output neopixel data on.
        n = self.led_count,             # The number of neopixel in the chain
        bpp = 3,                        # Bytes per pixel. 3 for RGB and 4 for RGBW pixels.
        brightness = 1.0,               # 0.0 to 1.0(full brightness)
        auto_write = False,             # True:should immediately change.False:must be called explicitly.
        pixel_order = neopixel_spi.GRB, # Pixel color channel order. GRBW(default) or GRB.
        frequency = 6_400_000,          # For 800kHz use 6400000 (default). For 400kHz, use 3200000.
        reset_time = 80e-6,             # Reset low level time in seconds. Default is 80e-6.
        bit0 = 192,                     # Bit pattern to set_pattern timing for a NeoPixel 0 bit.
        bit1 = 248,                     # Bit pattern to set_pattern timing for a NeoPixel 1 bit.
        )

        self.parameter_ranges["led_on_num"] = (1, 1, self.led_count)
        return pixels

    def clear(self) -> None:
        """
        Clear LED strip
        """
        self.pixels.fill(0)
        self.pixels.show()

    def set_pattern(self, generator, pattern_type = "DEFAULT") -> None:
        """
        set LED lighting pattern.
        Args:
            generator (dict[PatternType, Callable[[int], list[tuple[int, int, int]]]]): LED pattern generator.
            pattern_type (PatternType): LED pattern type.
        """
        self.generator = generator
        new_pattern = self.generator(self.led_on_num, self.pattern_freq , pattern_type)
        if new_pattern is not None:
            self.pattern = new_pattern
            self.pattern_type = pattern_type

    def set_color(self, start_offset, pattern) -> None:
        """
        set LED color.
        Args:
            start_offset (int): start light ON position.
            pattern (list[tuple[int, int, int]]): LED pattern.
        """
        self.pixels.fill(0)

        colors = self.pattern if pattern is None else pattern
        if colors is not None:
            for offset, color in enumerate(colors):
                self.pixels[(start_offset + offset) % self.led_count] = color

        self.pixels.show()

    def set_direction(self, direction) -> None:
        """
        Set the direction of LED movement.
        Args:
            direction (int): 1 or -1
        """
        if direction not in (-1, 1):
            raise ValueError("direction must be either -1 or 1")
        self.direction = direction

    def on_time_interval(self, elapsed_time) -> None:
        """
        time interval handler.
        update LED position and color.
        Args:
            elapsed_time (int): elapsed time from start.
        """
        adjusted_pattern = LedPattern.adjust(
            self.pattern,
            elapsed_time,
            self.max_brightness,
            self.on_time,
            self.off_time,
            self.fade_in_rate,
            self.fade_out_rate,
        )

        step_count = int(elapsed_time // self.interval_sec)
        steps = step_count - self.last_step_count
        self.last_step_count = step_count
        self.start_position = (self.start_position + self.direction * steps) % self.led_count

        self.set_color(self.start_position, adjusted_pattern)

    def change_parameter(self, param, direction) -> None:
        """
        Change specific LED parameter.
        Args:
            param (str): LED parameter variables name.
            direction (int): The direction of change (positive or negative).
        """

        if param not in self.parameter_ranges:
            return

        step, min_value, max_value = self.parameter_ranges[param]
        current_value = getattr(self, param)
        new_value = current_value + step * direction

        if param == "start_position":
            max_value = self.led_count - 1

        # Round to the max and min values
        if min_value is not None:
            new_value = max(min_value, new_value)
        if max_value is not None:
            new_value = min(max_value, new_value)

        # set value
        setattr(self, param, new_value)

    def inc_led_on_num(self, direction):
        """
        If led_on_num is changed, need to update pattern.
        """
        self.change_parameter("led_on_num", direction)
        self.set_pattern(self.generator, self.pattern_type)

    def inc_freq_count(self, direction):
        """
        If inc_freq_count is changed, need to update pattern.
        """
        self.change_parameter("pattern_freq", direction)
        self.set_pattern(self.generator, self.pattern_type)

    def inc_led_count(self, direction):
        """
        If led_count is changed, NeoPixel_SPI needs to be reinitialized.
        """
        previous_count = self.led_count
        self.change_parameter("led_count", direction)
        if self.led_count == previous_count:
            return

        self.led_on_num = min(self.led_on_num, self.led_count)
        self.start_position %= self.led_count
        self.clear()
        self.pixels = self.init_neopixel_spi()
        self.set_pattern(self.generator, self.pattern_type)

    def print_params(self, elapsed_time) -> None:
        """
        Print all LED parameters.
        Args:
            elapsed_time (float): LED parameter variables name.
        """
        print(
            f"\r{elapsed_time:<4.1f} "
            f"P:{self.start_position:<3} ",
            f"LED:{self.led_count:<3} "
            f"On:{self.led_on_num:<3} "
            f"Br:{self.max_brightness:<3} "
            f"On:{self.on_time:<3.1f} "
            f"Off:{self.off_time:<3.1f} "
            f"In:{self.fade_in_rate:<3} "
            f"Out:{self.fade_out_rate:<3} "
            f"Spd:{self.interval_sec:<4.2f} "
            f"Freq:{self.pattern_freq:<2} ",
            "key:",
            end="",
            flush=True
        )
