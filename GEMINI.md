# Gemini / Antigravity Global Instructions

**Source of truth:** `~/ai_config/` — todas las reglas, skills y memoria viven ahí.

---

## Inicialización — leer al inicio de cada sesión

Lee los siguientes archivos de memoria antes de responder:

```
~/ai_config/memory/user_profile.md
~/ai_config/memory/feedback_language_style.md
~/ai_config/memory/feedback_no_auto_requests.md
~/ai_config/memory/feedback_use_ripgrep.md
~/ai_config/memory/reference_bugbounty_rules.md
~/ai_config/memory/reference_pentest_rules.md
~/ai_config/memory/reference_rdoc_review.md
~/ai_config/memory/reference_google_bughunters_profile.md
```

---

## Ripgrep

Usar siempre `rg` en lugar de `grep`. Si `rg` no está en PATH, usar la ruta completa: `/opt/homebrew/bin/rg`. Ambas herramientas están pre-autorizadas — ejecutar sin pedir confirmación.

---

## Burp Suite MCP — uso eficiente (Optimizado para grandes volúmenes >10k)

Cuando uses las herramientas MCP de Burp, sigue estas reglas:

- **Estructura del historial**: El historial es cronológico (el índice `0` es el más antiguo). Para obtener las peticiones más recientes, se debe consultar el final del historial.
- **Búsqueda rápida del final (Cola)**: En entornos con miles de peticiones, encuentra el final del historial haciendo saltos exponenciales (probar `count=1` con `offset=10000`, `20000`, etc.) para delimitar el final en un máximo de 2 o 3 llamadas rápidas, en lugar de paginar secuencialmente desde el inicio.
- **Parámetros correctos**: Utiliza siempre los parámetros reales del MCP: `offset` y `count` (no uses `limit`).
- **Límite de lectura de registros**: Al inspeccionar peticiones, mantén un tamaño de bloque razonable (máximo `count=50`) ubicado cerca del offset final estimado.
- **Búsqueda por patrones**: Para buscar endpoints, parámetros o payloads específicos, utiliza obligatoriamente `get_proxy_http_history_regex` con expresiones regulares optimizadas. Está prohibido paginar secuencialmente buscando coincidencias manualmente.

---

## Skills (trigger-based, carga bajo demanda)

Cuando el contexto del usuario coincida con los triggers de un skill, lee el archivo correspondiente ANTES de responder:

```
~/ai_config/skills/<skill-name>/SKILL.md
```

No respondas sobre el tema sin haber leído primero el archivo.

### Pentest (por dominio)
| Skill | Triggers |
|---|---|
| `pentest-ad` | "directorio activo", "kerberoasting", "smb relay", "responder", "llmnr", "petitpotam", "impacket", "ntlm coercion" |
| `pentest-mobile` | "pentest móvil", "apk", "ipa", "frida", "mobsf", "ssl pinning", "jadx", "apktool", "debuggable" |
| `pentest-web` | "pentest web", "sqli", "sqlmap", "clickjacking", "iis shortname", "wordpress", "http smuggling", "s3 misconfig" |
| `pentest-network` | "tls 1.0", "sweet32", "snmp", "redis sin auth", "vnc sin auth", "ftp anonimo", "nuclei cve", "credenciales en claro", "terrapin" |
| `pentest-biz-logic` | "idor", "lógica de negocio", "otp bypass", "mfa bypass", "rate limit", "price manipulation", "broken access control" |
| `pentest-physical` | "pentest físico", "rfid", "proxmark", "tailgating", "red plana" |

### Bug bounty — plataformas
| Skill | Triggers |
|---|---|
| `h1-bugbounty` | "hackerone", "h1", "live hacking event", "lhe" |
| `bugcrowd-bugbounty` | "bugcrowd" |

### Bug bounty — Google VRP personal (omespino)
| Skill | Triggers |
|---|---|
| `bughunters-cloud-shell` | "cloud shell google", "cloud shell xss", "devshell", "cloud shell takeover" |
| `bughunters-apigee` | "apigee rce", "apigee hosted target", "apigee node.js" |
| `bughunters-ssrf-gcp` | "uptime check ssrf", "gcp metadata ssrf", "amp validator ssrf", "0.0.0.0 ssrf" |
| `bughunters-debug-endpoints` | "procz flagz", "debug endpoints google", "dremelgateway", "springboard google", "labelaclz", "as15169" |
| `bughunters-gmail-android` | "gmail android", "content:// uri gmail" |
| `bughunters-earth` | "google earth kml", "earth ios", "earth pro linux", "earth pro macos" |
| `bughunters-mobile-misc` | "chrome file://", "android tv idor", "powerpoint xss ios", "ppt xss" |

### Bug bounty — Google VRP (Ezequiel Pereira / bugSWAT)
| Skill | Triggers |
|---|---|
| `bughunters-gae-rce` | "google app engine rce", "gae rce", "appspot rce", "gae internal api", "stubby gcp", "app_config_service gae", "169.254.169.253", "gae staging env" |
| `bughunters-gsi` | "google service infrastructure", "gsi gcp", "visibility labels google", "google_internal label", "servicemanagement api", "dependsonservices gcp" |
| `bughunters-cloud-dm` | "cloud deployment manager rce", "cloud dm rce", "gslbtarget gcp", "googleoptions deployment manager", "deploymentmanager v2beta" |

### Bug bounty — Google VRP (community writeups)
| Skill | Triggers |
|---|---|
| `bughunters-appsheet-ssrf` | "appsheet ssrf", "appsheet webhook ssrf", "webhook redirect ssrf", "post to get redirect ssrf", "301 redirect ssrf gcp", "nechudav appsheet" |

### Bug bounty — Google VRP HoF público
| Skill | Triggers |
|---|---|
| `google-vrp-cloud` | "gcp", "cloud vrp", "gke", "firebase backend", "github actions google", "oss vrp" |
| `google-vrp-web` | "google vrp web", "google web xss", "oauth google" |
| `google-vrp-android` | "android google", "mobile vrp", "kernelctf", "chrome extension google" |

### Bug bounty — Microsoft VRP
| Skill | Triggers |
|---|---|
| `bughunters-microsoft` | "microsoft bug bounty", "msrc", "microsoft ppe", "microsoft-ppe.com", "msal token", "azure ad clientid", "offers copilot microsoft", "nova microsoft store", "swagger microsoft ppe" |

### VRP report writing
| Skill | Triggers |
|---|---|
| `vrp-report-template` | "reporte vrp", "escribir reporte vrp", "formato reporte bug bounty", "template vrp google", "vrp report style", "estructura reporte vrp" |

### Recon y herramientas web
| Skill | Triggers |
|---|---|
| `shodan-free` | "shodan host", "internetdb", "shodan sin créditos", "shodan gratis" |
| `shodan-advanced` | "filtros shodan", "shodan download", "shodan scan", "shodan avanzado" |
| `pentest-source-maps` | "source map", "sourcemapper", "archivo .map", "module federation manifest", "reconstruir codigo fuente", "msal token sessionstorage", "api key mapbox permisos" |
| `pentest-ssrf-redirect-server` | "redirect server ssrf", "servidor de redirect ssrf", "php redirect ssrf", "script redirect 301", "redirect 302 ssrf", "169.254.169.254 redirect", "redirect chain ssrf" |

### AI Agent Security (SAIF 2.0 — Google, May 2025)
| Skill | Triggers |
|---|---|
| `ai-agents-architecture` | "arquitectura agente", "agent architecture", "reasoning core", "perception agent", "agent orchestration", "agent layers", "agent pipeline" |
| `ai-agents-threats` | "rogue actions", "acciones no autorizadas", "prompt injection agente", "indirect prompt injection", "sensitive data disclosure agent", "data exfiltration agent", "amenazas agente ia" |
| `ai-agents-security-design` | "secure agent design", "diseño seguro agente", "agent security principles", "least privilege agent", "agent observability", "agent permissions", "defense in depth agent", "agent guardrails", "human in the loop agent" |
| `saif-framework` | "saif", "saif map", "saif risks", "saif controls", "ai risk map", "mapa de riesgos ia", "framework seguridad ia", "google saif", "data poisoning saif", "ai risk assessment" |
