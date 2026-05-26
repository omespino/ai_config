#!/usr/bin/env python3
"""
Expose Burp's existing SSE MCP server as a stdio MCP server for clients that do
not support SSE transport directly.
"""

import asyncio
import json
import os
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.server import NotificationOptions, Server

REMOTE_URL = os.getenv("BURP_MCP_SSE_URL", "http://127.0.0.1:9876/")

server = Server("burp-suite-bridge")
_session: ClientSession | None = None


def _require_session() -> ClientSession:
    if _session is None:
        raise RuntimeError(f"Bridge is not connected to the remote Burp MCP at {REMOTE_URL}")
    return _session


def _error_text(message: str) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=message)]


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return (await _require_session().list_tools()).tools


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.ContentBlock]:
    result = await _require_session().call_tool(name, arguments or {})
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


async def main() -> None:
    async with sse_client(REMOTE_URL) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            global _session
            _session = session

            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                await server.run(
                    read_stream,
                    write_stream,
                    server.create_initialization_options(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                )


if __name__ == "__main__":
    asyncio.run(main())
