---
name: bughunters-cloud-dm
description: 'Google VRP report by Ezequiel Pereira — RCE in Google Cloud Deployment Manager via undocumented googleOptions field in v2beta/dogfood API. transport:GSLB redirects DM requests through internal GSLB to any blade: target. Requests execute as cloud-dm-staging@prod.google.com. $31,337 reward + $133,337 VRP prize = $164,674 total. Discovery — undocumented API versions (alpha/dogfood) found via Cloud Console metrics; Proto over HTTP (application/x-protobuf) in staging used to reverse-engineer hidden protobuf enum values. Spanish triggers — "cloud deployment manager rce", "cloud dm rce", "gslbtarget gcp", "googleoptions deployment manager", "type provider gslb", "dogfood api gcp", "blade target gcp", "deploymentmanager v2beta", "gslb transport gcp", "deployment manager interno".'
---

## RCE en Google Cloud Deployment Manager (Ezequiel Pereira, 2020)

**Reward:** $31,337 (mayo 2020) + $133,337 VRP prize (marzo 2021) = **$164,674 total**

**Servicio afectado:** Cloud Deployment Manager v2beta / dogfood API  
`deploymentmanager.googleapis.com`

---

### Descubrimiento de versiones de API no documentadas

Las versiones `alpha`, `dogfood` y `staging` se descubren mirando las métricas del Google Cloud Console — el frontend hace requests a estas versiones que no aparecen en la documentación pública.

```
GET /deploymentmanager/dogfood/projects/{PROJECT}/global/types
```

Esta llamada al dogfood API revela los "base types" internos, que exponen el campo `googleOptions` en las configuraciones de Type Provider.

---

### Campo `googleOptions` — el vector principal

El dogfood API exponía un campo no documentado `googleOptions` en Type Provider configs con los siguientes sub-campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `gslbTarget` | String | Formato `blade:<TARGET>` o `gslb:<TARGET>` |
| `descriptorUrlServerSpec` | String | Target spec para el descriptor |
| `transport` | Enum | Incluye valor oculto `GSLB` |
| `credentialType` | Enum | `GAIAMINT`, `ENDUSERCREDS` |
| `injectProject` | Bool | — |
| `deleteIntent` | Bool | — |
| `isLocalProvider` | Bool | — |
| `ownershipKind` | Enum | — |

El valor clave es `transport: GSLB` — redirige los requests de Deployment Manager a través del Global Service Load Balancer interno de Google.

---

### Explotación paso a paso

**Paso 1 — Enumerar targets GSLB internos**

Al listar los base types del dogfood API, la respuesta contiene referencias a targets `blade:` internos. Estos son los mismos identificadores que se usan internamente en Google para direccionar servicios.

**Paso 2 — Crear un Type Provider malicioso**

```json
POST /deploymentmanager/v2beta/projects/{PROJECT}/global/typeProviders

{
  "name": "my-type-provider",
  "options": {
    "googleOptions": {
      "gslbTarget": "blade:apphosting-admin-nightly",
      "descriptorUrlServerSpec": "blade:apphosting-admin-nightly",
      "transport": "GSLB"
    }
  },
  "descriptorUrl": "https://target-api.googleapis.com/$discovery/rest"
}
```

Ejemplos de targets internos válidos:
- `blade:apphosting-admin-nightly` → App Engine Admin API (test env)
- `blade:corp-issuetracker-api` → issuetracker.corp.googleapis.com
- Cualquier servidor interno de Google accesible via GSLB

**Paso 3 — Triggear el descriptor fetch**

```
POST /deploymentmanager/v2beta/projects/{PROJECT}/global/typeProviders/{TP}/listTypes
```

La operación asíncrona intenta obtener el descriptor del endpoint interno. La respuesta revela el schema de la API interna o errores con stack traces marcados como "Debugging information, only visible to internal IPs."

**Paso 4 — Llamar APIs internas**

Con el Type Provider configurado, se pueden hacer llamadas a las APIs internas del target. Los requests se ejecutan con las credenciales de:
```
cloud-dm-staging@prod.google.com
```
Este service account tiene acceso delegado a recursos internos de Google, lo que permitiría bypassear controles de acceso.

---

### Técnica — Proto over HTTP para reverse engineering

En el staging environment, el API acepta:
```
Content-Type: application/x-protobuf
```

Esto permite comparar respuestas JSON vs binario protobuf para reverse-engineer los field numbers de mensajes protobuf no documentados, descubriendo enum values ocultos como `GSLB` en el campo `transport`.

Metodología:
1. Enviar request JSON normal → anotar campos conocidos
2. Enviar mismo request con `Content-Type: application/x-protobuf`
3. Comparar encoding binario para inferir field numbers
4. Fuzz valores de enums con field numbers descubiertos → encontrar `GSLB`

---

### Impacto real demostrado

**Acceso a App Engine Admin API (test env):**
- Deployar aplicaciones en el environment GAE de pruebas (bloqueado externamente desde 2018)
- Target: `test.apphosting.sandbox.googleapis.com`

**Acceso a Issue Tracker Corp:**
- Obtener schema completo via `listTypes` 
- Target: `blade:corp-issuetracker-api` → `issuetracker.corp.googleapis.com`

**Information disclosure:**
- Targets GSLB inválidos devuelven páginas de error internas con Java stack traces
- Confirmación de existencia de servicios internos via respuestas de error diferenciadas

---

### Pattern generalizable

1. **Buscar versiones de API no documentadas** — `alpha`, `dogfood`, `staging`, `internal` — via Cloud Console DevTools o enumeración directa
2. **Listar base types / schemas del API interno** — frecuentemente exponen campos con `GOOGLE_INTERNAL` visibility o campos completamente ausentes de docs públicas
3. **Fuzz enum values** — crear recursos repetidamente cambiando el valor del enum; error diferente = valor oculto existe
4. **Proto over HTTP como herramienta de recon** — si el staging acepta `application/x-protobuf`, usar para mapear field numbers de mensajes ocultos
5. **Type Providers en DM como SSRF vector** — cualquier servicio que permita especificar un target externo para "fetch descriptor" es un potencial SSRF → si acepta `blade:` o `gslb:` targets → acceso a infra interna

---

### Timeline
- **7 mayo 2020** — descubrimiento y reporte via VRP grant
- **8 mayo 2020** — escalado a P0 en 5 minutos
- **19 mayo 2020** — $31,337 reward
- **20 mayo 2020** — fix confirmado (`gslbTarget`/`descriptorUrlServerSpec` ignorados)
- **Marzo 2021** — $133,337 VRP prize adicional por write-up
