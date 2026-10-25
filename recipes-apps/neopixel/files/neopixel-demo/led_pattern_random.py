"""
LED ramdom color pattern generator.
"""

import colorsys
import random

from led_pattern import LedPattern

# --------------------------------------------------------------------------------------------------
# Random color settings
# LED_ON_RATE       | 0 to 100                          |  |
# COLOR_NUM         | 0 < RANDOM_COLOR_NUM < LED_ON_NUM |  |
# PRIMARY_COLOR_RATE| 0 to 100                          |  |
# --------------------------------------------------------------------------------------------------
LED_ON_RATE = 75
COLOR_NUM = 16
PRIMARY_COLOR_RATE = 50

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

def generate(
    led_num:int = 20,
    color_num:int = 16,
    led_on_rate:int = 75,
    primary_color_rate:int = 70,
) -> list[tuple[int, int, int]]:
    """
    Generate a random color pattern with a target proportion of lit LEDs.

    Args:
        led_num (int): Number of LEDs represented by the returned pattern.
        led_on_rate (int): Target proportion of lit LEDs, from 0 to 100 percent.
        color_num (int): Number of candidate colors to generate.
        primary_color_rate (int): Chance (0-100%) to choose each candidate from
            PRIMARY_COLORS. Remaining candidates are generated from HSV values.

    Returns:
        A list of led_num RGB tuples. The number of lit LEDs is rounded to
        the nearest whole LED; unlit LEDs are black.
    """

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
            color = random.choice(PRIMARY_COLORS)

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
