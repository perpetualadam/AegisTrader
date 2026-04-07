"""Token-bucket style limiter for outbound orders per minute."""

from __future__ import annotations

import time
from collections import deque
from typing import Deque


class OrderRateLimiter:
    """Allows at most `max_per_minute` orders in any rolling 60-second window."""

    def __init__(self, max_per_minute: int):
        if max_per_minute < 1:
            raise ValueError("max_per_minute must be >= 1")
        self.max_per_minute = max_per_minute
        self._timestamps: Deque[float] = deque()

    def _prune(self) -> None:
        cutoff = time.time() - 60.0
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

    def acquire(self) -> bool:
        """
        Reserve a slot for one order. Returns True if allowed, False if rate cap hit.
        """
        self._prune()
        if len(self._timestamps) >= self.max_per_minute:
            return False
        self._timestamps.append(time.time())
        return True

    def release(self) -> None:
        """Optional: if acquire reserved but order not sent, release last slot."""
        if self._timestamps:
            self._timestamps.pop()
