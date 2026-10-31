"""
LED rainbow color pattern generator.
"""

import colorsys

from enum import StrEnum
from led_pattern import LedPattern

class PatternType(StrEnum):
    DEFAULT = "DEFAULT"

# --------------------------------------------------------------------------------------------------
# Rainbow color settings
RAINBOW_COLORS =[
    #  R, G, B : 0 to 255
    (255, 0, 0),    # Red    as start color
    (128, 0, 128),  # Purple as end color
]

# --------------------------------------------------------------------------------------------------
PALETTES = {
    PatternType.DEFAULT: RAINBOW_COLORS,
}

def generate(
        led_on_num,
        pattern_type= PatternType.DEFAULT
) -> list[tuple[int, int, int]] | None:
    """
    Generate an HSV-interpolated color pattern between two RGB colors.

    Args:
        led_on_num (int): Number of LEDs in the returned pattern.
        pattern_type (PatternType): LED pattern type.
    Returns:
        A list of RGB tuples interpolated between the endpoint colors.
    """
    start_color, end_color = LedPattern.get_boundary_colors(PALETTES[pattern_type])
    LedPattern.validate_led_count(led_on_num)

    if led_on_num == 0: return None
    if led_on_num == 1: return [start_color]

    start_hue, start_saturation, start_value \
        = colorsys.rgb_to_hsv(*(channel / 255 for channel in start_color))
    end_hue, end_saturation, end_value \
        = colorsys.rgb_to_hsv(*(channel / 255 for channel in end_color))
    hue_difference = (end_hue - start_hue) % 1.0

    pattern = []
    for index in range(led_on_num):
        fraction = index / (led_on_num - 1)
        hue = (start_hue + hue_difference * fraction) % 1.0
        saturation = start_saturation + (end_saturation - start_saturation) * fraction
        value = start_value + (end_value - start_value) * fraction
        pattern.append(
            tuple(
                round(channel * 255)
                for channel in colorsys.hsv_to_rgb(hue, saturation, value)
            )
        )

    return pattern
