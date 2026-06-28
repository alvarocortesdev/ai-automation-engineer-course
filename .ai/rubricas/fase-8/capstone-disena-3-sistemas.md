---
ejercicio_id: fase-8/capstone-disena-3-sistemas
fase: fase-8
sub_unidad: "8.P"
version: 1
---

# Rúbrica — Capstone Fase 8: Diseña 3 sistemas en papel

> Rúbrica **analítica** para un **capstone de diseño/razonamiento** (sin código). Lo que se evalúa es el
> **criterio de arquitectura** sobre los tres sistemas —números, trade-offs, aislamiento, HITL, frescura,
> ADRs— **no** si los diagramas coinciden con la solución de referencia. Hay varias arquitecturas
> defendibles; lo que separa un diseño pensado de uno copiado es que **cada caja tiene un número o un
> trade-off detrás**, y que el alumno lo defiende bajo repregunta.
>
> El corrector evalúa los **tres** sistemas. Un capstone con dos sistemas sólidos y uno ausente o vacío
> está, como máximo, `en-progreso`.

## Objetivos evaluados
- **O1** — Diseñar en papel los tres sistemas (RAG multi-tenant, tickets con IA, pipeline de datos), cada
  uno con requisitos, diagrama Mermaid que renderiza y las decisiones que el sistema exige.
- **O2** — Defender cada decisión con un número o un trade-off explícito (qué se sacrifica + alternativa
  descartada).
- **O3** — Registrar las decisiones clave como ADRs y comunicar los diseños de forma defendible sin notas.

## Criterios y niveles

### C1 — Método aplicado a los 3 sistemas (¿hay diseño completo?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta uno o más sistemas, o los diagramas no renderizan / no reflejan un flujo real. Cajas genéricas sin secciones. |
| **en-progreso** | Los tres existen pero alguno está a medias (sin requisitos explícitos, sin "nunca", o diagrama que no compila). El método de los 6 pasos no se nota. |
| **competente** | Los tres sistemas tienen las 6 secciones, diagramas que renderizan, y un "esto no puede pasar nunca" por sistema. Se reconoce el método (requisitos → número → diagrama → cuello de botella → trade-offs → ADR). |
| **excelente** | Además, cada sistema identifica explícitamente su **cuello de botella propio** (RAG = costo/cuota de tokens; tickets = acción irreversible; pipeline = frescura) y el diseño se ordena alrededor de él. |

### C2 — Números de servilleta (¿hay un número, y manda?) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay cálculos, o los diseños no se apoyan en ningún número. |
| **en-progreso** | Da algún número pero la aritmética no se muestra o es incoherente (p. ej. costo/hora del RAG sin escalar por QPS y 3600; "frescura" sin una ventana concreta). |
| **competente** | Muestra la aritmética en los tres: RAG → costo/hora a 50 QPS; tickets → reembolsos/día y aprobaciones HITL/día (contrastadas con la capacidad humana); pipeline → throughput + **ventana de frescura** numérica. |
| **excelente** | Usa el número para **priorizar/decidir**: el costo del RAG ordena las intervenciones de ahorro; las aprobaciones/día validan que el HITL no se vuelve cuello humano; la ventana de frescura decide entre CDC incremental y rebuild nocturno. |

### C3 — Seguridad en el diseño (OWASP web + LLM/Agentic) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No aborda aislamiento de tenants ni guardrails; propone que el LLM ejecute acciones directamente. |
| **en-progreso** | Menciona un filtro `tenant_id` o un guardrail, pero como algo opcional; no nombra el riesgo ni el "fail-closed". |
| **competente** | **S1:** filtro `tenant_id` **obligatorio** tratado como seguridad. **S2:** reparto "LLM propone / código dispone" + guardrail de schema + HITL para lo irreversible. **S3:** validación de datos en la frontera (data contracts). |
| **excelente** | Blinda de verdad: filtro fail-closed (parte de la firma, test negativo) e índice dedicado para tenants regulados (S1); HITL para acción sensible **aunque la confianza sea 0.99** + least-privilege (S2); aísla documentos corruptos sin tumbar la corrida (S3). Enmarca con vocabulario OWASP (LLM01/05/06, vector weaknesses). |

### C4 — Eval / observabilidad / frescura pensadas (hilos transversales) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona evals, trazas ni estrategia de frescura. |
| **en-progreso** | Las menciona de pasada sin ubicarlas en el diseño ("habría que monitorear"). |
| **competente** | Ubica trazas (tokens/latencia/costo por paso) en S1/S2; un **eval gate** en S2 (qué métrica: routing/extracción correcta); tests de calidad (frescura/volumen/schema drift) en S3. |
| **excelente** | El eval gate de S2 dice **de dónde sale el golden set** (trazas reales) y que **bloquea el deploy** ante regresión; S3 versiona el modelo de embeddings con blue/green del índice y nombra qué pasa cuando el modelo cambia. |

### C5 — Trade-offs + ADRs (juicio de ingeniería) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay trade-offs defendidos ni ADRs, o son afirmaciones ("uso lo mejor") sin sacrificio nombrado. |
| **en-progreso** | Algún trade-off suelto sin número; ADR ausente o sin las tres partes. |
| **competente** | **≥ 2 trade-offs por sistema**, cada uno nombrando qué sacrifica y su impacto; **un ADR por sistema** con Contexto/Decisión/Consecuencias. |
| **excelente** | Cada ADR nombra la **alternativa descartada** y la **consecuencia negativa aceptada**; los trade-offs se defienden como decisiones de **negocio** (no "porque es mejor") y aguantan la opción contraria. |

### C6 — Comunicación defendible (senior) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Documentos confusos, sin estructura, o que no se podrían presentar. |
| **en-progreso** | Legibles pero sin foco; mezclan niveles de detalle; no se distingue la decisión clave del relleno. |
| **competente** | Los tres documentos son claros, estructurados en las 6 secciones, y honestos sobre sus límites. |
| **excelente** | Defendibles **en voz alta sin notas** y bajo repregunta; el alumno puede recitar el método y aplicarlo a un sistema fuera del capstone. (Inglés técnico en el write-up = señal de Track-0 interiorizado.) |

## Errores típicos a marcar
- **Diagramas sin números:** cajas bonitas, cero aritmética detrás (el error #1 de esta ronda).
- **"Usa siempre el mejor modelo"** (S1): ignora el ruteo; quema costo donde la calidad no cambia.
- **Filtro `tenant_id` opcional** (S1): tratado como relevancia, no como seguridad fail-closed.
- **Confianza alta = auto-ejecutar el reembolso** (S2): la confianza auto-reportada no es probabilidad
  calibrada; la acción irreversible va a HITL siempre (LLM06).
- **Idempotencia tardía o ausente** (S2): no es el primer chequeo; el agente "nuevo" igual hereda
  at-least-once.
- **Eval gate que mide fluidez** (S2): debe medir **decisión correcta** (routing/extracción), no prosa.
- **Pipeline que "termina" en la vector DB** (S3): no define ventana de frescura ni qué pasa al cambiar el
  documento fuente o el modelo de embeddings.
- **Re-embedding total sin justificar** (S3): elige rebuild nocturno o CDC sin contrastar costo vs
  frescura con un número.
- **ADR sin alternativa descartada:** es una preferencia, no una decisión.
- (transversal) Confundir caché semántico con prompt caching; cola en el chat interactivo; cambiar de
  modelo sin eval gate.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.
- Tres diseños exhaustivos y vocabulario impecable, pero **sin los números específicos** de cada spec
  (50 QPS y 45% en S1; reembolsos/día y capacidad humana en S2; ventana de frescura y 5.000 cambios/día
  en S3).
- ADRs que enumeran "consecuencias" sin nombrar la alternativa descartada ni el costo aceptado.
- Prosa genérica intercambiable entre sistemas; el cuello de botella propio de cada uno no aparece.
- **Verificación sugerida:** pide cambiar un número de una spec (p. ej. la ventana de frescura de S3 de
  24 h a 5 min, o 3 → 30 tenants regulados en S1) y rehacer la decisión. Si razonó, la decisión cambia y
  lo justifica; si dependió de la IA, repite el mismo diseño. O pídele que aplique los 6 pasos a un
  sistema nuevo en voz alta ("diseña un acortador de URLs").

## Feedback sugerido (graduado)
> Nunca dar el diseño antes de que el alumno cierre su intento. Hay varias arquitecturas válidas.
- **Pista (nivel 1):** "Empieza por el número de cada sistema antes de dibujar. ¿Cuánto cuesta una hora
  de RAG a 50 QPS sin caché? ¿Cuántas aprobaciones HITL al día generan los reembolsos, y aguanta eso tu
  equipo? ¿Cuál es la ventana de frescura del pipeline? Sin esos números no sabes qué optimizar."
- **Pregunta socrática (nivel 2):** "En el sistema 2, si el webhook del mismo ticket llega dos veces y
  además es un reembolso, ¿qué barrera de tu plano de control actúa primero y por qué? Si tu respuesta no
  es 'la idempotencia, antes que nada de IA', repasa el orden de los chequeos."
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa que cada caja de tus tres diagramas
  tenga un número o un trade-off. En cada ADR, nombra explícitamente la alternativa que descartaste y la
  consecuencia negativa que aceptas. Y para el pipeline, decide CDC incremental vs rebuild nocturno
  poniendo lado a lado el costo del re-embedding total y la ventana de frescura que propusiste."

## Conexión con el proyecto / capstone
- Este **es** el capstone de la Fase 8 y el ensayo directo de la ronda de system design de Track-0
  (mock interviews en inglés, system design en ~40 min). Integra 8.1 (capacidad/cuellos de botella),
  8.2 (límites/DDD), 8.5 (arquitectura de IA a escala), 7.7/7.2 (agente confiable) y 7.5x/7.6 (data
  engineering + frescura). Los tres documentos son piezas de portafolio defendibles, no un trámite.
