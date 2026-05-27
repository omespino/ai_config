#!/usr/bin/env python3
"""
Expose Burp's existing SSE MCP server as a stdio MCP server for clients that do
not support SSE transport directly.

The SSE reconnect loop runs as a background task so the stdio server stays alive
if Burp is restarted mid-session.
"""

import asyncio
import json
import logging
import os
import traceback
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.server import NotificationOptions, Server

logging.basicConfig(
    filename="/tmp/burp_bridge.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)

REMOTE_URL = os.getenv("BURP_MCP_SSE_URL", "http://127.0.0.1:9876/")
RECONNECT_DELAY = 5

server = Server("burp-suite-bridge")
_session: ClientSession | None = None


def _require_session() -> ClientSession:
    if _session is None:
        raise RuntimeError(f"Bridge is not connected to Burp MCP at {REMOTE_URL}")
    return _session


def _error_text(message: str) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=message)]


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return (await _require_session().list_tools()).tools


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.ContentBlock]:
    logging.debug("call_tool: %s args=%s", name, arguments)
    try:
        result = await _require_session().call_tool(name, arguments or {})
        logging.debug("call_tool result: isError=%s content=%s", result.isError, result.content)
    except Exception:
        logging.error("call_tool exception:\n%s", traceback.format_exc())
        raise

    if result.content:
        return result.content

    if result.structuredContent is not None:
        return _error_text(json.dumps(result.structuredContent, indent=2, ensure_ascii=True))

    if result.isError:
        return _error_text(f"Remote Burp MCP tool '{name}' failed without content.")

    return _error_text(f"Remote Burp MCP tool '{name}' returned no content.")


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    return (await _require_session().list_resources()).resources


@server.list_resource_templates()
async def list_resource_templates() -> list[types.ResourceTemplate]:
    return (await _require_session().list_resource_templates()).resourceTemplates


@server.read_resource()
async def read_resource(uri: Any) -> list[types.TextResourceContents | types.BlobResourceContents]:
    return (await _require_session().read_resource(uri)).contents


@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    return (await _require_session().list_prompts()).prompts


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    return await _require_session().get_prompt(name, arguments)


async def _sse_reconnect_loop() -> None:
    global _session
    while True:
        try:
            logging.info("Connecting to Burp SSE at %s", REMOTE_URL)
            async with sse_client(REMOTE_URL) as streams:
                async with ClientSession(*streams) as session:
                    await session.initialize()
                    _session = session
                    logging.info("SSE session ready")
                    # Hold here until the SSE connection drops.
                    # anyio will cancel this sleep when the SSE reader task fails.
                    await asyncio.sleep(86400)
        except asyncio.CancelledError:
            _session = None
            logging.info("SSE loop cancelled")
            return
        except Exception:
            _session = None
            logging.warning("SSE dropped, retrying in %ds:\n%s", RECONNECT_DELAY, traceback.format_exc())
            await asyncio.sleep(RECONNECT_DELAY)


async def main() -> None:
    logging.info("Bridge starting, target=%s", REMOTE_URL)

    sse_task = asyncio.create_task(_sse_reconnect_loop())

    # Wait up to 15s for the initial SSE connection before serving stdio.
    deadline = asyncio.get_event_loop().time() + 15
    while _session is None and asyncio.get_event_loop().time() < deadline:
        await asyncio.sleep(0.05)

    if _session is None:
        logging.warning("Burp SSE not available within 15s; bridge will serve stdio anyway and reconnect when Burp starts")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logging.info("stdio server ready")
        try:
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            )
        finally:
            sse_task.cancel()
            try:
                await sse_task
            except asyncio.CancelledError:
                pass


if __name__ == "__main__":
    asyncio.run(main())
