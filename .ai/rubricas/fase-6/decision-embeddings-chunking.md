---
ejercicio_id: fase-6/decision-embeddings-chunking
fase: fase-6
sub_unidad: "6.5"
version: 1
---

# Rúbrica — Decisión: modelo de embeddings + chunking

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio de diseño: **no hay respuesta única**. El corrector evalúa la **calidad de la justificación y del trade-off**, no que el alumno coincida con la solución de referencia. Una elección distinta a la canónica es **competente** si está bien defendida con la restricción dominante.

## Objetivos evaluados

- **O1** — Elegir un modelo de embeddings (local vs API, dimensiones, idioma) según la restricción dominante.
- **O2** — Diseñar una estrategia de chunking apropiada al tipo de documento.
- **O3** — Identificar el riesgo dominante de cada diseño.

## Criterios y niveles

### C1 — Elección de modelo justificada por la restricción dominante · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige "el mejor" o "el más grande" sin nombrar restricción; o ignora una restricción dura (p. ej. propone una API para datos que no pueden salir de la infra). |
| **en-progreso** | Nombra una restricción pero la decisión no se sigue de ella (dice "privacidad" pero elige API), o no menciona idioma cuando el corpus no es inglés. |
| **competente** | En los tres escenarios identifica la restricción que manda y la decisión de modelo se deriva de ella (local para datos privados; multilingüe para idioma; recorte de dimensiones / modelo barato para costo a escala). |
| **excelente** | Además razona el trade-off con números o consecuencias concretas (dimensiones ↔ RAM/latencia; costo por millón de tokens; "subo a `large` solo si los evals lo exigen") y menciona la regla consulta-y-corpus-mismo-modelo. |

### C2 — Estrategia de chunking apropiada · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Mismo chunking para todo sin pensar el tipo de documento (p. ej. chunks de capítulo para FAQs de 1 frase), o no menciona chunking. |
| **en-progreso** | Propone un tamaño razonable pero sin justificarlo, u olvida el solape donde importa, o no nota que en las FAQs cortas el chunking "no aplica" (cada FAQ ya es un chunk). |
| **competente** | Ajusta el chunking al documento: párrafos con solape para manuales largos; "no aplica / 1 FAQ = 1 chunk" para textos ya cortos; párrafo por producto para dedup. Justifica el tamaño. |
| **excelente** | Conecta el tamaño con la granularidad del retrieval y el costo del contexto (chunk grande = vector borroso + más tokens en RAG), y menciona el solape como protección de ideas-en-el-límite. |

### C3 — Riesgo concreto identificado · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra ningún riesgo, o nombra uno genérico sin relación con el escenario. |
| **en-progreso** | Nombra un riesgo real pero sin mitigación, o lo aplica al escenario equivocado. |
| **competente** | Al menos un riesgo concreto y pertinente con mitigación (p. ej. "los códigos `E_4521` no los encuentra la semántica → hybrid search"; "umbral de dedup fijo sin medir → calibrarlo en el corpus"). |
| **excelente** | Identifica riesgos en los tres escenarios y conecta con conceptos de la lección/curso (hybrid search 6.7, evals 6.9, privacidad/local 6.10). |

## Errores típicos a marcar

- **"El mejor modelo"** sin restricción: la pregunta de un usuario, no de un ingeniero.
- **Proponer una API para datos que no pueden salir de la infra** (viola la restricción dura del escenario 1).
- **Ignorar el idioma**: elegir un modelo solo-inglés para corpus en español/multilingüe.
- **Chunk de capítulo entero para FAQs cortas** (diluye el vector) o **chunkear lo que ya es corto**.
- **Solo búsqueda semántica donde hay identificadores exactos** (códigos, SKUs) sin reconocer la necesidad de hybrid search.
- **Umbral de coseno o de dedup fijo "0.8/0.95"** presentado como universal, sin decir que se calibra en el corpus.
- **Confundir más dimensiones con más calidad** sin notar el costo de RAM/latencia a escala.

## Señales de dependencia-IA

> Indicios de que el alumno usó IA para *pensar* en vez de *aprender*. Describir sin acusar; proponer verificación.

- Decisiones impecables y exhaustivas pero **no puede defender oralmente** por qué eligió local vs API en el escenario 1.
- Menciona modelos o números muy específicos (nombres de modelos recientes, precios exactos) que no calzan con el nivel del resto de su entrega ni con la lección.
- Las tres respuestas suenan a plantilla idéntica sin adaptarse a las diferencias reales de cada escenario.
- **Verificación sugerida:** pídele que, en una frase y sin notas, diga qué cambiaría en el escenario 2 si los datos **sí** fueran sensibles. Si entendió, salta a "local / self-hosted" al instante; si dependió de la IA, titubea.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca incluir la solución completa.**

- **Pista (nivel 1):** "En el escenario 1 elegiste bien el idioma. Vuelve a leer la frase 'los datos no pueden salir de la infraestructura': ¿qué te dice eso sobre usar una API externa?"
- **Pregunta socrática (nivel 2):** "Tu buscador del escenario 1 usa solo coseno. Un usuario busca el código `E_4521`. ¿Crees que el embedding lo distingue de otros 'errores' parecidos? ¿Qué otra técnica de búsqueda lo encontraría exacto?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Para datos privados, la restricción dominante es privacidad → modelo local (Sentence Transformers self-hosted), no API. Y donde hay identificadores exactos, combina semántica con palabra clave (hybrid search): la semántica encuentra el concepto, BM25 encuentra el código literal."

## Conexión con el proyecto / capstone

- Estas decisiones son, literalmente, los **ADRs** de la fase de ingest del Capstone F6 (Plataforma RAG): qué modelo de embeddings, qué chunking, y por qué. Defender el trade-off aquí es el ensayo de defenderlo frente al revisor del capstone y frente a un entrevistador.
