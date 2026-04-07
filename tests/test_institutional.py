"""Tests for institutional controls (circuit breaker, rate limit, OMS, broker idempotency)."""

import os
import sys
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from broker.broker_api import MockBrokerAPI
from institutional.circuit_breaker import FailureWindowCircuitBreaker
from institutional.rate_limiter import OrderRateLimiter
from oms.reconciliation import reconcile_with_broker
from oms.models import LocalOrderState, OrderRecord
from oms.order_registry import OrderRegistry


class TestCircuitBreaker:
    def test_opens_after_threshold(self):
        cb = FailureWindowCircuitBreaker(threshold=3, window_sec=60.0)
        assert not cb.is_open()
        cb.record_failure()
        cb.record_failure()
        assert not cb.is_open()
        cb.record_failure()
        assert cb.is_open()

    def test_success_clears(self):
        cb = FailureWindowCircuitBreaker(threshold=2, window_sec=60.0)
        cb.record_failure()
        cb.record_success()
        cb.record_failure()
        assert not cb.is_open()


class TestRateLimiter:
    def test_cap(self):
        rl = OrderRateLimiter(max_per_minute=2)
        assert rl.acquire()
        assert rl.acquire()
        assert not rl.acquire()


class TestMockBrokerIdempotency:
    def test_same_client_order_id(self):
        b = MockBrokerAPI("k", "s")
        b.connect()
        r1 = b.place_order("BTCUSDT", "buy", 0.1, "market", 50000.0, None, "cid-1")
        r2 = b.place_order("BTCUSDT", "buy", 0.1, "market", 50000.0, None, "cid-1")
        assert r1.success and r2.success
        assert r1.order_id == r2.order_id


class TestReconciliation:
    def test_missing_exchange_id_flagged(self):
        reg = OrderRegistry()
        reg.register_intent(
            OrderRecord(
                client_order_id="c1",
                symbol="X",
                side="buy",
                quantity=1.0,
                state=LocalOrderState.SUBMITTED,
                exchange_order_id=None,
                venue_symbol="XUSDT",
            )
        )
        mock = MockBrokerAPI("k", "s")
        mock.connect()
        disc = reconcile_with_broker(mock, reg)
        assert any(d["type"] == "missing_exchange_id" for d in disc)
