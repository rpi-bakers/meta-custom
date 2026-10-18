import importlib.util
import pathlib
import sys
import types
import unittest
from contextlib import ExitStack
from unittest.mock import Mock, patch


DEMO_DIR = pathlib.Path(__file__).resolve().parent
BLINK_PATH = DEMO_DIR / "blink.py"


class FakeNeoPixelSPI:
    instances = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.values = [0] * kwargs["n"]
        self.frames = []
        self.fill_calls = []
        self.instances.append(self)

    def fill(self, color):
        self.fill_calls.append(color)
        self.values = [color] * len(self.values)

    def __setitem__(self, index, color):
        self.values[index] = color

    def show(self):
        self.frames.append(list(self.values))


def load_blink_module():
    fake_board = types.ModuleType("board")
    fake_board.SPI = Mock(return_value=object())
    fake_neopixel_spi = types.ModuleType("neopixel_spi")
    fake_neopixel_spi.GRB = "GRB"
    fake_neopixel_spi.NeoPixel_SPI = FakeNeoPixelSPI

    spec = importlib.util.spec_from_file_location("blink_under_test", BLINK_PATH)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(
        sys.modules,
        {
            "board": fake_board,
            "neopixel_spi": fake_neopixel_spi,
            "termios": types.ModuleType("termios"),
            "tty": types.ModuleType("tty"),
        },
    ):
        with patch.object(sys, "path", [str(DEMO_DIR), *sys.path]):
            spec.loader.exec_module(module)
    return module


blink = load_blink_module()


class MainTests(unittest.TestCase):
    def setUp(self):
        FakeNeoPixelSPI.instances.clear()
        blink.LED_NUM = 5
        blink.NUM_PIXELS = 5
        blink.LED_ON_NUM = 3
        blink.MAX_BRIGHTNESS = 50
        blink.START_COLOR = (255, 0, 0)
        blink.END_COLOR = (0, 0, 255)
        blink.START_POSITION = 0
        blink.DELAY = 0.01
        blink.POSITION_INTERVAL = 0.1
        blink.MOVE_REVERSE = True
        blink.ON_TIME = 1.0
        blink.OFF_TIME = 0.5
        blink.FADE_IN_RATE = 10
        blink.FADE_OUT_RATE = 1

    def test_main_uses_stub_renders_pattern_wraps_and_clears_on_exit(self):
        clock = Mock(side_effect=(10.0, 10.01, 10.11))
        stdin = Mock()
        stdin.isatty.return_value = True
        stdin.fileno.return_value = 17

        with ExitStack() as stack:
            spi_factory = stack.enter_context(patch.object(blink.board, "SPI"))
            stack.enter_context(
                patch.object(blink, "enable_single_key_input", return_value=None)
            )
            restore_terminal = stack.enter_context(
                patch.object(blink, "restore_terminal")
            )
            stack.enter_context(patch.object(blink.sys, "stdin", stdin))
            select_call = stack.enter_context(patch.object(blink.select, "select"))
            select_call.side_effect = (
                ([], [], []),
                ([], [], []),
                ([17], [], []),
            )
            read_call = stack.enter_context(patch.object(blink.os, "read"))
            read_call.return_value = b"q"
            stack.enter_context(patch.object(blink.time, "monotonic", clock))
            stack.enter_context(patch.object(blink.time, "sleep"))
            blink.main()

        pixels = FakeNeoPixelSPI.instances[0]
        spi_factory.assert_called_once_with()
        self.assertEqual(
            pixels.kwargs,
            {
                "spi": spi_factory.return_value,
                "n": 5,
                "bpp": 3,
                "brightness": 1.0,
                "auto_write": False,
                "pixel_order": "GRB",
                "frequency": blink.SPI_FREQUENCY,
                "reset_time": 80e-6,
                "bit0": 192,
                "bit1": 248,
            },
        )
        self.assertEqual(len(pixels.frames), 4)
        self.assertEqual(pixels.frames[0], [0] * 5)

        first_frame = pixels.frames[1]
        self.assertEqual(
            {index for index, color in enumerate(first_frame) if color != 0},
            {0, 1, 2},
        )
        second_frame = pixels.frames[2]
        self.assertEqual(
            {index for index, color in enumerate(second_frame) if color != 0},
            {0, 1, 4},
        )
        self.assertEqual(pixels.frames[3], [0] * 5)
        self.assertEqual(pixels.fill_calls, [0] * 4)
        read_call.assert_called_once_with(17, 1)
        restore_terminal.assert_called_once_with(None)

    def test_invalid_settings_fail_before_device_initialization(self):
        blink.LED_ON_NUM = blink.LED_NUM + 1
        with patch.object(blink.board, "SPI") as spi_factory:
            with self.assertRaisesRegex(ValueError, "LED_ON_NUM"):
                blink.main()
        spi_factory.assert_not_called()
        self.assertEqual(FakeNeoPixelSPI.instances, [])

    def test_keys_switch_between_gradation_rainbow_and_random_patterns(self):
        blink.MAX_BRIGHTNESS = 100
        blink.FADE_IN_RATE = 0
        clock = Mock(side_effect=(10.0, 10.01, 10.02, 10.03))
        stdin = Mock()
        stdin.isatty.return_value = True
        stdin.fileno.return_value = 17
        gradation = [(10, 20, 30), (40, 50, 60), (70, 80, 90)]
        rainbow = [(90, 80, 70), (60, 50, 40), (30, 20, 10)]

        with ExitStack() as stack:
            stack.enter_context(patch.object(blink.board, "SPI"))
            stack.enter_context(
                patch.object(blink, "enable_single_key_input", return_value=None)
            )
            stack.enter_context(patch.object(blink, "restore_terminal"))
            stack.enter_context(patch.object(blink.sys, "stdin", stdin))
            select_call = stack.enter_context(patch.object(blink.select, "select"))
            select_call.side_effect = (([17], [], []),) * 4
            read_call = stack.enter_context(patch.object(blink.os, "read"))
            read_call.side_effect = (b"2", b"1", b"3", b"q")
            stack.enter_context(patch.object(blink.time, "monotonic", clock))
            stack.enter_context(patch.object(blink.time, "sleep"))
            gradation_generator = stack.enter_context(
                patch.object(
                    blink.ledPattern,
                    "generate_gradation_pattern",
                    side_effect=(gradation, gradation),
                )
            )
            rainbow_generator = stack.enter_context(
                patch.object(
                    blink.ledPattern,
                    "generate_rainbow_pattern",
                    return_value=rainbow,
                )
            )
            random_pattern = [(1, 2, 3), (0, 0, 0), (4, 5, 6)]
            random_generator = stack.enter_context(
                patch.object(
                    blink.ledPattern,
                    "generate_random_pattern",
                    return_value=random_pattern,
                )
            )
            blink.main()

        pixels = FakeNeoPixelSPI.instances[0]
        self.assertEqual(pixels.frames[1][:3], rainbow)
        self.assertEqual(pixels.frames[2][:3], gradation)
        self.assertEqual(pixels.frames[3], random_pattern + [0] * 2)
        self.assertEqual(pixels.frames[-1], [0] * 5)
        gradation_generator.assert_any_call(
            3, blink.START_COLOR, blink.END_COLOR
        )
        self.assertEqual(gradation_generator.call_count, 2)
        rainbow_generator.assert_called_once_with(
            3, blink.RAINBOW_START_COLOR, blink.RAINBOW_END_COLOR
        )
        self.assertEqual(
            (blink.RAINBOW_START_COLOR, blink.RAINBOW_END_COLOR),
            ((255, 0, 0), (128, 0, 128)),
        )
        random_generator.assert_called_once_with(
            blink.LED_ON_NUM, blink.RANDOM_LED_ON_RATE, blink.RANDOM_COLOR_NUM
        )


if __name__ == "__main__":
    unittest.main()
