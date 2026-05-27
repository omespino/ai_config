---
name: ai-agents-architecture
description: Arquitectura completa de agentes de IA — capas Application/Agent/Orchestration, componentes Perception, Reasoning Core, Rendering, Memory, Tools, RAG, flujo de datos y puntos de seguridad en cada etapa. Basado en SAIF 2.0 y whitepaper Google May 2025. Triggers — "arquitectura agente", "agent architecture", "componentes agente", "agent components", "reasoning core", "perception agent", "rendering agent", "agent memory", "agent orchestration", "tool use agent", "rag agent", "agent layers", "capas agente ia", "agent workflow", "agent pipeline".
---

## Source
Google SAIF 2.0 — Focus on Agents (saif.google/focus-on-agents)
Google Whitepaper: "Google's Approach for Secure AI Agents: An Introduction" (May 2025) — Santiago Díaz, Christoph Kern, Kara Olive

---

## Agent Architecture Overview

Three logical layers (Figure 1 del whitepaper):

```
User Interaction
      ↕
┌─────────────────────────────────────┐  ← Application layer
│              Application            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐  ← Agent layer
│  Perception          Rendering      │
│  ┌────────────────┐                 │
│  │System instruct.│                 │
│  │User query det. │                 │
│  └───────┬────────┘                 │
│          ↓                          │
│       Reasoning Core                │
│       ┌──────────┐                  │
│       │ Model(s) │  LLM planning    │
│       └────┬─────┘                  │
└────────────┼────────────────────────┘
             │ (iterative reasoning loop)
┌────────────▼────────────────────────┐  ← Orchestration layer
│ Content(RAG)  Agent memory  Models  │
│                  Tools              │
└─────────────────────────────────────┘
```

---

## Layer 1: Application

**Function:** Interface principal entre el usuario y el agente.

- Recibe **instrucciones explícitas del usuario** (sync: comando directo | async: evento desencadena la acción automáticamente)
- Recibe **inputs contextuales implícitos** — datos pasivamente recolectados del entorno (lecturas de sensores, estado de la app, documentos abiertos recientemente)

**Security implication:**
- Crítico: distinguir instrucciones del usuario de confianza vs datos contextuales no confiables
- Fallo aquí → prompt injection desde el entorno (un email, una página web, un documento)
- Agentes asíncronos: el usuario puede no estar presente para supervisar → riesgo mayor

**Questions to consider:**
- ¿Qué tipos de inputs procesa el agente y puede distinguir los de confianza de los contextuales?
- ¿Actúa síncronamente (user presente) o asíncronamente (user ausente)?
- ¿El usuario puede inspeccionar, aprobar y revocar permisos de acciones, memoria y personalizaciones?
- En multi-usuario: ¿cómo sabe el agente qué usuario da instrucciones y mantiene memoria aislada?

---

## Layer 2: Agent — Perception

**Function:** Input transformation — procesa y comprende inputs antes de enviarlos al Reasoning Core.

### Sub-components:

**System Instructions**
- Definen las capacidades, permisos y límites del agente (qué acciones puede tomar, qué tools puede usar)
- **Security:** Deben estar claramente delimitadas y separadas de los datos del usuario
- Usar tokens de control especiales para prevenir prompt injection
- Separation es crítica: datos del usuario pueden contener instrucciones falsas que mezclan con las reales

**User Query Details**
- Los detalles específicos de la petición del usuario, post-procesados
- Se combinan con system instructions y datos contextuales (agent memory, external info) para formar el prompt estructurado al reasoning core

**Security implication at Perception:**
- El handoff Perception → Reasoning Core es la junctura de seguridad más crítica
- Debe distinguir confiablemente: instrucciones del usuario controlador vs datos no confiables externos
- Fallo → el reasoning core opera con instrucciones adversariales como si fueran legítimas

---

## Layer 2: Agent — Reasoning Core

**Function:** El cerebro del agente. Procesa el prompt estructurado (system instructions + user query + context), razona sobre el objetivo y genera un plan de acciones.

- Generalmente uno o más LLMs (puede haber LLM separado para reasoning y para planning)
- Planning es **iterativo**: "reasoning loop" — el plan se refina con nueva información o resultados de acciones previas
- Genera secuencias de acciones / tool calls que permiten al agente afectar el mundo real

**Security implications:**
- LLM planning es **probabilístico** e inherentemente impredecible y propenso a errores de interpretación
- Arquitecturas LLM actuales NO proveen separación rigurosa entre partes del prompt (system vs user vs external)
- El reasoning loop iterativo **compone vulnerabilidades**: cada ciclo introduce oportunidades de lógica errónea, divergencia de intent, o hijacking por datos maliciosos
- Agentes de alta autonomía con planning multi-step complejo → riesgo significativamente mayor

**Questions to consider:**
- ¿Cómo maneja el agente instrucciones ambiguas o conflictivas? ¿Puede pedir clarificación?
- ¿Qué nivel de autonomía tiene en planning? ¿Hay constrains en complejidad o longitud del plan?
- ¿Requiere confirmación del usuario antes de ejecutar acciones de alto riesgo o irreversibles?

---

## Layer 2: Agent — Rendering

**Function:** Output transformation — toma el output generado por el agente y lo formatea para visualización en la app del usuario (browser, mobile app).

- Agentes generalmente producen en formato universal (Markdown) → interpretado y renderizado por el cliente
- Si el output no es sanitizado correctamente según el content type → vulnerabilidades graves

**Security implications:**
- Output sin sanitizar → data exfiltration (URLs crafted), XSS (Cross-Site Scripting)
- Imagen en Markdown con URL maliciosa → exfiltración de datos cuando se fetcha la imagen
- El rendering es el **boundary final** entre contenido dinámico del agente y el contexto confiable de la app del usuario

**Questions to consider:**
- ¿Cómo se aísla la memoria del agente entre usuarios para prevenir data leakage?
- ¿Qué detiene inputs maliciosos almacenados (prompt injections) de causar daño persistente?
- ¿Qué procesos de sanitización se aplican al renderizar output para prevenir XSS?
- ¿Cómo se valida el output renderizado (URLs generadas, contenido embebido) para prevenir SDD?

---

## Layer 3: Orchestration

**Function:** Gestiona y coordina los servicios y fuentes de datos externos que el agente necesita para completar tareas.

### Sub-components:

**Agent Memory**
- Permite al agente retener contexto y aprender hechos entre interacciones
- Tipos: short-term (contexto de sesión), long-term (facts persistidos entre sesiones), episodic, procedural
- **Security:** Si datos maliciosos se almacenan en memoria → persistent attacks (el agente actúa diferente en futuras interacciones no relacionadas)
- Requiere aislamiento estricto entre usuarios y potencialmente entre contextos del mismo usuario

**Tools**
- APIs y servicios externos que el agente usa para actuar en el mundo
- Pueden incluir: envío de emails, queries a DBs, acceso a file systems, control de dispositivos, interacción con browser elements, compras
- **Security:** Riesgo de deceptive tool descriptions en tools de terceros → engañan al agente para ejecutar funciones no intencionadas
- Acceso no controlado a tools con poderes altos → impacto masivo si el planning está comprometido
- Requiere: autenticación robusta, autorización, least-privilege por tool y por tarea

**Content (RAG) — Retrieval-Augmented Generation**
- Provee al agente con conocimiento curado para fundamentar sus respuestas
- **Security:** Data poisoning — si el atacante corrompe la fuente de conocimiento → manipula el output del agente

**Auxiliary Models (opcional)**
- Modelos AI adicionales independientes del reasoning core (ej: clasificadores de seguridad/safety)
- Como parte del AI supply chain → tienen sus propias vulnerabilidades explotables para atacar el sistema agentico mayor
- Ej: un safety classifier comprometido que deja pasar acciones maliciosas

**Security implications at Orchestration:**
- Orchestration es donde rogue plans se traducen en **impacto real en el mundo**
- Tool use sin control → delete files, purchases, data transfer, settings changes en medical devices
- Nuevas tools (especialmente third-party) → deceptive descriptions o implementaciones inseguras

**Questions to consider:**
- ¿El conjunto de acciones disponibles está claramente definido? ¿Los usuarios pueden inspeccionar y dar consent?
- ¿Cómo se identifican acciones de consecuencias severas y se someten a controles específicos?
- ¿Qué salvaguardas (sandboxing, user controls, sensitive deployment exclusions) previenen que el agente exponga capacidades de alto privilegio en contextos de bajo privilegio?

---

## Security Touchpoints Summary

| Component | Primary Risk | Key Control |
|---|---|---|
| Application | Prompt injection desde entorno | Input boundary enforcement, trust distinction |
| Perception (System instr.) | Mezcla de instrucciones vs datos | Delimiters, control tokens |
| Perception (User query) | Datos adversariales como instrucciones | Input validation, sanitization |
| Reasoning Core | Hijacking del plan, misalignment | Adversarial training, guard models |
| Rendering | XSS, data exfiltration via output | Output sanitization, content-type validation |
| Agent Memory | Persistent injection, cross-user leakage | Memory isolation, access controls |
| Tools | Rogue actions, privilege abuse | Least privilege, auth/authz per tool |
| Content (RAG) | Data poisoning | Training data sanitization, integrity checks |
| Auxiliary Models | Supply chain attacks | Model integrity management |

---

## Agent Autonomy Spectrum

La complejidad del plan determina el nivel de autonomía → escalado directo de riesgo:

- **Low autonomy:** Selección de workflow predefinido
- **Medium autonomy:** Orquestación de acciones multi-step con paths predefinidos
- **High autonomy:** Orquestación dinámica de acciones multi-step sin paths predefinidos

**Regla:** A mayor autonomía → mayor severidad potencial de un fallo de seguridad.
