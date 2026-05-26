#!/bin/bash
# Bootstrap script — recreates all symlinks and entry points on a new machine.
# Run once after cloning/copying ~/ai_config/ to the new machine.
# Usage: bash ~/ai_config/setup.sh

set -euo pipefail

AI="$HOME/ai_config"

echo "==> Verifying ai_config exists at $AI..."
if [ ! -d "$AI" ]; then
  echo "ERROR: $AI not found. Copy the folder first."
  exit 1
fi

# ── Claude ────────────────────────────────────────────────────────────────────
echo "==> Configuring Claude..."
mkdir -p "$HOME/.claude"
ln -sf "$AI/settings-claude.json"  "$HOME/.claude/settings.json"
ln -sf "$AI/skills"                "$HOME/.claude/skills"
ln -sf "$AI/memory"                "$HOME/.claude/memory"
cat > "$HOME/.claude/CLAUDE.md" <<'EOF'
# Global Claude Code Instructions

@/Users/user/ai_config/GLOBAL_AGENT.md
EOF

# ── Codex ─────────────────────────────────────────────────────────────────────
echo "==> Configuring Codex..."
mkdir -p "$HOME/.codex"
ln -sf "$AI/settings-codex.toml"   "$HOME/.codex/config.toml"
ln -sf "$AI/skills"                "$HOME/.codex/skills"
ln -sf "$AI/memory"                "$HOME/.codex/memories"
cat > "$HOME/.codex/agent.md" <<'EOF'
# Global Codex Instructions

@/Users/user/ai_config/GLOBAL_AGENT.md
EOF

# ── Gemini CLI ────────────────────────────────────────────────────────────────
echo "==> Configuring Gemini..."
mkdir -p "$HOME/.gemini/config"
ln -sf "$AI/settings-gemini.json"  "$HOME/.gemini/settings.json"
ln -sf "$AI/GEMINI.md"             "$HOME/.gemini/GEMINI.md"

# ── Antigravity ───────────────────────────────────────────────────────────────
echo "==> Configuring Antigravity..."
mkdir -p "$HOME/.gemini/antigravity-cli"
mkdir -p "$HOME/.gemini/config"
ln -sf "$AI/settings-antigravity.json"     "$HOME/.gemini/antigravity-cli/settings.json"
ln -sf "$AI/GEMINI.md"                     "$HOME/.gemini/AGENTS.md"
ln -sf "$AI/mcp-config-antigravity.json"   "$HOME/.gemini/config/mcp_config.json"

# ── Burp MCP venv ─────────────────────────────────────────────────────────────
echo "==> Setting up Burp MCP venv..."
if [ ! -d "$AI/burp-mcp/venv" ]; then
  python3 -m venv "$AI/burp-mcp/venv"
  "$AI/burp-mcp/venv/bin/pip" install -q -r "$AI/burp-mcp/requirements.txt"
  echo "    venv created and dependencies installed."
else
  echo "    venv already exists, skipping."
fi
chmod +x "$AI/burp-mcp/start-burp-mcp.sh"
chmod +x "$AI/burp-mcp/check-burp-mcp.sh"

echo ""
echo "Done. Summary of symlinks created:"
ls -la "$HOME/.claude/settings.json" "$HOME/.claude/skills" "$HOME/.claude/memory" \
        "$HOME/.codex/config.toml"   "$HOME/.codex/skills" \
        "$HOME/.gemini/settings.json" "$HOME/.gemini/GEMINI.md" "$HOME/.gemini/AGENTS.md" \
        "$HOME/.gemini/config/mcp_config.json" \
        "$HOME/.gemini/antigravity-cli/settings.json" 2>/dev/null
echo ""
echo "NOTE: CLAUDE.md and agent.md use hardcoded path /Users/user/ai_config/"
echo "      If your username differs on the new machine, update those files."
