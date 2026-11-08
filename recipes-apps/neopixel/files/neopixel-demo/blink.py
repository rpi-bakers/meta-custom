#!/usr/bin/env python3

"""
LED blinking application.
"""

import config as cfg

from led_strip import LedStrip
from key_input import KeyInput
from config_keybind import ConfigKeyBind, QuitRequested
from time_keeper import TimeKeeper

# ==================================================================================================
# Main
# ==================================================================================================
def main():
    """
    Main function to run the LED blink demo.
    """

    settings = cfg.load_settings()

    # create object instances
    led = LedStrip(
        settings["LED_NUM"],
        settings["LED_ON_NUM"],
        settings["START_POSITION"],
        settings["MAX_BRIGHTNESS"],
        settings["ON_TIME"],
        settings["OFF_TIME"],
        settings["FADE_IN_RATE"],
        settings["FADE_OUT_RATE"],
        settings["CYCLE_SEC"],
        settings["PATTERN_FREQ"],
    )
    led.set_direction(-1 if settings["MOVE_REVERSE"] else 1)
    keyboard = KeyInput()
    timekeeper = TimeKeeper(settings["TIME_INTERVAL"], led.on_time_interval)
    keyconfig = ConfigKeyBind(led, settings["PATTERN"])

    try:
        led.clear()
        timekeeper.start()
        led.print_params(0)

        while True:
            key = keyboard.read()
            function = keyconfig.functions.get(key, None)
            led.print_params(timekeeper.elapsed_time)
            if function is not None:
                timekeeper.stop()
                function()
                timekeeper.start()
                print(f"{key} ", end="", flush=True)

    except (KeyboardInterrupt, QuitRequested):
        pass

    finally:
        try:
            if timekeeper is not None:
                timekeeper.stop()
        finally:
            try:
                cfg.save_settings({
                    "LED_NUM": led.led_count,
                    "LED_ON_NUM": led.led_on_num,
                    "START_POSITION": led.start_position,
                    "MAX_BRIGHTNESS": led.max_brightness,
                    "ON_TIME": led.on_time,
                    "OFF_TIME": led.off_time,
                    "FADE_IN_RATE": led.fade_in_rate,
                    "FADE_OUT_RATE": led.fade_out_rate,
                    "CYCLE_SEC": led.interval_sec,
                    "TIME_INTERVAL": timekeeper.interval,
                    "PATTERN_FREQ": led.pattern_freq,
                    "MOVE_REVERSE": led.direction == -1,
                    "PATTERN": keyconfig.pattern,
                })
            finally:
                try:
                    if keyboard is not None:
                        keyboard.restore_terminal()
                finally:
                    led.clear()

# ==================================================================================================
if __name__ == "__main__":
    main()
