# MCP Platform Integration

AegisTrader can consume **external MCP (Model Context Protocol) servers** for market data and brokerage — for example TradingView MCP servers and crypto-exchange MCP servers — without rewriting the scanner or execution loop.

## What you get

| Capability | How it plugs in |
|------------|-----------------|
| Market data (quotes / OHLCV) | `mcp_bridge` → scanner `_try_api_price_data` → `PriceData` |
| Live brokerage | `MCPBroker` (`BrokerAPI`) via `BROKER_NAME=mcp` |
| Multi-server registry | `mcp_bridge/servers.default.json` (override with `MCP_SERVERS_PATH`) |
| Tool name differences | Per-server `tools` + `args_schema` maps logical names → concrete MCP tools |

Vision/Selenium TradingView automation still works; MCP is an optional, faster API path.

## Requirements

- Python **3.10+** for the official `mcp` SDK
- `pip install "mcp>=1.28,<3"` (already listed in `requirements.txt`)
- One or more MCP servers running locally (stdio) or over HTTP/SSE

## Quick setup

1. Copy env defaults and enable the bridge:

```bash
cp .env.example .env
```

```env
MCP_ENABLED=true
MCP_SERVERS_PATH=mcp_bridge/servers.default.json
MCP_MARKET_DATA_SERVER=tradingview
MARKET_DATA_PROVIDERS=mcp,binance
CHART_DATA_SOURCE=api_first
# Optional: skip browser when MCP returns prices and YOLO is off
# SCAN_USE_YOLO=false
# SCAN_SKIP_BROWSER_WHEN_API_ONLY=true
```

2. Edit the registry and enable servers you actually run:

```json
"tradingview": {
  "enabled": true,
  "transport": "stdio",
  "command": "npx",
  "args": ["-y", "tradingview-mcp"],
  "roles": ["market_data", "screener"],
  ...
}
```

3. Align tool names with your MCP server. Different TradingView/crypto MCP packages expose different tool IDs (`get_quote`, `get_historical_data`, `get_klines`, …). List candidates under `tools.get_quote` / `tools.get_ohlcv`; the client probes `list_tools` and picks the first match.

4. Restart AegisTrader (`python main.py`). Startup summary shows MCP status and provider order.

## TradingView MCP (market data)

Typical roles: `market_data`, `screener`.

Use TradingView-style tickers already on assets (`BINANCE:BTCUSDT`, `NASDAQ:AAPL`). The bridge prefers `tradingview_ticker` when calling MCP.

Example env:

```env
MCP_ENABLED=true
MCP_MARKET_DATA_SERVER=tradingview
MARKET_DATA_PROVIDERS=mcp,binance
CHART_DATA_SOURCE=api_first
```

Binance public REST remains a fallback for crypto when MCP is down.

## Crypto MCP (market data + broker)

1. Enable a server with `"roles": ["market_data", "broker"]` (see `crypto` or `binance_mcp` in the default registry).
2. For HTTP servers:

```json
"binance_mcp": {
  "enabled": true,
  "transport": "http",
  "url": "http://127.0.0.1:8000/mcp",
  "roles": ["market_data", "broker"],
  ...
}
```

3. For live trading through MCP:

```env
LIVE_TRADING=true
BROKER_NAME=mcp
MCP_ENABLED=true
MCP_BROKER_SERVER=crypto
BROKER_API_KEY=...
BROKER_API_SECRET=...
```

Credentials can be forwarded into the MCP subprocess via registry `env` entries using `${BROKER_API_KEY}` placeholders.

`Execution` and `ResilientBrokerAdapter` stay unchanged — `MCPBroker` is just another `BrokerAPI`.

## Logical tools

| Logical name | Used for |
|--------------|----------|
| `get_ohlcv` | Candles → `PriceData` |
| `get_quote` | Last price / quote → `PriceData` |
| `place_order` / `cancel_order` / `get_order` | Brokerage |
| `get_balance` / `get_positions` / `get_account` | Account state |
| `screen` / `technical_analysis` | Available for future strategy hooks |

## Adding a new platform MCP

1. Add a block under `servers` in your registry JSON.
2. Set `transport` (`stdio` | `http` | `sse`), command/args or `url`.
3. Declare `roles` (`market_data`, `broker`, `screener`, …).
4. Fill `tools` candidate lists and `args_schema` aliases for that server’s argument names.
5. Set `enabled: true` and point `MCP_MARKET_DATA_SERVER` / `MCP_BROKER_SERVER` at the key.

No Python changes required unless you need a custom payload parser (extend `mcp_bridge/parsers.py`).

## Architecture

```
.env / servers JSON
        │
        ▼
 mcp_bridge.client.MCPClientManager  (background asyncio loop)
        │
        ├─► mcp_bridge.market_data ──► scanner (PriceData)
        └─► mcp_bridge.broker.MCPBroker ──► execution (BrokerAPI)
```

## Troubleshooting

| Symptom | Check |
|---------|--------|
| MCP stays off | `MCP_ENABLED=true`, Python ≥ 3.10, `pip show mcp` |
| “server is disabled” | `"enabled": true` in registry for that key |
| Tool not found | Run the MCP server in Inspector; update `tools` candidates |
| Empty prices | Confirm payload shape; extend `payload_to_price_data` if needed |
| Broker connect fails | Server must include role `broker`; `BROKER_NAME=mcp` |

## Safety

- Treat MCP sessions (especially TradingView cookies / exchange keys) like production secrets.
- Prefer paper mode (`LIVE_TRADING=false`) while validating a new MCP server.
- Keep kill switch / rate limits / circuit breaker enabled for MCP brokers the same as native ones.
