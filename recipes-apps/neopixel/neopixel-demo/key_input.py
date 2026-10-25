"""
key input class.
"""

import sys
import os
import select
import tty
import termios

class QuitRequested(Exception):
    """Raised when the user presses q."""

class KeyBoard:
    """
    key input control.
    """

    def __init__(self):
        """
        init class.
        """
        self.settings = None
        self.enable_single_key_input()

    def __del__(self):
        """
        destruct class.
        """
        self.restore_terminal()

    @staticmethod
    def read():
        """
        Read one available key from an interactive terminal without blocking.
        if input "q", raise QuitRequested.
        """
        if not sys.stdin.isatty():
            return None

        file_descriptor = sys.stdin.fileno()
        readable, _, _ = select.select([file_descriptor], [], [], 0)

        if not readable:
            return None

        key = os.read(file_descriptor, 1).decode("ascii", errors="ignore").lower()
        print("Input key:", key, end="", flush=True)

        if key == "q":
            raise QuitRequested

        return key

    def enable_single_key_input(self):
        """
        Enable immediate key reads and restore the terminal when finished.
        """

        if not sys.stdin.isatty():
            return None

        file_descriptor = sys.stdin.fileno()
        previous_settings = termios.tcgetattr(file_descriptor)
        tty.setcbreak(file_descriptor)
        self.settings = file_descriptor, previous_settings

        return None

    def restore_terminal(self):
        """
        Restore terminal settings changed for single-key input.
        """
        if self.settings is not None:
            file_descriptor, previous_settings = self.settings
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, previous_settings)
