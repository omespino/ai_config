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

### Bug bounty — Google VRP (Ezequiel Pereira / bugSWAT)
- `bughunters-gae-rce` — GAE Host header injection to internal googleplex sites ($10k), /etc/passwd.borg LFI Java 8, $36k RCE via internal GAE APIs: stubby RPC to any Google server + app_config_service (quota/permissions/SuperApp/Google3 access). Staging env via Host: <PROJECT>.prom-nightly.sandbox.google.com. Internal endpoint 169.254.169.253:10001. Triggers: "google app engine rce", "gae rce", "appspot rce", "gae internal api", "stubby gcp", "app_config_service gae", "169.254.169.253", "gae staging env", "app engine host header", "gae host injection", "gae java interno".
- `bughunters-gsi` — Google Service Infrastructure hidden fields/methods via GOOGLE_INTERNAL visibility label. Detection — hidden field: JSON error vs silent ignore; hidden method: 404 JSON vs HTML broken-robot. Bug 1 — enable internal services via dependsOnServices ($5k). Bug 2 — enable any service + override limits via staging serviceConfig ($7.5k). Discovery via Cloud Console DevTools. Triggers: "google service infrastructure", "gsi gcp", "visibility labels google", "google_internal label", "servicemanagement api", "dependsonservices gcp", "enable internal service gcp", "esf google", "staging appengine sandbox googleapis", "service infrastructure bug".
- `bughunters-cloud-dm` — RCE in Google Cloud Deployment Manager via undocumented googleOptions field (gslbTarget/transport:GSLB) in v2beta/dogfood API. Redirects DM requests through internal GSLB to any blade: target, executing as cloud-dm-staging@prod.google.com. $164,674 total reward. Discovery via Cloud Console metrics + Proto over HTTP (application/x-protobuf) enum fuzzing. Triggers: "cloud deployment manager rce", "cloud dm rce", "gslbtarget gcp", "googleoptions deployment manager", "type provider gslb", "dogfood api gcp", "blade target gcp", "deploymentmanager v2beta", "gslb transport gcp", "deployment manager interno".

### Bug bounty — Microsoft VRP
- `bughunters-microsoft` — MSRC program, PPE environments (*.microsoft-ppe.com), MSAL.js token extraction, Swagger/OpenAPI exposure, unauthenticated AI agent endpoints, identity injection (roles/claims), Azure App Service hostname disclosure, React Fiber env switching. Real findings: Nova (storedeveloper) + Offers Copilot. Triggers: "microsoft bug bounty", "msrc", "microsoft ppe", "microsoft-ppe.com", "msal token", "azure ad clientid", "offers copilot microsoft", "nova microsoft store", "swagger microsoft ppe", "azure app service hostname", "microsoft ai agent unauth".

### Bug bounty — VRP report writing
- `vrp-report-template` — omespino's VRP report style: one-line Summary (product + vuln + impact), numbered Steps with sub-steps, concrete URLs/commands/output, brief Attack scenario. Anti-patterns, token verification commands, Google reward table. Triggers: "reporte vrp", "escribir reporte vrp", "formato reporte bug bounty", "template vrp google", "vrp report style", "reporte bug bounty google", "estructura reporte vrp".

### Bug bounty — Google VRP (community writeups)
- `bughunters-appsheet-ssrf` — SSRF en AppSheet Workflows/Bots vía webhook 301 redirect POST→GET → GCP metadata (169.254.169.254), robo de SA token vía logs. Por nechudav. Triggers: "appsheet ssrf", "appsheet webhook ssrf", "appsheet workflows ssrf", "webhook redirect ssrf", "post to get redirect ssrf", "301 redirect ssrf gcp", "nechudav appsheet".

### Bug bounty — Google VRP (HoF public research)
- `google-vrp-cloud` — GCP LB/CDN HTTP parser quirks, GitHub Actions pwn requests, GCS bucket squatting, GKE WIF, Zip Slip, Apigee sandbox, Composer RCE, Cloud Shell root. Triggers: "gcp", "cloud vrp", "gke", "firebase backend", "github actions google", "oss vrp", "cloud armor".
- `google-vrp-web` — XSS, OAuth misconfigs, SSRF, IDOR in Google web services (Drive, Docs, Gmail, YouTube, Workspace). Triggers: "google web xss", "oauth google", "drive docs gmail idor", "google vrp web".
- `google-vrp-android` — Android intent redirects, path traversal, Chrome extension UXSS, kernelCTF/v8CTF, Fuchsia/gVisor. Triggers: "android google", "mobile vrp", "chrome extension google", "kernelctf".

### Cloud infra (offensive + build)
- `gke-terraform-offensive` — GKE/GCP Terraform offensive: recon (public control plane, exposed tfstate), Terraform/tfstate attack surface (plaintext secrets, GCS backend, SA keys in CI), misconfig catalog (public CP, legacy ABAC, no Workload Identity, legacy metadata/kube-env, over-priv node SA, no NetworkPolicy/shielded nodes), attack chains (SSRF→169.254.169.254 node SA token, pod→cluster takeover, container escape, RBAC privesc, kube-env kubelet cert theft), GCP post-exploitation, + hardened private GKE build module. references/: misconfig-catalog, attack-playbook, audit-checklist (CIS), hardened-gke.tf. Triggers: "gke", "terraform gcp", "atacar gke", "gke misconfig", "tfstate expuesto", "workload identity", "metadata 169.254.169.254 gke", "node service account gke", "kube-env", "container escape gke", "rbac privesc", "cluster privado gke", "gke hardening".

### Recon
- `shodan-free` — Zero-credit commands: host, count, domain, honeyscore, InternetDB CIDR sweep. Triggers: "shodan host", "internetdb", "shodan sin créditos", "reconocimiento pasivo shodan", "shodan gratis".
- `shodan-advanced` — Filtered search, download/parse/convert, stats/facets, scan submit, alerts, REST API, Python. Triggers: "filtros shodan", "shodan download", "shodan scan", "shodan alerts", "shodan api", "shodan avanzado".
- `pentest-source-maps` — Source map extraction with sourcemapper, module-federation.manifest.json, recovery of TypeScript/JS source, secrets hunting (MSAL clientId, Google Maps key, Mapbox token, AWS), commented-out routes vs active backend endpoints, MSAL sessionStorage token extraction, API key permissions scripts (Google Maps + Mapbox). Triggers: "source map", "sourcemapper", "archivo .map", "module federation manifest", "reconstruir codigo fuente", "msal token sessionstorage", "api key mapbox permisos", "google maps key".
- `pentest-ssrf-redirect-server` — SSRF redirect server templates (PHP/Python/Node.js), 301/302/307 behavior, all cloud metadata endpoints (GCP/AWS/Azure), IP filter bypass table (IPv6 mapped, octal, decimal, CNAME), VPS setup, redirect chain. Triggers: "redirect server ssrf", "servidor de redirect ssrf", "php redirect ssrf", "python redirect ssrf", "script redirect 301", "redirect 302 ssrf", "metadata redirect", "ssrf vps redirect", "169.254.169.254 redirect", "redirect chain ssrf".

### AI Agent Security (SAIF 2.0 — Google, May 2025)
- `ai-agents-architecture` — Arquitectura completa de agentes IA: capas Application/Agent/Orchestration, componentes Perception, Reasoning Core, Rendering, Memory, Tools, RAG. Flujo de datos y security touchpoints por componente. Triggers: "arquitectura agente", "agent architecture", "reasoning core", "perception agent", "agent orchestration", "agent layers", "agent pipeline".
- `ai-agents-threats` — Modelo de amenazas completo para agentes IA: Rogue Actions (prompt injection directo/indirecto, misalignment), Sensitive Data Disclosure (data exfiltration via tool side-effects, output manipulation/XSS), catálogo de los 15 riesgos SAIF, attack scenarios library. Triggers: "rogue actions", "acciones no autorizadas", "prompt injection agente", "indirect prompt injection", "sensitive data disclosure agent", "data exfiltration agent", "agent threat model", "amenazas agente ia".
- `ai-agents-security-design` — Diseño seguro de agentes: 3 principios core (Human Controllers, Limited Powers, Observable Actions), controles (Agent User Controls, Agent Permissions con AAA dinámico, Agent Observability), defense-in-depth híbrido (Layer 1: runtime policy enforcement + Layer 2: reasoning-based defenses), assurance activities, security design checklist. Triggers: "secure agent design", "diseño seguro agente", "agent security principles", "least privilege agent", "agent observability", "agent permissions", "defense in depth agent", "agent guardrails", "human in the loop agent".
- `saif-framework` — Framework SAIF completo: 4 áreas (Data/Infrastructure/Model/Application), 15 riesgos del SAIF Risk Map con causas/impacto/mitigaciones/ejemplos reales, catálogo completo de ~22 controles organizados por dominio, AI development lifecycle security, risk self-assessment, alineación con NIST AI RMF. Triggers: "saif", "saif map", "saif risks", "saif controls", "ai risk map", "mapa de riesgos ia", "framework seguridad ia", "google saif", "data poisoning saif", "ai risk assessment".

## Memory Index

@/Users/user/ai_config/memory/MEMORY.md
