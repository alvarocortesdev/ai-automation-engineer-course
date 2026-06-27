---
ejercicio_id: fase-6/fusion-hibrida-rrf
fase: fase-6
sub_unidad: "6.7"
version: 1
---

# Rúbrica — Retrieval híbrido: RRF + metadata filtering fail-closed

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. El objetivo de fondo no es que los tests compilen, sino que el alumno entienda **por qué RRF fusiona por posición y no por score**, por qué el resultado debe ser **determinista** (testeable), y por qué el filtro de metadata es una **frontera de seguridad fail-closed** y no un detalle de relevancia.

## Objetivos evaluados

- **O1** — Fusionar varios rankings con RRF usando la posición (no el score) y de forma determinista.
- **O2** — Filtrar candidatos por metadata con cierre seguro (fail-closed) como frontera de control de acceso.
- **O3** — Componer fusión + filtro + recorte en un retrieval híbrido top-k correcto.

## Criterios y niveles

### C1 — Corrección de RRF · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Suma o promedia los **scores originales** en vez de usar la posición; o usa rank 0-based (`1/(k+0)` para el primero); o no acumula cuando un doc está en varias listas. |
| **en-progreso** | Fórmula RRF correcta (1-based, acumula) pero **no determinista**: no rompe empates, así que el orden de dos docs con igual score varía entre corridas. |
| **competente** | `1/(k+rank)` 1-based, acumulado sobre todas las listas, ordenado descendente con tie-break por `doc_id` ascendente. Pasan los tests de RRF. |
| **excelente** | Además explica **por qué** RRF ignora los scores (coseno y BM25 no son comparables) y por qué el determinismo importa (no se puede testear ni evaluar lo no determinista). |

### C2 — Seguridad del filtrado (fail-closed) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Fail-**open**: un doc al que le falta la clave del filtro **pasa** (p. ej. usa `metadata.get(d, {}).get(c) != valor_prohibido` o asume que la clave existe y revienta/ignora). |
| **en-progreso** | Fail-closed para claves faltantes pero rompe con un doc ausente de `metadata` (KeyError) o no preserva el orden de entrada. |
| **competente** | Fail-closed completo: doc sin la clave **o** ausente de `metadata` no pasa; exige **todas** las claves del filtro; filtro vacío deja pasar todo; preserva orden. Pasan los tests. |
| **excelente** | Nombra, por iniciativa, el riesgo concreto (multi-tenant data leak) y conecta con OWASP LLM / control de acceso del Capstone. |

### C3 — Composición e ingeniería (testing real) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `recuperar_hibrido` reimplementa RRF o el filtro en vez de **reusar** las funciones; o no recorta a `k_final`; no agregó test propio. |
| **en-progreso** | Compone bien pero pierde el score RRF (devuelve solo ids) o revienta si `k_final` > candidatos; test propio trivial. |
| **competente** | Reusa `rrf_fusion` + `filtrar_por_metadata`, devuelve `(doc_id, score)` en orden fusionado recortado a `k_final`; agregó un test borde genuino. |
| **excelente** | El test propio captura un borde razonado (k_final=0, filtro de dos claves donde el doc cumple solo una, listas vacías) y lo explica. |

## Errores típicos a marcar

- **Sumar los scores originales** (coseno + BM25) en vez de usar RRF: los scores no son comparables; ese es el motivo de existir de RRF.
- **Rank 0-based** (`1/(k+0)`): cambia todos los puntajes; el primer puesto debe ser `1/(k+1)`.
- **No acumular** cuando un doc está en varias listas (sobrescribe en vez de sumar) → pierde la ventaja de la fusión.
- **No romper empates** → resultado no determinista; los tests fallan de forma intermitente.
- **Filtro fail-open**: el doc sin la clave pasa. Es el bug de seguridad central del ejercicio; marcarlo aunque "los tests felices" pasen.
- **`recuperar_hibrido` que filtra ANTES de fusionar de forma que pierde el score**, o que reimplementa la lógica en vez de componer.
- (transversal) No añadir el caso borde propio; confiar en que "se ve bien" sin un test que fije el comportamiento.

## Señales de dependencia-IA

> Indicios de que el alumno usó IA para *pensar* en vez de *aprender*. Describir sin acusar; proponer verificación.

- Usa `numpy`/`pandas` o una librería de RRF pese a que el enunciado pide Python puro a mano.
- Implementación impecable pero **no sabe explicar** por qué RRF usa posición y no score, ni por qué el filtro va fail-closed.
- Maneja casos borde exóticos que el enunciado no pide con un estilo que no calza con el resto de su código.
- **Verificación sugerida:** pídele que, sin correr código, diga el orden de `rrf_fusion([["a","b"],["b","a"]])`. Si entendió la acumulación, responde "empatan → `a` antes que `b` por el tie-break" al instante; si dependió de la IA, necesita ejecutar.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca incluir el código de la solución.**

- **Pista (nivel 1):** "Tu fusión corre, pero ¿qué estás sumando: los scores originales o la posición? Recuerda por qué un coseno de 0.7 y un BM25 de 12.3 no se pueden sumar directamente."
- **Pregunta socrática (nivel 2):** "En tu filtro, ¿qué pasa con un documento al que le falta el campo `tenant`? ¿Pasa o no pasa? Si pasara, ¿qué dato podrías estar mostrándole al cliente equivocado?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Para el determinismo, ordena por una tupla `(-score, doc_id)`: el `-score` da el descendente y el `doc_id` rompe empates de forma estable. Sin el segundo término, dos empates pueden salir en cualquier orden y tus tests fallarán a veces."

## Conexión con el proyecto / capstone

- Este motor es el **retrieval híbrido + control de acceso** del **Capstone F6 (Plataforma RAG)**: RRF es cómo fusionas la búsqueda vectorial y la BM25; el filtro fail-closed es la frontera multi-tenant. Quien lo implementó a mano puede diagnosticar por qué su RAG no engancha un identificador exacto (falta BM25) o por qué filtró un chunk del tenant equivocado (filtro fail-open) en vez de quedar a ciegas frente a un framework.
