---
name: feedback-spa-scraping
description: SPAs Angular/React sirven docs como archivos .md/.json estáticos — extraer la estructura del bundle JS en lugar de usar Playwright para renderizar.
metadata:
  type: feedback
---

Cuando un sitio de documentación es una SPA (Angular, React, Vue) y `html2text`/`curl` devuelven contenido vacío, el contenido real suele estar en archivos estáticos servidos por JS.

**Regla:** Antes de instalar Playwright o un headless browser, inspeccionar el bundle JS principal para encontrar las rutas de los assets estáticos.

**Why:** En `antigravity.google`, el SPA Angular cargaba docs desde `/assets/docs/{path}/{slug}.md`. El array `DOCS_STRUCTURE` estaba embebido en `main-SUIVHLSS.js` y contenía todos los paths. Descargar los `.md` directamente fue instantáneo y no requirió renderizado JS.

**How to apply:**
1. Si `html2text` o `curl` devuelven HTML vacío con `<app-root>` o similar → SPA confirmado.
2. Descargar el bundle JS principal (`main-*.js`, `app-*.js`, etc.) desde el HTML.
3. Buscar en el bundle patrones como `DOCS_STRUCTURE`, `routes`, `pages`, `slug:`, `path:` para encontrar la estructura de contenido.
4. Buscar el patrón `fetch('/assets/...')` o `import('...')` para encontrar dónde viven los assets.
5. Una vez identificadas las rutas, descargar los archivos directamente con `curl`.

**Herramienta de búsqueda en el bundle:**
```bash
curl -s --compressed <bundle-url> | python3 -c "
import sys, re
c = sys.stdin.read()
# Buscar estructura de docs
m = re.search(r'DOCS_STRUCTURE=(\[.*?\]);', c)
if m: print(m.group(1)[:2000])
"
```
