import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from broker.symbol_resolver import resolve_venue_symbol


def test_binance_mapped():
    assert resolve_venue_symbol("BINANCE:BTCUSDT", "binance") == "BTCUSDT"


def test_mock_strip():
    assert resolve_venue_symbol("BINANCE:ETHUSDT", "mock") == "ETHUSDT"


def test_fallback_colon():
    assert resolve_venue_symbol("BINANCE:ADAUSDT", "binance") == "ADAUSDT"
