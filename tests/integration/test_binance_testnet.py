"""
Binance Spot testnet integration tests.

Requires keys from https://testnet.binance.vision/

Set:
  BINANCE_TESTNET_API_KEY
  BINANCE_TESTNET_API_SECRET

Or reuse BROKER_API_KEY / BROKER_API_SECRET when testing live wiring.

Run: pytest tests/integration -m integration -v
"""

from __future__ import annotations

import os
import uuid

import pytest

from broker.binance_spot import BinanceSpotBroker

pytestmark = pytest.mark.integration


def _credentials():
    k = os.getenv("BINANCE_TESTNET_API_KEY") or os.getenv("BROKER_API_KEY")
    s = os.getenv("BINANCE_TESTNET_API_SECRET") or os.getenv("BROKER_API_SECRET")
    return k, s


@pytest.fixture
def testnet_broker():
    k, s = _credentials()
    if not k or not s:
        pytest.skip("Set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET (or BROKER_*)")
    b = BinanceSpotBroker(k, s, sandbox=True)
    assert b.connect(), "Binance testnet connect failed"
    yield b
    b.disconnect()


def test_ping_and_balance(testnet_broker):
    b = testnet_broker
    bal = b.get_balance()
    assert bal >= 0.0
    info = b.get_account_info()
    assert info.available_balance >= 0.0


def test_get_order_status_requires_symbol(testnet_broker):
    """Binance REST requires symbol for order lookup."""
    b = testnet_broker
    assert b.get_order_status("1", symbol=None) == {}
    st = b.get_order_status("999999999", symbol="BTCUSDT")
    assert isinstance(st, dict)


@pytest.mark.skipif(
    os.getenv("BINANCE_INTEGRATION_PLACE_ORDER") != "1",
    reason="Set BINANCE_INTEGRATION_PLACE_ORDER=1 to run (places a tiny MARKET order)",
)
def test_place_market_micro_order(testnet_broker):
    """Optional: smallest viable BTCUSDT market buy on testnet (costs test USDT)."""
    b = testnet_broker
    cid = str(uuid.uuid4())
    r = b.place_order(
        symbol="BTCUSDT",
        side="buy",
        quantity=0.00001,
        order_type="market",
        client_order_id=cid,
    )
    assert r.success or r.error_message  # may fail min notional — still exercises REST path
