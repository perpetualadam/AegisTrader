"""
Multi-server MCP client manager with a sync façade over asyncio transports.

Supports MCP Python SDK v1 (ClientSession) and v2 (Client) where available.
Connections are kept alive on a dedicated background event loop.
"""

from __future__ import annotations

import asyncio
import logging
import os
import threading
from typing import Any, Dict, List, Optional, Tuple

from mcp_bridge.registry import (
    MCPServerConfig,
    load_server_registry,
    servers_for_role,
)

logger = logging.getLogger(__name__)


class MCPClientError(RuntimeError):
    """Raised when an MCP call fails."""


class MCPClientManager:
    """Connect to and call tools on multiple configured MCP servers."""

    def __init__(self, registry: Optional[Dict[str, MCPServerConfig]] = None):
        self.registry = registry if registry is not None else load_server_registry()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._sessions: Dict[str, Any] = {}
        self._tool_cache: Dict[str, List[str]] = {}
        self._lock = threading.RLock()
        self._started = False

    # ------------------------------------------------------------------ lifecycle
    def start(self) -> None:
        with self._lock:
            if self._started:
                return
            self._loop = asyncio.new_event_loop()
            self._thread = threading.Thread(
                target=self._run_loop,
                name="aegis-mcp-loop",
                daemon=True,
            )
            self._thread.start()
            self._started = True
            logger.info(
                "MCP client manager started (%d servers in registry)",
                len(self.registry),
            )

    def _run_loop(self) -> None:
        assert self._loop is not None
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def stop(self) -> None:
        with self._lock:
            if not self._started or self._loop is None:
                return
            fut = asyncio.run_coroutine_threadsafe(self._close_all(), self._loop)
            try:
                fut.result(timeout=15)
            except Exception as e:
                logger.debug("MCP shutdown error: %s", e)
            self._loop.call_soon_threadsafe(self._loop.stop)
            if self._thread:
                self._thread.join(timeout=5)
            self._sessions.clear()
            self._tool_cache.clear()
            self._started = False
            self._loop = None
            self._thread = None

    async def _close_all(self) -> None:
        for name, handle in list(self._sessions.items()):
            try:
                closer = handle.get("close")
                if closer:
                    await closer()
            except Exception as e:
                logger.debug("Error closing MCP server %s: %s", name, e)
        self._sessions.clear()

    def ensure_started(self) -> None:
        if not self._started:
            self.start()

    # ------------------------------------------------------------------ public API
    def list_enabled_servers(self) -> List[str]:
        return [n for n, s in self.registry.items() if s.enabled]

    def get_server(self, name: str) -> Optional[MCPServerConfig]:
        return self.registry.get(name)

    def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Optional[Dict[str, Any]] = None,
        *,
        timeout: float = 45.0,
    ) -> Any:
        """Call a tool by exact name on a named server. Returns raw SDK result."""
        self.ensure_started()
        assert self._loop is not None
        fut = asyncio.run_coroutine_threadsafe(
            self._call_tool_async(server_name, tool_name, arguments or {}),
            self._loop,
        )
        try:
            return fut.result(timeout=timeout)
        except Exception as e:
            raise MCPClientError(
                f"MCP tool call failed ({server_name}.{tool_name}): {e}"
            ) from e

    def call_logical_tool(
        self,
        server_name: str,
        logical_tool: str,
        values: Optional[Dict[str, Any]] = None,
        *,
        timeout: float = 45.0,
    ) -> Any:
        """
        Resolve a logical tool (e.g. get_quote) to a concrete server tool name,
        map arguments via args_schema, and invoke it.
        """
        cfg = self.registry.get(server_name)
        if not cfg:
            raise MCPClientError(f"Unknown MCP server '{server_name}'")
        if not cfg.enabled:
            raise MCPClientError(f"MCP server '{server_name}' is disabled")

        candidates = cfg.tool_candidates(logical_tool)
        if not candidates:
            raise MCPClientError(
                f"No tool mapping for logical tool '{logical_tool}' on '{server_name}'"
            )

        available = self.list_tools(server_name)
        chosen = None
        if available:
            avail_set = set(available)
            for name in candidates:
                if name in avail_set:
                    chosen = name
                    break
        if chosen is None:
            # Server may not support list_tools reliably — try first candidate
            chosen = candidates[0]

        args = cfg.map_arguments(logical_tool, values or {})
        return self.call_tool(server_name, chosen, args, timeout=timeout)

    def list_tools(self, server_name: str, *, timeout: float = 30.0) -> List[str]:
        self.ensure_started()
        with self._lock:
            if server_name in self._tool_cache:
                return list(self._tool_cache[server_name])
        assert self._loop is not None
        fut = asyncio.run_coroutine_threadsafe(
            self._list_tools_async(server_name),
            self._loop,
        )
        try:
            names = fut.result(timeout=timeout)
        except Exception as e:
            logger.debug("list_tools failed for %s: %s", server_name, e)
            return []
        with self._lock:
            self._tool_cache[server_name] = names
        return list(names)

    def call_first_for_role(
        self,
        role: str,
        logical_tool: str,
        values: Optional[Dict[str, Any]] = None,
        *,
        preferred: Optional[str] = None,
        timeout: float = 45.0,
    ) -> Tuple[str, Any]:
        """
        Try enabled servers for ``role`` until one succeeds.
        Returns (server_name, raw_result).
        """
        servers = servers_for_role(
            self.registry, role, only_enabled=True, preferred=preferred
        )
        if not servers:
            raise MCPClientError(f"No enabled MCP servers with role '{role}'")

        errors: List[str] = []
        for cfg in servers:
            try:
                result = self.call_logical_tool(
                    cfg.name, logical_tool, values, timeout=timeout
                )
                return cfg.name, result
            except Exception as e:
                errors.append(f"{cfg.name}: {e}")
                logger.debug(
                    "MCP role=%s logical=%s failed on %s: %s",
                    role,
                    logical_tool,
                    cfg.name,
                    e,
                )
        raise MCPClientError(
            f"All MCP servers failed for role={role} tool={logical_tool}: "
            + "; ".join(errors)
        )

    # ------------------------------------------------------------------ async internals
    async def _ensure_session(self, server_name: str) -> Any:
        if server_name in self._sessions:
            return self._sessions[server_name]["client"]

        cfg = self.registry.get(server_name)
        if not cfg:
            raise MCPClientError(f"Unknown MCP server '{server_name}'")
        if not cfg.enabled:
            raise MCPClientError(f"MCP server '{server_name}' is disabled")

        handle = await self._connect(cfg)
        self._sessions[server_name] = handle
        return handle["client"]

    async def _connect(self, cfg: MCPServerConfig) -> Dict[str, Any]:
        """
        Establish a session. Prefers SDK v2 Client; falls back to v1 ClientSession.
        """
        # --- SDK v2 high-level Client ---
        try:
            from mcp import Client  # type: ignore

            if cfg.transport in ("http", "sse", "streamable_http") and cfg.url:
                client = Client(cfg.url)
                await client.__aenter__()
                return {
                    "client": client,
                    "close": lambda: client.__aexit__(None, None, None),
                    "style": "v2",
                }

            if cfg.transport == "stdio" and cfg.command:
                from mcp.client.stdio import stdio_client  # type: ignore

                try:
                    from mcp import StdioServerParameters  # type: ignore
                except ImportError:
                    from mcp.client.stdio import StdioServerParameters  # type: ignore

                env = {**os.environ, **(cfg.env or {})}
                params = StdioServerParameters(
                    command=cfg.command,
                    args=cfg.args or [],
                    env=env,
                    cwd=cfg.cwd,
                )
                transport_cm = stdio_client(params)
                transport = await transport_cm.__aenter__()
                # v2 Client can wrap a transport tuple
                try:
                    client = Client(transport_cm)  # may not accept already-entered
                except TypeError:
                    client = None

                if client is not None:
                    try:
                        await client.__aenter__()
                        return {
                            "client": client,
                            "close": self._make_close(client, transport_cm),
                            "style": "v2",
                        }
                    except Exception:
                        pass

                # Fall through to v1 session on the open transport
                read, write = transport
                return await self._v1_session_from_streams(
                    read, write, extra_cm=transport_cm
                )

        except ImportError:
            pass
        except Exception as e:
            logger.debug("MCP v2 connect path failed for %s: %s", cfg.name, e)

        # --- SDK v1 ClientSession ---
        return await self._connect_v1(cfg)

    async def _connect_v1(self, cfg: MCPServerConfig) -> Dict[str, Any]:
        from mcp import ClientSession  # type: ignore

        if cfg.transport in ("http", "streamable_http") and cfg.url:
            try:
                from mcp.client.streamable_http import streamablehttp_client  # type: ignore

                cm = streamablehttp_client(cfg.url)
                streams = await cm.__aenter__()
                read, write = streams[0], streams[1]
                return await self._v1_session_from_streams(read, write, extra_cm=cm)
            except ImportError:
                from mcp.client.sse import sse_client  # type: ignore

                cm = sse_client(cfg.url)
                read, write = await cm.__aenter__()
                return await self._v1_session_from_streams(read, write, extra_cm=cm)

        if cfg.transport == "sse" and cfg.url:
            from mcp.client.sse import sse_client  # type: ignore

            cm = sse_client(cfg.url)
            read, write = await cm.__aenter__()
            return await self._v1_session_from_streams(read, write, extra_cm=cm)

        if cfg.transport == "stdio" and cfg.command:
            from mcp.client.stdio import stdio_client  # type: ignore

            try:
                from mcp import StdioServerParameters  # type: ignore
            except ImportError:
                from mcp.client.stdio import StdioServerParameters  # type: ignore

            env = {**os.environ, **(cfg.env or {})}
            params = StdioServerParameters(
                command=cfg.command,
                args=cfg.args or [],
                env=env,
                cwd=cfg.cwd,
            )
            cm = stdio_client(params)
            read, write = await cm.__aenter__()
            return await self._v1_session_from_streams(read, write, extra_cm=cm)

        raise MCPClientError(
            f"Unsupported MCP transport/config for server '{cfg.name}' "
            f"(transport={cfg.transport})"
        )

    async def _v1_session_from_streams(
        self, read: Any, write: Any, extra_cm: Any = None
    ) -> Dict[str, Any]:
        from mcp import ClientSession  # type: ignore

        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()

        async def _close() -> None:
            try:
                await session.__aexit__(None, None, None)
            finally:
                if extra_cm is not None:
                    await extra_cm.__aexit__(None, None, None)

        return {"client": session, "close": _close, "style": "v1"}

    def _make_close(self, client: Any, transport_cm: Any):
        async def _close() -> None:
            try:
                await client.__aexit__(None, None, None)
            finally:
                try:
                    await transport_cm.__aexit__(None, None, None)
                except Exception:
                    pass

        return _close

    async def _call_tool_async(
        self, server_name: str, tool_name: str, arguments: Dict[str, Any]
    ) -> Any:
        client = await self._ensure_session(server_name)
        style = self._sessions[server_name].get("style")
        if style == "v2":
            return await client.call_tool(tool_name, arguments)
        # v1 ClientSession
        return await client.call_tool(tool_name, arguments=arguments)

    async def _list_tools_async(self, server_name: str) -> List[str]:
        client = await self._ensure_session(server_name)
        result = await client.list_tools()
        tools = getattr(result, "tools", result)
        names: List[str] = []
        for t in tools or []:
            name = getattr(t, "name", None)
            if name:
                names.append(str(name))
            elif isinstance(t, dict) and "name" in t:
                names.append(str(t["name"]))
        return names


_manager: Optional[MCPClientManager] = None
_manager_lock = threading.Lock()


def get_mcp_manager(force_reload: bool = False) -> MCPClientManager:
    """Singleton MCP client manager."""
    global _manager
    with _manager_lock:
        if _manager is None or force_reload:
            if _manager is not None:
                try:
                    _manager.stop()
                except Exception:
                    pass
            _manager = MCPClientManager()
        return _manager


def reset_mcp_manager() -> None:
    """Test helper — tear down singleton."""
    global _manager
    with _manager_lock:
        if _manager is not None:
            try:
                _manager.stop()
            except Exception:
                pass
            _manager = None
