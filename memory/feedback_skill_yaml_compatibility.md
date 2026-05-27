---
name: feedback-skill-yaml-compatibility
description: SKILL.md frontmatter rules — no `: ` in unquoted description (use ` — ` em dash), and description must be ≤ 1024 characters. Both cause Codex to skip the skill with a warning.
metadata:
  type: feedback
---

Los archivos `SKILL.md` tienen un bloque frontmatter YAML. El campo `description` tiene dos restricciones que Codex valida al cargar skills:

## Regla 1 — Sin `: ` dentro del value

Nunca usar `: ` (dos puntos + espacio) dentro del valor del campo `description` si no está entre comillas. El parser YAML lo interpreta como un nuevo key de mapping y lanza `invalid YAML: mapping values are not allowed in this context`.

**Why:** `saif-framework/SKILL.md` y `ai-agents-architecture/SKILL.md` fallaron con este error. El parser detectó `completo: 4` e `IA: capas` como nuevos keys de mapping.

**Fix:** Reemplazar `: ` por ` — ` (em dash). Es el patrón más limpio y consistente con los demás skills.

## Regla 2 — Máximo 1024 caracteres

El campo `description` no puede superar 1024 caracteres. Codex lanza `invalid description: exceeds maximum length of 1024 characters` y salta el skill completo.

**Why:** `ai-agents-threats/SKILL.md` superó el límite al agregar los 5 fallos de Gemini CLI RCE con triggers extendidos — llegó a 2897 chars.

**Fix:** Condensar la lista de triggers — mantener solo los más distintivos, eliminar variantes redundantes. Verificar el largo antes de aplicar con: `python3 -c "print(len('...description...'))"`.

## How to apply (ambas reglas)

1. Redactar la descripción con ` — ` en lugar de `: `.
2. Medir el largo: `python3 -c "print(len('tu description'))"` — debe ser ≤ 1024.
3. Si supera el límite, recortar la lista de triggers eliminando variantes redundantes o combinando sinónimos.
4. Objetivo práctico: apuntar a ~800 chars para tener margen al actualizar en el futuro.
5. Verificar también que no haya otros caracteres YAML especiales sin escapar: `{`, `}`, `[`, `]`, `#` al inicio de value.
