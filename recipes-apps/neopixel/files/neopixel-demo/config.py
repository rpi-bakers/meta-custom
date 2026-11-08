"""
User settings for NeoPixel demo.
"""

import json
import math
from pathlib import Path

# --------------------------------------------------------------------------------------------------
# Device settings
# --------------------------------------------------------------------------------------------------
# LED_NUM       | 1 to 164          | Number of LEDs connected to the SPI LED strip |
# MAX_BRIGHTNESS| 0(Off) to 100[%]  | Brightness MAX limit of the LEDs.             |
# Depends on power supply current and SPI bus frequency
# In a experiment, 164 LEDs worked at 5V, 1.8A.
# --------------------------------------------------------------------------------------------------
LED_NUM = 164
MAX_BRIGHTNESS = 5

# --------------------------------------------------------------------------------------------------
# LED settings
# --------------------------------------------------------------------------------------------------
# START_POSITION    | 0 to LED_NUM - 1  | Initial starting position of the lit area.|
# LED_ON_NUM        | 0 to LED_NUM      | The number of LEDs to use.                |
# --------------------------------------------------------------------------------------------------
START_POSITION = 0
LED_ON_NUM = 100

# --------------------------------------------------------------------------------------------------
# Blink timing
# --------------------------------------------------------------------------------------------------
# TIME_INTERVAL | 0 to x.xxxx   | Main loop cycle time [seconds]                |
# CYCLE_SEC     | 0 to x.xx     | Time to stay at current LED position [seconds]|
# ON_TIME       | 0 to x        | LED ON duration [seconds]                     |
# OFF_TIME      | 0 to x        | LED OFF duration[seconds]                     |
# FADE_IN_RATE  | 0 to 100      | Fade-in duration = ON_TIME  * rate / 100      |
# FADE_OUT_RATE | 0 to 100      | Fade-out duration = OFF_TIME * rate / 100     |
# MOVE_REVERSE  | True or False | False: forward / True: reverse                |
# --------------------------------------------------------------------------------------------------
TIME_INTERVAL = 0.1
CYCLE_SEC = 0.5
ON_TIME = 1.5
OFF_TIME = 0.5
FADE_IN_RATE = 80
FADE_OUT_RATE = 80
MOVE_REVERSE = False
PATTERN_FREQ = 10

SETTINGS_PATH = Path(__file__).with_name("settings.json")

DEFAULT_SETTINGS = {
    "LED_NUM": LED_NUM,
    "LED_ON_NUM": LED_ON_NUM,
    "START_POSITION": START_POSITION,
    "MAX_BRIGHTNESS": MAX_BRIGHTNESS,
    "ON_TIME": ON_TIME,
    "OFF_TIME": OFF_TIME,
    "FADE_IN_RATE": FADE_IN_RATE,
    "FADE_OUT_RATE": FADE_OUT_RATE,
    "CYCLE_SEC": CYCLE_SEC,
    "TIME_INTERVAL": TIME_INTERVAL,
    "PATTERN_FREQ": PATTERN_FREQ,
    "MOVE_REVERSE": MOVE_REVERSE,
    "PATTERN": "gradation",
}

PATTERN_OPTIONS = {
    "gradation",
    "rainbow",
    "random",
    "halloween_jack_o_lantern",
    "halloween_witch_portion",
    "halloween_vampire_night",
    "halloween_ghostly_moon",
    "halloween_black_cat",
}


def _validate_settings(settings):
    if not isinstance(settings, dict):
        raise ValueError("settings.json must contain a JSON object")

    unknown_keys = settings.keys() - DEFAULT_SETTINGS.keys()
    if unknown_keys:
        raise ValueError(f"Unknown settings in settings.json: {', '.join(sorted(unknown_keys))}")

    validated = DEFAULT_SETTINGS.copy()
    validated.update(settings)

    integer_ranges = {
        "LED_NUM": (1, 300),
        "LED_ON_NUM": (1, 300),
        "START_POSITION": (0, None),
        "MAX_BRIGHTNESS": (0, 100),
        "FADE_IN_RATE": (0, 100),
        "FADE_OUT_RATE": (0, 100),
        "PATTERN_FREQ": (1, 50),
    }
    for name, (minimum, maximum) in integer_ranges.items():
        value = validated[name]
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{name} in settings.json must be an integer")
        if value < minimum or (maximum is not None and value > maximum):
            raise ValueError(f"{name} in settings.json is out of range")

    if validated["LED_ON_NUM"] > validated["LED_NUM"]:
        raise ValueError("LED_ON_NUM in settings.json cannot exceed LED_NUM")
    if validated["START_POSITION"] >= validated["LED_NUM"]:
        raise ValueError("START_POSITION in settings.json must be less than LED_NUM")

    number_ranges = {
        "ON_TIME": (0.0, 10.0),
        "OFF_TIME": (0.0, 10.0),
        "CYCLE_SEC": (0.01, 10.0),
        "TIME_INTERVAL": (0.01, 10.0),
    }
    for name, (minimum, maximum) in number_ranges.items():
        value = validated[name]
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(value)
            or not minimum <= value <= maximum
        ):
            raise ValueError(f"{name} in settings.json must be between {minimum} and {maximum}")
        validated[name] = float(value)

    if not isinstance(validated["MOVE_REVERSE"], bool):
        raise ValueError("MOVE_REVERSE in settings.json must be a boolean")
    if not isinstance(validated["PATTERN"], str) or validated["PATTERN"] not in PATTERN_OPTIONS:
        raise ValueError("PATTERN in settings.json is not a supported pattern")

    return validated


def load_settings():
    """Load and validate persisted settings, falling back to defaults if none exist."""
    try:
        with SETTINGS_PATH.open(encoding="utf-8") as settings_file:
            settings = json.load(settings_file)
    except FileNotFoundError:
        return DEFAULT_SETTINGS.copy()
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {SETTINGS_PATH}: {error}") from error

    return _validate_settings(settings)


def save_settings(settings):
    """Validate and persist current settings as formatted JSON."""
    validated = _validate_settings(settings)
    with SETTINGS_PATH.open("w", encoding="utf-8") as settings_file:
        json.dump(validated, settings_file, indent=4)
        settings_file.write("\n")

# --------------------------------------------------------------------------------------------------
# LED Animation Timing Chart
# --------------------------------------------------------------------------------------------------
#   |<- one cycle ------------------------------------>|
#   |<---------- ON_TIME -------------><-- OFF_TIME -->|
#   |<-FADE_IN_->|                     |<- FADE_OUT_ ->|
#   |   _RATE[%] |                     |    _RATE[%]   |
#   |            +---------------------+               |
#   |          /                          \            |
#   |       /                                 \        |
#   |    /                                        \    |
#   | /                                              \ |
#   +------------+---------------------+---------------+--> time
#   ^            ^                     ^               ^
#   |            |                     |               |
#   ON start    Fade-in end           OFF start       OFF end
#
# Position
# ==============================================================================
#
# [MOVE_REVERSE = False] LED 0               LED 1                LED 2
#   ●                    ●                    ●                    ●
#   +-----CYCLE_SEC------>-----CYCLE_SEC------>-----CYCLE_SEC------>  time
#   ●                    ●                    ●                    ●
# [MOVE_REVERSE =  True] LED 2                LED 1                LED 0
# =============================================================================
