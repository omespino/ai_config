---
name: shodan-advanced
description: Shodan advanced features requiring API key and credits: filtered search (1 credit/query), download + parse + convert results, statistics/facets, on-demand scanning (shodan scan submit, 1 credit/IP), network monitoring alerts (create/list/enable/stream), REST API and Python library usage. Full filter reference: net, org, product, version, os, http.title, ssl.cert, vuln (paid), has_screenshot (paid). Common search queries for databases, cameras, industrial systems, default passwords, vulnerable RDP. Spanish triggers — "filtros shodan", "shodan download", "shodan search avanzado", "shodan scan", "shodan alerts", "shodan api", "shodan créditos", "shodan monitor", "shodan facets", "shodan python", "shodan vuln filter", "shodan filtrar por org", "buscar servicios expuestos shodan".
---

## Shodan — Advanced / Credits Features

**Rule:** present any command that consumes credits or contacts target IPs before running. Wait for explicit approval (per `feedback_no_auto_requests.md`).

---

## Filtered Search (1 credit per query)
```bash
shodan search 'product:mongodb'
shodan search 'product:nginx country:US city:"New York"'
shodan search --fields ip_str,port,os smb
```

**Filter reference:**
```
# Network
net:192.168.0.0/24    ip:1.2.3.4    hostname:example.com    asn:AS15169    port:22

# Geo
country:US   city:"San Francisco"   state:CA   postal:94102

# Service
product:nginx   version:1.14.0   os:"Windows Server 2019"
http.title:"Dashboard"   http.html:"login"   http.status:200
http.component:wordpress   ssl.cert.subject.cn:*.example.com
ssl.cert.expired:true   ssl:true   tag:cloud

# Vuln (Small Business plan+)
vuln:CVE-2019-0708   has_vuln:true

# Screenshots (Freelancer plan+)
has_screenshot:true   screenshot.label:webcam
```

**Negation:** `-port:443` (exclude), `+port:80` (require), `"exact phrase"`

---

## Download + Parse + Convert
```bash
# Download (1 credit per 100 results)
shodan download results.json.gz "apache country:US"
shodan download --limit 5000 results.json.gz "nginx"
shodan download --limit -1 all.json.gz "query"   # all available

# Parse
shodan parse --fields ip_str,port,hostnames results.json.gz
shodan parse --fields ip_str,port,org --separator , results.json.gz > out.csv

# Convert
shodan convert results.json.gz csv
shodan convert results.json.gz xlsx
shodan convert results.json.gz kml    # Google Earth
```

---

## Statistics / Facets (1 credit)
```bash
shodan stats nginx
shodan stats --facets domain,port,asn --limit 5 nginx
shodan stats --facets country,org -O stats.csv apache
```
Common facets: `country, org, port, product, version, vuln, domain, asn, city, ssl.version, http.component, tag`

---

## On-Demand Scanning (1 credit/IP — active probing, always confirm first)
```bash
shodan scan submit 192.0.2.10
shodan scan list
shodan scan status SCAN_ID
shodan scan protocols            # ~80+ scanner modules
shodan download --limit -1 results.json.gz "scan:SCAN_ID"
```
Cannot re-scan same IP within 24h (non-Enterprise).

---

## Network Monitoring / Alerts
```bash
shodan alert create "engagement-1" 192.0.2.0/24
shodan alert list
shodan alert triggers
shodan alert enable ALERT_ID new_service
shodan alert enable ALERT_ID vulnerable
shodan alert enable ALERT_ID open_database
shodan stream --alert ALERT_ID    # real-time stream
shodan alert remove ALERT_ID
```

---

## REST API + Python
```bash
# Direct API
curl -s "https://api.shodan.io/shodan/host/1.1.1.1?key=YOUR_KEY" | jq
curl -s "https://api.shodan.io/shodan/host/search?key=YOUR_KEY&query=apache" | jq
curl -s "https://api.shodan.io/dns/domain/example.com?key=YOUR_KEY" | jq
```

```python
import shodan
api = shodan.Shodan('YOUR_API_KEY')
results = api.search('apache')
for r in results['matches']:
    print(r['ip_str'], r['port'])
```

---

## Common Search Queries
| Purpose | Query |
|---|---|
| MongoDB databases | `product:mongodb` |
| Redis (no auth) | `product:redis` |
| Elasticsearch | `product:elastic port:9200` |
| Open VNC | `port:5900 "authentication disabled"` |
| Anonymous FTP | `"230 Login successful" port:21` |
| Jenkins | `"X-Jenkins" port:8080` |
| Exposed Docker API | `port:2375 product:docker` |
| WordPress | `http.component:wordpress` |
| Exposed K8s API | `product:"kubernetes" port:6443` |
| Vulnerable RDP (paid) | `port:3389 vuln:CVE-2019-0708` |
| Log4Shell candidates (paid) | `vuln:CVE-2021-44228` |
| SSL cert search | `ssl.cert.subject.cn:*.target.com` |
| Self-signed certs | `ssl.cert.issuer.cn:self-signed` |

---

## Org recon workflow
```bash
shodan download target.json.gz 'org:"Target Company"'
shodan parse --fields ip_str,port,product target.json.gz
shodan stats --facets port,product,country 'org:"Target Company"'
```

## Troubleshooting
| Issue | Solution |
|---|---|
| `Query credits exhausted` | Use free commands (host, count, domain, InternetDB) |
| `country:"United States"` returns 0 | Use `country:US` (ISO-2 only) |
| `vuln:` returns 0 | Requires Small Business plan; use InternetDB `vulns` field instead |
| Rate-limited | Add `time.sleep(1)` between API requests |
