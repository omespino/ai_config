# GKE / GCP Terraform Misconfiguration Catalog

Resource-by-resource. For each: the insecure value, the secure value, and the exact offensive impact. Settings refer to the `hashicorp/google` provider.

---

## google_container_cluster

### master_authorized_networks_config
- **Insecure**: block absent, or `cidr_blocks` includes `0.0.0.0/0`.
- **Secure**:
  ```hcl
  master_authorized_networks_config {
    cidr_blocks { cidr_block = "203.0.113.10/32"; display_name = "bastion" }
    gcp_public_cidrs_access_enabled = false
  }
  ```
- **Impact**: public API server. `curl -sk https://<CP>/version` (version disclosure → CVE mapping), anonymous `/healthz`, exposes auth/token brute surface and any unauth API CVE.

### private_cluster_config
- **Insecure**: absent → nodes receive **public IPs**, control plane public.
- **Secure**:
  ```hcl
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = true
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }
  ```
- **Impact**: public node IPs are directly reachable — exposed kubelet (`10250` read-only/exec), NodePort services, SSH.

### enable_legacy_abac
- **Insecure**: `true`.
- **Secure**: `false` (default — assert it explicitly in audits).
- **Impact**: ABAC grants broad, hard-to-audit permissions that sit *underneath* RBAC; effectively bypasses least-privilege RBAC design.

### workload_identity_config  ← single most important control
- **Insecure**: absent.
- **Secure**: `workload_identity_config { workload_pool = "${var.project}.svc.id.goog" }` and per-pool node config `workload_metadata_config { mode = "GKE_METADATA" }`.
- **Impact (absent)**: every pod can read the **node's** SA token from `169.254.169.254`. One SSRF/RCE in any pod = node SA compromise. Enabling WI inserts the `gke-metadata-server` which only hands a pod its bound GCP SA, not the node SA.

### network_policy / datapath_provider
- **Insecure**: `network_policy { enabled = false }` and default datapath.
- **Secure**: `datapath_provider = "ADVANCED_DATAPATH"` (Dataplane v2) or `network_policy { enabled = true; provider = "CALICO" }`.
- **Impact**: no east-west segmentation; a compromised pod reaches every other pod/service (DBs, internal APIs, metadata of neighbors).

### release_channel
- **Insecure**: absent + pinned old `min_master_version`.
- **Secure**: `release_channel { channel = "REGULAR" }`.
- **Impact**: stale control plane / kubelet → unpatched CVEs.

### enable_shielded_nodes
- **Insecure**: `false`.
- **Secure**: `true` (+ per-node `shielded_instance_config`).
- **Impact**: no secure boot / integrity monitoring → bootkit/rootkit persistence on nodes survives.

### binary_authorization
- **Insecure**: disabled.
- **Secure**: `binary_authorization { evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE" }`.
- **Impact**: arbitrary/unsigned images run → supply-chain and tampered-image execution.

---

## google_container_node_pool / node_config

### service_account
- **Insecure**: omitted → uses the **default Compute Engine SA** (`<num>-compute@developer.gserviceaccount.com`), historically `roles/editor`.
- **Secure**: dedicated minimal SA (see hardened module).
- **Impact**: node SA token (via 4.1) = project Editor. Full read/write of compute, storage, secrets — effectively project takeover.

### oauth_scopes
- **Insecure**: `["https://www.googleapis.com/auth/cloud-platform"]`.
- **Secure**: drop to logging/monitoring/AR-read; rely on IAM not scopes.
- **Impact**: even a low-IAM SA with `cloud-platform` scope has full API breadth bounded only by IAM — widens blast radius.

### metadata (disable-legacy-endpoints / kube-env)
- **Insecure**: `metadata = { disable-legacy-endpoints = "false" }`.
- **Secure**: `metadata = { disable-legacy-endpoints = "true" }`.
- **Impact**: `v1beta1` metadata served **without** the `Metadata-Flavor: Google` header → header-less SSRF reaches the token endpoint. Legacy `kube-env` attribute exposes `KUBELET_CERT/KEY` → impersonate `system:node:*`.

### shielded_instance_config
- **Insecure**: `enable_secure_boot = false`, `enable_integrity_monitoring = false`.
- **Secure**: both `true`.

### image_type
- **Insecure**: `UBUNTU` with extra packages / docker.
- **Secure**: `COS_CONTAINERD` (Container-Optimized OS, read-only rootfs, smaller surface).

---

## Terraform state & secret resources

### backend "gcs"
- **Insecure**: state bucket with broad IAM or `allUsers`/`allAuthenticatedUsers` read; no uniform bucket-level access.
- **Secure**: dedicated bucket, `uniform_bucket_level_access = true`, versioning, CMEK, IAM limited to the CI SA; never public.
- **Impact**: readable state bucket = **full plaintext credential dump** (see below).

### kubernetes_secret / random_password / google_service_account_key
- These resources **store their value verbatim in state**, regardless of `sensitive = true` (which only hides it from CLI output, not from the state file).
- **Impact**: anyone who reads `terraform.tfstate` gets every k8s Secret, generated password, and SA private key in cleartext.
- **Defense**: avoid `google_service_account_key` entirely (use Workload Identity / WIF); keep secrets in Secret Manager referenced by data sources, not created in TF; lock down the state bucket as the real boundary.

---

## Quick audit grep (read-only, local repo)
```
rg -n "enable_legacy_abac\s*=\s*true" .
rg -n "0\.0\.0\.0/0" .
rg -n "disable-legacy-endpoints\s*=\s*\"false\"" .
rg -n "cloud-platform" .
rg -n "google_service_account_key" .
rg -nL "workload_identity_config" --glob '*.tf'   # files MISSING WI
rg -n "backend\s+\"gcs\"" .
```
