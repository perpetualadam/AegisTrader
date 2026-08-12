"""
Load and resolve MCP server registry configuration.
"""

from __future__ import annotations

import json
import logging
import os
import re
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


@dataclass
class MCPServerConfig:
    """One configured MCP server endpoint."""

    name: str
    enabled: bool = False
    transport: str = "stdio"  # stdio | http | sse
    command: Optional[str] = None
    args: List[str] = field(default_factory=list)
    cwd: Optional[str] = None
    env: Dict[str, str] = field(default_factory=dict)
    url: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    tools: Dict[str, List[str]] = field(default_factory=dict)
    args_schema: Dict[str, Dict[str, List[str]]] = field(default_factory=dict)

    def has_role(self, role: str) -> bool:
        return role.lower() in {r.lower() for r in self.roles}

    def tool_candidates(self, logical: str) -> List[str]:
        raw = self.tools.get(logical, [])
        if isinstance(raw, str):
            return [raw]
        return list(raw or [])

    def map_arguments(self, logical: str, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map logical arg names (symbol, timeframe, ...) to server-specific names
        using the first alias listed in args_schema for each provided value.
        """
        schema = self.args_schema.get(logical, {})
        out: Dict[str, Any] = {}
        for logical_key, value in values.items():
            if value is None:
                continue
            aliases = schema.get(logical_key)
            if aliases:
                out[aliases[0]] = value
            else:
                out[logical_key] = value
        return out


def _expand_env(value: str) -> str:
    def repl(match: re.Match) -> str:
        key = match.group(1)
        return os.getenv(key, "")

    return _ENV_PATTERN.sub(repl, value)


def _expand_env_in_obj(obj: Any) -> Any:
    if isinstance(obj, str):
        return _expand_env(obj)
    if isinstance(obj, list):
        return [_expand_env_in_obj(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _expand_env_in_obj(v) for k, v in obj.items()}
    return obj


def _normalize_tools(tools: Dict[str, Any]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for key, val in (tools or {}).items():
        if isinstance(val, str):
            out[key] = [val]
        elif isinstance(val, list):
            out[key] = [str(x) for x in val]
        else:
            out[key] = []
    return out


def _normalize_args_schema(schema: Dict[str, Any]) -> Dict[str, Dict[str, List[str]]]:
    out: Dict[str, Dict[str, List[str]]] = {}
    for logical, fields in (schema or {}).items():
        if not isinstance(fields, dict):
            continue
        out[logical] = {}
        for field_name, aliases in fields.items():
            if isinstance(aliases, str):
                out[logical][field_name] = [aliases]
            elif isinstance(aliases, list):
                out[logical][field_name] = [str(a) for a in aliases]
    return out


def parse_server_entry(name: str, raw: Dict[str, Any]) -> MCPServerConfig:
    raw = _expand_env_in_obj(deepcopy(raw))
    return MCPServerConfig(
        name=name,
        enabled=bool(raw.get("enabled", False)),
        transport=str(raw.get("transport", "stdio")).lower().strip(),
        command=raw.get("command"),
        args=list(raw.get("args") or []),
        cwd=raw.get("cwd"),
        env={str(k): str(v) for k, v in (raw.get("env") or {}).items()},
        url=raw.get("url"),
        roles=[str(r) for r in (raw.get("roles") or [])],
        tools=_normalize_tools(raw.get("tools") or {}),
        args_schema=_normalize_args_schema(raw.get("args_schema") or {}),
    )


def default_servers_path() -> Path:
    return Path(__file__).resolve().parent / "servers.default.json"


def load_server_registry(path: Optional[str] = None) -> Dict[str, MCPServerConfig]:
    """Load MCP server configs from JSON. Missing file → empty registry."""
    if path:
        p = Path(path)
    else:
        try:
            from config import MCP_SERVERS_PATH

            p = Path(MCP_SERVERS_PATH)
        except ImportError:
            p = default_servers_path()

    if not p.is_file():
        logger.warning("MCP servers registry not found at %s", p)
        return {}

    with open(p, encoding="utf-8") as f:
        data = json.load(f)

    servers_raw = data.get("servers", data)
    if not isinstance(servers_raw, dict):
        logger.error("Invalid MCP servers registry format in %s", p)
        return {}

    registry: Dict[str, MCPServerConfig] = {}
    for name, entry in servers_raw.items():
        if not isinstance(entry, dict):
            continue
        registry[name] = parse_server_entry(name, entry)
    return registry


def servers_for_role(
    registry: Dict[str, MCPServerConfig],
    role: str,
    *,
    only_enabled: bool = True,
    preferred: Optional[str] = None,
) -> List[MCPServerConfig]:
    """Return servers that advertise ``role``, preferred name first."""
    matches = [
        s
        for s in registry.values()
        if s.has_role(role) and (s.enabled or not only_enabled)
    ]
    if preferred:
        matches.sort(key=lambda s: 0 if s.name == preferred else 1)
    return matches
