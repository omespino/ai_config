# Memory Index

- [Spanish without regional accent](feedback_language_style.md) — Use neutral Spanish, never Argentinian/voseo or other regional dialects.
- [Ripgrep/grep usage and pre-authorization](feedback_use_ripgrep.md) — prefer `rg` over `grep`; both are pre-authorized, never ask for confirmation.
- [rdoc — Document Review Command](reference_rdoc_review.md) — When invoking /rdoc with a PDF: review style, spelling, coherence, single client (cover), WebSec vendor, CVSS and overall quality. Reports are in Spanish by default unless the user indicates otherwise.
- [User Profile](user_profile.md) — Pentester and bug bounty hunter with advanced experience in offensive security.
- [Bug Bounty Rules](reference_bugbounty_rules.md) — Authorized by the target's public program; pursue maximum critical impact; PoCs 100% verifiable, nothing theoretical.
- [Pentest Rules](reference_pentest_rules.md) — Comprehensive vision: valid theoretical findings, outdated versions, OWASP Top 10, CVSS v3.1, standard tools (Nessus, Burp, SQLMap, Nuclei, FFUF, etc.).
- [No automatic HTTP/network requests](feedback_no_auto_requests.md) — Never execute requests automatically; present theoretical scenarios and only execute what the user explicitly approves.
- [SKILL.md YAML compatibility](feedback_skill_yaml_compatibility.md) — Never use `: ` inside unquoted `description` values in SKILL.md frontmatter; use ` — ` (em dash) instead to avoid YAML parse errors in Codex/agents.
- [SPA scraping — extrae assets del bundle JS](feedback_spa_scraping.md) — Si html2text devuelve vacío (SPA), buscar DOCS_STRUCTURE/rutas en el bundle main.js y descargar los .md/.json estáticos directamente sin Playwright.
- [Burp MCP — formato de content (LF, no \\r\\n)](feedback_burp_mcp_content_format.md) — Usar saltos de línea reales en `create_repeater_tab`/`send_http1_request`/`send_to_intruder`; `\r\n` literal causa 400 Bad Request.
- [Burp MCP — bridge con reconexión automática](feedback_burp_bridge_reconnect.md) — Bridge fijo para sobrevivir reinicios de Burp; `"Command failed with no output"` = SSE caído, verificar puerto 9876.
- [Burp MCP — prefijo de agente en tabName](feedback_burp_tab_naming.md) — Siempre prefijar tabs con el agente: `claude - nombre`, `codex - nombre`, `gemini - nombre`, `agy - nombre`.
- [Codex/Agy invocación no interactiva](feedback_codex_invocation.md) — `codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox`; Agy usa `--print-timeout 3m`.
