---
ejercicio_id: fase-7/cdc-arquitectura-frescura
fase: fase-7
sub_unidad: "7.6"
version: 1
---

# Rúbrica — ¿CDC o batch? Diseña la frescura de dos RAGs

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. Es un ejercicio de **diseño/criterio**: se evalúan las decisiones y su justificación, no la prosa. **Nunca entregar la solución de referencia.**

## Objetivos evaluados

- **O1:** Decidir batch incremental vs CDC+streaming por la **causa** (freshness, volumen, costo operativo), no por la moda.
- **O2:** Elegir kappa vs lambda y explicar el replay/reproceso del histórico.
- **O3:** Ubicar table format (Iceberg/Delta) y medallion; manejar los 4 modos de falla (orden, deletes, backfill, evento venenoso).

## Criterios y niveles

### C1 — Decisión por la causa (batch vs CDC), distinta para A y B · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige lo mismo para A y B, o "CDC siempre porque es mejor/más moderno", sin atarse al volumen ni a la freshness. |
| **en-progreso** | Distingue A de B pero la justificación es superficial ("B es más grande") sin cruzar freshness × volumen × costo operativo. |
| **competente** | A → batch incremental (pocos cambios/día, latencia de minutos OK; pero resuelve el delete explícito); B → CDC+streaming (volumen altísimo + freshness en segundos + plata en juego). Cada una justificada por su causa. |
| **excelente** | Lo anterior + reconoce explícitamente que CDC en A sería **over-engineering** y pone el criterio en una regla reutilizable (cruce freshness × razón-de-cambio). |

### C2 — kappa/lambda + replay · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No elige, o confunde kappa con "lo nuevo" y lambda con "lo viejo" sin entender batch+speed vs un solo camino. |
| **en-progreso** | Elige kappa pero no explica el replay (cómo re-indexaría al cambiar de modelo de embeddings). |
| **competente** | Elige kappa para CDC→RAG con argumento (un solo camino, log re-procesable) y explica re-indexar vía **replay** del topic por el mismo consumidor. |
| **excelente** | Lo anterior + reconoce cuándo lambda se justificaría (necesidad de re-procesamiento batch garantizado en paralelo) y el costo de su lógica duplicada. |

### C3 — Table format, medallion y modos de falla · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona modos de falla, o cree que medallion = batch / que un table format siempre hace falta. |
| **en-progreso** | Cubre algunos modos de falla pero deja fuera el **delete** (el más importante para RAG) o el evento venenoso. |
| **competente** | Ubica el table format (gana su sitio en B para replay barato; over-engineering en A) y maneja los 4 modos de falla con un mecanismo concreto cada uno. |
| **excelente** | Lo anterior + conecta cada modo de falla con el concepto de 7.2 (orden→`lsn`, delete→propagar, backfill→replay/snapshot, venenoso→DLQ) y nota que medallion puede vivir dentro del stream. |

## Errores típicos a marcar

- **Misma decisión para A y B** ("CDC para ambos") → no internalizó que CDC es un trade-off, no un default; el costo operativo de Kafka/slots no se justifica con 5 cambios/día.
- **Olvida el DELETE** en los modos de falla → el fantasma en el índice es *el* problema que distingue CDC de polling; omitirlo es el error más grave.
- **kappa por moda** sin explicar el replay → repite la palabra sin entender que el log re-procesable es lo que la hace funcionar.
- **Table format "porque sí"** en el escenario chico → over-engineering; o creer que medallion implica batch.
- **Persigue exactly-once** como si fuera gratis → ignora que idempotencia + at-least-once es el patrón sano.
- (transversales) No menciona costo (USD/freshness) en ninguna decisión; no pone DLQ para el evento venenoso; ignora el riesgo operativo del replication slot que retiene WAL.

## Señales de dependencia-IA

- Diseño que enumera TODAS las herramientas de moda (Iceberg + Delta + Paimon + Flink + RisingWave) sin elegir ni justificar — catálogo en vez de criterio.
- Justificación elocuente que **no calza** con la decisión (defiende CDC para A "por la freshness" cuando el propio enunciado dice que minutos bastan).
- Vocabulario perfecto (kappa, streamhouse, Kappa Plus) sin poder responder "¿y por qué NO usarías CDC en el escenario A?".

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Vuelve a leer el requisito de freshness de cada escenario (minutos vs segundos) y el volumen de cambios. ¿De verdad las dos respuestas deberían ser iguales?"
- **Pregunta socrática (nivel 2):** "Si A cambia 5 veces al día y tolera minutos de latencia, ¿qué te *aporta* Kafka que un job incremental cada pocos minutos no? ¿Y qué te *cuesta* operarlo? Aparte: en A, ¿cómo te enteras de un documento **borrado** si eliges batch?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu cruce es freshness × razón-de-cambio: A (laxa + poco) → batch incremental, con un paso explícito para detectar borrados; B (estricta + muchísimo) → CDC+streaming, kappa (replay del log para re-indexar) y un table format para abaratar ese replay. Para los modos de falla, no inventes: orden con `lsn`, delete propagado, backfill por replay, venenoso a DLQ — son los reflejos de 7.2."

## Conexión con el proyecto / capstone

- Esta decisión es exactamente la que el alumno debe defender en el write-up de trade-offs del capstone de F7 (DoD §8): "usé/no usé CDC porque...". Elegir bien —incluido elegir *no* usar streaming— y justificarlo por la causa es la señal de seniority que el capstone estrella busca.
