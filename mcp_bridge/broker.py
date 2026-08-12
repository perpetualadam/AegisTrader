"""
BrokerAPI implementation that executes orders through an MCP broker server.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from broker.broker_api import AccountInfo, BrokerAPI, OrderResult
from mcp_bridge.client import MCPClientError, get_mcp_manager
from mcp_bridge.parsers import (
    extract_payload,
    payload_to_balance,
    payload_to_order_fields,
    payload_to_positions,
)

logger = logging.getLogger(__name__)


class MCPBroker(BrokerAPI):
    """
    Live/paper brokerage via an external MCP server with broker-role tools.

    Configure with BROKER_NAME=mcp and MCP_BROKER_SERVER=<registry name>.
    The MCP server must expose place_order / cancel_order / balance tools
    (names are remapped via servers registry tools + args_schema).
    """

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        sandbox: bool = True,
        server_name: Optional[str] = None,
    ):
        super().__init__(api_key, api_secret, sandbox)
        if server_name:
            self.server_name = server_name
        else:
            try:
                from config import MCP_BROKER_SERVER

                self.server_name = (MCP_BROKER_SERVER or "crypto").strip()
            except ImportError:
                self.server_name = "crypto"
        self._manager = get_mcp_manager()

    def connect(self) -> bool:
        try:
            from config import MCP_ENABLED
        except ImportError:
            MCP_ENABLED = True

        if not MCP_ENABLED:
            logger.error("MCPBroker requires MCP_ENABLED=true")
            return False

        cfg = self._manager.get_server(self.server_name)
        if not cfg:
            logger.error("MCP broker server '%s' not in registry", self.server_name)
            return False
        if not cfg.enabled:
            logger.error(
                "MCP broker server '%s' is disabled — set enabled:true in registry",
                self.server_name,
            )
            return False
        if not cfg.has_role("broker"):
            logger.error(
                "MCP server '%s' does not advertise broker role", self.server_name
            )
            return False

        try:
            self._manager.ensure_started()
            # Probe connectivity via list_tools (best-effort)
            self._manager.list_tools(self.server_name)
            self.is_connected = True
            logger.info("Connected to MCP broker server '%s'", self.server_name)
            return True
        except Exception as e:
            logger.error("Failed to connect MCP broker '%s': %s", self.server_name, e)
            self.is_connected = False
            return False

    def disconnect(self):
        self.is_connected = False
        logger.info("Disconnected MCP broker '%s'", self.server_name)

    def _call(self, logical: str, values: Dict[str, Any]) -> Any:
        if not self.is_connected:
            raise MCPClientError("MCP broker not connected")
        return self._manager.call_logical_tool(self.server_name, logical, values)

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
        values: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "order_type": order_type,
        }
        if price is not None:
            values["price"] = price
        if stop_price is not None:
            values["stop_price"] = stop_price
        if client_order_id is not None:
            values["client_order_id"] = client_order_id

        try:
            raw = self._call("place_order", values)
            fields = payload_to_order_fields(extract_payload(raw))
            return OrderResult(
                success=fields["success"],
                order_id=fields["order_id"],
                status=fields["status"],
                fill_price=fields["fill_price"],
                filled_quantity=fields["filled_quantity"],
                fees=fields["fees"],
                error_message=fields["error_message"],
                timestamp=time.time(),
            )
        except Exception as e:
            logger.error("MCP place_order failed: %s", e)
            return OrderResult(
                success=False,
                error_message=str(e),
                timestamp=time.time(),
            )

    def cancel_order(self, order_id: str, symbol: Optional[str] = None) -> bool:
        values: Dict[str, Any] = {"order_id": order_id}
        if symbol:
            values["symbol"] = symbol
        try:
            raw = self._call("cancel_order", values)
            payload = extract_payload(raw)
            if isinstance(payload, bool):
                return payload
            if isinstance(payload, dict):
                if "success" in payload:
                    return bool(payload["success"])
                status = str(payload.get("status", "")).lower()
                return status in ("canceled", "cancelled", "success", "ok")
            return True
        except Exception as e:
            logger.error("MCP cancel_order failed: %s", e)
            return False

    def get_order_status(
        self, order_id: str, symbol: Optional[str] = None
    ) -> Dict[str, Any]:
        values: Dict[str, Any] = {"order_id": order_id}
        if symbol:
            values["symbol"] = symbol
        try:
            raw = self._call("get_order", values)
            payload = extract_payload(raw)
            if isinstance(payload, dict):
                return payload
            return {"order_id": order_id, "raw": payload}
        except Exception as e:
            return {"order_id": order_id, "error": str(e)}

    def get_account_info(self) -> AccountInfo:
        balance = self.get_balance()
        positions = self.get_positions()
        try:
            raw = self._call("get_account", {})
            payload = extract_payload(raw)
            if isinstance(payload, dict):
                bal = payload_to_balance(payload)
                if bal is not None:
                    balance = bal
                avail = payload.get("available_balance") or payload.get("available")
                try:
                    available = float(avail) if avail is not None else balance
                except (TypeError, ValueError):
                    available = balance
                return AccountInfo(
                    balance=balance,
                    available_balance=available,
                    positions=positions,
                    margin_used=float(payload.get("margin_used") or 0.0),
                    margin_available=float(
                        payload.get("margin_available") or available
                    ),
                )
        except Exception as e:
            logger.debug("MCP get_account fallback to balance/positions: %s", e)

        return AccountInfo(
            balance=balance,
            available_balance=balance,
            positions=positions,
        )

    def get_positions(self) -> List[Dict[str, Any]]:
        try:
            raw = self._call("get_positions", {})
            return payload_to_positions(extract_payload(raw))
        except Exception as e:
            logger.debug("MCP get_positions failed: %s", e)
            return []

    def get_balance(self) -> float:
        try:
            raw = self._call("get_balance", {})
            bal = payload_to_balance(extract_payload(raw))
            if bal is not None:
                return bal
        except Exception as e:
            logger.debug("MCP get_balance failed: %s", e)
        try:
            raw = self._call("get_account", {})
            bal = payload_to_balance(extract_payload(raw))
            if bal is not None:
                return bal
        except Exception:
            pass
        return 0.0
