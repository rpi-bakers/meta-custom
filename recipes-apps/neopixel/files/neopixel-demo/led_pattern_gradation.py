"""
LED gradation color pattern generator.
"""

from led_pattern import LedPattern


def generate(
        led_on_num,
        start_color,
        end_color) -> list[tuple[int, int, int]]:
    """
    Generate a linear RGB gradient between two colors.

    Args:
        led_on_num (int): Number of LEDs in the returned pattern.
        start_color (tuple[int, int, int]): RGB color for the first LED.
        end_color (tuple[int, int, int]): RGB color for the last LED.

    Returns:
        A list of RGB tuples interpolated between the endpoint colors.
    """
    LedPattern.validate_led_count(led_on_num)
    LedPattern.validate_color(start_color, "start_color")
    LedPattern.validate_color(end_color, "end_color")

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
