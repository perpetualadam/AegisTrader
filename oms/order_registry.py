"""Tracks client ↔ exchange order IDs for OMS and audit correlation."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Dict, Optional

from oms.models import LocalOrderState, OrderRecord
from oms.sqlite_store import SqliteOMSStore


class OrderRegistry:
    """
    Order registry with optional SQLite persistence (survives process restarts).
    When sqlite_path is None, uses in-memory storage only.
    """

    def __init__(self, sqlite_path: Optional[Path] = None) -> None:
        self._by_client: Dict[str, OrderRecord] = {}
        self._lock = threading.Lock()
        self._store: Optional[SqliteOMSStore] = None
        if sqlite_path is not None:
            self._store = SqliteOMSStore(sqlite_path)
            for rec in self._store.load_all():
                self._by_client[rec.client_order_id] = rec

    def register_intent(self, rec: OrderRecord, internal_order_id: Optional[str] = None) -> None:
        with self._lock:
            self._by_client[rec.client_order_id] = rec
            if self._store:
                self._store.upsert(rec, internal_order_id=internal_order_id)

    def mark_submitted(self, client_order_id: str, exchange_order_id: Optional[str]) -> None:
        with self._lock:
            r = self._by_client.get(client_order_id)
            if r:
                r.state = LocalOrderState.SUBMITTED
                r.exchange_order_id = exchange_order_id
                if self._store:
                    self._store.upsert(r)

    def mark_terminal(self, client_order_id: str, state: LocalOrderState) -> None:
        with self._lock:
            r = self._by_client.get(client_order_id)
            if r:
                r.state = state
                if self._store:
                    self._store.upsert(r)

    def get(self, client_order_id: str) -> Optional[OrderRecord]:
        with self._lock:
            return self._by_client.get(client_order_id)

    def snapshot(self) -> Dict[str, OrderRecord]:
        with self._lock:
            return dict(self._by_client)


_registry: Optional[OrderRegistry] = None


def get_order_registry() -> OrderRegistry:
    global _registry
    if _registry is None:
        from config import OMS_DB_PATH, OMS_USE_SQLITE

        if OMS_USE_SQLITE and OMS_DB_PATH:
            _registry = OrderRegistry(Path(OMS_DB_PATH))
        else:
            _registry = OrderRegistry(None)
    return _registry


def reset_order_registry_singleton() -> None:
    """Test helper: clear singleton so next get_order_registry() rebuilds."""
    global _registry
    _registry = None


def set_order_registry_singleton(registry: OrderRegistry) -> None:
    """Test helper: inject a registry instance."""
    global _registry
    _registry = registry
