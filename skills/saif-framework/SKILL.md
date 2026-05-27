---
name: saif-framework
description: Google's Secure AI Framework (SAIF) completo: 4 áreas de componentes (Data, Infrastructure, Model, Application), 15 riesgos del SAIF Risk Map con causas/impacto/mitigaciones, catálogo completo de controles (Data/Infrastructure/Model/Application/Assurance/Governance), AI development lifecycle security, risk self-assessment approach. Basado en saif.google. Triggers — "saif", "saif framework", "saif map", "saif risks", "saif controls", "ai risk map", "mapa de riesgos ia", "framework seguridad ia", "ai security framework", "google saif", "secure ai framework", "riesgos ia google", "controles seguridad ia", "ai risk assessment", "evaluacion riesgos ia", "model creator", "model consumer", "data poisoning saif", "ai development security", "lifecycle seguridad ia".
---

## Source
Google SAIF (Secure AI Framework) — saif.google
Introducido en 2023 como externalización del framework interno de Google para seguridad de AI.
SAIF 2.0 actualizado con foco en agentes (2025).

---

## What is SAIF?

**SAIF = Google's Secure AI Framework** — guía para construir y desplegar AI responsablemente.

**Audiencias:**
- **Model Creators:** Organizaciones que entrenan/finetunean modelos (foundation models o modelos domain-specific)
- **Model Consumers:** Organizaciones que construyen aplicaciones/productos AI usando modelos vía API o descargados — sin crearlos

**Qué ofrece:**
1. **SAIF Risk Map** — paradigma y vocabulario compartido para navegar AI risks y controls
2. **SAIF Risk Self Assessment** — evaluación interactiva de riesgos de la organización
3. **AI Development Security Primer** — el proceso de desarrollo AI a través del lens de security risks
4. **Agent-specific Risk Map** — extensión especializada para sistemas agenticos (SAIF 2.0)
5. **Resources** — whitepapers técnicos profundos

---

## SAIF Map: 4 Component Areas

El SAIF Map categoriza el desarrollo AI en cuatro áreas:

```
┌─────────────────────────────────────────────────────────┐
│                       DATA                              │
│  Data Sources → Data Filtering/Processing → Training    │
│                          Data                           │
├─────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE                        │
│  Model Frameworks & Code │ Training/Tuning/Evaluation   │
│  Data & Model Storage    │ Model Serving                │
├─────────────────────────────────────────────────────────┤
│                      MODEL                              │
│  The Model (code + weights) │ Input Handling            │
│                             │ Output Handling           │
├─────────────────────────────────────────────────────────┤
│                   APPLICATION                           │
│  User Interaction │ Agent/Plugin │ Integrations         │
└─────────────────────────────────────────────────────────┘
```

**El mapa se divide horizontalmente:**
- **Mitad superior** — path del modelo al deployment en aplicación (User Queries → Application → Model) → más relevante para **Model Consumers**
- **Mitad inferior** — path de desarrollo del modelo (Data → Training → Model) → más relevante para **Model Creators**

---

## DATA Components

**Por qué los datos son críticos en AI:**
A diferencia del software tradicional (instrucciones estáticas), en AI el **data juega el rol del código** — determina el comportamiento del modelo a través de los weights. Comprometer los weights es tan dañino como comprometer el código.

### Data Sources
Repositorios/fuentes de origen del training data: databases, APIs, web scraping, sensor data.
- Calidad y diversidad impactan directamente las capacidades del modelo
- **Security risk:** Datos pueden ser poisoned antes de ingestion

### Data Filtering and Processing
Limpieza, transformación y preparación de datos: labeling, deduplication, sanitization, synthetic data generation.
- **Security risk:** Datos maliciosos pueden sobrevivir el filtering si no hay controles adecuados

### Training Data
El subset final curado que se alimenta al modelo durante training.
- Determina los patterns internos (weights) del modelo
- **Security risk:** Cualquier dato corrupto aquí tiene impacto directo en el comportamiento del modelo

---

## INFRASTRUCTURE Components

### Model Frameworks and Code
Code y frameworks para entrenar y usar el modelo (arquitectura, layers, inference).
- Framework code generalmente necesario también para inferencia (no solo training)
- **Security risk:** Supply chain attacks, tampering en dependencies

### Training, Tuning, and Evaluation
- **Training:** Ajuste de probabilidades para extraer patterns correctos
- **Tuning (fine-tuning):** Ajuste de subset de probabilidades para task específica (más común y económico que training completo)
- **Evaluation:** Testing del modelo contra nuevos datos — ocurre durante training (por checkpoint) y post-training
- **Security risk:** Datos o code maliciosos introducidos en cualquier fase

### Data and Model Storage
- **Training data storage:** Desde ingestion hasta uso en training
- **Model storage:** Local (durante training, checkpoints), published (model hub tras training)
- **Security risk:** Exfiltración, tampering, acceso no autorizado

### Model Serving
Sistemas y procesos para desplegar el modelo en producción.
- **Security risk:** Tampering del modelo en producción, denial of service

---

## MODEL Components

### The Model
Par de code + weights, creado con datos durante training. Útil cuando se despliega en aplicaciones.

### Input Handling
Componentes que filtran, sanitizan y protegen contra inputs potencialmente maliciosos.
- Actúa como control contra numerosos riesgos
- "Área madura para más investigación y desarrollo"

### Output Handling
Componentes que filtran, sanitizan y protegen contra outputs no deseados, inesperados o peligrosos.
- Principal línea de defensa contra varios riesgos

---

## APPLICATION Components

### User Interaction
Los usuarios interactúan con modelos AI de forma más natural (prompting vs APIs clásicas) — esto introduce nuevos vectores (prompt injection).

### Agent/Plugin
Sistemas que actúan en nombre del usuario — ver SAIF Agent Extension para el mapa especializado de agentes.

### Integrations
Integraciones con sistemas externos — cada integración es superficie de ataque adicional.

---

## Complete Risk Catalog (15 Risks)

### GROUP 1: Data Risks (primarily Model Creators)

**DP — Data Poisoning**
- **Qué es:** Alterar fuentes de datos durante training (delete/modify/inject adversarial data) → degradar performance, sesgar resultados, crear backdoors
- **Comparable a:** Modificar maliciosamente la lógica de una aplicación
- **Cuándo ocurre:** Durante training/tuning, en storage, antes de ingestion (web crawl poisoning)
- **Backdoors:** Alteraciones específicas del training data → modelo funciona normalmente pero se activa maliciosamente bajo condiciones específicas
- **Controls:** Training Data Sanitization, Secure-by-Default ML Tooling, Model and Data Integrity Management, Model and Data Access Controls, Model and Data Inventory Management
- **Real example:** Investigadores mostraron que podían contaminar indirectamente datasources populares con costo mínimo

**UTD — Unauthorized Training Data**
- **Qué es:** Training con datos no autorizados para ese modelo
- **Impacto:** Legal, ético, regulatory
- **Incluye:** Datos de usuario sin consent, datos con copyright, datos legalmente restringidos
- **Controls:** Training Data Sanitization, Training Data Management
- **Real example:** Spotify removió tracks de AI generados por modelo entrenado con datos sin licencia

**MST — Model Source Tampering**
- **Qué es:** Tampering del source code, dependencies o weights del modelo (supply chain o insider attacks)
- **Tipos:** Code tampering, dependency confusion, model architecture backdoors (sobreviven full retraining)
- **Controls:** Secure-by-Default ML Tooling, Model and Data Integrity Management, Model and Data Access Controls, Model and Data Inventory Management
- **Real example:** PyTorch nightly build atacado con dependency confusion attack

**EDH — Excessive Data Handling**
- **Qué es:** Colección/retención/procesamiento/sharing de datos de usuario más allá de lo permitido por políticas
- **Incluye:** User queries, inputs, interactions, personalizations, derived models
- **Impacto:** Legal, policy, regulatory challenges
- **Controls:** User Data Management

### GROUP 2: Infrastructure Risks

**ME — Model Exfiltration**
- **Qué es:** Robo del modelo (code + weights) via vulnerabilidades en storage/serving
- **Controls:** Model and Data Inventory Management, Model and Data Access Controls, Secure-by-Default ML Tooling

**MDT — Model Deployment Tampering**
- **Qué es:** Manipulación de modelos en producción dentro del serving infrastructure
- **Controls:** Secure-by-Default ML Tooling

**DoML — Denial of ML Service**
- **Qué es:** Overwhelming del modelo con queries excesivas O "sponge examples" (explotan el funcionamiento del modelo para degradar performance)
- **Controls:** Input Validation and Sanitization, Application Access Management (rate limiting, load balancing)

**MRE — Model Reverse Engineering**
- **Qué es:** Reverse engineering de weights via excesivas queries al modelo + análisis de respuestas
- **Controls:** Application Access Management (rate limiting)

### GROUP 3: Model/Application Risks

**IIC — Insecure Integrated Component**
- **Qué es:** Integraciones en app/agent components que permiten manipulación de inputs/outputs → acceso no autorizado, código malicioso, sistemas comprometidos
- **Controls:** Agent Permissions (permisos estrictos para agents/plugins)

**PI — Prompt Injection**
- **Qué es:** Instrucciones maliciosas en inputs confunden al modelo → ejecuta acciones no intencionadas
- **Riesgo inherente:** Confusión entre instrucciones y datos de input en los LLMs
- **Controls:** Input Validation and Sanitization, Output Validation and Sanitization, Adversarial Training and Testing

**MEv — Model Evasion**
- **Qué es:** Inputs crafted para evadir comportamiento esperado o detección del modelo
- **Controls:** Adversarial Training and Testing

**SDD — Sensitive Data Disclosure (Updated in SAIF 2.0)**
- **Qué es:** El modelo revela datos sensibles (training data memorizado, datos en prompt, datos del usuario)
- **En agentes:** Amplificado porque los agentes pueden tener acceso privilegiado a email, archivos, sistema completo
- **Dos tipos de leakage:**
  1. Datos provistos al modelo durante uso (user input, datos que pasan por sistemas integrados)
  2. Datos usados para training/tuning del modelo
- **Controls:** Privacy Enhancing Technologies, Output Validation and Sanitization, Adversarial Training and Testing, User Transparency and Controls, Agent User Control, Agent Permissions, Agent Observability

**ISD — Inferred Sensitive Data**
- **Qué es:** El modelo infiere y revela datos sensibles que no fueron provistos explícitamente
- **Controls:** Privacy Enhancing Technologies, Output Validation and Sanitization, Adversarial Training and Testing

**IMO — Insecure Model Output**
- **Qué es:** Output del modelo que introduce vulnerabilidades de seguridad en aplicaciones downstream
- **Controls:** Output Validation and Sanitization

**RA — Rogue Actions (Updated in SAIF 2.0)**
- **Qué es:** Comportamientos del agente no intencionados, dañinos o violadores de políticas
- **En agentes:** El agente usa acceso privilegiado para realizar acciones que el usuario no quería
- **Controls:** Output Validation and Sanitization, Agent User Control, Agent Permissions, Agent Observability

---

## Complete Controls Catalog

### DATA Controls

| Control | Who | Description | Risks Addressed |
|---|---|---|---|
| Privacy Enhancing Technologies | Model Creators | Minimizar, de-identificar o restringir uso de PII en training/evaluation | SDD, ISD |
| Training Data Management | Model Creators | Asegurar que todos los datos de training estén autorizados | ISD, UTD |
| Training Data Sanitization | Model Creators | Detectar y remover/remediar datos poisoned o sensibles | DP, UTD |
| User Data Management | Both | Almacenar/procesar/usar datos de usuario en compliance con consent | SDD, EDH |

### INFRASTRUCTURE Controls

| Control | Who | Description | Risks Addressed |
|---|---|---|---|
| Model and Data Inventory Management | Both* | Inventariar y trackear todos los datos, code, modelos y tools | DP, MST, ME |
| Model and Data Access Controls | Both* | Minimizar acceso interno a modelos, weights, datasets en storage y producción | DP, MST, ME |
| Model and Data Integrity Management | Both* | Asegurar que datos, modelos y code sean verifiably integrity-protected | DP, MST |
| Secure-by-Default ML Tooling | Both* | Usar frameworks, libraries, sistemas seguros para desarrollo/deployment | DP, MST, ME, MDT |

*Both = Model Creators + Model Consumers (si almacenan modelos)

### MODEL Controls

| Control | Who | Description | Risks Addressed |
|---|---|---|---|
| Input Validation and Sanitization | Both | Bloquear o restringir queries adversariales a modelos | PI |
| Output Validation and Sanitization | Both | Bloquear, nullificar o sanitizar output inseguro antes de pasar a apps/usuarios | PI, RA, SDD, ISD |
| Adversarial Training and Testing | Both | Hacer modelos robustos contra inputs adversariales en su contexto de uso | MEv, PI, SDD, ISD, IMO |

### APPLICATION Controls (Updated in SAIF 2.0)

| Control | Who | Description | Risks Addressed |
|---|---|---|---|
| Application Access Management | Model Consumers | Solo usuarios/endpoints autorizados pueden acceder a recursos para acciones autorizadas | DoML, MRE |
| User Transparency and Controls | Model Consumers | Informar a usuarios de riesgos AI con disclosures; dar transparencia y control sobre uso de sus datos | SDD, EDH |
| **Agent User Control** | Model Consumers | Asegurar aprobación del usuario para acciones del agente que alteran datos o actúan en su nombre | SDD, RA |
| **Agent Permissions** | Model Consumers | Least-privilege como upper bound en permisos del sistema agentico. El uso de privilegios debe ser **contextual y dinámico** (adaptarse al user query y trusted contextual info). Agentes que acceden a info del usuario deben compartir solo info contextualmente apropiada (reference monitors) | IIC, SDD, RA |
| **Agent Observability** (NEW) | Model Consumers | Asegurar que acciones, tool use y reasoning del agente sean transparentes y auditables via logging | SDD, RA |

### ASSURANCE Controls (Apply to ALL risks)

| Control | Who | Description |
|---|---|---|
| Red Teaming | Both | Ataques adversariales auto-driven en AI infrastructure y productos |
| Vulnerability Management | Both | Testing y monitoring continuo de producción para regressions de seguridad/privacidad |
| Threat Detection | Both | Detectar y alertar sobre ataques internos o externos a AI assets/infrastructure |
| Incident Response Management | Both | Gestionar respuesta a incidentes de seguridad/privacidad AI |

### GOVERNANCE Controls (Apply to ALL risks)

| Control | Who | Description |
|---|---|---|
| User Policies and Education | Model Consumers | Publicar políticas AI de seguridad/privacidad comprensibles para usuarios |
| Internal Policies and Education | Both | Publicar políticas AI de seguridad/privacidad comprensivas para empleados |
| Product Governance | Both | Validar que todos los modelos y productos AI cumplen requerimientos de seguridad/privacidad |
| Risk Governance | Both | Inventariar, medir y monitorear riesgo residual AI en la organización |

---

## AI Development Lifecycle — Security at Each Stage

### Data Phase
1. **Data Sourcing and Ingestion**
   - Risks: Unauthorized training data, Data poisoning
   - Questions: ¿Es la data de alta calidad? ¿Hay derechos de uso? ¿Ethical concerns? ¿Bias potencial? ¿Se puede verificar integridad (cryptographic signatures)?

2. **Data Cleaning and Augmentation**
   - Risks: Data poisoning sobrevive cleaning, sensitive data en training set
   - Controls: Data sanitization, labeling quality, PII removal

### Infrastructure Phase
3. **Training, Tuning, Evaluation**
   - Risks: Model Source Tampering, Data Poisoning
   - Security: Secure-by-default frameworks, integrity verification, adversarial evaluation

4. **Model and Framework Code**
   - Risks: Supply chain attacks en dependencies
   - Security: Software supply chain integrity, dependency scanning

5. **Data Storage**
   - Risks: Data exfiltration, tampering en storage
   - Security: Access controls, encryption, integrity management

6. **Model Storage**
   - Risks: Model exfiltration, tampering
   - Security: Access controls, inventory tracking

7. **Model Serving**
   - Risks: Model Deployment Tampering, DoML, MRE
   - Security: Secure serving infrastructure, rate limiting, load balancing

### Application Phase
8. **Model Selection**
   - Consider: Security track record del provider, evaluation adversarial del modelo

9. **User Interactions**
   - Risks: Prompt Injection, SDD, Model Evasion
   - Security: Input/output validation, user transparency controls

10. **Agent and Tool Usage**
    - Risks: Rogue Actions, SDD, IIC, PI
    - Security: Agent User Control, Agent Permissions, Agent Observability

11. **Model Integration**
    - Risks: IIC (insecure integrations)
    - Security: Strict integration permissions, secure-by-default APIs

12. **Application Testing**
    - Risks: Regressions no detectadas
    - Security: Red teaming, adversarial testing, vulnerability management

---

## SAIF Risk Self-Assessment Approach

**Preguntas clave del self-assessment:**

**Para Model Creators:**
- ¿Tienes gestión robusta de todos los training/tuning/evaluation data para asegurar que no entren datos sensibles, no autorizados o maliciosos?
- ¿Puedes detectar, remover y remediar cambios maliciosos o accidentales en training data?
- ¿Se usa data sensible del usuario en training/tuning/evaluation?
- ¿Tienes inventario completo de todos los modelos, datasets y ML artifacts (code)?
- ¿Tienes access controls robustos en modelos, datasets y artifacts?
- ¿Puedes asegurar que data, modelos y code no pueden ser tampered sin detección?
- ¿Los frameworks, libraries y hardware usados están analizados y protegidos contra vulnerabilidades?

**Para Model Consumers (additional):**
- ¿Proteges tus aplicaciones AI contra queries maliciosas a gran escala?
- ¿Usas diseños secure-by-default en aplicaciones integradas con AI?
- ¿Realizas adversarial testing y training para mejorar resistencia?
- ¿Construyes o despliegas agentes que pueden tomar acciones en nombre de usuarios?

---

## SAIF and Industry Standards Alignment

SAIF se alinea con:
- **NIST AI Risk Management Framework (AI RMF)**
- **NIST Secure Software Development Framework (SSDF)**
- **Coalition for Secure AI (CoSAI)** — Google compartió el SAIF Risk Assessment, Risk Map y descriptions con CoSAI para acelerar desarrollo de soluciones open-source

---

## Quick Reference: Risk → Controls Mapping

| Risk | Primary Controls |
|---|---|
| Data Poisoning | Training Data Sanitization, Integrity Mgmt, Access Controls |
| Unauthorized Training Data | Training Data Management, Training Data Sanitization |
| Model Source Tampering | Secure ML Tooling, Integrity Mgmt, Access Controls, Inventory |
| Excessive Data Handling | User Data Management |
| Model Exfiltration | Inventory, Access Controls, Secure ML Tooling |
| Model Deployment Tampering | Secure-by-Default ML Tooling |
| Denial of ML Service | Input Validation, Application Access Management |
| Model Reverse Engineering | Application Access Management |
| Insecure Integrated Component | Agent Permissions |
| Prompt Injection | Input Validation, Output Validation, Adversarial Training |
| Model Evasion | Adversarial Training and Testing |
| Sensitive Data Disclosure | PETs, Output Validation, Adversarial Training, User Transparency, Agent Controls |
| Inferred Sensitive Data | PETs, Output Validation, Adversarial Training |
| Insecure Model Output | Output Validation and Sanitization |
| Rogue Actions | Output Validation, Agent User Control, Agent Permissions, Agent Observability |
