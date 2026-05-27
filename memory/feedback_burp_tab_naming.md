---
name: feedback-burp-tab-naming
description: Burp MCP — siempre prefijar el tabName con el agente que lo crea (claude, codex, gemini, agy, etc.)
metadata:
  type: feedback
---

Al crear tabs en Burp via MCP (`create_repeater_tab`, `send_to_intruder`, `send_to_scanner` o cualquier tool que acepte `tabName`), el nombre del tab SIEMPRE debe incluir un prefijo que identifique el agente que lo creó, seguido del nombre descriptivo del tab.

**Why:** El usuario trabaja con múltiples agentes simultáneamente (Claude, Codex, Gemini, Antigravity/agy) y necesita identificar de un vistazo qué agente generó cada tab en Burp.

**Formato:** `<agente> - <nombre descriptivo>`

**Ejemplos por agente:**
- Claude Code → `claude - IDOR MantenimientoPersona`
- Codex → `codex - Login Brute Force`
- Gemini → `gemini - SQLi PadronPersona`
- Antigravity → `agy - XSS Ingreso`

**How to apply:**
- Aplicar en TODA tool de Burp MCP que tenga parámetro `tabName`: `create_repeater_tab`, `send_to_intruder`, y cualquier futura tool similar.
- Si el nombre ya incluye contexto suficiente, igualmente anteponer el prefijo del agente.
- El prefijo va en minúsculas, separado por ` - ` (espacio-guion-espacio).
