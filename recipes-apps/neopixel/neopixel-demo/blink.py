#!/usr/bin/env python3

"""neopixcel LED blinking application """

import os
import sys
import math
import termios
import select
import time
import tty

import board
import neopixel_spi

import led_pattern

# ==================================================================================================
# User settings
# ==================================================================================================

# --------------------------------------------------------------------------------------------------
# Device settings
# --------------------------------------------------------------------------------------------------
# LED_NUM | 1 to 164 | Number of LEDs connected to the SPI LED strip |
# Depends on power supply current and SPI bus frequency
# In a experiment, 164 LEDs worked at 5V, 1.8A.
# --------------------------------------------------------------------------------------------------
LED_NUM = 164

# --------------------------------------------------------------------------------------------------
# LED settings
# --------------------------------------------------------------------------------------------------
# LED_ON_NUM        | 0 to LED_NUM      | Number of LEDs to light                   |
# START_POSITION    | 0 to LED_NUM - 1  | Initial starting position of the lit area.|
# --------------------------------------------------------------------------------------------------
LED_ON_NUM = 20
START_POSITION = 0

# --------------------------------------------------------------------------------------------------
# Color settings
# --------------------------------------------------------------------------------------------------
# MAX_BRIGHTNESS| 0(Off) to 100[%]      | Brightness MAX limit of the LEDs          |
# START_COLOR   |0 to 255 each (R,G,B)  | Color on the START_POSITION               |
# END_COLOR     |0 to 255 each (R,G,B)  | Color on the START_POSITION + LED_ON_NUM  |
# --------------------------------------------------------------------------------------------------
MAX_BRIGHTNESS = 5
START_COLOR = (255, 0, 0)
END_COLOR = (0, 0, 255)
RAINBOW_START_COLOR = (255, 0, 0)
RAINBOW_END_COLOR = (128, 0, 128)
RANDOM_LED_ON_RATE = 75
RANDOM_COLOR_NUM = 16
PRIMARY_COLOR_RATE = 50

# --------------------------------------------------------------------------------------------------
# Blink timing
# --------------------------------------------------------------------------------------------------
# LOOP_WAIT         | 0 to x.xxxx   | Main loop cycle time [seconds]                |
# POSITION_INTERVAL | 0 to x.xx     | Time to stay at current LED position [seconds]|
# ON_TIME           | 0 to x        | LED ON duration [seconds]                     |
# OFF_TIME          | 0 to x        | LED OFF duration[seconds]                     |
# FADE_IN_RATE      | 0 to 100      | Fade-in duration = ON_TIME  * rate / 100      |
# FADE_OUT_RATE     | 0 to 100      | Fade-out duration = OFF_TIME * rate / 100     |
# MOVE_REVERSE      | True or False | False: forward / True: reverse                |
# --------------------------------------------------------------------------------------------------
# LED Animation Timing Chart
# --------------------------------------------------------------------------------------------------
#   |<- one cycle ---------------------------------------------------->|
#   |<---------- ON_TIME -------------><-- OFF_TIME -->|<- LOOP_WAIT ->|
#   |<-FADE_IN_->|                     |<- FADE_OUT_ ->|
#   |   _RATE[%] |                     |    _RATE[%]   |
#   |            +---------------------+               |
#   |          /                          \            |
#   |       /                                 \        |
#   |    /                                        \    |
#   | /                                              \ |
#   +------------+---------------------+---------------+--------------> time
#   ^            ^                     ^               ^
#   |            |                     |               |
#   ON start    Fade-in end           OFF start       OFF end
#
# Position
# ==============================================================================
#
# [MOVE_REVERSE = False] LED 0               LED 1                LED 2
#   ●                    ●                    ●                    ●
#   +-POSITION_INTERVAL-->-POSITION_INTERVAL-->-POSITION_INTERVAL-->  time
#   ●                    ●                    ●                    ●
# [MOVE_REVERSE =  True] LED 2                LED 1                LED 0
# =============================================================================
LOOP_WAIT = 0.005
POSITION_INTERVAL = 0.5
ON_TIME = 1.5
OFF_TIME = 0.5
FADE_IN_RATE = 80
FADE_OUT_RATE = 80
MOVE_REVERSE = False

# ==================================================================================================
# NeoPixel Device settings
# Change this if your LED strip uses another pixel order.
# --------------------------------------------------------------------------------------------------
NUM_PIXELS = LED_NUM
PIXEL_ORDER = neopixel_spi.GRB
SPI_FREQUENCY = 6_400_000

# ==================================================================================================
# Helper functions
# ==================================================================================================

class QuitRequested(Exception):
    """Raised when the user presses q."""


def read_key():
    """Read one available key from an interactive terminal without blocking."""
    if not sys.stdin.isatty():
        return None

    file_descriptor = sys.stdin.fileno()
    readable, _, _ = select.select([file_descriptor], [], [], 0)
    if not readable:
        return None
    return os.read(file_descriptor, 1).decode("ascii", errors="ignore").lower()


def enable_single_key_input():
    """Enable immediate key reads and restore the terminal when finished."""
    if not sys.stdin.isatty():
        return None

    file_descriptor = sys.stdin.fileno()
    previous_settings = termios.tcgetattr(file_descriptor)
    tty.setcbreak(file_descriptor)
    return file_descriptor, previous_settings


def restore_terminal(settings):
    """Restore terminal settings changed for single-key input."""
    if settings is not None:
        file_descriptor, previous_settings = settings
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, previous_settings)



def validate_settings():
    """
    Validate user settings to ensure they are within acceptable ranges.
    Raises ValueError if any setting is invalid.
    """
    if not isinstance(LED_NUM, int) or isinstance(LED_NUM, bool) or LED_NUM <= 0:
        raise ValueError("LED_NUM must be a positive integer")
    if (
        not isinstance(LED_ON_NUM, int)
        or isinstance(LED_ON_NUM, bool)
        or not 0 <= LED_ON_NUM <= LED_NUM
    ):
        raise ValueError("LED_ON_NUM must be an integer from 0 to LED_NUM")
    if (
        not isinstance(START_POSITION, int)
        or isinstance(START_POSITION, bool)
        or not 0 <= START_POSITION < LED_NUM
    ):
        raise ValueError("START_POSITION must be an LED index from 0 to LED_NUM - 1")
    if not isinstance(MOVE_REVERSE, bool):
        raise ValueError("MOVE_REVERSE must be a boolean")

    for value, name in (
        (LOOP_WAIT, "LOOP_WAIT"),
        (POSITION_INTERVAL, "POSITION_INTERVAL"),
        (ON_TIME, "ON_TIME"),
        (OFF_TIME, "OFF_TIME"),
    ):
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(value)
            or value < 0
        ):
            raise ValueError(f"{name} must be a finite non-negative number")
    if LOOP_WAIT == 0 or POSITION_INTERVAL == 0:
        raise ValueError("LOOP_WAIT and POSITION_INTERVAL must be greater than zero")
    if ON_TIME + OFF_TIME == 0:
        raise ValueError("ON_TIME and OFF_TIME cannot both be zero")

    for value, name in (
        (MAX_BRIGHTNESS, "MAX_BRIGHTNESS"),
        (FADE_IN_RATE, "FADE_IN_RATE"),
        (FADE_OUT_RATE, "FADE_OUT_RATE"),
    ):
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(value)
            or not 0 <= value <= 100
        ):
            raise ValueError(f"{name} must be between 0 and 100")

# ==================================================================================================
# Main
# ==================================================================================================
def main():
    """
    Main function to run the LED blink demo.
    """
    validate_settings()
    pattern = led_pattern.generate_gradation_pattern(
        LED_ON_NUM, START_COLOR, END_COLOR
    )

    # --------------------------------------------------------
    # Initialize SPI
    pixels = neopixel_spi.NeoPixel_SPI(
        spi=board.SPI(),        # The SPI bus to output neopixel data on.
        n=NUM_PIXELS,           # The number of neopixels in the chain
        bpp=3,                  # Bytes per pixel. 3 for RGB and 4 for RGBW pixels.
        brightness=1.0,         # 0.0 to 1.0(full brightness)
        auto_write=False,       # True:should immediately change.False:must be called explicitly.
        pixel_order=PIXEL_ORDER,# Pixel color channel order. GRBW(default) or GRB.
        frequency=6_400_000,    # For 800kHz use 6400000 (default). For 400kHz, use 3200000.
        reset_time=80e-6,       # Reset low level time in seconds. Default is 80e-6.
        bit0=192,               # Bit pattern to set timing for a NeoPixel 0 bit.
        bit1=248,               # Bit pattern to set timing for a NeoPixel 1 bit.
    )
    start_position = START_POSITION

    terminal_settings = None
    try:
        terminal_settings = enable_single_key_input()

        pixels.fill(0)
        pixels.show()
        animation_start = time.monotonic()
        next_position_time = animation_start + POSITION_INTERVAL
        direction = -1 if MOVE_REVERSE else 1

        while True:
            # --------------------------------------------------------
            # Press 1 for RGB gradation, 2 for rainbow, 3 for random, and q to quit.
            key = read_key()
            if key == "q":
                raise QuitRequested
            if key == "1":
                pattern = led_pattern.generate_gradation_pattern(
                    LED_ON_NUM, START_COLOR, END_COLOR
                )
            elif key == "2":
                pattern = led_pattern.generate_rainbow_pattern(
                    LED_ON_NUM, RAINBOW_START_COLOR, RAINBOW_END_COLOR
                )
            elif key == "3":
                pattern = led_pattern.generate_random_pattern(
                    LED_ON_NUM, RANDOM_LED_ON_RATE, RANDOM_COLOR_NUM, PRIMARY_COLOR_RATE
                )

            # --------------------------------------------------------
            now = time.monotonic()
            if now >= next_position_time:
                steps = int((now - next_position_time) // POSITION_INTERVAL) + 1
                start_position = (start_position + direction * steps) % NUM_PIXELS
                next_position_time += steps * POSITION_INTERVAL

            adjusted_pattern = led_pattern.adjust_led_brightness(
                pattern,
                now - animation_start,
                MAX_BRIGHTNESS,
                ON_TIME,
                OFF_TIME,
                FADE_IN_RATE,
                FADE_OUT_RATE,
            )

            pixels.fill(0)
            for offset, color in enumerate(adjusted_pattern):
                pixels[(start_position + offset) % NUM_PIXELS] = color
            pixels.show()
            time.sleep(LOOP_WAIT)


    except (KeyboardInterrupt, QuitRequested):
        pass

    finally:
        try:
            restore_terminal(terminal_settings)
        finally:
            pixels.fill(0)
            pixels.show()

if __name__ == "__main__":
    main()
