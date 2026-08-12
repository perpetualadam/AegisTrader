"""Market data providers (API / MCP) — faster than screenshot OCR for OHLCV."""

from market_data.binance_public import fetch_binance_kline_as_price_data, timeframe_to_binance_interval

__all__ = [
    "fetch_binance_kline_as_price_data",
    "timeframe_to_binance_interval",
]


def fetch_mcp_price_data(*args, **kwargs):
    """Lazy re-export — avoids hard dependency when MCP is unused."""
    from mcp_bridge.market_data import fetch_mcp_price_data as _fetch

    return _fetch(*args, **kwargs)


__all__.append("fetch_mcp_price_data")
