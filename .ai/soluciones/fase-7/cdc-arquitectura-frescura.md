---
ejercicio_id: fase-7/cdc-arquitectura-frescura
fase: fase-7
sub_unidad: "7.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una vara de medir de un ejercicio de **diseño**: hay varias respuestas defendibles. Lo que importa es que la decisión esté **justificada por la causa**, no que coincida palabra por palabra con esto.

# Solución de referencia — ¿CDC o batch? Frescura de dos RAGs

## Sección 1 — Decisión por escenario (la clave: deben ser distintas)

**Escenario A (RAG legal) → batch incremental programado.**
- **Causa:** ~5 cambios/día y latencia aceptable de **minutos**. El volumen de cambios es ínfimo frente al corpus (3.000 docs); montar Kafka + Debezium + replication slots es **costo operativo sin retorno** (over-engineering). Un job incremental cada pocos minutos (orquestado, estilo 7.5c) da la freshness requerida.
- **Pero el delete no es opcional:** compliance exige que una política derogada deje de citarse. Un "upsert de lo que existe" deja fantasmas. Solución sin CDC: o un campo `estado/derogado` que el job lee y traduce a `delete` en el vector DB, o comparar el set de ids actuales vs los indexados y borrar los que faltan (reconciliación). El delete se resuelve **explícito**, aunque sea batch.

**Escenario B (RAG de catálogo) → CDC + streaming.**
- **Causa:** miles de cambios/minuto + freshness en **segundos** + plata en juego (precio viejo = pérdida). Aquí el batch no alcanza (re-indexar 80k cada pocos minutos es carísimo y aún así lento), y el polling perdería estados intermedios y borrados. CDC log-based captura cada cambio en orden, y el reductor re-embeddea **solo lo que cambió** (la mayoría de los cambios son de precio/stock — *no* re-embeddees si el `contenido` textual no cambió; el precio puede ir como metadata del vector sin re-embedding).

> Si el alumno elige lo mismo para ambos, es el error de fondo: CDC es un trade-off, no un default.

## Sección 2 — kappa vs lambda (para B)

- **Kappa.** Un solo camino: el log de CDC *es* el stream re-procesable. Una sola lógica de ingest/re-embedding, una fuente de verdad. Re-indexar todo al cambiar el modelo de embeddings = **replay** del topic (o de la tabla histórica) desde el inicio por el mismo consumidor. No mantienes un job batch gemelo que se desincroniza.
- **Lambda** se justificaría solo si necesitaras, en paralelo, un re-procesamiento batch garantizado con lógica distinta a la de streaming — al costo de **duplicar y mantener dos implementaciones**. Para CDC→RAG no aporta; kappa es más simple y suficiente.

## Sección 3 — Table format (Iceberg/Delta)

- **En B: gana su sitio.** Guardar el histórico de cambios en una tabla **Iceberg/Delta** (ACID, upsert/delete, time-travel) hace el **replay barato y reproducible**: el lake actúa como sink *y* source de streaming ("Kappa Plus"/streamhouse). Cuando cambias de modelo de embeddings, re-lees la tabla como stream en vez de re-extraer de la fuente OLTP.
- **En A: over-engineering.** Con 3.000 docs y 5 cambios/día no necesitas un lakehouse; un almacenamiento simple + el vector DB bastan.
- **Medallion** es ortogonal: en B podrías tener bronze (eventos CDC crudos), silver (deduplicados/limpios), gold (chunks listos para embeddear) **dentro** del stream. No implica batch.

## Sección 4 — Modos de falla (para el diseño de streaming de B)

| Falla | Manejo | Concepto de 7.2 |
|---|---|---|
| **Fuera de orden** | Ordenar/aplicar por `lsn`/offset; el reductor colapsa a la intención final por key (el último gana), así el orden dentro de la ventana se respeta. | idempotencia + orden del log |
| **DELETE** | Propagar el `delete` al vector DB por id (no quede fantasma). El tombstone de Kafka se ignora como dato. | (el agujero que el polling no cubre) |
| **Backfill / reproceso** | Replay del topic desde un offset / re-snapshot inicial de Debezium; idempotencia garantiza que reprocesar no duplica. | replay |
| **Evento venenoso** | A una **DLQ** tras N reintentos; no bloquea el stream; se inspecciona aparte. | DLQ / poison message |

## Rango de respuestas aceptables

- A en batch y B en CDC es la respuesta "natural", pero un alumno puede defender **B con micro-batch de segundos** si argumenta bien el costo operativo de Kafka vs la tolerancia real; lo que NO se acepta es "CDC para ambos porque es mejor" ni "batch para B" (no alcanza la freshness/volumen).
- Para A, cualquier mecanismo de delete explícito (flag de baja, reconciliación de ids) es válido; lo que se marca es **omitir el delete**.
- kappa es la elección esperada para B; lambda es aceptable solo con una justificación seria de re-procesamiento batch en paralelo.
- El table format puede declararse innecesario en B si el alumno argumenta que el vector DB + un log retenido bastan para su escala — defendible si reconoce el costo del replay sin él.

## Qué distingue "excelente"

- Una **regla reutilizable** (cruce freshness × razón-de-cambio) en vez de dos decisiones sueltas.
- Reconocer explícitamente **cuándo CDC es over-engineering** (la honestidad de "opcional").
- Conectar cada modo de falla con su concepto de 7.2 y mencionar costo (USD/freshness) en la decisión.
