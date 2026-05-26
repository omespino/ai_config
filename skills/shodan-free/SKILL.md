---
name: shodan-free
description: 'Shodan free/zero-credit commands for passive recon. Commands that cost 0 credits and require no API key or Membership: shodan host (full host record), shodan count (result count with filters), shodan domain (subdomain + DNS dump), shodan honeyscore (honeypot probability), InternetDB API (internetdb.shodan.io, no key, CIDR sweeps with xargs -P). Also covers CLI setup (shodan init, shodan info). Spanish triggers — "shodan host", "internetdb", "shodan dominio", "shodan sin créditos", "reconocimiento pasivo shodan", "shodan gratis", "shodan passivo", "shodan count", "internetdb shodan", "shodan honeyscore".'
---

## Shodan — Free / Zero-Credit Commands

**Important:** propose any command that touches a target IP/domain before running (per `feedback_no_auto_requests.md`). Free Shodan commands are passive and generally safe, but still confirm first.

---

## Setup
```bash
pip install shodan
shodan init YOUR_API_KEY
shodan info    # shows credits: Membership = 100/100; free signup = 0/0
shodan myip    # your external IP
```

---

## Free commands (0 credits, no key needed for some)

### `shodan host` — full host record
```bash
shodan host 1.1.1.1
```
Returns: hostnames, country, org, open ports, banners (from last crawl).

### `shodan count` — count results (even filtered = 0 credits)
```bash
shodan count openssh
shodan count 'product:nginx country:US'
```
Size a result set before paying for download.

### `shodan domain` — subdomain + DNS dump
```bash
shodan domain example.com
```
Returns all subdomains Shodan knows + A/AAAA/MX/NS records. Best free surface enumeration.

### `shodan honeyscore` — honeypot probability
```bash
shodan honeyscore 192.168.1.100
# Returns float 0.0 (not honeypot) to 1.0 (likely honeypot)
# Treat > 0.5 as suspicious
```

### InternetDB — free, no API key, no credits
```bash
curl -s https://internetdb.shodan.io/1.1.1.1 | jq
```
Returns: ports, hostnames, vulns, tags, CPEs. Ideal for CIDR sweeps.

**Parallel CIDR sweep (no auth, no rate-limit signaling):**
```bash
seq 1 254 | xargs -P 20 -I {} \
  curl -s "https://internetdb.shodan.io/192.0.2.{}" \
  | jq -c '{ip, ports, vulns, hostnames}' \
  | tee internetdb_sweep.jsonl
```

---

## Free passive recon workflow (0 cost)
```bash
shodan domain target.com                          # subdomains
shodan count 'org:"Target Company"'               # surface size
shodan host <IP>                                  # per-IP details
curl -s https://internetdb.shodan.io/<IP> | jq   # quick vuln check
```

---

## Credit system reference
| Command | Cost |
|---|---|
| `shodan host`, `shodan count`, `shodan domain`, `shodan honeyscore`, `internetdb` | **0** |
| `shodan search` (no filter) | 0 |
| `shodan search` (with filter) | 1 query credit |
| `shodan download` per 100 results | 1 query credit |
| `shodan scan submit` per IP | 1 scan credit |
| `shodan stats` | 1 query credit |
