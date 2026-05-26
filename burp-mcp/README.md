# Global Burp MCP Bridge

This directory is the stable Codex-global Burp MCP bridge.

Codex global config:

```toml
[mcp_servers.burp-suite]
command = "/Users/user/.codex/burp-mcp/start-burp-mcp.sh"
```

The bridge exposes Burp's local SSE MCP endpoint as MCP-over-stdio for Codex.
It expects the Burp Suite MCP extension to be running and listening at:

```text
http://127.0.0.1:9876/
```

Override the SSE URL when needed:

```bash
BURP_MCP_SSE_URL=http://127.0.0.1:9876/ /Users/user/.codex/burp-mcp/start-burp-mcp.sh
```

Quick connectivity check:

```bash
/Users/user/.codex/burp-mcp/check-burp-mcp.sh
```
