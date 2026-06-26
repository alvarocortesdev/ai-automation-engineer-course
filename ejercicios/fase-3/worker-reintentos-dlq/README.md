# Ejercicio 3.16b — Implementa un worker con reintentos y DLQ (Python puro)

> **Modalidad: código (Python puro, sin IA).** Sin broker, sin Redis, sin Celery: implementas la **semántica** de una cola —reintentos con tope, dead-letter queue (DLQ) e idempotencia bajo at-least-once— para que el patrón se te quede en el cuerpo antes de tocar una herramienta real.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.16` Colas y procesamiento async
**Ruta:** opcional / profundización · **Timebox:** 40–45 min

## 🎯 Objetivo

Implementar `procesar_cola(jobs, handler)` que: ejecuta cada job con el `handler`, **reintenta** ante excepción hasta `max_attempts`, manda a la **DLQ** los que agotan intentos (poison messages), y —porque la entrada simula entrega **at-least-once**— **deduplica** por `job.id` para no reprocesar un job ya completado. El objetivo profundo: entender por qué la deduplicación por id es el equivalente de la **idempotencia** bajo at-least-once.

## 📋 Contexto

Celery y BullMQ son detalles de sintaxis; lo que se queda es el **patrón**: encolado → en proceso → (hecho | reintento → DLQ), con entrega at-least-once que obliga a idempotencia. Implementarlo a mano una vez vale más que leer diez tutoriales. Es, además, la columna de la confiabilidad de integración que verás en la Fase 7 (idempotency keys, DLQ, replay).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Traza en papel un job que falla siempre antes de teclear.
2. Solo entonces, consulta la lección (secciones 4.5–4.6) o documentación oficial si lo necesitas.
3. **Solo al final**, usa IA para *revisar* — no para generar `procesar_cola`.
4. Mañana, reescríbela de memoria y explica por qué la dedup por id es la idempotencia bajo at-least-once.

## 🛠️ Instrucciones

1. Abre `solucion.py` e implementa `procesar_cola(jobs, handler)` **sin cambiar la firma** ni el dataclass `Job`, respetando el contrato del docstring.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **los 5 tests pasen en verde**.
4. Agrega al menos **un test tuyo** en `test_worker.py` (p. ej. `max_attempts=1` → un solo intento, o un duplicado de un id que va a la DLQ).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: éxito al primer intento; flaky que se recupera dentro del tope (handler llamado exactamente `max_attempts`); siempre-falla → DLQ con `attempts == max_attempts` (sin loop infinito); dedup at-least-once (handler una sola vez por id ya hecho); mezcla done/dlq.
- [ ] El job que siempre falla termina en `dlq` tras **exactamente** `max_attempts` llamadas.
- [ ] Un mismo `job.id` que aparece dos veces se procesa **una sola vez** (idempotencia).
- [ ] Agregaste al menos un test propio.
- [ ] Puedes explicar, **sin notas**, por qué at-least-once obliga a deduplicar y dónde nace el doble efecto si no lo haces.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Usa una `collections.deque` como cola FIFO: saca del frente (`popleft`), y al fallar reencola al final (`append`) **después** de incrementar `job.attempts`. La condición de DLQ tras un fallo es `job.attempts >= job.max_attempts`. Para la idempotencia, mantén un `set` de ids ya completados: **antes** de llamar al handler, si `job.id` ya está en el set, salta el job (no lo ejecutes, no lo dupliques en `done`); al completar con éxito, agrega el id al set. Cuidado con el orden: el primer intento también cuenta, así que con `max_attempts=3` el handler se llama 3 veces antes de la DLQ. Revisa la sección 4.6 (ciclo de vida) de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `solucion.py` + el `test_worker.py` con tu test añadido (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/worker-reintentos-dlq.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/worker-reintentos-dlq.md` — no la mires antes de intentarlo.
