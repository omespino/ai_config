---
name: feedback-burp-bridge-reconnect
description: Burp MCP bridge — muere cuando Burp se reinicia; fix aplicado con reconexión automática en ambos bridges
metadata:
  type: feedback
---

El bridge SSE→stdio de Burp MCP muere cuando Burp se reinicia o la conexión SSE se interrumpe, porque el diseño original anidaba el servidor stdio dentro del contexto SSE. Al caer el SSE, todo el proceso terminaba → tool calls devuelven `"Command failed with no output"`.

**Why:** Diseño frágil: `async with sse_client → ClientSession → stdio_server`. Una sola desconexión SSE mata el bridge completo.

**Fix aplicado (2026-05-27, v2):** El bug real era `anyio.ClosedResourceError`: cuando Burp cierra el SSE limpiamente (EOF al reiniciar), el `asyncio.sleep(86400)` NO se interrumpe, `_session` queda obsoleta y el siguiente `call_tool` explota. Fix en dos partes:

1. `call_tool` captura `ClosedResourceError` → devuelve error legible + llama `_reconnect_signal.set()`
2. `_sse_reconnect_loop` espera en `_reconnect_signal.wait()` en vez de `sleep(86400)` → cuando la señal llega, sale del contexto SSE y reconecta en 5s

El bridge ahora:
- Detecta drops de SSE en el primer `call_tool` fallido
- Reconecta automáticamente en ~5s sin morir
- Devuelve mensaje claro: `"Burp SSE connection was lost. Reconnecting... retry in ~5s."`

**Archivos modificados:**
- `~/.codex/burp-mcp/burp_stdio_bridge.py`
- `~/ai_config/burp-mcp/burp_stdio_bridge.py`

**How to apply:** Si el error `"Command failed with no output"` vuelve a aparecer en tool calls de Burp: verificar que Burp esté corriendo en el puerto 9876 (`curl http://127.0.0.1:9876/`) y reiniciar la sesión del agente para que el bridge se reconecte.
