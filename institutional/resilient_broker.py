"""Broker wrapper: retries with backoff, audit of attempts, delegates idempotent client IDs."""

from __future__ import annotations

import logging
import random
import time
from typing import Any, Dict, List, Optional

from broker.broker_api import AccountInfo, BrokerAPI, OrderResult
from institutional.audit_log import AuditLog

logger = logging.getLogger(__name__)


class ResilientBrokerAdapter(BrokerAPI):
    """
    Wraps a concrete BrokerAPI with bounded retries on transient failures.
    Does not retry on explicit rejection (success=False with non-retry message).
    """

    RETRY_SUBSTRINGS = ("timeout", "rate", "429", "503", "502", "connection", "temporar")

    def __init__(
        self,
        inner: BrokerAPI,
        max_retries: int,
        backoff_base_sec: float,
        audit: Optional[AuditLog],
    ):
        super().__init__(inner.api_key, inner.api_secret, inner.sandbox)
        self._inner = inner
        self.max_retries = max(0, max_retries)
        self.backoff_base_sec = max(0.05, backoff_base_sec)
        self._audit = audit

    def connect(self) -> bool:
        return self._inner.connect()

    def disconnect(self) -> None:
        self._inner.disconnect()

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
        last: Optional[OrderResult] = None
        for attempt in range(self.max_retries + 1):
            if self._audit:
                self._audit.append(
                    "broker_place_attempt",
                    {
                        "attempt": attempt,
                        "symbol": symbol,
                        "side": side,
                        "order_type": order_type,
                        "client_order_id": client_order_id,
                    },
                )
            try:
                last = self._inner.place_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    order_type=order_type,
                    price=price,
                    stop_price=stop_price,
                    client_order_id=client_order_id,
                )
            except Exception as e:
                logger.exception("Broker place_order raised: %s", e)
                last = OrderResult(
                    success=False,
                    error_message=str(e),
                    timestamp=time.time(),
                )
                if attempt < self.max_retries and self._retryable_exception(str(e)):
                    self._sleep_backoff(attempt)
                    continue
                return last

            if last.success:
                if self._audit:
                    self._audit.append(
                        "broker_place_ok",
                        {
                            "symbol": symbol,
                            "client_order_id": client_order_id,
                            "exchange_order_id": last.order_id,
                        },
                    )
                return last

            msg = (last.error_message or "").lower()
            if attempt < self.max_retries and self._retryable_message(msg):
                self._sleep_backoff(attempt)
                continue
            if self._audit:
                self._audit.append(
                    "broker_place_reject",
                    {
                        "symbol": symbol,
                        "client_order_id": client_order_id,
                        "error": last.error_message,
                    },
                )
            return last

        return last or OrderResult(success=False, error_message="no result", timestamp=time.time())

    def cancel_order(self, order_id: str, symbol: Optional[str] = None) -> bool:
        return self._inner.cancel_order(order_id, symbol=symbol)

    def get_order_status(self, order_id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        return self._inner.get_order_status(order_id, symbol=symbol)

    def get_account_info(self) -> AccountInfo:
        return self._inner.get_account_info()

    def get_positions(self) -> List[Dict[str, Any]]:
        return self._inner.get_positions()

    def get_balance(self) -> float:
        return self._inner.get_balance()

    def _sleep_backoff(self, attempt: int) -> None:
        # Full jitter around exponential backoff
        cap = self.backoff_base_sec * (2**attempt)
        delay = random.uniform(0, cap)
        time.sleep(delay)

    def _retryable_message(self, msg: str) -> bool:
        return any(s in msg for s in self.RETRY_SUBSTRINGS)

    def _retryable_exception(self, msg: str) -> bool:
        return self._retryable_message(msg.lower())
