---
ejercicio_id: fase-8/estimacion-capacidad-cuello-botella
fase: fase-8
sub_unidad: "8.1"
version: 1
---

# Rúbrica — Estimación de capacidad y diagnóstico de cuello de botella

> Rúbrica **analítica** para un ejercicio **a-mano** de razonamiento. Lo que se evalúa es la
> **calidad del razonamiento con números**, no la prosa ni que el resultado coincida al decimal. Dos
> alumnos pueden llegar a QPS pico distintos con factores de pico distintos: ambos pueden estar
> **competentes** si declararon y justificaron el supuesto. El corrector **no** entrega el análisis:
> guía con pistas hasta que el alumno lo reconstruya.

## Objetivos evaluados

- **O1** — Estimar capacidad (DAU → QPS promedio → QPS pico → concurrencia con Little), mostrando la aritmética.
- **O2** — Identificar el recurso que se satura primero (compartido y no clonable) con su métrica de saturación.
- **O3** — Proponer un plan de escala ordenado por costo/beneficio, cada paso con su trade-off.
- **O4** — Identificar un punto CAP y defender C vs A como decisión de negocio.

## Criterios y niveles

### C1 — Estimación de capacidad · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay aritmética, o solo da el QPS promedio sin pico, o no calcula concurrencia. |
| **en-progreso** | Calcula QPS pero usa el **promedio** para dimensionar (olvida el factor de pico), o aplica mal la ley de Little (sobre el promedio, no el pico). |
| **competente** | DAU → requests/día → QPS promedio → **QPS pico** (factor declarado y justificado) → **concurrencia** = tasa pico × latencia. Aritmética mostrada y coherente. |
| **excelente** | Además ata la concurrencia a un recurso concreto (p. ej. "190 en vuelo contra un pool de 30 conexiones") y nota el ratio lecturas/escrituras como dato que guiará el plan. |

### C2 — Diagnóstico del cuello de botella · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Dice "la CPU" o "los servidores" sin más, o no identifica ningún cuello. |
| **en-progreso** | Sospecha de la DB pero no explica por qué la app (stateless) no es el cuello, o no nombra una métrica. |
| **competente** | Identifica la **base de datos primaria** (recurso compartido, no clonable, sin réplicas ni caché) como cuello, distingue que la capa de app es clonable, y nombra la métrica de saturación que lo confirmaría (USE: saturación del pool/CPU de la DB; RED: duración subiendo). |
| **excelente** | Señala además que el **connection pool (30)** se satura antes que la CPU de la DB dada la concurrencia calculada, y razona el orden de saturación. |

### C3 — Plan de escala con trade-offs · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Una sola intervención, o "comprar una DB más grande" como primera/única opción (escala vertical sin justificar). |
| **en-progreso** | ≥3 intervenciones pero sin ordenar por costo/beneficio, o sin nombrar trade-offs. |
| **competente** | ≥3 intervenciones **ordenadas** (típico: caché de lecturas → réplicas de lectura → escalar app horizontal), cada una con su trade-off explícito (caché: obsolescencia/invalidación; réplicas: replication lag). |
| **excelente** | Cuantifica el impacto de la caché (un hit ratio razonable quita ~X% de carga de lectura de la DB) y justifica por qué va **antes** que las réplicas (más barata, mayor impacto). |

### C4 — Decisión CAP · mapea: O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona CAP, o lo enuncia como "elige 2 de 3". |
| **en-progreso** | Enuncia CAP correctamente pero no lo aterriza a un punto del sistema, o no defiende la elección. |
| **competente** | Señala un punto real (p. ej. contador de comentarios/votos, o consistencia de un comentario recién publicado entre réplicas) y elige C o A **justificándolo como decisión de negocio**. |
| **excelente** | Reconoce que distintos puntos del sistema pueden elegir distinto (el feed tolera AP; una acción de moderación quiere CP) y lo deja en un ADR. |

### C5 — Comunicación (diagrama + claridad)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin diagrama, o el diagrama no refleja el plan propuesto. |
| **competente** | Diagrama Mermaid que renderiza, refleja el sistema escalado y anota el presupuesto de latencia por salto. |
| **excelente** | El diagrama distingue lecturas (caché/réplicas) de escrituras (primaria) y el presupuesto p99 suma de forma coherente. |

## Errores típicos a marcar

- Dimensionar con el **QPS promedio** en vez del **pico** (subdimensiona; es el error #1).
- Asumir que el cuello es la **CPU de la app** sin notar que es clonable y que la DB es el recurso único.
- "Más servidores = más rápido": confundir throughput con latencia (escalar horizontal no baja la latencia de un request lento).
- Proponer escala **vertical** ("una DB más grande") como primera opción sin agotar caché/réplicas.
- Tratar la caché como magia: olvidar la **obsolescencia** y el problema de invalidación.
- Olvidar el **replication lag** al proponer réplicas de lectura.
- Enunciar CAP como "elige 2 de 3" (P no es opcional).
- (transversal) No conectar el diagnóstico con una **métrica** (RED/USE) que lo verificaría: diagnóstico sin observabilidad es adivinanza.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- Análisis con vocabulario impecable ("PACELC", "consistent hashing") pero **sin la aritmética**
  concreta sobre los números de `sistema.md` (4M usuarios, 5% DAU, 82 req/usuario, pool de 30).
- Un plan genérico de "caché + réplicas + sharding + microservicios" que no se ancla a este sistema
  (p. ej. propone sharding cuando el volumen claramente cabe en un nodo).
- **Verificación sugerida:** pedir que recalcule el QPS pico y la concurrencia en voz alta con sus
  propios números, y que diga qué pasa con el pool de 30 conexiones bajo esa concurrencia. Si
  estimó de verdad, lo hace al instante.

## Feedback sugerido (graduado)

> Nunca entregar el análisis completo antes de que el alumno cierre su intento.

- **Pista (nivel 1):** "Empieza por convertir DAU en requests/día y luego en QPS. ¿El tráfico es
  uniforme las 24 h? Si no, ¿por cuánto multiplicas para el pico?"
- **Pregunta socrática (nivel 2):** "De tus componentes, ¿cuál puedes duplicar agregando otro igual,
  y cuál es **uno solo** que todos pegan? ¿Cuál crees que se queda sin aire primero, y qué métrica te
  lo confirmaría?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu plan salta a réplicas, pero el 97%
  del tráfico son lecturas a datos que casi no cambian. ¿Qué técnica quita ese 80% de carga de la DB
  casi gratis, y qué precio paga (en frescura del dato)? Ordena por costo/beneficio y nombra el
  trade-off de cada paso."

## Conexión con el proyecto / capstone

- Es el ensayo directo del **capstone de la Fase 8** ("diseña 3 sistemas en papel"): cada uno de los
  3 sistemas debe abrir con esta misma estimación de capacidad antes de dibujar cajas, y cada
  trade-off (caché, réplicas, CAP) se documenta como ADR.
