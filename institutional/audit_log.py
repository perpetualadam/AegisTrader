"""Append-only JSONL audit trail for orders and risk decisions (no secrets)."""

from __future__ import annotations

import json
import logging
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class AuditLog:
    """
    Tamper-evident append-only log (JSON Lines). Each line is one event.
    Suitable for post-trade review; rotate/archive via logrotate or ops tooling.
    """

    def __init__(self, path: Path, enabled: bool = True):
        self._path = path
        self._enabled = enabled
        self._lock = threading.Lock()
        if enabled:
            self._path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event_type: str, payload: Dict[str, Any]) -> None:
        if not self._enabled:
            return
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "unix_ts": time.time(),
            "event_type": event_type,
            "payload": _sanitize_payload(payload),
        }
        line = json.dumps(record, default=str) + "\n"
        try:
            with self._lock:
                with open(self._path, "a", encoding="utf-8") as f:
                    f.write(line)
        except OSError as e:
            logger.error("Audit log write failed: %s", e)

    def path(self) -> Path:
        return self._path


def _sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Strip fields that must never appear in audit (defense in depth)."""
    blocked = {"api_key", "api_secret", "password", "token", "secret", "credential"}
    out: Dict[str, Any] = {}
    for k, v in payload.items():
        lk = str(k).lower()
        if any(b in lk for b in blocked):
            out[k] = "[REDACTED]"
        elif isinstance(v, dict):
            out[k] = _sanitize_payload(v)
        else:
            out[k] = v
    return out


_audit_singleton: Optional[AuditLog] = None


def get_audit_log() -> AuditLog:
    global _audit_singleton
    if _audit_singleton is None:
        from config import AUDIT_LOG_ENABLED, AUDIT_LOG_PATH

        path = Path(AUDIT_LOG_PATH)
        _audit_singleton = AuditLog(path, enabled=AUDIT_LOG_ENABLED)
    return _audit_singleton
