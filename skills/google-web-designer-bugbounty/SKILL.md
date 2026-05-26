---
name: google-web-designer-bugbounty
description: Google Web Designer bug bounty research for authorized testing of client-side attack surfaces in ad documents, templates, and project packages. Use when investigating Google Web Designer GWD files, template metadata, gwd_workspace.json, remoteAssets handling, preview behavior, symlink/path traversal issues, CSS injection, command injection, client-side RCE chains, or CVE-2025-1079 and CVE-2025-4613.
---

# Google Web Designer Bug Bounty

Use this skill for authorized bug bounty work against Google Web Designer project and template handling. Keep work scoped to owned labs, program-permitted targets, and benign proof of impact. Do not provide stealth, persistence, credential theft, or harmful payloads; use harmless markers such as writing a controlled text file or launching a calculator only when the program allows local PoCs.

## Quick Workflow

1. Confirm scope: target version, OS, install source, bug bounty authorization, and whether testing project/template files is allowed.
2. Identify the package type: ad document, saved template, ZIP package, extracted template directory, or source project.
3. Inspect high-risk files:
   - `gwd_workspace.json`
   - HTML containing `<script id="gwd-template-data" type="application/json">`
   - template `remoteAssets`
   - project links/assets used by preview
   - symlinks inside extracted packages on macOS/Linux
4. Map findings to the known patterns in [references/attack-surfaces.md](references/attack-surfaces.md).
5. Build a minimal, non-destructive reproduction with clear user-interaction steps and version boundaries.
6. Write the report around root cause, affected versions, user interaction, platform specificity, impact, fix expectation, and patch bypass checks.

## What To Test

Prioritize parser and file-boundary mistakes in client-side project import flows:

- CSS values loaded from project configuration and inserted into UI CSS.
- Template metadata that names files, URLs, assets, or local paths.
- URL parsing mismatches between browser semantics and filesystem semantics.
- Archive extraction assumptions and default template locations.
- Preview features that resolve package-relative paths.
- macOS/Linux symlinks that escape an intended project directory.
- Windows-only path separator handling, UNC paths, startup folder writes, or Chrome/CEF command-line behavior.

## Report Shape

For each candidate bug, capture:

- Tested Google Web Designer version and release channel.
- OS and platform-specific behavior.
- Exact package structure, with only the minimum files needed.
- The first vulnerable sink: CSS property assignment, remote asset download path, preview path resolution, or subprocess command-line argument.
- User interaction required: open file, use template, edit template, preview, click swatches, etc.
- Security boundary crossed: arbitrary file write, path traversal outside template root, symlink escape, command injection, or client-side RCE.
- Patch status and regression angle compared with CVE-2025-1079, CVE-2025-4613, and the 2025 CSS injection issue.

## Source Reference

Load [references/attack-surfaces.md](references/attack-surfaces.md) when you need concrete version data, payload-safe reproduction ideas, source URLs, CVE details, or bug bounty report checklist language.
