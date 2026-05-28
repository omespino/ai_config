---
name: Ripgrep/grep usage and pre-authorization
description: Prefer ripgrep over grep, and user has pre-authorized both tools so no confirmation is ever needed
type: feedback
originSessionId: 6673f0e2-c178-4809-8cc5-5301467e98a9
---

1. Always invoke `rg` (ripgrep) instead of `grep`/`egrep`/`fgrep` for text search.
2. Both `rg` and `grep` are **unconditionally pre-authorized** — never ask for permission, never pause for confirmation, never announce you're about to run them. Just execute immediately.

**Why:** Explicit user preference (confirmed 2026-05-05 and 2026-05-28). Ripgrep is faster and has better defaults; confirmation prompts add noise in pentest/triage workflows.

**How to apply:**
- Default to `rg` for any new search; only fall back to `grep` if `rg` is unavailable in the environment.
- Never preface with "I'll run grep, ok?", "do you want me to search?", or any similar phrase. Just run it.
- Authorization covers: piped searches (`cmd | rg pattern`), recursive (`rg -r`), any flag combination, `grep -r`, `egrep`, `fgrep`.
- This authorization does NOT extend to other tools chained alongside (e.g., `rg ... | curl` — the curl still requires normal approval).
- **PATH fallback (macOS):** If `rg` is not found in PATH, use the full path `/opt/homebrew/bin/rg`. This applies to Gemini CLI and Agy which run with a restricted PATH in headless mode.
