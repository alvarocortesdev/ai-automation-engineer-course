---
ejercicio_id: fase-6/eleccion-vector-db
fase: fase-6
sub_unidad: "6.6"
version: 1
---

# Rúbrica — Decisión: vector DB + índice + métrica + filtrado

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio de **diseño**: no hay respuesta única. El corrector evalúa la **calidad del trade-off**, no la coincidencia literal con la solución de referencia. El objetivo de fondo: que el alumno **derive** cada decisión de una restricción dominante y reconozca el **riesgo de seguridad** que introduce tener embeddings en una base.

## Objetivos evaluados

- **O1** — Elegir una vector DB según la restricción dominante (no "la mejor").
- **O2** — Justificar HNSW vs IVFFlat por el trade-off velocidad/recall/memoria y la métrica adecuada.
- **O3** — Identificar un riesgo de vector/embedding weakness y su mitigación.

## Criterios y niveles

### C1 — Elección de DB derivada de la restricción · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige "la mejor" o "la más popular" sin restricción; o la misma DB para los tres escenarios sin justificar. |
| **en-progreso** | Nombra una restricción pero la elección no se deriva de ella (p. ej. "ya tienen Postgres" pero elige Qdrant sin razón de escala). |
| **competente** | Cada DB se deriva de una restricción dominante explícita (Postgres existente → pgvector; escala+multi-tenant → dedicada; prototipo → Chroma; Azure managed → Azure AI Search). |
| **excelente** | Reconoce que más de una opción es defendible y justifica el corte; menciona el costo operacional de agregar un sistema nuevo cuando ya hay Postgres. |

### C2 — Índice y métrica justificados · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No elige índice, o dice "HNSW porque es más rápido" sin más; métrica ausente o incoherente. |
| **en-progreso** | Elige índice pero solo por velocidad, sin tocar memoria ni construcción; métrica nombrada pero no justificada. |
| **competente** | Al menos un escenario justifica HNSW vs IVFFlat por **memoria** o **tiempo/datos de construcción**; la métrica (coseno por defecto en texto) es coherente. |
| **excelente** | Menciona que para vectores normalizados el producto interno equivale al coseno y es más barato; o que IVFFlat necesita datos representativos antes de construir. |

### C3 — Riesgo de seguridad del vector store · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona ningún riesgo de seguridad, o solo riesgos genéricos ("hay que tener cuidado"). |
| **en-progreso** | Nombra un riesgo pero sin mitigación, o sin ligarlo al escenario. |
| **competente** | Cada escenario nombra un riesgo concreto (envenenamiento por ingest abierto, fuga por inversión de embeddings, fuga multi-tenant) con una mitigación real. |
| **excelente** | Conecta el riesgo con la decisión técnica (p. ej. multi-tenant → pre-filter server-side o colecciones separadas; wiki editable → validar ingest + tratar lo recuperado como no confiable, enlazando con 6.2/6.14). |

### C4 — Comunicación / defensa (ADR-able) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Decisiones sin justificación; no se podría defender en entrevista. |
| **competente** | Cada decisión tiene 1–2 frases de por qué; usa la plantilla completa. |
| **excelente** | El documento se lee como un ADR: trade-off explícito, alternativa descartada y bajo qué número cambiaría de opinión. |

## Errores típicos a marcar

- "La mejor vector DB es X" sin restricción → no entendió que la elección es contextual.
- Agregar una DB dedicada cuando ya hay Postgres y el volumen es moderado (complejidad regalada).
- HNSW/IVFFlat elegido solo por "velocidad", ignorando memoria y construcción.
- Olvidar el riesgo multi-tenant en el escenario 2 (es **el** punto del escenario).
- Filtrado por tenant tratado como relevancia y no como aislamiento de datos.
- (transversal) ningún trade-off defendible; "depende" sin comprometerse a una decisión.

## Señales de dependencia-IA

- Tres escenarios con prosa sofisticada e idéntica estructura retórica pero **sin** comprometerse a una decisión concreta (hedging tipo "podrías usar cualquiera").
- Menciona herramientas que no salieron en la lección con detalles de tier/precio inventados (alucinación típica).
- **Verificación sugerida:** pídele que defienda en voz alta por qué en el escenario 2 el filtrado por tenant es seguridad y no relevancia. Si lo razonó, lo explica con el ejemplo de "devolver docs de otro cliente"; si lo copió, se queda en generalidades.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca escribir la decisión por el alumno.**

- **Pista (nivel 1):** "Para cada escenario, ¿cuál es la **una** cosa que, si la ignoras, hunde el proyecto? Esa es tu restricción dominante; deja que ella elija la DB."
- **Pregunta socrática (nivel 2):** "En el escenario 2, si dos clientes comparten la misma colección y el filtro por tenant se aplica como post-filter, ¿qué puede ver el cliente A del cliente B?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu elección de HNSW está bien, pero falta el eje memoria: con decenas de millones de vectores el grafo de HNSW es caro en RAM. Decide explícitamente si esa RAM la pagas (HNSW) o si tuneas IVFFlat para ahorrarla, y di bajo qué número cambiarías."

## Conexión con el proyecto / capstone

- Esta decisión es **literalmente** el ADR de almacenamiento del **Capstone F6 (Plataforma RAG)**. El escenario multi-tenant y los riesgos de embedding alimentan la sección de seguridad ([6.14](/fase-6-ai-engineering/6-14-seguridad-llm/)) del Definition of Done, y la elección de índice entra en el budget de costo/latencia ([6.16](/fase-6-ai-engineering/6-16-costo-latencia-llmops/)).
