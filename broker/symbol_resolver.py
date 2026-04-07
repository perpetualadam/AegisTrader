"""
Map TradingView tickers (e.g. BINANCE:BTCUSDT) to venue-native symbols (e.g. BTCUSDT).

Loads `data/symbol_map.json` (override with SYMBOL_MAP_PATH). Unknown tickers use
venue-specific fallbacks (e.g. strip EXCHANGE: prefix for Binance spot).
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_cache: Optional[Dict[str, Any]] = None
_cache_path: Optional[Path] = None


def _load_map() -> Dict[str, Any]:
    global _cache, _cache_path
    from config import SYMBOL_MAP_PATH

    path = Path(SYMBOL_MAP_PATH)
    if _cache is not None and _cache_path == path:
        return _cache

    if path.is_file():
        with open(path, encoding="utf-8") as f:
            _cache = json.load(f)
    else:
        logger.warning("Symbol map file not found at %s — using heuristics only", path)
        _cache = {"mappings": {}}
    _cache_path = path
    return _cache


def resolve_venue_symbol(tradingview_ticker: str, venue: str) -> str:
    """
    Return the venue's native symbol for order placement.

    venue: broker name, e.g. 'binance', 'mock'
    """
    venue = venue.lower().strip()
    data = _load_map()
    mappings: Dict[str, Any] = data.get("mappings", {})

    key = tradingview_ticker.strip()
    if key in mappings:
        entry = mappings[key]
        if isinstance(entry, str):
            return entry.upper()
        if isinstance(entry, dict) and venue in entry:
            return str(entry[venue]).upper()

    per_venue = mappings.get("by_venue", {})
    if venue in per_venue and key in per_venue[venue]:
        return str(per_venue[venue][key]).upper()

    return _fallback_heuristic(key, venue)


def _fallback_heuristic(tradingview_ticker: str, venue: str) -> str:
    """Best-effort mapping when JSON has no explicit row."""
    s = tradingview_ticker.strip().upper()
    if venue == "binance":
        # BINANCE:BTCUSDT -> BTCUSDT
        if ":" in s:
            parts = s.split(":", 1)
            if len(parts) == 2 and re.match(r"^[A-Z0-9]{4,}$", parts[1]):
                return parts[1]
        # Already native
        if re.match(r"^[A-Z0-9]{4,}$", s):
            return s
    if venue == "mock":
        if ":" in s:
            return s.split(":", 1)[1]
        return s
    logger.warning(
        "No explicit symbol map for %s venue=%s — using ticker as-is",
        tradingview_ticker,
        venue,
    )
    return s.replace(":", "") if ":" in s else s
