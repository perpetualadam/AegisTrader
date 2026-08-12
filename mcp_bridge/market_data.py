"""
Fetch PriceData via configured MCP market-data servers (TradingView, crypto, etc.).
"""

from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING

from mcp_bridge.client import MCPClientError, get_mcp_manager
from mcp_bridge.parsers import extract_payload, payload_to_price_data

if TYPE_CHECKING:
    from vision.ocr_reader import PriceData

logger = logging.getLogger(__name__)


def _mcp_enabled() -> bool:
    try:
        from config import MCP_ENABLED

        return bool(MCP_ENABLED)
    except ImportError:
        return False


def _preferred_market_data_server() -> Optional[str]:
    try:
        from config import MCP_MARKET_DATA_SERVER

        return (MCP_MARKET_DATA_SERVER or "").strip() or None
    except ImportError:
        return None


def fetch_mcp_price_data(
    symbol: str,
    timeframe: str = "1h",
    *,
    server: Optional[str] = None,
) -> Optional["PriceData"]:
    """
    Query MCP market-data tools for a quote/OHLCV and map to PriceData.

    Tries get_ohlcv first, then get_quote.
    ``symbol`` should be the platform ticker (e.g. BINANCE:BTCUSDT or BTCUSDT).
    """
    if not _mcp_enabled():
        return None

    manager = get_mcp_manager()
    preferred = server or _preferred_market_data_server()
    values_ohlcv = {"symbol": symbol, "timeframe": timeframe}
    values_quote = {"symbol": symbol}

    # Prefer named server when provided
    attempts = []
    if preferred:
        attempts.append(("named", preferred))
    attempts.append(("role", None))

    last_err: Optional[Exception] = None
    for mode, name in attempts:
        try:
            if mode == "named" and name:
                cfg = manager.get_server(name)
                if not cfg or not cfg.enabled:
                    continue
                for logical in ("get_ohlcv", "get_quote"):
                    vals = values_ohlcv if logical == "get_ohlcv" else values_quote
                    try:
                        raw = manager.call_logical_tool(name, logical, vals)
                        pd = payload_to_price_data(extract_payload(raw))
                        if pd is not None:
                            logger.debug(
                                "MCP market data via %s.%s for %s",
                                name,
                                logical,
                                symbol,
                            )
                            return pd
                    except Exception as e:
                        last_err = e
                        logger.debug(
                            "MCP %s.%s failed for %s: %s", name, logical, symbol, e
                        )
                continue

            # role-based failover across enabled market_data servers
            for logical in ("get_ohlcv", "get_quote"):
                vals = values_ohlcv if logical == "get_ohlcv" else values_quote
                try:
                    srv, raw = manager.call_first_for_role(
                        "market_data",
                        logical,
                        vals,
                        preferred=preferred,
                    )
                    pd = payload_to_price_data(extract_payload(raw))
                    if pd is not None:
                        logger.debug(
                            "MCP market data via %s.%s for %s", srv, logical, symbol
                        )
                        return pd
                except MCPClientError as e:
                    last_err = e
                    logger.debug("MCP role market_data/%s: %s", logical, e)
        except Exception as e:
            last_err = e
            logger.debug("MCP market data attempt failed: %s", e)

    if last_err:
        logger.warning("MCP market data unavailable for %s: %s", symbol, last_err)
    return None


def try_mcp_market_data(asset, timeframe: str = "1h") -> Optional["PriceData"]:
    """
    Scanner-friendly helper: accept an Asset (or ticker string) and fetch PriceData.
    Uses TradingView ticker when available (better for TradingView MCP servers).
    """
    if not _mcp_enabled():
        return None

    if isinstance(asset, str):
        symbol = asset
    else:
        symbol = getattr(asset, "tradingview_ticker", None) or getattr(
            asset, "symbol", None
        )
    if not symbol:
        return None

    try:
        return fetch_mcp_price_data(symbol, timeframe)
    except Exception as e:
        logger.debug("try_mcp_market_data skipped: %s", e)
        return None
