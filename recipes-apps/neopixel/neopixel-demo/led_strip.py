"""LED strip controler
"""

import math
import board
import neopixel_spi
import led_pattern
import config as cfg

SPI_FREQUENCY = 6_400_000
PIXEL_ORDER = neopixel_spi.GRB

class LedStrip:
    """Led strip
    """

    def __init__(
            self,
            led_count,
            led_on_num,
            pattern,
            start_position,
            max_brightness,
            on_time,
            off_time,
            fade_in_rate,
            fade_out_rate,
            cycle_sec
    ):
        """
        Args:
            led_count (int): number of LEDs
            led_on_num (int): number of LEDs light on
            pattern (LED pattern array): LED pattern
            start_position (int): start position
            max_brightness (int): maximum brightness
            on_time (float): start time
            off_time (float): stop time
            fade_in_rate (float): fade in rate
            fade_out_rate (float): fade out rate
            cycle_sec (float): cycle time
        """
        self.inc_keymap = "wertyuiop"
        self.dec_keymap = "sdfghjkl;"

        if not isinstance(led_count, int) or isinstance(led_count, bool) or led_count <= 0:
            raise ValueError("led_count must be a positive integer")
        if not isinstance(start_position, int) or isinstance(start_position, bool):
            raise ValueError("start_position must be an integer")
        if not 0 <= start_position < led_count:
            raise ValueError("start_position must be a valid LED index")
        if (
            not isinstance(cycle_sec, (int, float))
            or isinstance(cycle_sec, bool)
            or not math.isfinite(cycle_sec)
        ):
            raise ValueError("cycle_sec must be a finite number")

        self.led_count = led_count
        self.led_on_num = led_on_num
        self.pattern = pattern
        self.max_brightness = max_brightness
        self.on_time = on_time
        self.off_time = off_time
        self.fade_in_rate = fade_in_rate
        self.fade_out_rate = fade_out_rate
        self.cycle_sec = cycle_sec
        self.direction = 1
        self.start_position = start_position
        self.last_step_count = 0
        self.pixels = neopixel_spi.NeoPixel_SPI(
        spi=board.SPI(),        # The SPI bus to output neopixel data on.
        n=led_count,            # The number of neopixel in the chain
        bpp=3,                  # Bytes per pixel. 3 for RGB and 4 for RGBW pixels.
        brightness=1.0,         # 0.0 to 1.0(full brightness)
        auto_write=False,       # True:should immediately change.False:must be called explicitly.
        pixel_order=PIXEL_ORDER,# Pixel color channel order. GRBW(default) or GRB.
        frequency=SPI_FREQUENCY,# For 800kHz use 6400000 (default). For 400kHz, use 3200000.
        reset_time=80e-6,       # Reset low level time in seconds. Default is 80e-6.
        bit0=192,               # Bit pattern to set_pattern timing for a NeoPixel 0 bit.
        bit1=248,               # Bit pattern to set_pattern timing for a NeoPixel 1 bit.
        )
        self.clear()

        # パラメータごとの
        # (増減幅, 最小値, 最大値)
        self.parameter_settings = {             # key assign
            "led_count": (1, 1, 300),   # ws
            "led_on_num": (1, 1, 300),  # ed
            "max_brightness": (1, 0, 100),      # rf
            "on_time": (0.1, 0.0, 10.0),        # tg
            "off_time": (0.1, 0.0, 10.0),       # yh
            "fade_in_rate": (1, 0, 100),        # uj
            "fade_out_rate": (1, 0, 100),       # ik
            "cycle_sec": (0.1, 0.1, 10.0),      # ol
            "start_position": (1, 0, None),     # p;
        }

        self.key_map = self.create_parameter_key_map()

    def clear(self):
        """Clear LED strip
        """
        self.pixels.fill(0)
        self.pixels.show()

    def set_color(self, start_offset: int, pattern = None) -> None:
        """set_pattern LED color

        Args:
            start_offset (int): start light ON position.
            pattern (LED pattern array): LED pattern.
        """
        self.pixels.fill(0)

        colors = self.pattern if pattern is None else pattern
        for offset, color in enumerate(colors):
            self.pixels[(start_offset + offset) % self.led_count] = color

        self.pixels.show()

    def set_direction(self, direction) -> None:
        """Set the direction of LED movement.
        Args:1 or -1
        """
        if direction not in (-1, 1):
            raise ValueError("direction must be either -1 or 1")
        self.direction = direction

    def on_time_interval(self, elapsed_time) -> None:
        """time interval handler

        Args:
            elapsed_time (int): elapsed time from start.
        """
        adjusted_pattern = led_pattern.adjust_led_pattern(
            self.pattern,
            elapsed_time,
            self.max_brightness,
            self.on_time,
            self.off_time,
            self.fade_in_rate,
            self.fade_out_rate,
        )

        step_count = int(elapsed_time // self.cycle_sec)
        steps = step_count - self.last_step_count
        self.last_step_count = step_count
        self.start_position = (self.start_position + self.direction * steps) % self.led_count
        self.set_color(self.start_position, adjusted_pattern)


    def create_parameter_key_map(self):
        """パラメータ増減用のキーアサインを作成する"""
        key_map = {}

        for key, parameter in zip(
                self.inc_keymap,
                self.parameter_settings
        ):
            key_map[key] = (parameter, 1)

        for key, parameter in zip(
                self.dec_keymap,
                self.parameter_settings
        ):
            key_map[key] = (parameter, -1)

        return key_map

    def change_parameter(self, parameter, direction):
        """指定されたパラメータを増減する"""

        if parameter not in self.parameter_settings:
            return

        step, min_value, max_value = self.parameter_settings[parameter]

        # 現在値を取得
        current_value = getattr(self, parameter)

        # 増減
        new_value = current_value + step * direction

        # start_position の最大値は led_count - 1
        if parameter == "start_position":
            max_value = self.led_count - 1

        # 最小値・最大値でクランプ
        if min_value is not None:
            new_value = max(min_value, new_value)

        if max_value is not None:
            new_value = min(max_value, new_value)

        # 値を設定
        setattr(self, parameter, new_value)

    def handle_params_change_key(self, key):
        """キー入力を処理する"""

        if key not in self.key_map:
            return None

        parameter, direction = self.key_map[key]
        self.change_parameter(parameter, direction)

        return None

    def print_params(self):
        print(
            f"\rLED:{self.led_count:<3} "
            f"LedOn:{self.led_on_num:<3} "
            f"Brightness[%]:{self.max_brightness:<3} "
            f"On[s]:{self.on_time:<4.1f} "
            f"Off[s]:{self.off_time:<4.1f} "
            f"FadeIn[%]:{self.fade_in_rate:<3} "
            f"FadeOut[%]:{self.fade_out_rate:<3} "
            f"Cycle[s]:{self.cycle_sec:<4.1f} "
            f"Pos:{self.start_position:<3} ",
            end="",
            flush=True
        )