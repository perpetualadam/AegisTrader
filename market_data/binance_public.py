"""
Binance Spot public REST klines — no API keys required for market data.

Typical latency: tens of ms vs seconds for browser + OCR.
"""

from __future__ import annotations

import logging
from typing import Optional

import requests

from vision.ocr_reader import PriceData

logger = logging.getLogger(__name__)

# Binance spot intervals supported by /api/v3/klines
_INTERVAL_MAP = {
    "1m": "1m",
    "3m": "3m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "2h": "2h",
    "4h": "4h",
    "6h": "6h",
    "8h": "8h",
    "12h": "12h",
    "1d": "1d",
    "3d": "3d",
    "1w": "1w",
    "d": "1d",
    "h": "1h",
    "w": "1w",
}


def timeframe_to_binance_interval(timeframe: str) -> str:
    """Map TradingView-style timeframe (e.g. 1h, 4h, 1d) to Binance interval string."""
    tf = timeframe.strip().lower()
    if tf in _INTERVAL_MAP:
        return _INTERVAL_MAP[tf]
    # e.g. "60" -> 1h heuristic
    if tf.isdigit():
        m = int(tf)
        if m <= 60:
            return "1h"
        return "1d"
    return "1h"


def fetch_binance_kline_as_price_data(
    symbol: str,
    timeframe: str,
    base_url: Optional[str] = None,
) -> Optional[PriceData]:
    """
    Fetch the latest completed kline (or last candle) and map to PriceData.

    symbol: venue pair, e.g. BTCUSDT (uppercase)
    """
    try:
        from config import BINANCE_PUBLIC_BASE_URL as _cfg_url
    except ImportError:
        _cfg_url = "https://api.binance.com"
    base = (base_url or _cfg_url or "https://api.binance.com").rstrip("/")

    interval = timeframe_to_binance_interval(timeframe)
    sym = symbol.upper().replace(" ", "")
    url = f"{base}/api/v3/klines"
    params = {"symbol": sym, "interval": interval, "limit": 1}

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        logger.warning("Binance klines request failed for %s: %s", sym, e)
        return None

    if not data or not isinstance(data, list):
        return None

    k = data[-1]
    # [openTime, open, high, low, close, volume, closeTime, ...]
    try:
        o, h, low, c, vol = float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5])
    except (IndexError, ValueError, TypeError):
        return None

    import time as _t

    return PriceData(
        current_price=c,
        open_price=o,
        high_price=h,
        low_price=low,
        close_price=c,
        volume=vol,
        change_percent=None,
        change_value=None,
        timestamp=_t.time(),
    )
