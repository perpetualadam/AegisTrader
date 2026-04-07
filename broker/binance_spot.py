"""
Binance Spot API adapter (production + testnet).

Requires: pip install python-binance

Spot testnet: https://testnet.binance.vision/ — set BROKER_SANDBOX=true and use testnet keys.
"""

from __future__ import annotations

import logging
import time
from decimal import ROUND_DOWN, Decimal
from typing import Any, Dict, List, Optional

from broker.broker_api import AccountInfo, BrokerAPI, OrderResult

logger = logging.getLogger(__name__)

try:
    from binance.client import Client
except ImportError:
    Client = None  # type: ignore


def _quantize_to_step(quantity: float, step_size: float) -> str:
    """Return quantity string respecting LOT_SIZE (no scientific notation)."""
    if step_size <= 0:
        return str(quantity)
    q = Decimal(str(quantity))
    step = Decimal(str(step_size))
    n = (q / step).to_integral_value(rounding=ROUND_DOWN) * step
    s = format(n.normalize(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s if s else "0"


def _get_lot_step(client: Any, symbol: str) -> float:
    info = client.get_symbol_info(symbol)
    if not info:
        raise ValueError(f"Unknown symbol {symbol}")
    for f in info.get("filters", []):
        if f.get("filterType") == "LOT_SIZE":
            return float(f["stepSize"])
    return 1e-8


class BinanceSpotBroker(BrokerAPI):
    """Binance Spot REST adapter (sandbox=testnet spot)."""

    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        super().__init__(api_key, api_secret, sandbox)
        self.client = None

    def connect(self) -> bool:
        if Client is None:
            logger.error("python-binance is not installed. Run: pip install python-binance")
            return False
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=self.sandbox)
            self.client.ping()
            self.is_connected = True
            mode = "testnet" if self.sandbox else "live"
            logger.info("Connected to Binance Spot (%s)", mode)
            return True
        except Exception as e:
            logger.error("Binance connect failed: %s", e)
            self.is_connected = False
            return False

    def disconnect(self) -> None:
        self.client = None
        self.is_connected = False
        logger.info("Disconnected from Binance")

    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        order_type: str = "market",
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        client_order_id: Optional[str] = None,
    ) -> OrderResult:
        if not self.is_connected or not self.client:
            return OrderResult(
                success=False,
                error_message="Not connected to Binance",
                timestamp=time.time(),
            )
        sym = symbol.upper()
        side_u = "BUY" if side.lower() == "buy" else "SELL"
        try:
            step = _get_lot_step(self.client, sym)
            qty_str = _quantize_to_step(quantity, step)
            if qty_str in ("0", "0."):
                return OrderResult(
                    success=False,
                    error_message="Quantity rounds to zero (LOT_SIZE)",
                    timestamp=time.time(),
                )
            kwargs: Dict[str, Any] = {
                "symbol": sym,
                "side": side_u,
                "quantity": qty_str,
            }
            if client_order_id:
                kwargs["newClientOrderId"] = client_order_id[:36]

            if order_type.lower() == "market":
                kwargs["type"] = "MARKET"
                o = self.client.create_order(**kwargs)
            elif order_type.lower() == "limit":
                if price is None:
                    return OrderResult(
                        success=False,
                        error_message="LIMIT requires price",
                        timestamp=time.time(),
                    )
                kwargs["type"] = "LIMIT"
                kwargs["timeInForce"] = "GTC"
                kwargs["price"] = str(price)
                o = self.client.create_order(**kwargs)
            else:
                return OrderResult(
                    success=False,
                    error_message=f"Unsupported order type: {order_type}",
                    timestamp=time.time(),
                )

            return self._order_to_result(o, sym)
        except Exception as e:
            if Client is not None and e.__class__.__name__ == "BinanceAPIException":
                logger.warning("Binance order error: %s", e)
                code = getattr(e, "code", "")
                msg = getattr(e, "message", str(e))
                return OrderResult(
                    success=False,
                    error_message=f"{code} {msg}",
                    timestamp=time.time(),
                )
            logger.exception("Binance place_order failed")
            return OrderResult(
                success=False,
                error_message=str(e),
                timestamp=time.time(),
            )

    def _order_to_result(self, o: Dict[str, Any], symbol: str) -> OrderResult:
        oid = str(o.get("orderId", ""))
        status = o.get("status", "")
        executed = float(o.get("executedQty", 0) or 0)
        fills = float(o.get("cummulativeQuoteQty", 0) or 0)
        avg_px = 0.0
        if executed > 0 and fills > 0:
            avg_px = fills / executed
        fee = 0.0
        ok = status in ("FILLED", "PARTIALLY_FILLED", "NEW")
        return OrderResult(
            success=ok,
            order_id=oid,
            status=status,
            fill_price=avg_px if avg_px else None,
            filled_quantity=executed,
            fees=fee,
            timestamp=time.time(),
        )

    def cancel_order(self, order_id: str, symbol: Optional[str] = None) -> bool:
        if not self.is_connected or not self.client or not symbol:
            return False
        try:
            self.client.cancel_order(symbol=symbol.upper(), orderId=int(order_id))
            return True
        except Exception as e:
            logger.error("Binance cancel_order failed: %s", e)
            return False

    def get_order_status(self, order_id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        if not self.is_connected or not self.client or not symbol:
            return {}
        try:
            return self.client.get_order(symbol=symbol.upper(), orderId=int(order_id))
        except Exception as e:
            logger.debug("get_order_status %s: %s", order_id, e)
            return {}

    def get_account_info(self) -> AccountInfo:
        if not self.is_connected or not self.client:
            return AccountInfo(balance=0.0, available_balance=0.0)
        try:
            acc = self.client.get_account()
            usdt_free = 0.0
            usdt_locked = 0.0
            for b in acc.get("balances", []):
                if b["asset"] == "USDT":
                    usdt_free = float(b["free"])
                    usdt_locked = float(b["locked"])
                    break
            bal = usdt_free + usdt_locked
            return AccountInfo(
                balance=bal,
                available_balance=usdt_free,
                positions=[],
            )
        except Exception as e:
            logger.error("get_account_info: %s", e)
            return AccountInfo(balance=0.0, available_balance=0.0)

    def get_positions(self) -> List[Dict[str, Any]]:
        """Spot balances are not futures positions; return non-zero asset balances only."""
        if not self.is_connected or not self.client:
            return []
        try:
            acc = self.client.get_account()
            out: List[Dict[str, Any]] = []
            for b in acc.get("balances", []):
                f = float(b["free"])
                l = float(b["locked"])
                if f + l > 0:
                    out.append({"asset": b["asset"], "free": f, "locked": l})
            return out
        except Exception as e:
            logger.error("get_positions: %s", e)
            return []

    def get_balance(self) -> float:
        info = self.get_account_info()
        return info.balance
