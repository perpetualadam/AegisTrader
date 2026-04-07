"""Singleton bundle of institutional controls for wiring through main + execution."""

from __future__ import annotations

from typing import Optional

from institutional.audit_log import AuditLog, get_audit_log
from institutional.circuit_breaker import FailureWindowCircuitBreaker
from institutional.rate_limiter import OrderRateLimiter


class InstitutionalControls:
    def __init__(
        self,
        audit: AuditLog,
        circuit_breaker: FailureWindowCircuitBreaker,
        rate_limiter: OrderRateLimiter,
        kill_switch: bool,
    ):
        self.audit = audit
        self.circuit_breaker = circuit_breaker
        self.rate_limiter = rate_limiter
        self.kill_switch = kill_switch


_controls: Optional[InstitutionalControls] = None


def get_institutional_controls() -> InstitutionalControls:
    global _controls
    if _controls is None:
        from config import (
            KILL_SWITCH,
            MAX_ORDERS_PER_MINUTE,
            CIRCUIT_BREAKER_FAILURE_THRESHOLD,
            CIRCUIT_BREAKER_WINDOW_SEC,
        )

        _controls = InstitutionalControls(
            audit=get_audit_log(),
            circuit_breaker=FailureWindowCircuitBreaker(
                threshold=CIRCUIT_BREAKER_FAILURE_THRESHOLD,
                window_sec=float(CIRCUIT_BREAKER_WINDOW_SEC),
            ),
            rate_limiter=OrderRateLimiter(max_per_minute=MAX_ORDERS_PER_MINUTE),
            kill_switch=KILL_SWITCH,
        )
    return _controls
