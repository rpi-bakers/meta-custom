"""Periodic callback timer based on the process real-time interval timer."""

import math
import signal
from types import FrameType


class TimeKeeper:
    """Notify a callback at a fixed interval and track elapsed time."""
    def __init__(
            self,
            interval,
            on_time_interval
    ) -> None:
        """
        Initialize the timekeeper.
        Args:
            interval (float): time interval in seconds
            on_time_interval ((int -> None)): callback function to invoke when the timer
        """
        if not isinstance(interval, (int, float)) or isinstance(interval, bool):
            raise ValueError("interval must be a finite positive number")
        if not math.isfinite(interval) or interval <= 0:
            raise ValueError("interval must be a finite positive number")
        if not callable(on_time_interval):
            raise TypeError("on_time_interval must be callable")

        self.elapsed_time = 0.0
        self.interval = float(interval)
        self.on_time_interval = on_time_interval
        self._previous_handler = signal.getsignal(signal.SIGALRM)
        self.running = False
        self.handler_installed = True
        self.is_notify_processing = False

        signal.signal(signal.SIGALRM, self.on_signal)

    def start(self) -> None:
        """Start or restart periodic callback notifications."""
        if not self.handler_installed:
            signal.signal(signal.SIGALRM, self.on_signal)
            self.handler_installed = True
        self.elapsed_time = 0.0
        self.running = True
        signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)

    def stop(self) -> None:
        """Stop notifications and restore the previous SIGALRM handler."""
        if self.running:
            signal.setitimer(signal.ITIMER_REAL, 0)
            self.running = False
        if self.handler_installed:
            signal.signal(signal.SIGALRM, self._previous_handler)
            self.handler_installed = False

    def on_signal(self, signum: int, frame: FrameType | None) -> None:
        """Advance elapsed time and invoke the callback for a timer signal."""
        self.elapsed_time += self.interval

        # Skip notify if previous interrupt is processing.
        if not self.is_notify_processing:
            self.is_notify_processing = True
            self.on_time_interval(self.elapsed_time)
            self.is_notify_processing = False
