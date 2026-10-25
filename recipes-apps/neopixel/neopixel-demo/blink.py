#!/usr/bin/env python3

"""LED blinking application """

import time

import led_pattern
import config as cfg

from led_strip import LedStrip
from key_input import KeyBoard, QuitRequested
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
        led_pattern.get_pattern("GRADATION", cfg.LED_ON_NUM),
        cfg.START_POSITION,
        cfg.MAX_BRIGHTNESS,
        cfg.ON_TIME,
        cfg.OFF_TIME,
        cfg.FADE_IN_RATE,
        cfg.FADE_OUT_RATE,
        cfg.CYCLE_SEC,
    )
    led.set_direction( -1 if cfg.MOVE_REVERSE else 1)
    keyboard = KeyBoard()
    timekeeper = TimeKeeper(cfg.TIME_INTERVAL, led.on_time_interval)

    try:
        led.clear()
        timekeeper.start()

        while True:
            key = keyboard.read()
            led.handle_params_change_key(key)
            new_pattern = led_pattern.get_pattern(key, led.led_on_num)
            led.print_params()
            if new_pattern is not None:
                led.pattern = new_pattern

            time.sleep(cfg.TIME_INTERVAL / 2)

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

if __name__ == "__main__":
    main()
