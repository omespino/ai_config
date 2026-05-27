---
name: ai-agents-security-design
description: Diseño seguro de agentes de IA según Google SAIF 2.0 y whitepaper May 2025. Tres principios core (human controllers, limited powers, observable actions), controles (Agent User Controls, Agent Permissions con AAA, Agent Observability), defense-in-depth híbrido (runtime policy enforcement + reasoning-based defenses), assurance activities. Triggers — "secure agent design", "diseño seguro agente", "agent security principles", "principios seguridad agente", "least privilege agent", "privilegio mínimo agente", "agent observability", "observabilidad agente", "agent permissions", "permisos agente", "human in the loop agent", "human controller agent", "defense in depth agent", "defense in depth ia", "policy enforcement agent", "agent guardrails", "guardrails agente", "cómo diseñar agente seguro", "how to build secure agent", "agent aaa", "agent authentication authorization".
---

## Source
Google Whitepaper: "Google's Approach for Secure AI Agents: An Introduction" (May 2025)
Google SAIF 2.0 — Controls: Agent User Control, Agent Permissions, Agent Observability (saif.google/secure-ai-framework/controls)

---

## Framework: Three Core Principles for Agent Security

Para mitigar los riesgos de los agentes mientras se beneficia de su potencial, Google propone **tres principios core** para la seguridad de agentes. Cada principio tiene controles específicos e infraestructura requerida.

```
Principle 1: Well-defined human controllers  → Agent User Controls
Principle 2: Agent powers must have limitations → Agent Permissions (dynamic least privilege)
Principle 3: Agent actions must be observable → Agent Observability
```

---

## Principle 1: Agents Must Have Well-Defined Human Controllers

### Core Idea
Los agentes actúan como proxies o asistentes de humanos, heredando privilegios para acceder a recursos y ejecutar acciones. Por tanto, deben operar bajo supervisión humana clara.

**Requiere:**
- Cada agente debe tener un conjunto bien definido de usuarios controladores
- El sistema debe distinguir confiablemente instrucciones de un usuario controlador autorizado vs cualquier otro input (especialmente datos no confiables)
- Para acciones críticas o irreversibles → requerir **confirmación explícita del humano** antes de proceder

**Ejemplos de acciones que requieren confirmación humana:**
- Eliminar grandes cantidades de datos
- Autorizar transacciones financieras significativas
- Cambiar configuraciones de seguridad
- Enviar comunicaciones en nombre del usuario
- Cualquier acción irreversible con impacto fuera del sistema

### Multi-User and Multi-Agent Scenarios

**Agentes con múltiples usuarios:**
- Requieren identidades distintas y modelos de autorización claros
- Prevenir acceso cross-user a datos → memory isolation estricta
- Prevenir que un usuario desencadene accidentalmente acciones que impacten a otro
- Dar a usuarios tools para otorgar permisos granulares (vs permisos gruesos de single-user agent)
- Compartir configuraciones de agentes debe ser transparente: los usuarios deben entender cómo una configuración compartida altera el comportamiento

**Agentes en sistemas multi-agente:**
- Cada agente-subagente también necesita identidad verificable
- Trust hierarchy clara: qué agente puede instruir a cuál, con qué privilegios

### Controls
**Agent User Controls** — soportados por infraestructura que provee:
- Identidades de agente distintas y verificables
- Mecanismos de consentimiento del usuario
- Canales de input seguros para diferenciar comandos de usuario

---

## Principle 2: Agent Powers Must Have Limitations

### Core Idea
Los poderes de un agente (acciones que puede tomar, recursos a los que puede acceder) deben estar **cuidadosamente limitados** en línea con su propósito intencionado y la tolerancia al riesgo de su usuario controlador.

**Extensión del least privilege tradicional:**
- No solo *estáticamente* minimizar privilegios
- También *dinámicamente* alinear permisos con el propósito específico y el intent del usuario actual en cada query
- Esta distinción es crucial: los agentes operan en ecosistemas potencialmente unbounded y son susceptibles a errores de razonamiento

**Ejemplo de dynamic least privilege:**
- Agente de investigación → no debe tener poder para modificar cuentas financieras
- Agente general-purpose → debe poder confinar capacidades en runtime (ej: deshabilitar file deletion cuando la tarea es creative writing)
- Solo permisos relevantes activos para cada query específica

### Enforceable Requirements

1. **Niveles máximos de permiso deben ser definibles y aplicables**
2. **Agentes NO deben poder escalar sus propios privilegios** más allá de scopes pre-autorizados explícitamente
3. **Usuarios deben poder inspeccionar y revocar** cualquier autoridad delegada a un agente
4. **Prevenir sandbox escape** o acceso a capabilities de alto privilegio desde contextos de bajo privilegio

### Infrastructure Required: AAA for Agents

Adaptar y fortalecer infraestructura de Authentication, Authorization, and Auditing (AAA):

```
Authentication:
- Identidades de agente verificables (no simplemente "confiar en que el agente dice ser X")
- Distinguir: instrucciones del controlador vs datos procesados por el agente

Authorization:
- Sistemas granulares de permisos adaptados para agentes
- Scoped OAuth tokens (no tokens full-access)
- Dynamic permission scoping por contexto/query
- Reference monitors para exponer solo datos contextualmente apropiados

Auditing:
- Registro completo de qué permisos usó el agente y cuándo
- Capacidad de revocar permisos retroactivamente si es necesario
```

### Tool Permission Model

| Tool/Action | Ideal Permission Scope | Notes |
|---|---|---|
| Read files | Directorio específico, no `/` | Sandbox al scope mínimo |
| Write files | Solo paths necesarios para la tarea | No write acceso global |
| Send email | Solo después de confirmación del usuario | Acción de alto impacto |
| Web browsing | Solo dominios en whitelist si es posible | Limitar exfiltración |
| Execute code | Sandbox aislado sin acceso a filesystem real | Containment obligatorio |
| Database queries | Read-only por default; write solo cuando necesario | Principio de menor escritura |
| External APIs | Scoped credentials, no master keys | OAuth con scopes mínimos |

### Controls
**Agent Permissions** — implementado con:
- Sistemas de permisos granulares adaptados para agentes
- Scoped credential management (OAuth tokens con scopes mínimos)
- Sandboxing de ejecución de herramientas
- Robust AAA infrastructure for agents

---

## Principle 3: Agent Actions and Planning Must Be Observable

### Core Idea
La confianza, debugging efectivo, auditoría de seguridad, incident response y comprensión del usuario dependen de **transparencia en las actividades del agente**. No se puede garantizar que un agente actúa fielmente si sus operaciones son completamente opacas.

**Lo que debe ser observable y auditable:**
- Acciones del agente
- Tool use (qué tools invocó, con qué parámetros)
- Outputs generados
- Idealmente: pasos intermedios de razonamiento (reasoning steps)

### Logging Requirements

**Qué capturar:**
```
- Inputs recibidos (con metadata de fuente)
- System instructions activas en el momento
- Herramientas invocadas + parámetros exactos + outputs
- Reasoning steps (si el modelo los expone)
- Outputs finales generados
- Timestamps y contexto de sesión
- Usuario/identidad asociada
```

**Cómo capturarlo:**
- Logging robusto a través de toda la arquitectura del agente
- Logging seguro: proteger datos sensibles dentro de los propios logs
- Logs inmutables y con integridad verificable (para incident response)
- Centralización en sistemas de logging seguros

### Action Characterization

Las propiedades de las acciones deben estar **claramente caracterizadas**:

| Property | Why It Matters |
|---|---|
| Read-only vs state-changing | Actions que cambian estado necesitan más scrutiny |
| Handles sensitive data | Acciones con PII/secrets requieren controles adicionales |
| Reversible vs irreversible | Las irreversibles requieren confirmación humana |
| Internal vs external | Actions que salen del sistema corporativo son más riesgosas |
| Scope of impact | Afecta a 1 usuario, al equipo, a la empresa? |

Esta metadata es crucial para **mecanismos de seguridad automatizados** y para revisores humanos.

### Transparent UX

Las interfaces de usuario deben promover transparencia:
- Mostrar al usuario el "thought process" del agente
- Indicar las fuentes de datos consultadas
- Mostrar las acciones que el agente pretende tomar, especialmente para operaciones complejas o de alto riesgo
- Permitir al usuario pausar/aprobar/rechazar antes de ejecución (especialmente para acciones irreversibles)

### Controls
**Agent Observability** — infraestructura necesaria:
- Sistemas de logging seguros y centralizados
- APIs estandarizadas que expongan claramente las propiedades de las acciones
- UX transparente que da a los usuarios insights del "thought process" del agente

---

## Principles Summary Table (Figure 4 del whitepaper)

| Principle | Summary | Key Control Focus | Infrastructure Needs |
|---|---|---|---|
| 1. Human controllers | Ensures accountability, user control, and prevents agents from acting autonomously in critical situations without clear human oversight | Agent user controls | Distinct agent identities, user consent mechanisms, secure inputs |
| 2. Limited powers | Enforces appropriate, dynamically limited privileges, ensuring agents have only the capabilities and permissions necessary for their intended purpose and cannot escalate privileges inappropriately | Agent permissions | Robust AAA for agents, scoped credential management, sandboxing |
| 3. Observable actions | Requires transparency and auditability through robust logging of inputs, reasoning, actions, and outputs, enabling security decisions and user understanding | Agent observability | Secure/centralized logging, characterized action APIs, transparent UX |

---

## Google's Hybrid Defense-in-Depth Strategy

Dado que ni las medidas puramente determinísticas ni el razonamiento puro del modelo son suficientes solos, Google adopta un **enfoque híbrido de defense-in-depth**.

```
                                         ┌─────────────────────┐
Runtime Policy Enforcement ──────────►  │    AI Agent         │
(Layer 1: Deterministic)                 │                     │
                                         │  Application        │
Reasoning-based Defenses ────────────►  │  Perception         │
(Layer 2: AI-powered)                    │  Rendering          │
                                         │  Reasoning Core     │
Regression Testing        ───────────►  │  Orchestration      │
Variant Analysis                         └─────────────────────┘
Red Teams & Human Reviewers
```

### Layer 1: Traditional Deterministic Measures (Runtime Policy Enforcement)

**Qué son:** Policy engines que operan **fuera** del proceso de razonamiento del modelo AI. Monitorean y controlan las acciones del agente **antes** de ejecutarlas — actúan como security chokepoints.

**Cómo funcionan:**
1. El agente decide usar una tool o realizar una acción (ej: "send email", "purchase item")
2. La request es **interceptada por el policy engine**
3. El engine evalúa la request contra reglas predefinidas basadas en:
   - Riesgo inherente de la acción (¿es irreversible? ¿involucra dinero?)
   - Contexto actual
   - Chain de acciones previas (¿el agente procesó recientemente una fuente sospechosa?)
4. El engine determina: **allow** / **block** / **require user confirmation**

**Ejemplos de policies:**
```
# Spending limit policy
IF action == "purchase" AND amount > $500:
    BLOCK
IF action == "purchase" AND amount > $100:
    REQUIRE_USER_CONFIRMATION

# Suspicious data source policy
IF agent recently processed data from suspicious source:
    AND action == "send_email_external":
        REQUIRE_USER_CONFIRMATION (unless user explicitly approves)

# Irreversible action policy
IF action in [delete_files_bulk, financial_transfer, change_security_settings]:
    REQUIRE_EXPLICIT_HUMAN_CONFIRMATION
```

**Fortalezas:**
- Fiable y predecible (determinístico)
- Testable y auditable
- Limita efectivamente el worst-case impact de malfunción del agente
- No puede ser "convencido" por el LLM de saltarse una regla

**Limitaciones:**
- Definir políticas comprehensivas para ecosistemas de acción vastos es complejo y difícil de escalar
- Policies a menudo carecen de deep contextual understanding
- Reglas estáticas pueden bloquear acciones legítimas o permitir dañinas en contextos no anticipados
- Ejemplo: "enviar email después de leer un documento" es a veces deseable (resumir y enviar) y a veces dañino (exfiltrar datos) — una regla simple no captura ese matiz

### Layer 2: Reasoning-Based Defense Strategies

**Qué son:** Técnicas que usan los propios modelos AI para evaluar inputs, outputs o el razonamiento interno del agente para detectar riesgos potenciales. Complementan las guardrails determinísticas con contextual understanding.

#### Técnica 1: Adversarial Training

Durante el desarrollo del modelo, se le expone a numerosos ejemplos de ataques (prompt injection variados). El entrenamiento le enseña:
- Reconocer e ignorar instrucciones maliciosas embebidas en datos
- Flaggear inputs sospechosos para scrutiny
- Usar convenciones de prompt estructurado (delimiters, role tagging) para diferenciar instrucciones de confianza de inputs no confiables

#### Técnica 2: Specialized Guard Models (Classifiers)

Modelos AI más pequeños entrenados específicamente como **clasificadores de seguridad**:
- Examinan inputs u outputs buscando signos de ataque
- Detectan: lenguaje similar a instrucciones en datos del usuario, patrones maliciosos
- Funcionan como security analysts automatizados en el pipeline

```
Input → [Guard Classifier] → ¿Malicious? → Block/Flag
                           → ¿Safe? → Pass to Reasoning Core

Output → [Output Guard] → ¿Contains sensitive data? → Sanitize/Block
                        → ¿XSS patterns? → Strip/Escape
```

#### Técnica 3: Analysis and Prediction

Modelos que analizan el **plan de acción propuesto** por el agente:
- Predicen la probabilidad de que el plan conduzca a un outcome indeseable
- Flaggean planes de alto riesgo para review
- Pueden triggear policy enforcement más estricta antes de ejecución

**Fortalezas de Layer 2:**
- Puede manejar comportamientos dinámicos y contexto que las reglas estáticas no capturan
- Aprende a reconocer patrones de ataque más matizados o evolutivos
- Aumenta significativamente el costo y dificultad para atacantes

**Limitaciones:**
- Non-determinístico → no puede proveer garantías absolutas
- Los modelos aún pueden ser engañados por ataques novedosos
- Failure modes son impredecibles
- Por sí solos son insuficientes para escenarios que requieren garantías absolutas de seguridad

### Assurance Activities: Continuous Validation

Apoyan ambas capas:

| Activity | Purpose |
|---|---|
| **Regression testing** | Asegurar que los fixes permanezcan efectivos tras updates |
| **Variant analysis** | Proactivamente testear variaciones de amenazas conocidas para anticipar evolución del atacante |
| **Red teams** | Ataques simulados por experts humanos (automated + manual) |
| **User feedback** | Real-world insights sobre comportamiento en producción |
| **Security reviewers** | Auditorías formales del sistema |
| **External security researchers** | Perspectivas diversas (ej: Google VRP) para descubrir debilidades no anticipadas |

---

## Security Design Checklist

### Application Layer
- [ ] ¿El agente distingue confiablemente instrucciones del usuario de confianza vs datos contextuales?
- [ ] ¿Para operaciones asíncronas, hay mecanismos de oversight cuando el usuario no está presente?
- [ ] ¿El usuario puede revisar, aprobar y revocar permisos de memoria y personalizaciones?

### Perception Layer
- [ ] ¿Las system instructions están claramente delimitadas de los datos del usuario?
- [ ] ¿Se usan control tokens o delimiters para prevenir prompt injection?
- [ ] ¿El input es validado y sanitizado antes de pasar al reasoning core?

### Reasoning Core
- [ ] ¿El agente requiere confirmación del usuario para acciones de alto riesgo o irreversibles?
- [ ] ¿Hay constrains en la complejidad o longitud del plan?
- [ ] ¿El agente puede pedir clarificación ante instrucciones ambiguas o conflictivas?

### Rendering
- [ ] ¿El output es sanitizado apropiadamente según el content type?
- [ ] ¿Se previene la ejecución de JavaScript en el output del agente?
- [ ] ¿Las URLs generadas son validadas para prevenir exfiltración?

### Tools / Orchestration
- [ ] ¿El conjunto de acciones disponibles está claramente definido y los usuarios pueden entender sus implicaciones?
- [ ] ¿Se usa least privilege por tool y por tarea (dynamic scoping)?
- [ ] ¿Hay sandboxing para tools de alto impacto?
- [ ] ¿Las tools de terceros están auditadas para descriptions engañosas?

### Memory
- [ ] ¿La memoria está aislada entre usuarios?
- [ ] ¿Hay mecanismos para detectar y limpiar datos maliciosos en memoria?
- [ ] ¿Los usuarios tienen transparencia y control sobre qué se almacena?

### Logging / Observability
- [ ] ¿Se loguean inputs, tool invocations, parámetros y outputs?
- [ ] ¿Los logs son seguros (no contienen datos sensibles expuestos)?
- [ ] ¿Hay capacidad de audit trail para incident response?
- [ ] ¿La UX muestra al usuario las acciones planificadas antes de ejecutarlas?
