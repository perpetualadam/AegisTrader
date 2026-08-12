"""
Parse heterogeneous MCP tool results into AegisTrader DTOs.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from vision.ocr_reader import PriceData

logger = logging.getLogger(__name__)


def _price_data_cls():
    from vision.ocr_reader import PriceData

    return PriceData


def extract_payload(result: Any) -> Any:
    """
    Normalize MCP call_tool results across SDK versions into a Python object.

    Supports:
    - CallToolResult with structured_content / content
    - dict / list / str payloads
    """
    if result is None:
        return None

    if getattr(result, "is_error", False):
        text = _content_text(result)
        raise RuntimeError(text or "MCP tool returned an error")

    structured = getattr(result, "structured_content", None)
    if structured is not None:
        return structured

    # Some SDKs use .data
    data = getattr(result, "data", None)
    if data is not None:
        return data

    text = _content_text(result)
    if text is not None:
        return _maybe_json(text)

    if isinstance(result, (dict, list, str, int, float)):
        return result

    return result


def _content_text(result: Any) -> Optional[str]:
    content = getattr(result, "content", None)
    if not content:
        return None
    parts: List[str] = []
    for block in content:
        text = getattr(block, "text", None)
        if text is None and isinstance(block, dict):
            text = block.get("text")
        if text:
            parts.append(str(text))
    if not parts:
        return None
    return "\n".join(parts)


def _maybe_json(text: str) -> Any:
    text = text.strip()
    if not text:
        return text
    if text[0] in "{[":
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    return text


def _as_dict(payload: Any) -> Optional[Dict[str, Any]]:
    if isinstance(payload, dict):
        # unwrap common envelopes
        for key in ("data", "result", "quote", "ticker", "candle", "kline"):
            inner = payload.get(key)
            if isinstance(inner, dict):
                return inner
            if isinstance(inner, list) and inner and isinstance(inner[0], dict):
                return inner[-1]
        return payload
    if isinstance(payload, list) and payload:
        last = payload[-1]
        if isinstance(last, dict):
            return last
        if isinstance(last, (list, tuple)) and len(last) >= 5:
            # Binance-style kline row
            try:
                return {
                    "open": float(last[1]),
                    "high": float(last[2]),
                    "low": float(last[3]),
                    "close": float(last[4]),
                    "volume": float(last[5]) if len(last) > 5 else None,
                }
            except (TypeError, ValueError):
                return None
    return None


def _first_number(d: Dict[str, Any], keys: List[str]) -> Optional[float]:
    for key in keys:
        if key in d and d[key] is not None:
            try:
                return float(d[key])
            except (TypeError, ValueError):
                continue
        # nested price object
        if key in d and isinstance(d[key], dict):
            nested = _first_number(
                d[key],
                ["price", "last", "close", "value", "c"],
            )
            if nested is not None:
                return nested
    return None


def payload_to_price_data(payload: Any) -> Optional["PriceData"]:
    """Best-effort conversion of quote/OHLCV MCP payloads into PriceData."""
    if payload is None:
        return None

    PriceData = _price_data_cls()

    if isinstance(payload, (int, float)):
        v = float(payload)
        return PriceData(
            current_price=v,
            close_price=v,
            timestamp=time.time(),
        )

    d = _as_dict(payload)
    if d is None:
        # multi-quote map: { "BINANCE:BTCUSDT": {...} }
        if isinstance(payload, dict) and payload:
            first = next(iter(payload.values()))
            d = _as_dict(first)
        if d is None:
            logger.debug("Unable to parse MCP price payload: %r", type(payload))
            return None

    close = _first_number(
        d,
        [
            "close",
            "close_price",
            "c",
            "last",
            "last_price",
            "price",
            "current_price",
            "mark_price",
        ],
    )
    open_p = _first_number(d, ["open", "open_price", "o"])
    high = _first_number(d, ["high", "high_price", "h"])
    low = _first_number(d, ["low", "low_price", "l"])
    volume = _first_number(d, ["volume", "vol", "v", "base_volume"])
    change_pct = _first_number(
        d, ["change_percent", "change_pct", "percent_change", "changePercent"]
    )
    change_val = _first_number(d, ["change", "change_value", "changeValue"])

    if close is None and open_p is None and high is None and low is None:
        return None

    current = close if close is not None else open_p
    return PriceData(
        current_price=current,
        open_price=open_p,
        high_price=high,
        low_price=low,
        close_price=close if close is not None else current,
        volume=volume,
        change_percent=change_pct,
        change_value=change_val,
        timestamp=time.time(),
    )


def payload_to_order_fields(payload: Any) -> Dict[str, Any]:
    """Extract common order result fields from MCP broker tools."""
    d = _as_dict(payload) or {}
    if not d and isinstance(payload, dict):
        d = payload

    order_id = d.get("order_id") or d.get("orderId") or d.get("id") or d.get("clientOrderId")
    status = d.get("status") or d.get("order_status")
    fill_price = _first_number(d, ["fill_price", "avg_price", "average", "price", "executed_price"])
    filled_qty = _first_number(
        d, ["filled_quantity", "executedQty", "filled", "filled_qty", "quantity"]
    )
    fees = _first_number(d, ["fees", "commission", "fee"])
    success = d.get("success")
    if success is None:
        success = order_id is not None and str(status or "").lower() not in (
            "rejected",
            "failed",
            "error",
        )
    error_message = d.get("error_message") or d.get("error") or d.get("message")
    if success is False and not error_message:
        error_message = "MCP place_order reported failure"

    return {
        "success": bool(success),
        "order_id": str(order_id) if order_id is not None else None,
        "status": str(status) if status is not None else None,
        "fill_price": fill_price,
        "filled_quantity": filled_qty,
        "fees": fees,
        "error_message": str(error_message) if error_message and not success else None,
    }


def payload_to_balance(payload: Any) -> Optional[float]:
    d = _as_dict(payload)
    if d is None:
        if isinstance(payload, (int, float)):
            return float(payload)
        return None
    bal = _first_number(
        d,
        [
            "balance",
            "available_balance",
            "available",
            "equity",
            "total",
            "USDT",
            "usd",
            "free",
        ],
    )
    if bal is not None:
        return bal
    # balances list
    balances = d.get("balances") if isinstance(d, dict) else None
    if isinstance(balances, list):
        for row in balances:
            if not isinstance(row, dict):
                continue
            asset = str(row.get("asset") or row.get("currency") or "").upper()
            if asset in ("USDT", "USD", "BUSD", "USDC"):
                return _first_number(row, ["free", "available", "balance", "amount"])
    return None


def payload_to_positions(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [p for p in payload if isinstance(p, dict)]
    d = _as_dict(payload) or (payload if isinstance(payload, dict) else {})
    positions = d.get("positions") if isinstance(d, dict) else None
    if isinstance(positions, list):
        return [p for p in positions if isinstance(p, dict)]
    return []
