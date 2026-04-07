"""OMS datatypes shared by registry and SQLite store."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class LocalOrderState(str, Enum):
    PENDING_SUBMIT = "pending_submit"
    SUBMITTED = "submitted"
    FILLED = "filled"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


@dataclass
class OrderRecord:
    client_order_id: str
    symbol: str
    side: str
    quantity: float
    state: LocalOrderState = LocalOrderState.PENDING_SUBMIT
    exchange_order_id: Optional[str] = None
    tradingview_ticker: str = ""
    venue: str = ""
    venue_symbol: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
