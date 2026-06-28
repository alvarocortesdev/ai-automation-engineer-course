# cdc-reductor-reembedding — Reductor CDC → tareas de re-embedding

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.6` CDC y streaming → frescura de IA
**Ruta:** opcional/profundización · **Timebox:** 45 min (objetivo 25–45)

## 🎯 Objetivo

Implementar **a mano** el corazón de un consumidor CDC: de una tanda de change events
(en orden) a la lista **mínima, idempotente y debounced** de tareas (`upsert`/`delete`)
para el vector DB de un RAG. Sin Kafka, sin Debezium real: construyes la *lógica* que
vive en cualquier consumidor. Al terminar sabrás explicar por qué un consumidor CDC debe
ser idempotente, por qué hay que propagar los deletes y cómo se evita quemar tokens de
embedding re-embeddeando lo que no cambió.

## 📋 Contexto

Un stream CDC entrega eventos de cambio de la tabla `articulos`, en orden (por `lsn`).
Cada artículo, si existe, tiene un campo `contenido` que es **lo que se embeddea**. Tu
reductor recibe la tanda y el estado **ya indexado** en el vector DB (`{id: contenido}`),
y produce las tareas mínimas. Este ejercicio alimenta el **capstone de la Fase 7**: si tu
agente usa un RAG, este reductor es lo que lo mantiene fresco en producción.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento y feo.
2. Solo entonces, consulta la **documentación oficial**: <https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-events> (para ver el envelope real de Debezium).
3. **Solo al final**, usa IA para *revisar y explicar* tu solución — nunca para *generarla*.
4. Mañana, reescribe `reducir` **de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

### Parte obligatoria (nivel "competente")

Completa `reducir(eventos, indexado)` en `reductor.py` para que devuelva una lista de
`Tarea(accion, key, contenido)` con `accion ∈ {"upsert", "delete"}`, cumpliendo:

1. **Debounce** — varios eventos de la misma `key` se reducen a **su intención final** (la última por orden). Una sola tarea por key, como máximo.
2. **Mapeo de op** — `c`/`r`/`u` → la fila existe con su `contenido` final; `d` → borrada.
3. **Delete propagado** — key terminó borrada **y** estaba en `indexado` → `Tarea("delete", key)`.
4. **Nace y muere** — key terminó borrada y **no** estaba en `indexado` → ninguna tarea.
5. **No re-embeddear lo igual** — key viva con `contenido` **idéntico** al de `indexado` → ninguna tarea (no pagues un embedding por un vector igual).
6. **Upsert** — key viva con `contenido` **distinto** (o nueva) → `Tarea("upsert", key, contenido)`.
7. **Determinismo** — la lista sale **ordenada por `key`**.

Corre y deja en verde:

```bash
pip install pytest        # si no lo tienes
pytest -v
```

> **Cuidado con el orden:** primero construye el **estado final por key** recorriendo en
> orden (dos eventos de la misma key → gana el último); recién entonces decide la tarea
> comparando contra `indexado`. En un `d`, `after` es `None`: no intentes leer su `contenido`.

### Parte de profundización (nivel "excelente" — hilos transversales)

8. **Idempotencia** — agrega un test que pase **la misma tanda dos veces** (concatenada) y verifique que el resultado es idéntico a pasarla una vez (CDC es *at-least-once*).
9. **Tombstones** — acepta `op == "d"` con `after == None` sin reventar (ya cubierto si construyes el estado bien); opcionalmente ignora un tombstone puro.
10. **Observabilidad mínima** — un helper o el resultado expone un resumen tipo métrica (`upserts`, `deletes`, `skips_por_contenido_igual`): la base de la traza del pipeline.
11. **`WRITEUP.md`** (4–6 líneas): ¿por qué el reductor debe ser idempotente (qué garantiza CDC)? ¿Qué regla evita quemar tokens de embedding y cuánto ahorra frente a "re-embeddear cada evento"?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest -v` en verde (debounce, delete propagado, nace-y-muere, contenido igual, upsert, orden, idempotencia).
- [ ] Un mismo evento aplicado dos veces deja el resultado **idéntico** (idempotencia).
- [ ] Un artículo **borrado** que estaba indexado produce `delete`; uno borrado que **no** estaba indexado no produce nada.
- [ ] Un `UPDATE` cuyo `contenido` **no cambió** respecto del índice **no** produce tarea (ahorro de costo).
- [ ] Agregaste **al menos un test propio** con un caso borde (tanda vacía, solo metadata, etc.).
- [ ] Puedes **explicar sin notas**: idempotencia + debounce + propagar deletes, y el trade-off costo/freshness.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **Dos pasadas.** (1) Recorre los eventos *en orden* y arma `estado_final[key]`: para
  `c`/`r`/`u` guarda `("vivo", after["contenido"])`; para `d` guarda `("muerto", None)`.
  El último evento de cada key gana — eso *es* el debounce.
- (2) Para cada key (en `sorted(estado_final)`), decide la tarea comparando con `indexado`:
  `muerto` + estaba indexado → `delete`; `muerto` + no estaba → nada; `vivo` + contenido
  igual al indexado → nada; `vivo` + distinto (o nuevo) → `upsert`.
- **Idempotencia gratis:** como reduces al *estado final*, repetir eventos no cambia el
  resultado. Verifícalo con el test del punto 8.
- Lee la sección 4.4 de la lección `7.6` antes de mirar nada más.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (esta carpeta, con `reductor.py` completo + la salida de `pytest -v`),
- la **rúbrica**: `.ai/rubricas/fase-7/cdc-reductor-reembedding.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** (`.ai/soluciones/fase-7/cdc-reductor-reembedding/`) es material
del corrector — no la mires antes de intentarlo de verdad.
