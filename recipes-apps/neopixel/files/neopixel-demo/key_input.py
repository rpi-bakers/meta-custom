"""
key input class.
"""

import sys
import os

import select
import tty
import termios

class KeyInput:
    """
    key input control.
    """
    def __init__(self):
        """
        init class.
        """
        self._settings = None
        self._enable_single_key_input()

    def __del__(self):
        """
        destruct class.
        """
        self.restore_terminal()

    @staticmethod
    def read():
        """
        Read one available key from an interactive terminal without blocking.
        """
        if not sys.stdin.isatty():
            return None

        file_descriptor = sys.stdin.fileno()
        readable, _, _ = select.select([file_descriptor], [], [], 0)

        if not readable:
            return None

        key = os.read(file_descriptor, 1).decode("ascii", errors="ignore").lower()

        return key

    def restore_terminal(self):
        """
        Restore terminal settings changed for single-key input.
        """
        if self._settings is not None:
            file_descriptor, previous_settings = self._settings
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, previous_settings)

    ###############################################################################################
    # private
    ###############################################################################################
    def _enable_single_key_input(self):
        """
        Enable immediate key reads and restore the terminal when finished.
        """

        if not sys.stdin.isatty():
            return None

        file_descriptor = sys.stdin.fileno()
        previous_settings = termios.tcgetattr(file_descriptor)
        tty.setcbreak(file_descriptor)
        self._settings = file_descriptor, previous_settings

        return None