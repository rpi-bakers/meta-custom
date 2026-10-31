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

    # create object instances
    led = LedStrip(
        cfg.LED_NUM,
        cfg.LED_ON_NUM,
        cfg.START_POSITION,
        cfg.MAX_BRIGHTNESS,
        cfg.ON_TIME,
        cfg.OFF_TIME,
        cfg.FADE_IN_RATE,
        cfg.FADE_OUT_RATE,
        cfg.CYCLE_SEC,
        cfg.PATTERN_FREQ,
    )
    led.set_direction( -1 if cfg.MOVE_REVERSE else 1)
    keyboard = KeyInput()
    timekeeper = TimeKeeper(cfg.TIME_INTERVAL, led.on_time_interval)
    keyconfig = ConfigKeyBind(led)

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
                if keyboard is not None:
                    keyboard.restore_terminal()
            finally:
                led.clear()

# ==================================================================================================
if __name__ == "__main__":
    main()
