#!/usr/bin/env python3
"""
Burp Suite MCP Server
Integrates Burp Suite Professional REST API with Claude Code.

Requires Burp Suite REST API to be enabled:
  - Go to User options > Misc > REST API
  - Enable: "Service running"
  - Note the port (default 1337) and API key (optional)
"""

import asyncio
import base64
import json
import os
import sys
from typing import Any

import httpx
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# ---------------------------------------------------------------------------
# Configuration (override via environment variables)
# ---------------------------------------------------------------------------
BURP_HOST = os.getenv("BURP_HOST", "127.0.0.1")
BURP_PORT = int(os.getenv("BURP_PORT", "1337"))
BURP_API_KEY = os.getenv("BURP_API_KEY", "")
BURP_BASE_URL = f"http://{BURP_HOST}:{BURP_PORT}"

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
server = Server("burp-suite")


def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    if BURP_API_KEY:
        h["Authorization"] = f"Bearer {BURP_API_KEY}"
    return h


def _decode(b64: str | None) -> str:
    """Decode a base64 string returned by Burp API."""
    if not b64:
        return ""
    try:
        return base64.b64decode(b64).decode("utf-8", errors="replace")
    except Exception:
        return b64


def _fmt_request(item: dict) -> str:
    """Format a proxy history item into a readable summary."""
    req = item.get("request", {})
    resp = item.get("response", {})

    method = req.get("method", "?")
    url = req.get("url", req.get("path", "?"))
    host = item.get("host", req.get("host", ""))
    status = resp.get("statusCode", resp.get("status_code", "?"))
    length = resp.get("responseLength", resp.get("body_length", "?"))
    mime = resp.get("mimeType", resp.get("mime_type", ""))
    item_id = item.get("id", "?")

    # Some API versions embed raw bytes in base64
    raw_req = req.get("raw", "")
    raw_resp = resp.get("raw", "")

    lines = [
        f"[#{item_id}] {method} {url}",
        f"  Host   : {host}",
        f"  Status : {status}  Length: {length}  MIME: {mime}",
    ]

    if raw_req:
        decoded = _decode(raw_req)
        preview = decoded[:800] + ("..." if len(decoded) > 800 else "")
        lines.append(f"\n--- REQUEST ---\n{preview}")
    if raw_resp:
        decoded = _decode(raw_resp)
        preview = decoded[:800] + ("..." if len(decoded) > 800 else "")
        lines.append(f"\n--- RESPONSE ---\n{preview}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="burp_proxy_history",
            description=(
                "Get the last N HTTP requests/responses captured by Burp Suite's proxy. "
                "Returns method, URL, status code, length and a preview of headers/body."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "How many recent requests to return (default 5, max 50)",
                        "default": 5,
                    },
                    "filter": {
                        "type": "string",
                        "description": "Optional substring to filter URLs (e.g. '/api', 'login')",
                    },
                },
            },
        ),
        types.Tool(
            name="burp_request_detail",
            description="Get the full raw request and response for a specific proxy history item by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Proxy history item ID (from burp_proxy_history)",
                    }
                },
                "required": ["id"],
            },
        ),
        types.Tool(
            name="burp_site_map",
            description="Get URLs and endpoints discovered in the Burp Suite site map.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url_prefix": {
                        "type": "string",
                        "description": "Filter results to URLs starting with this prefix",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max number of entries to return (default 50)",
                        "default": 50,
                    },
                },
            },
        ),
        types.Tool(
            name="burp_scanner_issues",
            description="Get security vulnerabilities found by Burp Suite Scanner.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url_prefix": {
                        "type": "string",
                        "description": "Filter results to URLs starting with this prefix",
                    },
                    "severity": {
                        "type": "string",
                        "description": "Filter by severity: High, Medium, Low, Information",
                    },
                },
            },
        ),
        types.Tool(
            name="burp_active_scan",
            description="Launch an active scan against a URL using Burp Suite Scanner.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Target URL to scan",
                    }
                },
                "required": ["url"],
            },
        ),
        types.Tool(
            name="burp_send_to_repeater",
            description="Send a proxy history request to Burp Suite Repeater for manual testing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Proxy history item ID to send to Repeater",
                    }
                },
                "required": ["id"],
            },
        ),
        types.Tool(
            name="burp_status",
            description="Check Burp Suite connection status and REST API availability.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    async with httpx.AsyncClient(
        base_url=BURP_BASE_URL, headers=_headers(), timeout=15.0
    ) as client:
        try:
            result = await _dispatch(client, name, arguments)
        except httpx.ConnectError:
            result = (
                f"ERROR: Cannot connect to Burp Suite REST API at {BURP_BASE_URL}.\n\n"
                "To enable the REST API in Burp Suite:\n"
                "  1. Go to User options > Misc > REST API\n"
                "  2. Check 'Service running'\n"
                "  3. Note the port (default 1337) and optionally set an API key\n"
                "  4. Set BURP_PORT env var if using a different port\n"
                "  5. Set BURP_API_KEY env var if API key is configured"
            )
        except httpx.HTTPStatusError as e:
            result = f"HTTP {e.response.status_code}: {e.response.text[:500]}"
        except Exception as e:
            result = f"Error: {type(e).__name__}: {e}"

    return [types.TextContent(type="text", text=result)]


async def _dispatch(client: httpx.AsyncClient, name: str, args: dict) -> str:
    if name == "burp_status":
        return await _status(client)
    elif name == "burp_proxy_history":
        return await _proxy_history(client, args)
    elif name == "burp_request_detail":
        return await _request_detail(client, args)
    elif name == "burp_site_map":
        return await _site_map(client, args)
    elif name == "burp_scanner_issues":
        return await _scanner_issues(client, args)
    elif name == "burp_active_scan":
        return await _active_scan(client, args)
    elif name == "burp_send_to_repeater":
        return await _send_to_repeater(client, args)
    else:
        return f"Unknown tool: {name}"


async def _status(client: httpx.AsyncClient) -> str:
    """Check Burp API status."""
    # Try both common API path formats
    for path in ["/v0.1/", "/burp/versions", "/"]:
        try:
            r = await client.get(path)
            if r.status_code < 500:
                return (
                    f"Burp Suite REST API is reachable at {BURP_BASE_URL}\n"
                    f"Status: {r.status_code}\n"
                    f"Response preview: {r.text[:300]}"
                )
        except Exception:
            continue
    return f"Could not reach Burp Suite REST API at {BURP_BASE_URL}"


async def _proxy_history(client: httpx.AsyncClient, args: dict) -> str:
    limit = min(int(args.get("limit", 5)), 50)
    url_filter = args.get("filter", "").lower()

    # Burp REST API v0.1
    r = await client.get("/v0.1/proxy/history")
    r.raise_for_status()
    data = r.json()

    items = data if isinstance(data, list) else data.get("messages", data.get("history", []))

    # Apply URL filter
    if url_filter:
        items = [
            i for i in items
            if url_filter in str(i.get("request", {}).get("url", "")).lower()
            or url_filter in str(i.get("url", "")).lower()
        ]

    # Take last N
    items = items[-limit:]

    if not items:
        return "No proxy history items found."

    output = [f"Last {len(items)} proxy history items:\n{'='*60}"]
    for item in reversed(items):  # Most recent first
        output.append(_fmt_request(item))
        output.append("-" * 60)

    return "\n".join(output)


async def _request_detail(client: httpx.AsyncClient, args: dict) -> str:
    item_id = args["id"]
    r = await client.get(f"/v0.1/proxy/history/{item_id}")
    r.raise_for_status()
    item = r.json()

    req = item.get("request", {})
    resp = item.get("response", {})

    raw_req = _decode(req.get("raw", ""))
    raw_resp = _decode(resp.get("raw", ""))

    output = [
        f"Proxy History Item #{item_id}",
        "=" * 60,
        "=== REQUEST ===",
        raw_req or json.dumps(req, indent=2),
        "",
        "=== RESPONSE ===",
        raw_resp or json.dumps(resp, indent=2),
    ]
    return "\n".join(output)


async def _site_map(client: httpx.AsyncClient, args: dict) -> str:
    limit = int(args.get("limit", 50))
    url_prefix = args.get("url_prefix", "")

    params = {}
    if url_prefix:
        params["urlPrefix"] = url_prefix

    r = await client.get("/v0.1/target/sitemap", params=params)
    r.raise_for_status()
    data = r.json()

    entries = data if isinstance(data, list) else data.get("sitemap", [])
    entries = entries[:limit]

    if not entries:
        return "Site map is empty. Browse the target with Burp's browser first."

    lines = [f"Site map ({len(entries)} entries):", "=" * 60]
    for e in entries:
        url = e.get("url", e.get("host", "?"))
        status = e.get("statusCode", e.get("response", {}).get("statusCode", "?"))
        lines.append(f"  [{status}] {url}")

    return "\n".join(lines)


async def _scanner_issues(client: httpx.AsyncClient, args: dict) -> str:
    url_prefix = args.get("url_prefix", "")
    severity_filter = args.get("severity", "").lower()

    # List all scan tasks, then collect issues per task
    r = await client.get("/v0.1/scan")
    r.raise_for_status()
    scans_data = r.json()
    scans = scans_data if isinstance(scans_data, list) else scans_data.get("tasks", [])

    issues: list = []
    for scan in scans:
        task_id = scan.get("id", scan.get("task_id"))
        if task_id is None:
            continue
        params = {}
        if url_prefix:
            params["urlPrefix"] = url_prefix
        try:
            ri = await client.get(f"/v0.1/scan/{task_id}/issues", params=params)
            if ri.status_code == 200:
                data = ri.json()
                task_issues = data if isinstance(data, list) else data.get("issues", [])
                issues.extend(task_issues)
        except Exception:
            continue

    if severity_filter:
        issues = [i for i in issues if severity_filter in str(i.get("severity", "")).lower()]

    if not issues:
        return "No scanner issues found."

    lines = [f"Scanner issues ({len(issues)} total):", "=" * 60]
    for issue in issues:
        name = issue.get("name", issue.get("issueName", "Unknown"))
        sev = issue.get("severity", "?")
        conf = issue.get("confidence", "?")
        url = issue.get("url", issue.get("origin", "?"))
        detail = issue.get("issueDetail", issue.get("detail", ""))
        lines.append(f"\n[{sev} / {conf}] {name}")
        lines.append(f"  URL: {url}")
        if detail:
            lines.append(f"  Detail: {detail[:300]}")

    return "\n".join(lines)


async def _active_scan(client: httpx.AsyncClient, args: dict) -> str:
    url = args["url"]
    payload = {
        "scan_configurations": [{"type": "NamedConfiguration", "name": "Crawl and Audit - Balanced"}],
        "scope": {
            "include": [{"rule": url, "type": "SimpleScopeRule"}],
            "exclude": [],
        },
        "urls": [url],
    }
    r = await client.post("/v0.1/scan", json=payload)
    r.raise_for_status()
    data = r.json()
    scan_id = data.get("id", data.get("scan_id", "unknown"))
    return f"Active scan started. Scan ID: {scan_id}\nTarget: {url}"


async def _send_to_repeater(client: httpx.AsyncClient, args: dict) -> str:
    item_id = args["id"]
    # Get the request first
    r = await client.get(f"/v0.1/proxy/history/{item_id}")
    r.raise_for_status()
    item = r.json()

    # Send to Repeater via the Burp API
    payload = {"proxyHistoryId": item_id}
    r2 = await client.post("/v0.1/repeater/requests", json=payload)
    r2.raise_for_status()

    return f"Request #{item_id} sent to Burp Repeater successfully."


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="burp-suite",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
