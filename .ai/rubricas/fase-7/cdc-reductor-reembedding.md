---
ejercicio_id: fase-7/cdc-reductor-reembedding
fase: fase-7
sub_unidad: "7.6"
version: 1
---

# Rúbrica — Reductor CDC → tareas de re-embedding

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. **Nunca entregar el código de la solución de referencia.**

## Objetivos evaluados

- **O1:** Leer un change event (op c/u/d/r, before/after) y mapear cada operación a una acción de vector DB (upsert/delete).
- **O2:** Implementar un reductor idempotente y debounced (colapsar a la intención final, propagar deletes, no re-embeddear contenido idéntico) — el trade-off costo/freshness.
- **O3:** Argumentar por qué un consumidor CDC debe ser idempotente (at-least-once) y cómo convive con replay/reproceso.

## Criterios y niveles

### C1 — Corrección: el reductor produce las tareas mínimas correctas · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `pytest -v` no llega a verde; no colapsa (emite una tarea por evento), o intenta leer `after["contenido"]` en un `d` y revienta (`TypeError`). |
| **en-progreso** | Pasa algunos casos pero falla alguno clave: no propaga el delete, o emite tarea para la fila que nace-y-muere, o no respeta el orden por key. |
| **competente** | Las 7 reglas correctas; una sola tarea por key (debounce); deletes propagados solo si estaban indexados; lista ordenada por key; todos los tests provistos en verde. |
| **excelente** | Lo anterior + idempotencia verificada con un test propio (tanda ×2 == tanda ×1), tombstones tolerados, y/o resumen tipo métrica para observabilidad. |

### C2 — Calidad de ingeniería: tests reales + caso borde propio · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó ningún test propio; o "arregló" un test rojo cambiando el dato del test en vez de la lógica. |
| **en-progreso** | Agregó un test trivial que re-testea un caso ya cubierto. |
| **competente** | Agregó ≥1 test de caso borde con valor real (tanda vacía, solo metadata cambia, mezcla de keys con y sin cambio). |
| **excelente** | Tests que aíslan bien (un caso = una regla), nombres claros, y un test que verifica explícitamente la **idempotencia** (la tanda dos veces). |

### C3 — Comprensión demostrada: idempotencia y costo · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay WRITEUP, o no sabe por qué el reductor debe ser idempotente. |
| **en-progreso** | Menciona idempotencia pero no la liga a *at-least-once* de CDC, o no explica el ahorro de costo. |
| **competente** | Explica que CDC es at-least-once (eventos repetidos tras reinicio) y que upsert/delete por key lo vuelve seguro; nombra la regla "no re-embeddear contenido igual" como ahorro. |
| **excelente** | Lo anterior + pone número/orden de magnitud al ahorro (O(cambios) vs O(corpus)) y conecta con el RAG: por qué un delete no propagado deja un fantasma recuperable. |

## Errores típicos a marcar

- **No colapsa (debounce):** emite N tareas para N updates de la misma fila → no entendió "intención final". Caro en re-embeddings.
- **`TypeError` al leer `after["contenido"]` en un `d`** (after es None) → no respetó que el delete no trae `after`.
- **No propaga el delete:** la fila borrada queda indexada (fantasma) → el bug que arruina la frescura del RAG; el polling tiene exactamente este problema.
- **Emite tarea para la fila que nace y muere** dentro del lote sin estar indexada → ruido (delete sobre algo inexistente) o, peor, un upsert de algo ya borrado.
- **Re-embeddea contenido idéntico:** no compara contra `indexado` → quema tokens por un vector igual (antipatrón de costo).
- **Salida no determinista** (no ordena por key) → tests frágiles y resultados irreproducibles, que rompen la propia idempotencia.
- (transversales) Persigue *exactly-once* en vez de idempotencia + at-least-once (caro y frágil); olvida la DLQ para el evento venenoso; no instrumenta nada (sin resumen/traza).

## Señales de dependencia-IA

- Solución que mete una librería de streaming (Faust/Kafka/etc.) o un framework cuando el ejercicio pide la **lógica a mano**, y el alumno no sabe explicar qué hace el reductor por debajo.
- WRITEUP impecable con el vocabulario de la lección ("at-least-once", "debounce", "O(cambios)") que **no calza** con el código (p. ej. el código emite una tarea por evento, sin colapsar).
- Manejo sofisticado de tombstones/observabilidad junto a una lógica de delete-propagado ausente — inconsistencia de nivel.
- "Sé que debe ser idempotente" pero no puede responder *por qué CDC entrega eventos repetidos* (no entiende at-least-once).

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `pytest -v` y mira el primer rojo. ¿Tu función emite una tarea por *evento* o por *key*? Si es por evento, no estás colapsando a la intención final."
- **Pregunta socrática (nivel 2):** "¿Recorres los eventos una vez (decidiendo al vuelo) o construyes primero el estado final por key y luego decides? Para una fila con `c, u, u, d` en el mismo lote, ¿cuántas tareas deberían salir, y cuál? ¿Y si esa fila no estaba en `indexado`?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Separa en dos pasadas: (1) `estado_final[key]` = vivo/muerto + contenido, recorriendo en orden (el último gana = debounce); (2) por cada key en `sorted(...)`, decide: muerto+indexado→delete, muerto+no-indexado→nada, vivo+contenido==indexado→nada, vivo+distinto→upsert. El `TypeError` viene de leer `after['contenido']` en un `d`: en un delete, `after` es None — no lo necesitas, solo la key."

## Conexión con el proyecto / capstone

- Este reductor **es** el mecanismo que mantiene fresco el RAG del capstone de F7 en producción: el mismo reflejo at-least-once + idempotencia + DLQ del consumidor confiable de [7.2](/fase-7-automatizacion/7-2-integracion-confiabilidad/), aplicado al ingest en tiempo real. Si el alumno integra CDC en el capstone, este código es el núcleo; si decide *no* usar CDC, debe poder justificar por qué (volumen/freshness) — y eso también es señal de dominio.
