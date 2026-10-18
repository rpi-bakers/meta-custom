"""LED color and pattern generation utilities."""

import colorsys
import math
import random
from numbers import Real

# High-contrast color palette
PRIMARY_COLORS = [
    (255, 0, 0),       # Red
    (255, 128, 0),     # Orange
    (255, 255, 0),     # Yellow
    (0, 255, 0),       # Green
    (0, 255, 255),     # Cyan
    (0, 0, 255),       # Blue
    (128, 0, 255),     # Purple
    (255, 0, 255),     # Magenta
]

def _validate_color(color, name):
    if not isinstance(color, (list, tuple)) or len(color) != 3:
        raise ValueError(f"{name} must contain exactly three RGB values")
    if any(
        not isinstance(channel, int)
        or isinstance(channel, bool)
        or not 0 <= channel <= 255
        for channel in color
    ):
        raise ValueError(f"{name} RGB values must be integers from 0 to 255")


def _validate_led_count(led_count):
    if not isinstance(led_count, int) or isinstance(led_count, bool) or led_count < 0:
        raise ValueError("led_on_num must be a non-negative integer")


def _validate_time(value, name):
    if not isinstance(value, Real) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite non-negative number")


def _validate_pattern(pattern):
    if not isinstance(pattern, (list, tuple)):
        raise ValueError("pattern must be a list or tuple of RGB values")
    for index, color in enumerate(pattern):
        _validate_color(color, f"pattern[{index}]")

def hsl_to_rgb(hue, saturation=1, brightness=1):
    """
    Convert a hue, saturation, and brightness value to an RGB color.

    Args:
        hue: Hue angle in degrees.
        saturation: Saturation from 0.0 to 1.0.
        brightness: Brightness from 0.0 to 1.0.

    Returns:
        An RGB tuple with channels in the range 0 to 255.
    """
    hue = hue % 360
    _hi = int((hue/60)%6)
    _f = hue / 60.0 - _hi
    _p = brightness * (1 - saturation)
    _q = brightness * (1 - _f * saturation)
    _t = brightness * (1 - (1 - _f) * saturation)

    _r_val = 0
    _g_val = 0
    _b_val = 0

    if _hi == 0:
        _r_val = brightness
        _g_val = _t
        _b_val = _p
    if _hi == 1:
        _r_val = _q
        _g_val = brightness
        _b_val = _p
    if _hi == 2:
        _r_val = _p
        _g_val = brightness
        _b_val = _t
    if _hi == 3:
        _r_val = _p
        _g_val = _q
        _b_val = brightness
    if _hi == 4:
        _r_val = _t
        _g_val = _p
        _b_val = brightness
    if _hi == 5:
        _r_val = brightness
        _g_val = _p
        _b_val = _q

    r = int(_r_val * 255)
    g = int(_g_val * 255)
    b = int(_b_val * 255)
    return (r, g, b)

def adjust_led_brightness(
    pattern,
    elapsed_time,
    max_brightness,
    on_time,
    off_time,
    on_fade_rate,
    off_fade_rate):

    """
    Apply the repeating on/off cycle and fade envelope to an RGB pattern.

    Args:
        pattern: RGB colors, one per LED.
        elapsed_time: Time in seconds since the cycle began.
        max_brightness: Maximum output brightness as a percentage (0-100).
        on_time: Duration of the on phase in seconds.
        off_time: Duration of the off phase in seconds.
        on_fade_rate: Portion of the on phase used to fade in (0-100%).
        off_fade_rate: Portion of the off phase used to fade out (0-100%).

    Returns:
        A new RGB pattern scaled to the current brightness.
    """

    _validate_pattern(pattern)
    _validate_time(elapsed_time, "elapsed_time")
    _validate_time(on_time, "on_time")
    _validate_time(off_time, "off_time")
    for rate, name in (
        (max_brightness, "max_brightness"),
        (on_fade_rate, "on_fade_rate"),
        (off_fade_rate, "off_fade_rate"),
    ):
        if not isinstance(rate, Real) or not math.isfinite(rate) or not 0 <= rate <= 100:
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


def generate_gradation_pattern(led_on_num, start_color, end_color):
    """
    Generate a linear RGB gradient between two colors.

    Args:
        led_on_num: Number of LEDs in the returned pattern.
        start_color: RGB color for the first LED.
        end_color: RGB color for the last LED.

    Returns:
        A list of RGB tuples interpolated between the endpoint colors.
    """
    _validate_led_count(led_on_num)
    _validate_color(start_color, "start_color")
    _validate_color(end_color, "end_color")

    if led_on_num == 0:
        return []
    if led_on_num == 1:
        return [tuple(start_color)]

    return [
        tuple(
            round(start + (end - start) * index / (led_on_num - 1))
            for start, end in zip(start_color, end_color)
        )
        for index in range(led_on_num)
    ]


def generate_rainbow_pattern(led_on_num, start_color, end_color):
    """
    Generate an HSV-interpolated color pattern between two RGB colors.

    Args:
        led_on_num: Number of LEDs in the returned pattern.
        start_color: RGB color for the first LED.
        end_color: RGB color for the last LED.

    Returns:
        A list of RGB tuples interpolated between the endpoint colors.
    """
    _validate_led_count(led_on_num)
    _validate_color(start_color, "start_color")
    _validate_color(end_color, "end_color")
    if led_on_num == 0:
        return []
    if led_on_num == 1:
        return [tuple(start_color)]

    start_hue, start_saturation, start_value = colorsys.rgb_to_hsv(
        *(channel / 255 for channel in start_color)
    )
    end_hue, end_saturation, end_value = colorsys.rgb_to_hsv(
        *(channel / 255 for channel in end_color)
    )
    hue_difference = (end_hue - start_hue) % 1.0

    rainbow_pattern = []
    for index in range(led_on_num):
        fraction = index / (led_on_num - 1)
        hue = (start_hue + hue_difference * fraction) % 1.0
        saturation = start_saturation + (end_saturation - start_saturation) * fraction
        value = start_value + (end_value - start_value) * fraction
        rainbow_pattern.append(
            tuple(
                round(channel * 255)
                for channel in colorsys.hsv_to_rgb(hue, saturation, value)
            )
        )
    return rainbow_pattern

def generate_random_pattern(
    led_num,
    led_on_rate,
    color_num,
    primary_color_rate=70,
):
    """
    Generate a random color pattern with a target proportion of lit LEDs.

    Args:
        led_num: Number of LEDs represented by the returned pattern.
        led_on_rate: Target proportion of lit LEDs, from 0 to 100 percent.
        color_num: Number of candidate colors to generate.
        primary_color_rate: Chance (0-100%) to choose each candidate from
            PRIMARY_COLORS. Remaining candidates are generated from HSV values.

    Returns:
        A list of led_num RGB tuples. The number of lit LEDs is rounded to
        the nearest whole LED; unlit LEDs are black.
    """

    _validate_led_count(led_num)

    if (
        not isinstance(led_on_rate, Real)
        or isinstance(led_on_rate, bool)
        or not math.isfinite(led_on_rate)
        or not 0 <= led_on_rate <= 100
    ):
        raise ValueError("led_on_rate must be between 0 and 100")

    if (
        not isinstance(color_num, int)
        or isinstance(color_num, bool)
        or color_num <= 0
    ):
        raise ValueError("color_num must be a positive integer")

    if (
        not isinstance(primary_color_rate, Real)
        or isinstance(primary_color_rate, bool)
        or not math.isfinite(primary_color_rate)
        or not 0 <= primary_color_rate <= 100
    ):
        raise ValueError("primary_color_rate must be between 0 and 100")

    lit_count = round(led_num * led_on_rate / 100)

    if lit_count == 0:
        return [(0, 0, 0) for _ in range(led_num)]


    # ------------------------------------------------------------
    # Generate the palette of candidate colors.
    # ------------------------------------------------------------

    colors = []

    for _ in range(color_num):

        # Choose primary colors with the configured probability.
        if random.random() < primary_color_rate / 100:
            color = random.choice(PRIMARY_COLORS)

        else:
            # Generate a random color outside the primary palette.
            hue = random.uniform(0.0, 360.0)
            saturation = random.uniform(0.85, 1.0)
            brightness = random.uniform(0.85, 1.0)

            r, g, b = colorsys.hsv_to_rgb(
                hue / 360.0,
                saturation,
                brightness
            )

            color = (
                round(r * 255),
                round(g * 255),
                round(b * 255),
            )

        colors.append(color)

    # ------------------------------------------------------------
    # Randomly choose the positions of the lit LEDs.
    # ------------------------------------------------------------

    lit_positions = set(
        random.sample(range(led_num), lit_count)
    )

    # ------------------------------------------------------------
    # Build the output pattern.
    # ------------------------------------------------------------

    return [
        random.choice(colors)
        if position in lit_positions
        else (0, 0, 0)
        for position in range(led_num)
    ]
