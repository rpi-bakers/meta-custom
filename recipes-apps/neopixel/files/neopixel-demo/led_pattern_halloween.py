"""
LED multi-color gradation pattern generator.
"""

from enum import StrEnum
from led_pattern import LedPattern

class PatternType(StrEnum):
    JACK_O_LANTERN = "JACK_O_LANTERN"
    WITCH_PORTION = "WITCH_PORTION"
    VAMPIRE_NIGHT = "VAMPIRE_NIGHT"
    GHOSTLY_MOON = "GHOSTLY_MOON"
    BLACK_CAT = "BLACK_CAT"

# --------------------------------------------------------------------------------------------------
PALETTES = {
    PatternType.JACK_O_LANTERN: [
        (255, 69, 0),      # Orange Red
        (255, 215, 0),     # Gold / Yellow
        (255, 69, 0),      # Red Orange
        (139, 0, 139),     # Dark Magenta / Purple
    ],

    PatternType.WITCH_PORTION: [
        (173, 255, 47),    # Lime Green
        (0, 200, 100),     # Emerald Green
        (0, 255, 255),     # Cyan
        (128, 0, 128),     # Purple
    ],

    PatternType.VAMPIRE_NIGHT: [
        (255, 0, 0),       # Red
        (255, 0, 255),     # Magenta
        (128, 0, 128),     # Purple
        (25, 25, 112),     # Midnight Blue
    ],

    PatternType.GHOSTLY_MOON: [
        (255, 255, 255),   # White
        (0, 255, 255),     # Cyan
        (0, 0, 255),       # Blue
        (128, 0, 128),     # Purple
    ],

    PatternType.BLACK_CAT: [
        (0, 0, 0),         # Black
        (48, 0, 80),       # Dark Purple
        (255, 102, 0),     # Orange
        (255, 255, 0),     # Yellow
    ],
}

def generate(
        led_on_num,
        pattern_freq,
        pattern_type=PatternType.JACK_O_LANTERN
) -> list[tuple[int, int, int]] | None:
    """
    Generate a linear RGB gradient through multiple colors and repeat it.

    Args:
        led_on_num (int): Number of LEDs in the returned pattern.
        pattern_freq (int): Number of gradient repetitions across the LEDs.
        pattern_type (PatternType): LED pattern type.

    Returns:
        A list of RGB tuples interpolated between color stops.
    """
    color_stops = PALETTES[pattern_type]
    LedPattern.validate_led_count(led_on_num)

    if not color_stops:
        raise ValueError("color_stops must contain at least one color")

    for index, color in enumerate(color_stops):
        LedPattern.validate_color(color, f"color_stops[{index}]")

    if led_on_num == 0:
        return None

    if not isinstance(pattern_freq, int) or isinstance(pattern_freq, bool) or pattern_freq <= 0:
        raise ValueError("pattern_freq must be a positive integer")

    if led_on_num == 1:
        return [color_stops[0]]

    if len(color_stops) == 1:
        return [tuple(color_stops[0])] * led_on_num

    # Number of LEDs in one gradient pattern.
    pattern_num = (led_on_num + pattern_freq - 1) // pattern_freq

    # ------------------------------------------------------------
    # Generate one gradient pattern.
    # ------------------------------------------------------------

    random_pattern = []

    for index in range(pattern_num):
        if pattern_num == 1:
            position = 0
        else:
            position = index * (len(color_stops) - 1) / (pattern_num - 1)

        # Find the adjacent color stops.
        segment = min(int(position), len(color_stops) - 2)
        ratio = position - segment

        start_color = color_stops[segment]
        end_color = color_stops[segment + 1]

        # Interpolate RGB values.
        color = tuple(
            round(start + (end - start) * ratio)
            for start, end in zip(start_color, end_color)
        )

        random_pattern.append(color)

    # ------------------------------------------------------------
    # Repeat the gradient pattern.
    # ------------------------------------------------------------

    return [
        random_pattern[position % pattern_num]
        for position in range(led_on_num)
    ]
