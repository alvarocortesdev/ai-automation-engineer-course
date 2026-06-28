# cdc-arquitectura-frescura — ¿CDC o batch? Diseña la frescura de dos RAGs

> **Modalidad: a mano (sin código, sin IA).** Este ejercicio entrena tu **criterio de
> arquitectura de datos**: decidir cuándo CDC+streaming vale la pena y cuándo es
> over-engineering, elegir kappa vs lambda, y manejar los modos de falla. No se mide la
> prosa: se mide la **calidad de las decisiones** y que las justifiques **por la causa**.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.6` CDC y streaming → frescura de IA
**Ruta:** opcional/profundización · **Timebox:** 35 min

## 🎯 Objetivos

- **O1** — Decidir, para un caso concreto, **batch incremental vs CDC+streaming**, justificando por la **causa** (volumen de cambios, requisito de freshness, costo operativo), no por la moda.
- **O2** — Elegir **kappa vs lambda** para un pipeline de streaming y explicar cómo re-procesarías el histórico (replay).
- **O3** — Ubicar un **table format** (Iceberg/Delta) y la arquitectura **medallion** en el diseño, y nombrar el manejo de los modos de falla (orden, deletes, backfill, evento venenoso).

## 📋 Contexto

Antes de montar Kafka "porque suena bien", un ingeniero decide si lo necesita. Este diseño
es el criterio que separa al que sobre-ingenieriza del que elige la herramienta por la
restricción dominante. Conecta con el **capstone de la Fase 7**: si tu agente usa un RAG,
esta es la decisión de cómo lo mantienes fresco — y por qué.

## Los dos escenarios (decisiones opuestas: esa es la gracia)

- **Escenario A — RAG legal.** Corpus de ~3.000 documentos de políticas internas. Cambian
  **~5 veces al día**. Compliance: si una política se deroga, el RAG **no puede** seguir
  citándola; pero una latencia de **minutos** es aceptable.
- **Escenario B — RAG de catálogo.** ~80.000 SKUs. Precios y stock cambian **miles de veces
  por minuto**. Un agente de ventas consulta el RAG en vivo: una respuesta con precio viejo
  **cuesta plata** y la freshness importa en **segundos**.

## 📏 Primero-Sin-IA

1. Decídelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces consulta **documentación oficial** (Debezium, kappa, Iceberg/Delta).
3. **Solo al final**, usa IA para *cuestionar* tu diseño — no para *generarlo*.
4. Mañana, reconstruye de memoria la regla "cuándo CDC vale la pena".

## 🛠️ Tu tarea — entrega `diseno.md` con cuatro secciones

### Sección 1 — Decisión por escenario

Para A y para B, elige **batch incremental programado** (estilo orquestador 7.5c) **vs
CDC+streaming** (Debezium/Kafka). Justifica **por la causa**. Las respuestas **no** son la
misma para ambos — si te salen iguales, vuelve a pensar la freshness y el volumen.

### Sección 2 — kappa vs lambda

Para el escenario donde elegiste streaming: ¿kappa (un camino + replay) o lambda
(batch+speed)? ¿Por qué? ¿Cómo re-indexarías **todo** el corpus si cambias el modelo de
embeddings?

### Sección 3 — Table format

¿Un table format (Iceberg/Delta) **gana su sitio** en alguno? Di en cuál sí y en cuál es
over-engineering, y por qué (replay barato vs complejidad operativa).

### Sección 4 — Modos de falla

Para tu diseño de streaming, nombra cómo manejas: (a) un evento **fuera de orden**, (b) un
**DELETE** (que no quede fantasma en el índice), (c) un **backfill/reproceso** del
histórico, (d) un **evento venenoso**. Conecta cada uno con un concepto de la lección 7.2
(idempotency keys, DLQ, replay) cuando aplique.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] A y B tienen decisiones **distintas**, cada una justificada por su **causa** (no "CDC porque es mejor").
- [ ] La elección kappa/lambda está argumentada, incluido **cómo re-indexarías** (replay).
- [ ] La sección de table format distingue **cuándo sí / cuándo es over-engineering**.
- [ ] Los 4 modos de falla tienen un manejo concreto (deletes propagados, DLQ, idempotencia, orden por `lsn`).
- [ ] Puedes **explicar sin notas** por qué *no* siempre conviene CDC.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Cruza dos preguntas: ¿cuánto importa la freshness (minutos vs segundos)? y ¿cuánto cambia
el dato respecto de su tamaño (poco vs mucho)? Freshness laxa + pocos cambios → batch
incremental (montar Kafka es over-engineering, pero el **delete** lo resuelves explícito
igual). Freshness estricta + altísimo volumen → CDC+streaming, y ahí kappa + un table
format para replay barato tienen sentido. Modos de falla: orden → `lsn`/offset; delete →
propaga; backfill → replay/snapshot; venenoso → DLQ (todo eso es 7.2). Revisa la sección
4.5 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-7/cdc-arquitectura-frescura/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-7/cdc-arquitectura-frescura.md`
— no la mires antes de intentarlo de verdad. El corrector revisará tus **decisiones**
(batch vs CDC justificado por la causa, kappa/lambda, table format, modos de falla), no si
tu redacción es bonita.
