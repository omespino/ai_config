---
name: feedback-burp-bridge-reconnect
description: Burp MCP bridge — muere cuando Burp se reinicia; fix aplicado con reconexión automática en ambos bridges
metadata:
  type: feedback
---

El bridge SSE→stdio de Burp MCP muere cuando Burp se reinicia o la conexión SSE se interrumpe, porque el diseño original anidaba el servidor stdio dentro del contexto SSE. Al caer el SSE, todo el proceso terminaba → tool calls devuelven `"Command failed with no output"`.

**Why:** Diseño frágil: `async with sse_client → ClientSession → stdio_server`. Una sola desconexión SSE mata el bridge completo.

**Fix aplicado (2026-05-27):** Ambos bridges actualizados con loop de reconexión automática (`_sse_reconnect_loop`) que corre como background task independiente del servidor stdio. El bridge ahora:
- Espera hasta 15s para la primera conexión SSE al iniciar
- Si el SSE cae, reintenta cada 5 segundos sin morir
- El servidor stdio sigue vivo durante la reconexión

**Archivos modificados:**
- `~/.codex/burp-mcp/burp_stdio_bridge.py`
- `~/ai_config/burp-mcp/burp_stdio_bridge.py`

**How to apply:** Si el error `"Command failed with no output"` vuelve a aparecer en tool calls de Burp: verificar que Burp esté corriendo en el puerto 9876 (`curl http://127.0.0.1:9876/`) y reiniciar la sesión del agente para que el bridge se reconecte.
