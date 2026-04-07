import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from market_data.binance_public import timeframe_to_binance_interval
from vision.ocr_reader import PriceData
from scanner.market_scanner import _merge_api_first, _merge_api_strict


def test_timeframe_mapping():
    assert timeframe_to_binance_interval("1h") == "1h"
    assert timeframe_to_binance_interval("4h") == "4h"
    assert timeframe_to_binance_interval("1d") == "1d"


def test_merge_api_strict_matches_api_first_rule():
    api = PriceData(timestamp=1.0, current_price=100.0, high_price=101.0, low_price=99.0)
    ocr = PriceData(timestamp=2.0, current_price=50.0, change_percent=1.5)
    a = _merge_api_first(api, ocr)
    b = _merge_api_strict(api, ocr)
    assert a.current_price == 100.0 and b.current_price == 100.0
    assert a.change_percent == 1.5 and b.change_percent == 1.5
