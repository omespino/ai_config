# GKE Audit Checklist (CIS GKE Benchmark-aligned)

For pentest reports. Each item: what to verify, how (`gcloud`/`kubectl`/Terraform), CIS ref, and the finding if it fails. Rate findings CVSS v3.1.

---

## Control plane
| # | Check | Command / TF | CIS | Fail = finding |
|---|---|---|---|---|
| 1 | Private endpoint enabled | `privateClusterConfig.enablePrivateEndpoint=true` | 5.6.4 | Public control plane exposed |
| 2 | Authorized networks restricted | `masterAuthorizedNetworksConfig` ≠ `0.0.0.0/0` | 5.6.3 | API server reachable from Internet |
| 3 | Legacy ABAC disabled | `legacyAbac.enabled=false` | 5.8.4 | Overly broad authorization |
| 4 | Up-to-date version / release channel | `releaseChannel.channel` set | 5.5.x | Unpatched CVEs |
| 5 | Binary Authorization | `binaryAuthorization.evaluationMode` enforce | 5.10.x | Unsigned images run |

## Nodes
| # | Check | Command / TF | CIS | Fail = finding |
|---|---|---|---|---|
| 6 | Private nodes (no public IP) | `privateClusterConfig.enablePrivateNodes=true` | 5.6.5 | Nodes Internet-reachable |
| 7 | Dedicated minimal node SA | `nodeConfig.serviceAccount` ≠ default Compute SA | 5.2.1 | Node SA = project Editor |
| 8 | Restricted OAuth scopes | `nodeConfig.oauthScopes` ≠ `cloud-platform` | 5.2.x | Over-broad API scope |
| 9 | Legacy metadata disabled | `metadata.disable-legacy-endpoints=true` | 5.4.1 | Header-less metadata SSRF / kube-env theft |
| 10 | Shielded nodes | `shieldedInstanceConfig` secure boot + integrity | 5.5.x | Boot tampering / rootkit |
| 11 | COS_CONTAINERD image | `nodeConfig.imageType` | 5.5.1 | Larger node attack surface |
| 12 | Metadata concealment / WI metadata | `workloadMetadataConfig.mode=GKE_METADATA` | 5.4.x | Pods reach node SA token |

## Identity & RBAC
| # | Check | Command / TF | CIS | Fail = finding |
|---|---|---|---|---|
| 13 | Workload Identity enabled | `workloadIdentityConfig.workloadPool` set | 5.2.2 | SSRF/RCE → node SA compromise |
| 14 | No cluster-admin to broad subjects | `kubectl get clusterrolebindings -o wide` | 5.7.x | Excess privilege |
| 15 | SA token automount off by default | pod/SA `automountServiceAccountToken=false` | 5.1.5/6 | Token theft on pod compromise |
| 16 | Pod Security Admission `restricted` | namespace labels | 5.2.x | Privileged/hostPath pods allowed |

## Network
| # | Check | Command / TF | CIS | Fail = finding |
|---|---|---|---|---|
| 17 | NetworkPolicy / Dataplane v2 | `networkPolicy.enabled` or `ADVANCED_DATAPATH` | 5.6.7 | No east-west segmentation |
| 18 | No public NodePort / LB exposure | `kubectl get svc -A` | — | Unintended exposure |

## Secrets / state
| # | Check | Command / TF | Fail = finding |
|---|---|---|---|
| 19 | Application-layer secret encryption (CMEK) | `databaseEncryption.state=ENCRYPTED` | etcd secrets at rest |
| 20 | State bucket locked down | GCS uniform access, no `allUsers`, versioning, CMEK | Plaintext credential dump |
| 21 | No `google_service_account_key` in TF | `rg google_service_account_key` | Long-lived leakable keys |
| 22 | Secrets not stored in TF state | `kubernetes_secret`/`random_password` in state | Plaintext secrets in state |

---

## One-shot posture dump
```bash
gcloud container clusters describe <CLUSTER> --zone <ZONE> --format=json \
| jq '{private:.privateClusterConfig, authNets:.masterAuthorizedNetworksConfig, netpol:.networkPolicy, wi:.workloadIdentityConfig, abac:.legacyAbac, channel:.releaseChannel, ver:.currentMasterVersion, nodeSA:.nodeConfig.serviceAccount, scopes:.nodeConfig.oauthScopes, meta:.nodeConfig.metadata, shielded:.nodeConfig.shieldedInstanceConfig, dbEnc:.databaseEncryption}'
```
