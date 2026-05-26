#!/bin/bash
set -euo pipefail

URL="${BURP_MCP_SSE_URL:-http://127.0.0.1:9876/}"

echo "Checking Burp MCP SSE endpoint: $URL"
response="$(curl -i --max-time 5 "$URL" 2>&1 || true)"
printf '%s\n' "$response"

if printf '%s\n' "$response" | grep -q "Content-Type: text/event-stream"; then
  echo "endpoint_ok"
else
  echo "endpoint_unreachable"
fi

echo
echo "Checking stdio bridge dependencies"
"$(cd "$(dirname "$0")" && pwd)/venv/bin/python" -c 'import anyio, mcp, httpx_sse; print("deps_ok")'
