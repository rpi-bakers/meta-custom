"""
LED gradation color pattern generator.
"""

from enum import StrEnum
from led_pattern import LedPattern

class PatternType(StrEnum):
    DEFAULT = "DEFAULT"

GRADATION_DEFAULT = [
    (255, 0, 0),    # Red    as the starting color
    (0, 0, 255),    # Purple as the ending color
]

# --------------------------------------------------------------------------------------------------
PALETTES = {
    PatternType.DEFAULT: GRADATION_DEFAULT,
}

def generate(
        led_on_num,
        pattern_freq,
        pattern_type= PatternType.DEFAULT
) -> list[tuple[int, int, int]] | None:
    """
    Generate a linear RGB gradient between two colors.
    Args:
        led_on_num (int): Number of LEDs in the returned pattern.
        pattern_freq (int): Frequency of each patterns in the led_on_num.
        pattern_type (PatternType): LED pattern type.
    Returns:
        A list of RGB tuples interpolated between the endpoint colors.
    """
    start_color, end_color = LedPattern.get_boundary_colors(PALETTES[pattern_type])
    LedPattern.validate_led_count(led_on_num)

    if led_on_num == 0: return None
    if led_on_num == 1: return [start_color]

    return [
        tuple(
            round(start + (end - start) * ((index * pattern_freq / (led_on_num - 1)) % 1.0))
            for start, end in zip(start_color, end_color)
        )
        for index in range(led_on_num)
    ]
