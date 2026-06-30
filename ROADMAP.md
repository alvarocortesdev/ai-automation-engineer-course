# 🧭 Roadmap — AI / Automation Engineer (con columna vertebral Fullstack)

> **Columna vertebral de mi repositorio de estudio.**
> De recuperar autonomía de código → a semi-senior empleable → a senior en el nicho IA/Automatización.

**Autor:** Alvaro Cortés
**Perfil destino:** AI / Automation Engineer con base Fullstack sólida
**Objetivo de mercado:** entrar como **semi-senior** (banda CLP 1.6M–2.4M+), modalidad **remoto/híbrido**, con horizonte a **senior** tras el próximo trabajo.
**Última actualización:** 2026-06-25

---

## 0. Cómo usar este roadmap

### Por qué este orden (y no el de roadmap.sh)
Los roadmaps de roadmap.sh (Fullstack y AI Engineer) son buenos como *catálogo de temas*, pero asumen un principiante genérico. Este está **reordenado alrededor de tu carrera real**: ya hiciste RAG con Azure OpenAI, pipelines en Microsoft Fabric, OCR con Document Intelligence, automatización con n8n y una base de conocimiento para IA. No partes de cero en *contenido* — partes de cero en **fundamentos de ingeniería que te dan autonomía y seniority**. Esa es la diferencia que te subirá el sueldo: hoy puedes *orquestar* IA, pero el mercado semi-senior/senior paga por quien puede *construir y sostener* el software que la envuelve.

### El problema que este roadmap resuelve a propósito
Dijiste que "perdiste la capacidad de generar código por ti mismo" por apoyarte en la IA. Es un problema real y común, y **no es una falla de talento: es falta de práctica deliberada**. Por eso la **Fase 0** y la **Regla del Primero-Sin-IA** (abajo) están integradas en todo el roadmap. No se trata de no usar IA — se trata de no *depender* de ella para pensar.

### 📏 Regla del Primero-Sin-IA (aplica a TODO el roadmap)
> Para cada ejercicio o concepto nuevo:
> 1. **Intenta resolverlo solo**, a mano, aunque sea feo y lento (timebox: 25–45 min).
> 2. Solo entonces consulta documentación oficial.
> 3. **Solo al final** usa IA — y úsala para *revisar y explicar*, no para *generar*.
> 4. Reescribe la solución de memoria al día siguiente. Si no puedes, no lo aprendiste.

### ✅ Cómo marcar el avance
- `- [ ]` pendiente · `- [~]` en progreso · `- [x]` completado
- Cada **sub-unidad** se considera completa cuando: (a) entiendes el concepto sin notas, (b) hiciste el ejercicio sin IA, y (c) lo aplicaste en un proyecto.
- Al cerrar cada **Fase**, escribe un `RETROSPECTIVA.md` con: qué aprendiste, qué te costó, qué proyecto lo demuestra.

### 📁 Estructura sugerida del repositorio
```
estudio-ai-engineer/
├── ROADMAP.md                  ← este archivo (la columna vertebral)
├── progreso.md                 ← tu dashboard de avance (resumen por fase)
├── fase-0-fundamentos/
│   ├── README.md               ← objetivos + checklist de la fase
│   ├── 0.1-mentalidad/
│   │   ├── notas.md
│   │   ├── articulos.md        ← links que vayas leyendo
│   │   └── ejercicios/
│   └── proyecto-cli/
├── fase-1-lenguajes/
│   └── ...
├── ...
└── proyectos-portafolio/       ← los capstone que van a tu CV
    ├── 01-rag-app/
    ├── 02-automation-platform/
    └── 03-homebase/
```
> Convención: una carpeta por sub-unidad. Dentro, mínimo `notas.md`, `articulos.md`, `ejercicios/`. Los proyectos grandes van en `proyectos-portafolio/` con su propio repo o submódulo.

### ⏱️ Estimación realista (estudiando ~10–15 h/semana con pega)
| Bloque | Fases | Duración aprox. |
|---|---|---|
| Reconstrucción + lenguajes | 0–1 | 6–9 semanas |
| Ingeniería + backend + frontend | 2–4 | 12–16 semanas |
| DevOps/Cloud | 5 | 3–4 semanas |
| **Especialización IA** (tu acelerador) | 6 | 8–12 semanas |
| Automatización + arquitectura | 7–8 | 6–8 semanas |
| Portafolio + empleabilidad | 9 | en paralelo, continuo |
| **Total a "semi-senior empleable"** | — | **~9–12 meses** |

> Tu experiencia previa te deja **acelerar** Fases 3, 6 y 7 (ya las tocaste en producción). No las saltes, pero pasarás más rápido.

### 🛤️ Dos pistas en paralelo
- **Pista A (fundamentos):** Fases 0 → 8 en orden. Es donde reconstruyes autonomía.
- **Pista B (IA aplicada, ya):** desde el día 1 puedes seguir construyendo cosas de IA con lo que ya sabes (n8n, Azure OpenAI), para no perder ritmo ni motivación. La Fase 6 luego le da la base formal.

---

## 🗺️ Mapa general

```
FASE 0  Reconstrucción de fundamentos y autonomía
FASE 1  Lenguajes núcleo: Python sólido + TypeScript desde cero
FASE 2  Ingeniería de software (de junior a semi-senior)
FASE 3  Bases de datos y Backend
FASE 4  Frontend que respalda tu Fullstack
FASE 5  DevOps, Cloud y despliegue
FASE 6  AI Engineering  ★ tu especialización
FASE 7  Automatización y Orquestación  ★ tu otro pilar
FASE 8  System Design y Arquitectura (rumbo a senior)
FASE 9  Portafolio, marca y empleabilidad
```
★ = donde ya tienes ventaja competitiva real. Ahí es donde diferencias y cobras el premium.

---

# FASE 0 — Reconstrucción de fundamentos y autonomía

> 🎯 **Objetivo:** recuperar la capacidad de pensar y escribir código sin IA, y reforzar las bases que se asumen en todo lo demás.
> 💰 **Por qué importa:** sin esto, en cualquier entrevista técnica (live coding) te caes. Es el cimiento de tu credibilidad como semi-senior.

## 0.1 Mentalidad y método de estudio
- [ ] Interiorizar la **Regla del Primero-Sin-IA**
- [ ] Configurar el repo de estudio y el `progreso.md`
- [ ] Definir rutina semanal (bloques fijos de estudio sin distracciones)
- [ ] Técnica de *active recall* + *spaced repetition* (Anki opcional para conceptos)
- [ ] **Drill diario:** 1 problema pequeño resuelto a mano antes de tocar el teclado

## 0.2 Cómo funciona la web y un computador
- [ ] Modelo cliente–servidor, request/response
- [ ] HTTP/HTTPS: métodos, status codes, headers, body
- [ ] DNS, dominios, qué pasa al escribir una URL (si administras un dominio propio, formalízalo)
- [ ] Qué hace el navegador (render, JS engine)
- [ ] Puertos, IPs, NAT, proxies (ya lo tocas en tu homelab/Cloudflare Tunnel)

## 0.3 Terminal y Linux (ya tienes homelab Alpine — formaliza)
- [ ] Navegación, permisos, procesos, pipes, redirecciones
- [ ] `grep`, `sed`, `awk`, `find`, `curl`, `jq`
- [ ] Variables de entorno, `.bashrc`/`.zshrc`
- [ ] SSH a fondo (ya lo usas con tus repos y servidores)
- [ ] Scripting bash básico (automatizar tareas repetitivas)

## 0.4 Git y GitHub a fondo
- [ ] Modelo mental de Git (commits, árbol, HEAD, refs)
- [ ] Branching, merge vs rebase, resolución de conflictos
- [ ] Pull Requests, code review, buenas prácticas de commits (Conventional Commits)
- [ ] `.gitignore`, tags, releases, GitHub Flow
- [ ] Trabajar con repos remotos, forks, submódulos

## 0.5 Fundamentos de programación (re-hacerlos SIN IA)
- [ ] Tipos de datos, variables, operadores
- [ ] Control de flujo (if, loops), funciones, scope
- [ ] Estructuras: listas/arrays, diccionarios/maps, sets, tuplas
- [ ] Recursión, manejo de errores/excepciones
- [ ] Pensamiento algorítmico: descomponer un problema en pasos

### 🛠️ Proyecto Fase 0 — *CLI sin IA*
> Una herramienta de línea de comandos útil para ti (ej: gestor de notas de tu homelab, o un organizador de tu vault de Obsidian). **Escrita 100% sin asistencia de IA.** Es tu prueba de que recuperaste la autonomía.

---

# FASE 1 — Lenguajes núcleo: Python + TypeScript

> 🎯 **Objetivo:** dominar tus dos lenguajes clave — Python (tu lenguaje de IA) y TypeScript (tu mayor hueco fullstack, pedido en el 38% de las ofertas).
> 💰 **Por qué importa:** TypeScript es el filtro #1 que hoy te descarta de roles fullstack. Python sólido + TS te abre tanto el mundo IA como el web.

## 1.1 Python sólido (consolidar, no aprender de cero)
- [ ] Tipado y *type hints* (`typing`, `mypy`) — clave para código profesional
- [ ] POO: clases, herencia, composición, dataclasses
- [ ] Módulos, paquetes, entornos virtuales (`venv`, `uv`/`poetry`)
- [ ] Comprehensions, generadores, decoradores, context managers
- [ ] `async`/`await` y programación asíncrona
- [ ] Manejo de archivos, JSON, APIs (`requests`/`httpx`)
- [ ] `pydantic` (validación de datos — fundamental para IA y APIs)

## 1.2 JavaScript moderno (ES6+)
- [ ] `let`/`const`, arrow functions, destructuring, spread/rest
- [ ] Promesas, `async`/`await`, `fetch`
- [ ] Módulos ES, manejo del DOM, eventos
- [ ] Array methods (`map`, `filter`, `reduce`), inmutabilidad
- [ ] Closures, `this`, prototipos (entender el *por qué*)

## 1.3 TypeScript desde cero ⚠️ (tu prioridad #1 fullstack)
- [ ] Tipos básicos, interfaces vs types, unions, generics
- [ ] Narrowing, type guards, utility types (`Partial`, `Pick`, `Omit`…)
- [ ] Tipado de funciones, objetos, async
- [ ] Configuración (`tsconfig`), integración con Node y React
- [ ] `zod` (validación de esquemas — el equivalente JS de pydantic)

### 🛠️ Proyecto Fase 1 — *La misma app, dos lenguajes*
> Construye una pequeña API (ej: gestor de tu despensa de **HomeBase**) primero en **Python** y luego en **TypeScript/Node**. Comparar te fija ambos lenguajes y te da material de portafolio bilingüe.

---

# FASE 2 — Ingeniería de software (de junior a semi-senior)

> 🎯 **Objetivo:** las prácticas que separan a un junior de un semi-senior. Esto es lo que te hace *contratable* en la banda que buscas.
> 💰 **Por qué importa:** testing, código limpio y patrones son expectativa semi-senior. Los juniors los saltan; por eso cobran menos.

## 2.1 Estructuras de datos y algoritmos (nivel trabajo)
- [ ] Complejidad Big-O (intuición, no memorizar)
- [ ] Arrays, hashmaps, stacks, queues, listas enlazadas
- [ ] Árboles y grafos (nociones), búsqueda y ordenamiento
- [ ] ~30–50 problemas tipo entrevista (resueltos **sin IA primero**)

## 2.2 Clean Code y principios de diseño
- [ ] Nombres, funciones pequeñas, DRY, KISS, YAGNI
- [ ] **SOLID** (los 5 principios con ejemplos propios)
- [ ] Patrones de diseño esenciales (Factory, Strategy, Repository, Adapter, Observer)
- [ ] Refactoring (mejorar código sin romper comportamiento)

## 2.3 Testing (expectativa semi-senior)
- [ ] Pirámide de testing: unit / integration / e2e
- [ ] **pytest** (Python): fixtures, mocking, parametrize
- [ ] **Vitest/Jest** (JS/TS): unit + integration
- [ ] **Playwright** (e2e)
- [ ] TDD (nociones), coverage, qué *no* testear
- [ ] Testing de código que llama a LLMs (mocking de respuestas)

## 2.4 Debugging y código legado
- [ ] Debuggers (VS Code, `pdb`), breakpoints, lectura de stack traces
- [ ] Leer y modificar código que no escribiste (tu experiencia .NET legado ayuda)
- [ ] Logging estructurado vs `print`

## 2.5 Colaboración profesional
- [ ] Flujo de trabajo en equipo (issues, PRs, code review)
- [ ] Metodologías ágiles: Scrum/Kanban (ya usas Azure DevOps boards — formaliza)
- [ ] Documentación técnica (READMEs, ADRs)

### 🛠️ Proyecto Fase 2 — *Refactor + suite de tests*
> Toma el proyecto de la Fase 1 y: aplícale SOLID, agrégale una suite de tests completa (>80% coverage) y un pipeline que los corra. Documenta las decisiones en un `ARQUITECTURA.md`.

---

# FASE 3 — Bases de datos y Backend

> 🎯 **Objetivo:** construir backends robustos. Aquí conviven tu base de datos (ya fuerte) con dos stacks: Node/NestJS (TS) y Python/FastAPI (tu puente a IA).
> 💰 **Por qué importa:** REST API es el skill #1 del mercado (70%). El backend es donde vive la lógica de las apps de IA que quieres construir.

## 3.1 SQL y modelado (consolidar — ya tienes base sólida)
- [ ] Modelado relacional, normalización, claves, índices
- [ ] Queries avanzadas: JOINs, subqueries, CTEs, window functions
- [ ] **PostgreSQL a fondo** (transacciones, EXPLAIN, performance)
- [ ] Migraciones de esquema

## 3.2 ORMs y acceso a datos
- [ ] **Prisma** (TS) — ya lo conoces, profundiza
- [ ] **SQLAlchemy** (Python)
- [ ] Repaso EF Core/Dapper (ya los dominas — tu carta .NET)
- [ ] Cuándo ORM vs SQL crudo

## 3.3 Diseño de APIs REST (skill #1 del mercado)
- [ ] Principios REST, recursos, verbos, status codes
- [ ] Versionado, paginación, filtrado, manejo de errores
- [ ] Documentación con **OpenAPI/Swagger** (ya lo usas)
- [ ] Nociones de **GraphQL** y cuándo usarlo

## 3.4 Backend con Node.js + NestJS (TypeScript)
- [ ] Express (fundamentos) → **NestJS** (estructura empresarial, pedido en ofertas)
- [ ] Middlewares, inyección de dependencias, módulos
- [ ] Validación (zod/class-validator), manejo de errores global

## 3.5 Backend con Python + FastAPI ★ (tu puente a IA)
- [ ] **FastAPI**: rutas, dependencias, pydantic, async
- [ ] Documentación automática, validación, background tasks
- [ ] Es el framework estándar para servir modelos/RAG en producción

## 3.6 Autenticación y seguridad
- [ ] **JWT** y **OAuth2** (pedidos en ofertas)
- [ ] Hashing de contraseñas, sesiones vs tokens
- [ ] OWASP Top 10 (nociones), CORS, rate limiting, secrets management
- [ ] Seguridad específica de apps con IA (ver Fase 6.14)

## 3.7 Rendimiento y arquitectura backend
- [ ] **Redis** (caching, sesiones) — pedido en ofertas
- [ ] Colas de mensajes y procesamiento async (Celery / BullMQ)
- [ ] Webhooks y comunicación entre servicios (tu fuerte de automatización)

### 🛠️ Proyecto Fase 3 — *API de producción*
> Backend completo (FastAPI **o** NestJS) con: auth JWT, PostgreSQL + ORM, tests, documentación OpenAPI, rate limiting y manejo de errores. Base reutilizable para tus apps de IA.

---

# FASE 4 — Frontend que respalda tu Fullstack

> 🎯 **Objetivo:** poder construir la interfaz de las apps que diseñas, sin depender de nadie. No buscas ser frontend puro — buscas *ownership* de punta a punta.
> 💰 **Por qué importa:** React (44%) es el segundo skill más pedido. Un AI Engineer que también monta la UI de su demo vale más.

## 4.1 HTML, CSS y Tailwind
- [ ] HTML semántico, accesibilidad básica
- [ ] CSS: flexbox, grid, responsive
- [ ] **Tailwind CSS** (ya lo conoces de proyectos previos)

## 4.2 React + TypeScript (lleva tu formación a producción)
- [ ] Componentes, props, estado, eventos
- [ ] Hooks: `useState`, `useEffect`, `useContext`, custom hooks
- [ ] Renderizado, listas, formularios controlados
- [ ] React **con TypeScript** (tipado de props y estado)

## 4.3 Next.js (el estándar fullstack del mercado)
- [ ] App Router, Server Components vs Client Components
- [ ] API Routes / Server Actions (fullstack en un solo proyecto)
- [ ] Renderizado (SSR/SSG/ISR), data fetching
- [ ] Despliegue en Vercel (ya lo hiciste con el menú digital)

## 4.4 Estado y datos
- [ ] Data fetching (**TanStack Query**)
- [ ] Estado global (Zustand / Redux — Redux aparece en ofertas)
- [ ] Manejo de formularios (React Hook Form + zod)

## 4.5 UI para aplicaciones de IA ★
- [ ] **Streaming** de respuestas de LLM (token por token)
- [ ] Interfaces de chat, manejo de estados de carga/error
- [ ] Vercel AI SDK (nociones — acelera apps de IA)

### 🛠️ Proyecto Fase 4 — *Frontend de una app de IA*
> Interfaz en Next.js + TS para una app de chat/RAG que consuma tu backend de la Fase 3, con streaming de respuestas. Primer proyecto "fullstack + IA" de tu portafolio.

---

# FASE 5 — DevOps, Cloud y despliegue

> 🎯 **Objetivo:** llevar lo que construyes a producción de forma profesional. Esto sube tu techo salarial.
> 💰 **Por qué importa:** Docker (33%), CI/CD (32%), AWS (30%), Azure (17%). Tu Azure es un activo real — formalízalo y agrega AWS básico para no ser filtrado.

## 5.1 Docker a fondo (ya usas Compose)
- [ ] Imágenes, contenedores, volúmenes, redes, multi-stage builds
- [ ] **Docker Compose** para entornos multi-servicio (formaliza tu uso)
- [ ] Dockerizar apps Python y Node para producción

## 5.2 CI/CD con GitHub Actions
- [ ] Workflows, jobs, triggers, secrets
- [ ] Pipeline: lint → test → build → deploy
- [ ] (Ya lo tocaste con multi-flavor en Flutter — formaliza el concepto)

## 5.3 Cloud
- [ ] **Azure** ★ (tu fuerte): App Service, Functions, Storage, AI Search, OpenAI Service
- [ ] **AWS básico** (para pasar filtros): EC2, S3, IAM, Lambda, RDS
- [ ] Nociones de costos cloud (importante para apps de IA)

## 5.4 Despliegue
- [ ] Vercel (frontend/Next.js)
- [ ] Contenedores en cloud / VPS (tu homelab Alpine + Docker)
- [ ] Cloudflare Tunnel (ya lo usas — formaliza como skill)
- [ ] Variables de entorno y configuración por ambiente

## 5.5 Observabilidad y monitoreo
- [ ] Logging estructurado, métricas, health checks
- [ ] Herramientas (Datadog aparece en ofertas; alternativas open-source)
- [ ] Alertas y manejo de incidentes

## 5.6 Infraestructura como código (nociones)
- [ ] **Terraform** básico (aparece en ofertas como diferenciador)
- [ ] Reproducibilidad de infraestructura

### 🛠️ Proyecto Fase 5 — *Pipeline completo a producción*
> Despliega tu app fullstack+IA con: Dockerfile optimizado, CI/CD en GitHub Actions (test+build+deploy), monitoreo básico y deploy en cloud o en tu homelab con dominio propio.

---

# FASE 6 — AI Engineering ★ (tu especialización)

> 🎯 **Objetivo:** convertir tu experiencia práctica (RAG con Azure OpenAI, KB para IA) en **dominio formal y profundo**. Aquí dejas de "saber usar Claude" y pasas a *diseñar, construir, evaluar y sostener* sistemas de IA.
> 💰 **Por qué importa:** es tu mayor diferenciador y donde hay premium salarial (Python+IA paga 20–40% sobre el promedio). Pocos candidatos tienen producción real como la tuya.

> 📌 **Nota:** muchos de estos temas ya los tocaste. El objetivo aquí no es descubrirlos, es **entender los fundamentos** que hoy resuelves por intuición o con IA, para poder defenderlos en entrevista y diseñarlos desde cero.

## 6.1 Fundamentos de LLMs
- [ ] Qué es un LLM, tokens, embeddings, espacio vectorial (intuición)
- [ ] Inferencia vs entrenamiento, parámetros, context window
- [ ] Temperatura, top-p y otros parámetros de sampling
- [ ] Limitaciones: alucinaciones, cut-off de conocimiento, sesgos
- [ ] Panorama de modelos: OpenAI, **Anthropic (Claude)**, Gemini, open-source

## 6.2 Prompt Engineering (formal)
- [ ] Estructura de prompts, roles (system/user/assistant)
- [ ] Few-shot, chain-of-thought, ReAct
- [ ] Técnicas de robustez y consistencia
- [ ] Plantillas y versionado de prompts

## 6.3 APIs de LLM (consolidar — ya las usas)
- [ ] OpenAI API / Azure OpenAI (tu experiencia directa)
- [ ] **Anthropic API** (Claude) — ya lo usas con Claude Code
- [ ] Chat Completions, manejo de tokens y costos
- [ ] Manejo de rate limits, reintentos, streaming

## 6.4 Structured outputs, function calling y tool use ★
- [ ] Salidas estructuradas (JSON mode, structured outputs)
- [ ] Function calling / tool use (cómo el LLM invoca herramientas)
- [ ] Validación de salidas (pydantic/zod)
- [ ] **MCP (Model Context Protocol)** — ya lo tienes, es un skill *raro y valioso*. Profundiza: servidores MCP, integración con Claude

## 6.5 Embeddings y búsqueda semántica
- [ ] Qué son los embeddings, similitud de coseno
- [ ] Casos de uso: búsqueda semántica, clasificación, deduplicación
- [ ] Modelos de embeddings (OpenAI, open-source / Sentence Transformers)
- [ ] Chunking: estrategias y trade-offs

## 6.6 Vector Databases
- [ ] Qué resuelven, indexación, similarity search
- [ ] **pgvector** (Postgres — encaja con tu stack), **Qdrant**, Chroma
- [ ] **Azure AI Search** (tu experiencia directa — formaliza)
- [ ] Comparación y criterios de elección

## 6.7 RAG a fondo ★ (tu experiencia directa)
- [ ] Arquitectura completa: ingest → chunk → embed → store → retrieve → generate
- [ ] Estrategias de chunking y por qué importan
- [ ] Retrieval avanzado: hybrid search, **reranking**, metadata filtering
- [ ] RAG vs fine-tuning: cuándo cada uno
- [ ] Problemas comunes y cómo depurarlos (lo que ya viviste, ahora con nombre)

## 6.8 AI Agents y orquestación ★
- [ ] Qué es un agente (loop de razonamiento + herramientas)
- [ ] **LangChain** (fundamentos, cuándo sí/cuándo no)
- [ ] **LangGraph** (orquestación de agentes con estado — pedido en ofertas)
- [ ] Patrones: ReAct, multi-agente, human-in-the-loop
- [ ] Formaliza la orquestación que ya haces ad-hoc en n8n

## 6.9 Evaluación y observabilidad de LLM ★ (lo que casi nadie hace bien)
- [ ] Por qué evaluar es lo más difícil y lo más valorado
- [ ] Métricas de RAG (faithfulness, relevance) con **ragas**
- [ ] Trazabilidad y observabilidad: **LangSmith** / **Langfuse**
- [ ] Datasets de evaluación, regresión de prompts
- [ ] **Este módulo es un diferenciador senior. Inviértele tiempo.**

## 6.10 Modelos open-source y locales (tu homelab es una ventaja)
- [ ] **Ollama** (ya lo usas con DeepSeek-Coder) — formaliza
- [ ] **MLX** en Mac (ya lo configuraste)
- [ ] Hugging Face Hub, cuándo conviene local vs API
- [ ] Cuantización, trade-offs de costo/latencia/privacidad

## 6.11 Multimodal (tu interés en STT/voz encaja)
- [ ] Speech-to-Text: **Whisper**, Voxtral (ya los investigaste)
- [ ] Text-to-Speech, vision (image understanding), OCR/IDP
- [ ] Tu experiencia con **Azure Document Intelligence** aplica aquí

## 6.12 Fine-tuning (nociones)
- [ ] Cuándo fine-tuning vs RAG vs prompting
- [ ] Preparación de datasets, fine-tuning de modelos pequeños
- [ ] LoRA / PEFT (concepto)

## 6.13 AI Safety, seguridad y costos
- [ ] **Prompt injection** y cómo mitigarla (crítico en producción)
- [ ] Moderación, constrains de input/output, PII
- [ ] Gestión de tokens y costos en producción
- [ ] Privacidad y datos sensibles (encaja con tu enfoque local-first)

## 6.14 LLMOps / IA en producción ★
- [ ] Caching de respuestas, fallbacks entre modelos
- [ ] Monitoreo de costos, latencia y calidad en vivo
- [ ] Versionado de prompts y modelos, despliegue seguro
- [ ] Arquitectura de una app de IA escalable

### 🛠️ Proyecto Fase 6 — *Plataforma RAG de producción (capstone IA)*
> Una app RAG completa y sólida: ingest de documentos → vector DB → retrieval con reranking → generación con streaming → **evaluación con ragas** → observabilidad con Langfuse → desplegada con CI/CD. Idea con sentido para tu carrera: un asistente sobre tu **base de conocimiento SN2** o sobre documentación técnica. **Este es el proyecto estrella de tu CV.**

---

# FASE 7 — Automatización y Orquestación ★ (tu otro pilar)

> 🎯 **Objetivo:** formalizar y elevar tu experiencia de automatización (n8n, enrolamiento HubSpot→SII, dashboards) a ingeniería de integración y orquestación de nivel profesional.
> 💰 **Por qué importa:** es la otra mitad de tu título ("Automation Engineer") y combinada con IA te posiciona en un nicho con poca competencia y alta demanda corporativa.

## 7.1 Automatización de workflows (n8n a fondo — ya lo usas)
- [ ] Patrones de diseño de workflows robustos (idempotencia, reintentos, manejo de errores)
- [ ] Nodos custom, expresiones, sub-workflows
- [ ] n8n self-hosted (ya lo administras — documenta como skill)

## 7.2 Ingeniería de integración
- [ ] Webhooks, polling, eventos
- [ ] Integración de APIs de terceros (Zendesk, HubSpot, etc. — tu experiencia)
- [ ] Manejo de autenticación entre sistemas (API keys, OAuth)
- [ ] Diseño event-driven (productores/consumidores)

## 7.3 De RPA a código (tu proyecto real en iConstruye)
- [ ] Cuándo automatizar con código vs low-code vs RPA
- [ ] Migración de procesos legados a soluciones mantenibles
- [ ] Documentación de procesos (BPMN/UML — aparece en ofertas)

## 7.4 Pipelines de datos / ETL (generaliza tu experiencia en Fabric)
- [ ] Conceptos ETL/ELT (ya los hiciste con PySpark en Fabric)
- [ ] Orquestadores: **Airflow** / **Prefect** (estándar de mercado)
- [ ] Nociones de dbt, calidad de datos
- [ ] Pipelines que alimentan sistemas de IA (ingest para RAG)

## 7.5 Agentes de automatización con IA ★ (la convergencia)
- [ ] Combinar workflows + LLMs (n8n + agentes)
- [ ] Automatización inteligente: clasificación, extracción, routing con IA
- [ ] Tu experiencia de OCR + clasificación (AutoML) reformulada como IDP moderno

### 🛠️ Proyecto Fase 7 — *Automatización end-to-end con IA*
> Un sistema que reciba input (email/documento/ticket), lo procese con IA (clasifique/extraiga), tome decisiones y ejecute acciones en sistemas externos. Inspírate en tu flujo real de enrolamiento o en la curaduría de la KB. Demuestra los **dos pilares** de tu perfil a la vez.

---

# FASE 8 — System Design y Arquitectura (rumbo a senior)

> 🎯 **Objetivo:** pensar a nivel de sistema, no solo de feature. Es lo que separa semi-senior de senior y lo que se evalúa en entrevistas de roles mejor pagados.
> 💰 **Por qué importa:** Microservicios (24%) y arquitectura son el techo salarial. Empieza ahora aunque lo domines después del próximo trabajo.

## 8.1 Fundamentos de System Design
- [ ] Escalabilidad horizontal/vertical, load balancing
- [ ] Caching, CDNs, bases de datos a escala (réplicas, sharding — nociones)
- [ ] Consistencia vs disponibilidad (teorema CAP, intuición)
- [ ] Diseño de APIs a escala, rate limiting, idempotencia

## 8.2 Arquitectura de aplicaciones
- [ ] Arquitectura en capas, **Clean Architecture**, hexagonal
- [ ] Nociones de **DDD** (Domain-Driven Design)
- [ ] Monolito modular vs **microservicios** (cuándo cada uno)
- [ ] Comunicación entre servicios (REST, colas, eventos, **Kafka** nociones)

## 8.3 Arquitectura de sistemas de IA (tu especialización a nivel senior)
- [ ] Diseñar un sistema RAG/agente para escala y costo
- [ ] Separación de responsabilidades en apps de IA
- [ ] Estrategias de fallback, caching semántico, multi-modelo
- [ ] Trade-offs de latencia, costo y calidad en producción

### 🛠️ Ejercicio Fase 8 — *Diseña 3 sistemas en papel*
> Documenta el diseño (diagramas + decisiones) de: (1) una plataforma RAG multi-tenant, (2) un sistema de automatización de tickets con IA, (3) un pipeline de datos para IA. Usa Mermaid (ya lo manejas). Sin código — solo arquitectura y justificación.

---

# FASE 9 — Portafolio, marca y empleabilidad

> 🎯 **Objetivo:** convertir todo lo anterior en ofertas de trabajo concretas en tu banda salarial. Esto corre **en paralelo** desde el inicio.
> 💰 **Por qué importa:** el mejor stack no sirve si no sabes mostrarlo. Aquí están los multiplicadores de sueldo reales.

## 9.1 Portafolio de proyectos (la prueba de seniority)
- [ ] **Proyecto 1:** Plataforma RAG de producción (Fase 6)
- [ ] **Proyecto 2:** Automatización end-to-end con IA (Fase 7)
- [ ] **Proyecto 3:** **HomeBase** como fullstack+IA completo (TS, Next.js, tests, CI/CD, feature IA)
- [ ] Cada uno con README impecable, demo en vivo y arquitectura documentada

## 9.2 GitHub profesional (`acme`)
- [ ] Perfil README atractivo, repos limpios y documentados
- [ ] Commits consistentes (este repo de estudio ya aporta a eso)
- [ ] Pin de los 3 proyectos capstone

## 9.3 CV y posicionamiento
- [ ] Reorientar el encabezado a **"AI / Automation Engineer"** (no Fullstack Jr)
- [ ] Traducir tu experiencia a logros medibles (no tareas)
- [ ] LinkedIn alineado, optimizado para reclutadores de remoto

## 9.4 Inglés B2 → C1 ⚡ (el multiplicador más rentable)
- [ ] Práctica de conversación técnica (entrevistas en inglés)
- [ ] Reading/listening técnico avanzado
- [ ] **Impacto: B2 fluido suma ~35–45% y C1 ~50%+ al sueldo base; abre el mercado remoto-USD**

## 9.5 Preparación de entrevistas
- [ ] Live coding sin IA (vuelve a la Regla del Primero-Sin-IA)
- [ ] Preguntas de system design (Fase 8)
- [ ] Preguntas específicas de IA (RAG, agentes, evaluación)
- [ ] Behavioral / STAR, negociación salarial

## 9.6 Estrategia de postulación
- [ ] Apuntar a roles **IA/Automatización** (donde ya eres semi-senior), no fullstack-junior
- [ ] Priorizar empresas con pago en USD / remoto internacional (GetOnBoard, etc.)
- [ ] Mantener actualizado tu documento de demanda por stack

---

## 🎓 Cómo se ve "Senior" (tu objetivo post-próximo-trabajo)

No llegas a senior solo con más temas — llegas con **juicio**. Después de tu próximo rol, lo que te hará senior es:
- [ ] Diseñar sistemas de IA completos y defender los trade-offs (costo/latencia/calidad)
- [ ] Tomar decisiones de arquitectura y justificarlas ante un equipo
- [ ] Mentorear a otros y liderar técnicamente (ya lideraste soporte — recupera ese músculo)
- [ ] Ownership de producto: del problema de negocio a la solución en producción
- [ ] Profundidad real en evaluación/observabilidad de IA (lo que casi nadie domina)
- [ ] Inglés C1 y presencia en la comunidad (charlas, escritos, open-source)

**El plan de 18–24 meses:** este roadmap te lleva a semi-senior empleable (~9–12 meses). El próximo trabajo te da el contexto de producción a escala. Senior es la suma de ambos + el juicio que solo da resolver problemas reales con responsabilidad.

---

## 📚 Recursos base por área (verifica que sigan vigentes al usarlos)

- **Fundamentos/CS:** roadmap.sh, CS50 (Harvard), MDN Web Docs
- **Python:** docs oficiales, Real Python, "Fluent Python" (libro)
- **TypeScript:** TS Handbook oficial, "Total TypeScript" (Matt Pocock)
- **Backend:** FastAPI docs, NestJS docs
- **Frontend:** React docs (react.dev), Next.js docs, Vercel AI SDK docs
- **Testing:** docs de pytest, Vitest, Playwright
- **DevOps:** docs de Docker, GitHub Actions, Terraform
- **AI Engineering:** docs de OpenAI/Anthropic/Azure OpenAI, LangChain/LangGraph docs, "AI Engineering" (Chip Huyen, libro), curso de DeepLearning.AI
- **RAG/Eval:** docs de ragas, Langfuse, LlamaIndex
- **System Design:** "Designing Data-Intensive Applications" (libro), ByteByteGo

> Mantén una lista viva de recursos en cada carpeta de sub-unidad (`articulos.md`). Prefiere **documentación oficial** por sobre tutoriales sueltos.

---

## ✅ Tablero rápido de fases

- [ ] **Fase 0** — Reconstrucción de fundamentos y autonomía
- [ ] **Fase 1** — Lenguajes núcleo (Python + TypeScript)
- [ ] **Fase 2** — Ingeniería de software
- [ ] **Fase 3** — Bases de datos y Backend
- [ ] **Fase 4** — Frontend
- [ ] **Fase 5** — DevOps, Cloud y despliegue
- [ ] **Fase 6** — AI Engineering ★
- [ ] **Fase 7** — Automatización y Orquestación ★
- [ ] **Fase 8** — System Design y Arquitectura
- [ ] **Fase 9** — Portafolio y empleabilidad

---

> *"No se trata de no usar IA. Se trata de no necesitarla para pensar."*
> — Principio rector de este repositorio.
