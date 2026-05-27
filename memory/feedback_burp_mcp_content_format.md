---
name: feedback-burp-mcp-content-format
description: Burp MCP tools — usar saltos de línea reales (LF) en el parámetro content, nunca la secuencia literal \r\n
metadata:
  type: feedback
---

Para todas las herramientas Burp MCP que aceptan contenido HTTP (`create_repeater_tab`, `send_http1_request`, `send_http2_request`, `send_to_intruder`): escribir el request con saltos de línea reales (LF, 0x0A) en el valor del parámetro `content`. **Nunca** usar las secuencias de escape literales `\r\n` (4 caracteres: backslash-r-backslash-n).

**Why:** Cuando se pasa `\r\n` como texto en el parámetro del tool call, llega como 4 caracteres literales al Repeater/Intruder. Burp los envía tal cual al servidor → el servidor responde `400 Bad Request`. IIS/ASP.NET acepta LF-only sin problema.

**How to apply:**
- Escribir cada header en una línea separada con saltos de línea reales.
- No usar `\r\n`, `\\r\\n`, ni ninguna variante de escape textual.
- Quitar `Accept-Encoding: gzip, deflate, br` para que las respuestas lleguen legibles (texto plano).
- Dejar una línea vacía al final del request (fin de headers).

**Ejemplo correcto:**
```
GET /path HTTP/1.1
Host: target.example.com
User-Agent: Mozilla/5.0
Connection: close

```
