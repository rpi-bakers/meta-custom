"""
LED ramdom color pattern generator.
"""

import colorsys
import random

from enum import StrEnum
from led_pattern import LedPattern

class PatternType(StrEnum):
    DEFAULT = "DEFAULT"

# --------------------------------------------------------------------------------------------------
# Random color settings
# LED_ON_RATE       | 0 to 100                          |
# COLOR_NUM         | 0 < RANDOM_COLOR_NUM < LED_ON_NUM |
# PRIMARY_COLOR_RATE| 0 to 100                          |
# --------------------------------------------------------------------------------------------------
LED_ON_RATE = 75
COLOR_NUM = 8
PRIMARY_COLOR_RATE = 80

PRIMARY_COLORS = [
    (255, 0, 0),    # Red
    (255, 128, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (128, 0, 255),  # Purple
    (255, 0, 255),  # Magenta
]

# --------------------------------------------------------------------------------------------------
PALETTES = {
    PatternType.DEFAULT: PRIMARY_COLORS,
}

def generate(
        led_on_num,
        pattern_type= PatternType.DEFAULT
) -> list[tuple[int, int, int]] | None:
    """
    Generate a random color pattern with a target proportion of lit LEDs.
    Args:
        led_on_num (int): Number of LEDs in the returned pattern.
        pattern_type (PatternType): LED pattern type.
    Returns:
        A list of led_num RGB tuples. The number of lit LEDs is rounded to
        the nearest whole LED; unlit LEDs are black.
    """
    led_num = led_on_num
    color_num = COLOR_NUM
    led_on_rate = LED_ON_RATE
    primary_color_rate = PRIMARY_COLOR_RATE
    palette = PALETTES[pattern_type]

    LedPattern.validate_led_count(led_num)

    if not 0 <= led_on_rate <= 100:
        raise ValueError("led_on_rate must be between 0 and 100")
    if color_num <= 0:
        raise ValueError("color_num must be a positive integer")
    if not 0 <= primary_color_rate <= 100:
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
            color = random.choice(palette)
        else:
            # Generate a random color outside the primary palette.
            hue = random.uniform(0.0, 360.0)
            saturation = random.uniform(0.85, 1.0)
            brightness = random.uniform(0.85, 1.0)
            r, g, b = colorsys.hsv_to_rgb(hue / 360.0, saturation, brightness)
            color = (round(r * 255), round(g * 255), round(b * 255))

        colors.append(color)

    # ------------------------------------------------------------
    # Randomly choose the positions of the lit LEDs.
    # ------------------------------------------------------------
    lit_positions = set(random.sample(range(led_num), lit_count))

    # ------------------------------------------------------------
    # Build the output pattern.
    # ------------------------------------------------------------
    return [
        random.choice(colors)
        if position in lit_positions
        else (0, 0, 0)
        for position in range(led_num)
    ]
