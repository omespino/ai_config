# Global Agent Instructions

These instructions apply to every agent session (Claude, Codex, Gemini), regardless of working directory.
Source of truth: `~/ai_config/` — skills, memory and this file live there.

## User Profile and Rules

@/Users/user/ai_config/memory/user_profile.md

@/Users/user/ai_config/memory/feedback_language_style.md

@/Users/user/ai_config/memory/feedback_no_auto_requests.md

@/Users/user/ai_config/memory/feedback_use_ripgrep.md

## Engagement Rules

@/Users/user/ai_config/memory/reference_bugbounty_rules.md

@/Users/user/ai_config/memory/reference_pentest_rules.md

@/Users/user/ai_config/memory/reference_rdoc_review.md

@/Users/user/ai_config/memory/reference_google_bughunters_profile.md

@/Users/user/ai_config/memory/reference_google_vrp_rules.txt

## Skills (auto-discovered, trigger-based)

Skills live in `~/ai_config/skills/`. Each skill loads ONLY when its specific triggers match the context. Do NOT @-import them here — that defeats on-demand loading.

### Pentest skills (by domain)
- `pentest-ad` — Kerberoasting, SMB relay, LLMNR/Responder, NTLM coercion (PetitPotam), null auth, SMB shares. Triggers: "directorio activo", "kerberoasting", "smb relay", "responder", "llmnr", "petitpotam", "bloodhound", "impacket", "ntlm coercion".
- `pentest-mobile` — APK/IPA analysis, hardcoded secrets, debuggable flag, SQLite, SSL pinning bypass (Frida/objection). Triggers: "pentest móvil", "apk", "ipa", "frida", "mobsf", "ssl pinning", "jadx", "apktool", "debuggable", "objection".
- `pentest-web` — Info disclosure, clickjacking, SQLi (sqlmap), username enum, WordPress (wpscan), HTTP smuggling, S3 misconfig. Triggers: "pentest web", "sqli", "sqlmap", "clickjacking", "iis shortname", "wordpress", "wpscan", "http smuggling", "s3 misconfig".
- `pentest-network` — Credential exposure, CVEs (MSMQ/Dell/Struts/vCenter/Terrapin), deprecated TLS/SWEET32, SNMP/Redis/VNC/FTP/LDAP without auth. Triggers: "credenciales en claro", "default credentials", "tls 1.0", "sweet32", "snmp", "redis sin auth", "memcached", "vnc sin auth", "ftp anonimo", "nuclei cve", "wsus http", "terrapin".
- `pentest-biz-logic` — IDOR/BOLA, price manipulation, OTP/MFA bypass, rate limiting, ticket reuse, email DoS. Triggers: "idor", "bola", "lógica de negocio", "otp bypass", "mfa bypass", "rate limit", "price manipulation", "broken access control".
- `pentest-physical` — RFID cloning (Proxmark3), tailgating, flat network, VNC after physical access. Triggers: "pentest físico", "rfid", "proxmark", "tailgating", "red plana", "acceso físico".

### Bug bounty — platform skills
- `h1-bugbounty` — 43 HackerOne reports: SVG/XML XSS iOS, homoglyphs, SSRF webhooks, subdomain takeover, GitHub recon, Cisco ASA CVE, TLS/SSL. Triggers: "hackerone", "h1", "live hacking event", "lhe".
- `bugcrowd-bugbounty` — Resolved reports: Word .doc XSS iOS, Firebase APK, default creds network gear, email domain verification bypass, SVG XSS iOS, APK assets. Triggers: "bugcrowd", "bug bounty en bugcrowd".

### Bug bounty — Google VRP (personal reports omespino)
- `bughunters-cloud-shell` — Cloud Shell takeover chain: XSS (.md/SVG/filename) + LFI (file:// /files/) + container escape + SSH key exfil + root SSH. Triggers: "cloud shell google", "cloud shell xss", "devshell", "cloud shell takeover", "theia editor".
- `bughunters-apigee` — Apigee Node.js Hosted Target RCE as root via child_process.exec. Triggers: "apigee rce", "apigee hosted target", "apigee node.js", "apigee sandbox".
- `bughunters-ssrf-gcp` — Blind SSRF via Uptime Check (0.0.0.0 + redirect to [::169.254.169.254]) + SSRF AMP Validator → GCP metadata. Triggers: "uptime check ssrf", "gcp metadata ssrf", "amp validator ssrf", "0.0.0.0 ssrf", "ssrf gcp".
- `bughunters-debug-endpoints` — /procz LFI as root on Google infra (DremelGateway, springboard, UPI India, Mobile Harness), /flagz API keys, Google Fiber FTP/Telnet. Triggers: "procz flagz", "debug endpoints google", "dremelgateway", "springboard google", "labelaclz", "mobile harness server", "as15169".
- `bughunters-gmail-android` — Gmail Android email exfil via HTML attachment + content:// URI. Triggers: "gmail android", "content:// uri gmail", "gmail html attachment".
- `bughunters-earth` — Google Earth iOS KML XSS + geolocation; Pro Linux KML LFI (file:../etc/environment); Pro macOS null byte file read. Triggers: "google earth kml", "earth ios", "earth pro linux", "earth pro macos", "kml xss", "kml lfi".
- `bughunters-mobile-misc` — Chrome file:// LFI, Android TV IDOR sequential enum, PowerPoint 97-2003 XSS in Gmail/Drive iOS. Triggers: "chrome file://", "android tv idor", "powerpoint xss ios", "gmail ios xss", "ppt xss".

### Bug bounty — Google VRP (HoF public research)
- `google-vrp-cloud` — GCP LB/CDN HTTP parser quirks, GitHub Actions pwn requests, GCS bucket squatting, GKE WIF, Zip Slip, Apigee sandbox, Composer RCE, Cloud Shell root. Triggers: "gcp", "cloud vrp", "gke", "firebase backend", "github actions google", "oss vrp", "cloud armor".
- `google-vrp-web` — XSS, OAuth misconfigs, SSRF, IDOR in Google web services (Drive, Docs, Gmail, YouTube, Workspace). Triggers: "google web xss", "oauth google", "drive docs gmail idor", "google vrp web".
- `google-vrp-android` — Android intent redirects, path traversal, Chrome extension UXSS, kernelCTF/v8CTF, Fuchsia/gVisor. Triggers: "android google", "mobile vrp", "chrome extension google", "kernelctf".

### Recon
- `shodan-free` — Zero-credit commands: host, count, domain, honeyscore, InternetDB CIDR sweep. Triggers: "shodan host", "internetdb", "shodan sin créditos", "reconocimiento pasivo shodan", "shodan gratis".
- `shodan-advanced` — Filtered search, download/parse/convert, stats/facets, scan submit, alerts, REST API, Python. Triggers: "filtros shodan", "shodan download", "shodan scan", "shodan alerts", "shodan api", "shodan avanzado".

### AI Agent Security (SAIF 2.0 — Google, May 2025)
- `ai-agents-architecture` — Arquitectura completa de agentes IA: capas Application/Agent/Orchestration, componentes Perception, Reasoning Core, Rendering, Memory, Tools, RAG. Flujo de datos y security touchpoints por componente. Triggers: "arquitectura agente", "agent architecture", "reasoning core", "perception agent", "agent orchestration", "agent layers", "agent pipeline".
- `ai-agents-threats` — Modelo de amenazas completo para agentes IA: Rogue Actions (prompt injection directo/indirecto, misalignment), Sensitive Data Disclosure (data exfiltration via tool side-effects, output manipulation/XSS), catálogo de los 15 riesgos SAIF, attack scenarios library. Triggers: "rogue actions", "acciones no autorizadas", "prompt injection agente", "indirect prompt injection", "sensitive data disclosure agent", "data exfiltration agent", "agent threat model", "amenazas agente ia".
- `ai-agents-security-design` — Diseño seguro de agentes: 3 principios core (Human Controllers, Limited Powers, Observable Actions), controles (Agent User Controls, Agent Permissions con AAA dinámico, Agent Observability), defense-in-depth híbrido (Layer 1: runtime policy enforcement + Layer 2: reasoning-based defenses), assurance activities, security design checklist. Triggers: "secure agent design", "diseño seguro agente", "agent security principles", "least privilege agent", "agent observability", "agent permissions", "defense in depth agent", "agent guardrails", "human in the loop agent".
- `saif-framework` — Framework SAIF completo: 4 áreas (Data/Infrastructure/Model/Application), 15 riesgos del SAIF Risk Map con causas/impacto/mitigaciones/ejemplos reales, catálogo completo de ~22 controles organizados por dominio, AI development lifecycle security, risk self-assessment, alineación con NIST AI RMF. Triggers: "saif", "saif map", "saif risks", "saif controls", "ai risk map", "mapa de riesgos ia", "framework seguridad ia", "google saif", "data poisoning saif", "ai risk assessment".

## Memory Index

@/Users/user/ai_config/memory/MEMORY.md
