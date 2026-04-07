"""Periodic reconciliation between local registry and broker (extend per venue)."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from broker.broker_api import BrokerAPI
from oms.order_registry import LocalOrderState, OrderRegistry

logger = logging.getLogger(__name__)


def reconcile_with_broker(broker: BrokerAPI, registry: OrderRegistry) -> List[Dict[str, Any]]:
    """
    Compare locally tracked submitted orders with broker-reported status.
    Returns list of discrepancies for alerting/metrics.

    Full production implementations poll exchange order APIs and match fills.
    """
    discrepancies: List[Dict[str, Any]] = []
    for cid, rec in registry.snapshot().items():
        if rec.state not in (LocalOrderState.SUBMITTED, LocalOrderState.PENDING_SUBMIT):
            continue
        if not rec.exchange_order_id:
            discrepancies.append(
                {
                    "type": "missing_exchange_id",
                    "client_order_id": cid,
                    "symbol": rec.symbol,
                }
            )
            continue
        sym = rec.venue_symbol or rec.symbol
        remote = broker.get_order_status(rec.exchange_order_id, symbol=sym)
        if not remote:
            discrepancies.append(
                {
                    "type": "order_not_found_at_venue",
                    "client_order_id": cid,
                    "exchange_order_id": rec.exchange_order_id,
                }
            )
    if discrepancies:
        logger.warning("Reconciliation found %d discrepancy(ies)", len(discrepancies))
    return discrepancies
