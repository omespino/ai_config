---
name: bughunters-appsheet-ssrf
description: 'Google VRP writeup by nechudav — SSRF in AppSheet Workflows (Bots) via webhook 301 redirect POST→GET conversion to reach GCP metadata service (169.254.169.254). Service account token exfiltration via webhook response logs. v1beta1 legacy API vs v1 (requires Metadata-Flavor header). Spanish triggers — "appsheet ssrf", "appsheet webhook ssrf", "appsheet workflows ssrf", "appsheet bots ssrf", "webhook redirect ssrf", "post to get redirect ssrf", "301 redirect ssrf gcp", "nechudav appsheet".'
---

## Report: SSRF en AppSheet Workflows vía redirect 301 (nechudav)

**Fuente:** https://nechudav.blogspot.com/2021/12/ssrf-vulnerability-in-appsheet-google.html
**Programa:** Google VRP — marcado como fixed
**Producto afectado:** AppSheet (adquisición de Google) — funcionalidad Workflows / Bots

---

### Resumen

AppSheet Workflows (ahora llamados "AppSheet Bots") permiten automatizar comportamiento de la aplicación mediante reglas disparadas por eventos. La funcionalidad de **webhooks** ejecuta peticiones HTTP salientes cuando se modifica una tabla de datos.

---

### Vector de ataque

El cliente HTTP de AppSheet convierte peticiones **POST en GET** cuando sigue redirecciones HTTP 301. Esta conversión es el núcleo del bypass.

**Cadena de redirect hacia metadata:**
```
POST http://<ATTACKER_DOMAIN>/computeMetadata/v1beta1/instance/service-accounts/default/token
    ↓  (servidor atacante responde 301)
GET http://169.254.169.254/computeMetadata/v1beta1/instance/service-accounts/default/token
```

**Configuración del Workflow (webhook):**
- Método disponible: POST, DELETE, PATCH (no GET directo)
- URL apunta al dominio del atacante con path que imita el endpoint de metadata
- Trigger: agregar nueva fila a la tabla de la aplicación

**Resultado:** el token de la service account de AppSheet aparece en los **logs del webhook** dentro de la aplicación.

---

### Bypass del parche parcial

Google parcheó deshabilitando el endpoint legacy `/v1beta1/`. El endpoint actual `/v1/` requiere el header `Metadata-Flavor: Google` en la petición GET resultante, lo que limitó el impacto post-patch.

| Endpoint | Requiere header | Status post-patch |
|---|---|---|
| `/computeMetadata/v1beta1/...` | No | Deshabilitado |
| `/computeMetadata/v1/...` | `Metadata-Flavor: Google` | Forbidden (sin header) |

---

### Técnica clave: POST→GET en redirect 301

Este comportamiento (RFC permitido pero peligroso) es un patrón recurrente en SSRF:

```
# Servidor atacante (cualquier lenguaje)
HTTP/1.1 301 Moved Permanently
Location: http://169.254.169.254/computeMetadata/v1beta1/instance/service-accounts/default/token
```

El cliente AppSheet convierte automáticamente el POST a GET al seguir el redirect — sin necesitar ningún header adicional para el endpoint v1beta1.

---

### Impacto

- Robo del **access token de la service account** de AppSheet
- Acceso a recursos GCP asociados a esa service account (alcance depende de los permisos del SA)
- Exfiltración via logs visibles dentro de la propia aplicación AppSheet del atacante

---

### Patrones de detección / checklist

- Cualquier funcionalidad de **webhook saliente** que permita apuntar a IPs arbitrarias
- Verificar si el cliente HTTP hace POST→GET en 301 (comportamiento RFC 2616, §10.3.2)
- Probar redirect a `169.254.169.254`, `metadata.google.internal`, `[::169.254.169.254]`
- Revisar si la respuesta del webhook se registra en logs visibles para el usuario
- Comparar comportamiento con 301 vs 302 (302 también puede triggear POST→GET en algunos clientes)

---

### Relación con otros reports

- Ver `bughunters-ssrf-gcp` para técnicas de bypass de IP (0.0.0.0, octal, IPv6 mapped)
- `google-vrp-cloud` #80 y #110 — AppSheet Apigee SSRF vía OpenAPI spec URL (vector diferente, mismo producto)
