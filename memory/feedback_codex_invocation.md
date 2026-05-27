---
name: feedback-codex-invocation
description: Codex exec non-interactive invocation — flags required to run outside git repo and skip confirmations
metadata:
  type: feedback
---

Para correr Codex de forma no interactiva y autónoma, usar siempre:

```bash
codex exec \
  --skip-git-repo-check \
  --dangerously-bypass-approvals-and-sandbox \
  "prompt aquí"
```

**Why:** `codex exec` sin `--skip-git-repo-check` falla con "Not inside a trusted directory and --skip-git-repo-check was not specified" cuando el directorio no tiene `.git`. Sin `--dangerously-bypass-approvals-and-sandbox` requiere confirmación manual para cada acción.

**How to apply:** Siempre incluir ambos flags al lanzar Codex de forma autónoma desde Claude o cualquier script. El flag `--skip-git-repo-check` también acepta el config override `-c 'skip_git_repo_check=true'` si se prefiere vía config.

**Agy non-interactive:** Para Agy usar `agy --dangerously-skip-permissions --print-timeout 3m -p "prompt"`. El timeout por defecto (5m) puede causar salida vacía en tareas con herramientas lentas; bajar a 3m da output antes del timeout.
