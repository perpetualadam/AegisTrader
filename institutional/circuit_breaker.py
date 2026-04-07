"""Sliding-window failure circuit: halt new risk when error rate spikes."""

from __future__ import annotations

import time
from collections import deque
from typing import Deque


class FailureWindowCircuitBreaker:
    """
    Opens (halts) when at least `threshold` failures occur within `window_sec`.
    Automatically recovers as old failures age out of the window.
    """

    def __init__(self, threshold: int, window_sec: float):
        if threshold < 1:
            raise ValueError("threshold must be >= 1")
        if window_sec <= 0:
            raise ValueError("window_sec must be positive")
        self.threshold = threshold
        self.window_sec = window_sec
        self._failures: Deque[float] = deque()

    def _prune(self) -> None:
        cutoff = time.time() - self.window_sec
        while self._failures and self._failures[0] < cutoff:
            self._failures.popleft()

    def record_failure(self) -> None:
        self._prune()
        self._failures.append(time.time())

    def record_success(self) -> None:
        """Clear recent failure pressure after a healthy operation."""
        self._failures.clear()

    def is_open(self) -> bool:
        """True when circuit is open — caller should not submit new orders."""
        self._prune()
        return len(self._failures) >= self.threshold

    def failure_count(self) -> int:
        self._prune()
        return len(self._failures)
