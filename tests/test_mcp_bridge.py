"""Tests for MCP platform bridge (registry, parsers, broker/market wiring)."""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_bridge.registry import (
    load_server_registry,
    parse_server_entry,
    servers_for_role,
)
from mcp_bridge.parsers import (
    extract_payload,
    payload_to_balance,
    payload_to_order_fields,
    payload_to_price_data,
)
from mcp_bridge.client import reset_mcp_manager


class _FakePriceData:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


@pytest.fixture(autouse=True)
def _reset_manager():
    reset_mcp_manager()
    yield
    reset_mcp_manager()


class TestRegistry:
    def test_default_registry_loads(self):
        path = Path(__file__).resolve().parents[1] / "mcp_bridge" / "servers.default.json"
        registry = load_server_registry(str(path))
        assert "tradingview" in registry
        assert "crypto" in registry
        assert registry["tradingview"].has_role("market_data")
        assert registry["crypto"].has_role("broker")
        assert not registry["tradingview"].enabled  # disabled by default

    def test_env_expansion_in_server_env(self, monkeypatch):
        monkeypatch.setenv("BROKER_API_KEY", "secret-key")
        cfg = parse_server_entry(
            "demo",
            {
                "enabled": True,
                "transport": "stdio",
                "command": "node",
                "args": ["server.js"],
                "env": {"API_KEY": "${BROKER_API_KEY}"},
                "roles": ["broker"],
                "tools": {"place_order": "create_order"},
            },
        )
        assert cfg.env["API_KEY"] == "secret-key"
        assert cfg.tool_candidates("place_order") == ["create_order"]

    def test_map_arguments(self):
        cfg = parse_server_entry(
            "tv",
            {
                "tools": {"get_ohlcv": ["get_historical_data"]},
                "args_schema": {
                    "get_ohlcv": {
                        "symbol": ["symbol"],
                        "timeframe": ["interval", "timeframe"],
                    }
                },
            },
        )
        mapped = cfg.map_arguments(
            "get_ohlcv", {"symbol": "BINANCE:BTCUSDT", "timeframe": "1h", "extra": None}
        )
        assert mapped == {"symbol": "BINANCE:BTCUSDT", "interval": "1h"}

    def test_servers_for_role_preferred(self):
        path = Path(__file__).resolve().parents[1] / "mcp_bridge" / "servers.default.json"
        registry = load_server_registry(str(path))
        # force-enable for selection test
        registry["tradingview"].enabled = True
        registry["crypto"].enabled = True
        ordered = servers_for_role(
            registry, "market_data", preferred="crypto"
        )
        assert ordered[0].name == "crypto"


class TestParsers:
    def test_payload_to_price_data_from_quote(self):
        with patch("mcp_bridge.parsers._price_data_cls", return_value=_FakePriceData):
            pd = payload_to_price_data(
                {"price": 42000.5, "high": 43000, "low": 41000, "volume": 12.3}
            )
        assert pd is not None
        assert pd.current_price == 42000.5
        assert pd.high_price == 43000
        assert pd.volume == 12.3

    def test_payload_to_price_data_from_kline_row(self):
        with patch("mcp_bridge.parsers._price_data_cls", return_value=_FakePriceData):
            pd = payload_to_price_data(
                [[0, "100", "110", "90", "105", "55", 1]]
            )
        assert pd is not None
        assert pd.open_price == 100
        assert pd.close_price == 105
        assert pd.volume == 55

    def test_payload_to_order_fields(self):
        fields = payload_to_order_fields(
            {"orderId": "abc", "status": "FILLED", "avg_price": 1.5, "executedQty": 2}
        )
        assert fields["success"] is True
        assert fields["order_id"] == "abc"
        assert fields["fill_price"] == 1.5
        assert fields["filled_quantity"] == 2

    def test_payload_to_balance(self):
        assert payload_to_balance({"balance": 1234.5}) == 1234.5
        assert payload_to_balance(
            {"balances": [{"asset": "USDT", "free": "99.0"}]}
        ) == 99.0

    def test_extract_payload_error(self):
        result = MagicMock()
        result.is_error = True
        result.structured_content = None
        result.content = [MagicMock(text="boom")]
        with pytest.raises(RuntimeError, match="boom"):
            extract_payload(result)


class TestBrokerFactory:
    def test_create_broker_api_mcp(self):
        from broker.broker_api import create_broker_api
        from mcp_bridge.broker import MCPBroker

        broker = create_broker_api("mcp", "", "", True)
        assert isinstance(broker, MCPBroker)


class TestMarketDataWiring:
    def test_try_mcp_respects_disabled(self, monkeypatch):
        monkeypatch.setattr("config.MCP_ENABLED", False, raising=False)
        from mcp_bridge.market_data import fetch_mcp_price_data

        with patch("mcp_bridge.market_data._mcp_enabled", return_value=False):
            assert fetch_mcp_price_data("BINANCE:BTCUSDT", "1h") is None

    def test_scanner_provider_order_mcp(self):
        from scanner.market_scanner import _provider_order

        with patch("config.MARKET_DATA_PROVIDERS", ["binance", "mcp"]):
            assert _provider_order("mcp") == ["mcp"]
            assert _provider_order("binance") == ["binance"]

    def test_try_api_price_data_uses_mcp(self):
        from types import SimpleNamespace
        from scanner import market_scanner as ms

        asset = SimpleNamespace(
            symbol="BTCUSDT",
            market_type=SimpleNamespace(value="crypto"),
            tradingview_ticker="BINANCE:BTCUSDT",
        )
        fake = _FakePriceData(current_price=1.0, close_price=1.0, timestamp=0.0)

        with patch.object(ms, "_provider_order", return_value=["mcp"]), patch.object(
            ms, "_try_mcp_price", return_value=fake
        ) as mcp_mock, patch.object(ms, "_try_binance_klines") as binance_mock:
            out = ms._try_api_price_data(asset, "1h", "mcp")
            assert out is fake
            mcp_mock.assert_called_once()
            binance_mock.assert_not_called()


class TestConfigMcp:
    def test_config_summary_includes_mcp(self):
        from config import get_config_summary

        summary = get_config_summary()
        assert "mcp_enabled" in summary
        assert "market_data_providers" in summary
        assert "mcp_market_data_server" in summary

    def test_chart_source_mcp_valid(self, monkeypatch):
        monkeypatch.setenv("CHART_DATA_SOURCE", "mcp")
        monkeypatch.setenv("MARKET_DATA_PROVIDERS", "mcp")
        # re-import is heavy; validate allowed set via validate_config path
        import config as cfg

        monkeypatch.setattr(cfg, "CHART_DATA_SOURCE", "mcp")
        monkeypatch.setattr(cfg, "MARKET_DATA_PROVIDERS", ["mcp"])
        assert cfg.validate_config() is True
