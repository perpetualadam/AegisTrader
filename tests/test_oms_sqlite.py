"""OMS SQLite persistence."""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oms.models import LocalOrderState, OrderRecord
from oms.order_registry import OrderRegistry


def test_sqlite_roundtrip(tmp_path):
    db = tmp_path / "oms.db"
    reg = OrderRegistry(db)
    reg.register_intent(
        OrderRecord(
            client_order_id="cid-1",
            symbol="BTC",
            side="buy",
            quantity=0.01,
            state=LocalOrderState.PENDING_SUBMIT,
            tradingview_ticker="BINANCE:BTCUSDT",
            venue="binance",
            venue_symbol="BTCUSDT",
        ),
        internal_order_id="oid-1",
    )
    reg.mark_submitted("cid-1", "999001")
    reg.mark_terminal("cid-1", LocalOrderState.FILLED)

    reg2 = OrderRegistry(db)
    r = reg2.get("cid-1")
    assert r is not None
    assert r.state == LocalOrderState.FILLED
    assert r.exchange_order_id == "999001"
    assert r.venue_symbol == "BTCUSDT"
