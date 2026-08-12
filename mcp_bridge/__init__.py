"""
MCP bridge — connect AegisTrader to external platform MCP servers
(TradingView, crypto exchanges, etc.) for market data and brokerage.
"""

from mcp_bridge.client import MCPClientManager, get_mcp_manager

__all__ = [
    "MCPClientManager",
    "get_mcp_manager",
    "fetch_mcp_price_data",
    "try_mcp_market_data",
    "MCPBroker",
]


def __getattr__(name: str):
    # Lazy exports avoid importing vision/broker stacks until needed.
    if name in ("fetch_mcp_price_data", "try_mcp_market_data"):
        from mcp_bridge.market_data import fetch_mcp_price_data, try_mcp_market_data

        return {
            "fetch_mcp_price_data": fetch_mcp_price_data,
            "try_mcp_market_data": try_mcp_market_data,
        }[name]
    if name == "MCPBroker":
        from mcp_bridge.broker import MCPBroker

        return MCPBroker
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
