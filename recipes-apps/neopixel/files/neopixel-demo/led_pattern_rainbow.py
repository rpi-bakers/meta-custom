"""
LED rainbow color pattern generator.
"""

import colorsys
from  led_pattern import LedPattern

# --------------------------------------------------------------------------------------------------
# Rainbow color settings
# START_COLOR   |0 to 255 each (R,G,B)  | Color on the START_POSITION.              |
# END_COLOR     |0 to 255 each (R,G,B)  | Color on the START_POSITION + LED_ON_NUM. |
# --------------------------------------------------------------------------------------------------
START_COLOR = (255, 0, 0)
END_COLOR = (128, 0, 128)

def generate(
        led_on_num,
        start_color,
        end_color
) -> list[tuple[int, int, int]]:
    """
    Generate an HSV-interpolated color pattern between two RGB colors.

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

    start_hue, start_saturation, start_value = colorsys.rgb_to_hsv(
        *(channel / 255 for channel in start_color)
    )
    end_hue, end_saturation, end_value = colorsys.rgb_to_hsv(
        *(channel / 255 for channel in end_color)
    )
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
