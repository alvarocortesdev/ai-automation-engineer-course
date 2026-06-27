---
ejercicio_id: fase-6/diagnostico-rag
fase: fase-6
sub_unidad: "6.7"
version: 1
---

# Rúbrica — Diagnóstico de un RAG que falla + elección de técnica

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica. Lo que se evalúa no es "acertar la palabra clave" (hybrid/Contextual/Graph) sino el **razonamiento**: que el alumno ubique la etapa donde nace la falla, que **descarte** alternativas con una razón, y que diga **cómo lo mediría**. Un diagnóstico correcto sin "cómo lo mido" es media respuesta: en producción se diagnostica con datos, no con corazonadas.

## Objetivos evaluados

- **O1** — Ubicar la causa raíz en la etapa correcta del pipeline.
- **O2** — Elegir la técnica que arregla cada falla, descartando alternativas con razón.
- **O3** — Decidir HNSW vs IVFFlat por la restricción dominante y diseñar un filtro fail-closed.

## Criterios y niveles

### C1 — Diagnóstico (etapa + causa raíz) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Confunde la etapa: culpa al LLM o al prompt cuando la falla es de retrieval; o "subiría el top-k" como respuesta a todo. |
| **en-progreso** | Acierta la etapa en uno o dos casos pero en otro diagnostica al revés (de generación hacia arriba). |
| **competente** | Ubica las tres causas en la etapa correcta y aplica el orden recall → ranking → generación. |
| **excelente** | Explica *por qué* ese orden (no tiene sentido tocar el reranker si el chunk no está siquiera en el top-150) y lo nombra como hábito de diagnóstico. |

### C2 — Elección de técnica con trade-off · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Elige técnica sin justificar, o elige la más sofisticada "porque es mejor" (GraphRAG para un hecho puntual). |
| **en-progreso** | Elige la técnica correcta pero **no descarta** ninguna alternativa, o el descarte es vago. |
| **competente** | Para cada caso: técnica correcta + al menos una alternativa descartada con razón + cómo lo mediría (métrica concreta). |
| **excelente** | Razona el **costo/latencia** de la técnica (Contextual = costo de ingest una vez; reranking/Agentic/Graph = costo por query) y por qué no sobre-aplica. |

### C3 — Decisiones de índice y seguridad · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | HNSW vs IVFFlat al azar o sin razón; filtro de seguridad fail-open o "confío en el LLM". |
| **en-progreso** | Elige índice con una razón parcial; propone filtrar pero no lo llama fail-closed ni explica el incidente. |
| **competente** | HNSW por recall + RAM disponible + inserciones dinámicas; nombra qué cambiaría con RAM escasa (IVFFlat). Filtro fail-closed con el incidente de fuga descrito. |
| **excelente** | Menciona que IVFFlat se degrada con inserciones sin re-entrenar los clusters; propone pre-filtrar en la DB por costo; conecta el fail-closed con OWASP LLM / control de acceso. |

## Errores típicos a marcar

- **Diagnosticar de abajo hacia arriba**: tocar el prompt o el LLM antes de verificar si el chunk correcto está siquiera recuperado (recall@k).
- **"Subir el top-k" como cura universal**: mete ruido, dispara costo, empeora por _lost in the middle_.
- **Caso A** resuelto con "mejor modelo de embeddings" en vez de **hybrid search** (BM25 para el identificador exacto).
- **Caso B** resuelto con "subir el top-k" o "reranking" en vez de atacar el **chunk sin contexto** (Contextual Retrieval / documento padre). El reranking no arregla un chunk que es ambiguo en sí mismo.
- **Caso C** resuelto con hybrid o reranking; es multi-hop / relacional → **GraphRAG o Agentic RAG**.
- Sobre-aplicar GraphRAG/Agentic a casos de hecho puntual.
- No decir **cómo se mide** (sin recall@k, sin faithfulness): diagnóstico sin instrumento.
- Filtro de seguridad **fail-open** o delegado al LLM ("le digo que no mencione otros clientes").

## Señales de dependencia-IA

> Indicios de que el alumno usó IA para *pensar* en vez de *aprender*. Describir sin acusar; proponer verificación.

- Respuesta que enumera las cinco técnicas con definiciones de manual pero **no las mapea** correctamente a cada síntoma.
- Vocabulario sofisticado (HNSW, RRF, reranking) sin poder explicar **por qué** Contextual arregla el Caso B y no el reranking.
- Las tres respuestas suenan idénticas en estructura y registro, sin las dudas/tachones propios de un razonamiento a mano.
- **Verificación sugerida:** pídele que, en voz alta, dé el orden de diagnóstico para un síntoma nuevo ("el RAG cita el documento equivocado"). Si interiorizó el árbol, parte por "¿está el chunk correcto en lo recuperado?"; si dependió de la IA, salta a soluciones sin diagnosticar.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca incluir la solución completa.**

- **Pista (nivel 1):** "En el Caso B, los chunks ya son del tema correcto y aun así la respuesta es vaga. ¿Crees que el problema es *traer otros chunks* (retrieval) o *qué dice cada chunk en sí mismo* (su contenido)? Eso cambia la técnica."
- **Pregunta socrática (nivel 2):** "Si el chunk dice 'la empresa creció 3%' sin nombrar la empresa, ¿un reranker que lo lee junto a la pregunta puede saber de qué empresa habla? ¿Qué tendría que pasar en el *ingest* para que ese chunk dejara de ser ambiguo?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El Caso A es un identificador exacto: la semántica no engancha 'E_4521'. La palanca es agregar BM25 al retrieval (hybrid + RRF). Para medirlo, recall@k: ¿aparece el chunk de E_4521 entre los k recuperados antes y después de añadir BM25?"

## Conexión con el proyecto / capstone

- Este diagnóstico es la **defensa de diseño** del **Capstone F6 (Plataforma RAG)**: el "qué técnicas uso y por qué descarto las otras" es un ADR del proyecto, y el "cómo lo mido" es el [eval harness](/fase-6-ai-engineering/6-9-eval-driven-development/) que cierra el Definition of Done. Quien sabe diagnosticar antes de construir no quema semanas subiendo el top-k a ciegas.
