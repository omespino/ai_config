---
name: feedback-skill-yaml-compatibility
description: SKILL.md frontmatter must be YAML-valid — never use `: ` (colon+space) inside unquoted description values; use ` — ` (em dash) instead.
metadata:
  type: feedback
---

Los archivos `SKILL.md` tienen un bloque frontmatter YAML. El campo `description` debe ser YAML válido para que Codex (y otros agentes) puedan cargar el skill correctamente.

**Regla:** Nunca usar `: ` (dos puntos seguidos de espacio) dentro del valor del campo `description` si no está entre comillas. El parser YAML lo interpreta como un nuevo key de mapping y lanza `invalid YAML: mapping values are not allowed in this context`.

**Why:** `saif-framework/SKILL.md` y `ai-agents-architecture/SKILL.md` fallaron al cargar en Codex con exactamente este error. El parser detectó `completo: 4` e `IA: capas` como nuevos keys de mapping dentro del valor.

**How to apply:**
- Cuando escribas o edites el campo `description` de cualquier `SKILL.md`, reemplaza los `: ` dentro del valor por ` — ` (em dash).
- Ejemplo válido: `description: Arquitectura completa de agentes de IA — capas Application/Agent/Orchestration`
- Ejemplo inválido: `description: Arquitectura completa de agentes de IA: capas Application/Agent/Orchestration`
- Alternativa si es necesario: envolver todo el value en comillas dobles y escapar las comillas internas, o usar block scalar `|` / `>`. Pero ` — ` es el patrón más limpio y consistente con los demás skills.
- Verificar también que no haya otros caracteres YAML especiales sin escapar: `{`, `}`, `[`, `]`, `#` al inicio de value.
