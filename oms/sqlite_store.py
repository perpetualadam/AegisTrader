"""SQLite persistence for OMS order records."""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, List, Optional

from oms.models import LocalOrderState, OrderRecord


SCHEMA = """
CREATE TABLE IF NOT EXISTS oms_orders (
  client_order_id TEXT PRIMARY KEY NOT NULL,
  internal_order_id TEXT,
  tradingview_ticker TEXT,
  venue TEXT NOT NULL DEFAULT '',
  venue_symbol TEXT,
  symbol TEXT NOT NULL,
  side TEXT NOT NULL,
  quantity REAL NOT NULL,
  state TEXT NOT NULL,
  exchange_order_id TEXT,
  created_at REAL NOT NULL,
  updated_at REAL NOT NULL,
  extra_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_oms_state ON oms_orders(state);
CREATE INDEX IF NOT EXISTS idx_oms_exchange ON oms_orders(exchange_order_id);
"""


class SqliteOMSStore:
    """Thread-safe SQLite backend for order lifecycle."""

    def __init__(self, db_path: Path):
        self._path = db_path
        self._lock = threading.Lock()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._lock:
            conn = self._connect()
            try:
                conn.executescript(SCHEMA)
                conn.commit()
            finally:
                conn.close()

    def upsert(self, rec: OrderRecord, internal_order_id: Optional[str] = None) -> None:
        now = time.time()
        extra = json.dumps(rec.extra) if rec.extra else "{}"
        iid = internal_order_id or rec.extra.get("internal_order_id")
        with self._lock:
            conn = self._connect()
            try:
                existing = conn.execute(
                    "SELECT created_at FROM oms_orders WHERE client_order_id = ?",
                    (rec.client_order_id,),
                ).fetchone()
                created_at = existing[0] if existing else now
                conn.execute(
                    """
                    INSERT INTO oms_orders (
                      client_order_id, internal_order_id, tradingview_ticker, venue, venue_symbol,
                      symbol, side, quantity, state, exchange_order_id, created_at, updated_at, extra_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(client_order_id) DO UPDATE SET
                      internal_order_id = excluded.internal_order_id,
                      tradingview_ticker = excluded.tradingview_ticker,
                      venue = excluded.venue,
                      venue_symbol = excluded.venue_symbol,
                      symbol = excluded.symbol,
                      side = excluded.side,
                      quantity = excluded.quantity,
                      state = excluded.state,
                      exchange_order_id = excluded.exchange_order_id,
                      updated_at = excluded.updated_at,
                      extra_json = excluded.extra_json
                    """,
                    (
                        rec.client_order_id,
                        iid,
                        rec.tradingview_ticker,
                        rec.venue,
                        rec.venue_symbol,
                        rec.symbol,
                        rec.side,
                        rec.quantity,
                        rec.state.value,
                        rec.exchange_order_id,
                        created_at,
                        now,
                        extra,
                    ),
                )
                conn.commit()
            finally:
                conn.close()

    def load_all(self) -> List[OrderRecord]:
        with self._lock:
            conn = self._connect()
            try:
                rows = conn.execute("SELECT * FROM oms_orders").fetchall()
            finally:
                conn.close()
        out: List[OrderRecord] = []
        for row in rows:
            extra: dict = {}
            if row["extra_json"]:
                try:
                    extra = json.loads(row["extra_json"])
                except json.JSONDecodeError:
                    pass
            out.append(
                OrderRecord(
                    client_order_id=row["client_order_id"],
                    symbol=row["symbol"],
                    side=row["side"],
                    quantity=row["quantity"],
                    state=LocalOrderState(row["state"]),
                    exchange_order_id=row["exchange_order_id"],
                    tradingview_ticker=row["tradingview_ticker"] or "",
                    venue=row["venue"] or "",
                    venue_symbol=row["venue_symbol"],
                    extra=extra,
                )
            )
        return out
