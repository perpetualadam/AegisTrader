import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from market_data.binance_public import timeframe_to_binance_interval


def test_timeframe_mapping():
    assert timeframe_to_binance_interval("1h") == "1h"
    assert timeframe_to_binance_interval("4h") == "4h"
    assert timeframe_to_binance_interval("1d") == "1d"
