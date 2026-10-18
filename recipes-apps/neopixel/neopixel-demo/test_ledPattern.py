
import math
import random
import unittest


import ledPattern


class ValidationHelperTests(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def test_validate_color_accepts_rgb_byte_values(self):
        """_summary_
        """
        self.assertIsNone(ledPattern._validate_color((0, 128, 255), "color"))
        self.assertIsNone(ledPattern._validate_color([1, 2, 3], "color"))

    def test_validate_color_rejects_wrong_shape_or_channel_values(self):
        """_summary_
        """
        for color in (None, "red", (1, 2), (1, 2, 3, 4), (1, -1, 3), (1, 256, 3), (1, True, 3)):
            with self.subTest(color=color), self.assertRaises(ValueError):
                ledPattern._validate_color(color, "color")

    def test_validate_led_count_requires_a_nonnegative_integer(self):
        self.assertEqual(
            ledPattern.generate_gradation_pattern(0, (0, 0, 0), (255, 255, 255)), []
        )
        self.assertEqual(
            len(ledPattern.generate_gradation_pattern(5, (0, 0, 0), (255, 255, 255))),
            5,
        )
        for count in (-1, 1.5, True, "3"):
            with self.subTest(count=count), self.assertRaises(ValueError):
                ledPattern.generate_gradation_pattern(
                    count, (0, 0, 0), (255, 255, 255)
                )

    def test_validate_time_requires_a_finite_nonnegative_number(self):
        self.assertIsNone(ledPattern._validate_time(0, "time"))
        self.assertIsNone(ledPattern._validate_time(0.5, "time"))
        for value in (-1, math.inf, -math.inf, math.nan, "1"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                ledPattern._validate_time(value, "time")

    def test_validate_pattern_checks_each_rgb_color(self):
        self.assertIsNone(ledPattern._validate_pattern([(0, 0, 0), (255, 128, 1)]))
        for pattern in (None, "red", [(0, 0, 0), (256, 0, 0)]):
            with self.subTest(pattern=pattern), self.assertRaises(ValueError):
                ledPattern._validate_pattern(pattern)


class AdjustLedBrightnessTests(unittest.TestCase):
    pattern = [(200, 100, 50), (0, 255, 128)]

    def adjust(self, elapsed_time, **overrides):
        settings = {
            "maxBrightness": 80,
            "OnTime": 1.0,
            "OffTime": 1.0,
            "onFadeRate": 50,
            "offFadeRate": 50,
        }
        settings.update(overrides)
        return ledPattern.adjust_led_brightness(
            self.pattern, elapsed_time, **settings
        )

    def test_fade_in_reaches_capped_brightness_and_does_not_mutate_input(self):
        original = [color[:] for color in self.pattern]

        self.assertEqual(self.adjust(0), [(0, 0, 0), (0, 0, 0)])
        self.assertEqual(self.adjust(0.25), [(80, 40, 20), (0, 102, 51)])
        self.assertEqual(self.adjust(0.5), [(160, 80, 40), (0, 204, 102)])
        self.assertEqual(self.adjust(0.75), [(160, 80, 40), (0, 204, 102)])
        self.assertEqual(self.pattern, original)

    def test_fade_out_and_cycle_restart(self):
        self.assertEqual(self.adjust(1.0), [(160, 80, 40), (0, 204, 102)])
        self.assertEqual(self.adjust(1.25), [(80, 40, 20), (0, 102, 51)])
        self.assertEqual(self.adjust(1.5), [(0, 0, 0), (0, 0, 0)])
        self.assertEqual(self.adjust(2.0), [(0, 0, 0), (0, 0, 0)])
        self.assertEqual(self.adjust(2.5), [(160, 80, 40), (0, 204, 102)])

    def test_zero_fade_rates_switch_immediately(self):
        self.assertEqual(
            self.adjust(0, onFadeRate=0),
            [(160, 80, 40), (0, 204, 102)],
        )
        self.assertEqual(
            self.adjust(1.0, offFadeRate=0),
            [(0, 0, 0), (0, 0, 0)],
        )

    def test_zero_on_time_is_always_off(self):
        self.assertEqual(
            ledPattern.adjust_led_brightness(self.pattern, 0.2, 100, 0, 1, 50, 50),
            [(0, 0, 0), (0, 0, 0)],
        )

    def test_zero_off_time_keeps_leds_on_without_restarting_fade(self):
        expected = [(200, 100, 50), (0, 255, 128)]
        self.assertEqual(
            ledPattern.adjust_led_brightness(self.pattern, 0.5, 100, 1, 0, 50, 50),
            expected,
        )
        self.assertEqual(
            ledPattern.adjust_led_brightness(self.pattern, 1.0, 100, 1, 0, 50, 50),
            expected,
        )
        self.assertEqual(
            ledPattern.adjust_led_brightness(self.pattern, 1.5, 100, 1, 0, 50, 50),
            expected,
        )

    def test_empty_pattern_is_supported(self):
        self.assertEqual(ledPattern.adjust_led_brightness([], 0, 100, 1, 1, 50, 50), [])

    def test_rejects_invalid_pattern_time_and_percentage(self):
        invalid_cases = (
            ([(256, 0, 0)], 0, 100, 1, 1, 50, 50),
            (self.pattern, -1, 100, 1, 1, 50, 50),
            (self.pattern, math.inf, 100, 1, 1, 50, 50),
            (self.pattern, 0, 100, -1, 1, 50, 50),
            (self.pattern, 0, 101, 1, 1, 50, 50),
            (self.pattern, 0, 100, 1, 1, math.nan, 50),
        )
        for arguments in invalid_cases:
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                ledPattern.adjust_led_brightness(*arguments)


class GenerateGradationPatternTests(unittest.TestCase):
    def test_interpolates_endpoints_and_intermediate_rgb_values(self):
        self.assertEqual(
            ledPattern.generate_gradation_pattern(3, (255, 0, 0), (0, 0, 255)),
            [(255, 0, 0), (128, 0, 128), (0, 0, 255)],
        )

    def test_zero_and_one_led(self):
        self.assertEqual(
            ledPattern.generate_gradation_pattern(0, (255, 0, 0), (0, 0, 255)), []
        )
        self.assertEqual(
            ledPattern.generate_gradation_pattern(1, (255, 0, 0), (0, 0, 255)),
            [(255, 0, 0)],
        )

    def test_validates_led_count_and_colors(self):
        for count in (-1, 1.5, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                ledPattern.generate_gradation_pattern(count, (0, 0, 0), (255, 255, 255))
        for color in ((0, 0), (256, 0, 0), (0, False, 0), "red"):
            with self.subTest(color=color), self.assertRaises(ValueError):
                ledPattern.generate_gradation_pattern(2, color, (255, 255, 255))


class GenerateRainbowPatternTests(unittest.TestCase):
    def test_generates_requested_count_with_exact_endpoints(self):
        start = (255, 0, 0)
        end = (0, 0, 255)
        original_start, original_end = start[:], end[:]
        pattern = ledPattern.generate_rainbow_pattern(5, start, end)

        self.assertEqual(len(pattern), 5)
        self.assertEqual(pattern[0], start)
        self.assertEqual(pattern[-1], end)
        self.assertEqual(start, original_start)
        self.assertEqual(end, original_end)
        for color in pattern:
            self.assertEqual(len(color), 3)
            self.assertTrue(all(isinstance(channel, int) for channel in color))
            self.assertTrue(all(0 <= channel <= 255 for channel in color))

    def test_interpolates_hue_over_shortest_wraparound_path(self):
        pattern = ledPattern.generate_rainbow_pattern(
            3, (255, 0, 16), (255, 0, 0)
        )

        self.assertEqual(pattern[0], (255, 0, 16))
        self.assertEqual(pattern[-1], (255, 0, 0))
        self.assertGreater(pattern[1][0], 240)
        self.assertLess(pattern[1][1], 10)
        self.assertGreater(pattern[1][2], 5)

    def test_zero_and_one_led(self):
        self.assertEqual(
            ledPattern.generate_rainbow_pattern(0, (255, 0, 0), (0, 0, 255)), []
        )
        self.assertEqual(
            ledPattern.generate_rainbow_pattern(1, (255, 0, 0), (0, 0, 255)),
            [(255, 0, 0)],
        )

    def test_validates_led_count_and_colors(self):
        for count in (-1, 1.5, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                ledPattern.generate_rainbow_pattern(count, (0, 0, 0), (255, 255, 255))
        for color in ((0, 0), (256, 0, 0), (0, False, 0), "red"):
            with self.subTest(color=color), self.assertRaises(ValueError):
                ledPattern.generate_rainbow_pattern(2, (0, 0, 0), color)


class GenerateRandomPatternTests(unittest.TestCase):
    def test_generates_exact_lit_ratio_with_only_requested_random_colors(self):
        random.seed(1234)
        pattern = ledPattern.generate_random_pattern(10, 30, 2)

        lit_colors = [color for color in pattern if color != (0, 0, 0)]
        self.assertEqual(len(pattern), 10)
        self.assertEqual(len(lit_colors), 3)
        self.assertLessEqual(len(set(lit_colors)), 2)
        for color in pattern:
            self.assertEqual(len(color), 3)
            self.assertTrue(all(isinstance(channel, int) for channel in color))
            self.assertTrue(all(0 <= channel <= 255 for channel in color))

    def test_zero_and_full_lit_rates(self):
        self.assertEqual(
            ledPattern.generate_random_pattern(4, 0, 2),
            [(0, 0, 0)] * 4,
        )
        random.seed(1234)
        pattern = ledPattern.generate_random_pattern(4, 100, 2)
        self.assertEqual(len(pattern), 4)
        self.assertTrue(all(color != (0, 0, 0) for color in pattern))

    def test_validates_led_count_rate_and_color_count(self):
        for count in (-1, 1.5, True):
            with self.subTest(ledNum=count), self.assertRaises(ValueError):
                ledPattern.generate_random_pattern(count, 50, 2)
        for rate in (-1, 100.1, math.inf, math.nan, True):
            with self.subTest(ledOnRate=rate), self.assertRaises(ValueError):
                ledPattern.generate_random_pattern(4, rate, 2)
        for color_count in (0, -1, 1.5, True, 256 ** 3):
            with self.subTest(colorNum=color_count), self.assertRaises(ValueError):
                ledPattern.generate_random_pattern(4, 50, color_count)


if __name__ == "__main__":
    unittest.main()
