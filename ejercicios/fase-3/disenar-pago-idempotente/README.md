# Ejercicio 3.14 — Diseña un endpoint POST idempotente

> **Modalidad: razonamiento y diseño (sin IA, sin código que correr).** El cargo duplicado es el bug de resiliencia más caro; aquí diseñas la defensa completa antes de escribir una línea de servidor. Diseñar bien esto es lo que se pregunta en entrevistas de backend.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.14` Idempotencia y resiliencia
**Ruta:** crítica · **Timebox:** 35–40 min

## 🎯 Objetivo

Diseñar la idempotencia de un `POST /pagos`: el esquema de la tabla de idempotency keys (con el constraint que arbitra la carrera), el flujo "INSERT-primero" ante los tres escenarios clave (primer request, reintento terminado, dos requests concurrentes), los status HTTP de cada caso, y el trade-off fail-open vs fail-closed.

## 📋 Contexto

El capstone tendrá al menos un endpoint que crea/cobra/reserva: tiene que ser seguro de reintentar. Este ejercicio produce el material de un **ADR** real (la decisión de idempotencia, defendible y documentada) y siembra el outbox/reconciliación de la Fase 7.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Razona la carrera concurrente en una línea de tiempo antes de escribir.
2. Solo entonces consulta **documentación oficial** (Stripe Idempotent requests; IETF Idempotency-Key header).
3. **Solo al final**, usa IA para *revisar* tu diseño — no para generarlo.
4. Mañana, reescribe el flujo de la carrera de memoria.

## 🛠️ Instrucciones

1. Completa `esquema.sql` con la tabla `idempotency_keys` (columnas + constraint que arbitra la carrera + TTL).
2. Completa `diseno.md` respondiendo **todas** sus secciones:
   - decisiones de esquema,
   - flujo paso a paso para (a) primer request, (b) reintento terminado, (c) dos requests concurrentes con la misma clave,
   - tabla de status HTTP por caso (incluye "en vuelo" y "misma clave, body distinto"),
   - trade-off fail-open vs fail-closed para el pago,
   - las dos preguntas de defensa.
3. No hay tests: la entrega es tu razonamiento escrito.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El esquema tiene un constraint (`PRIMARY KEY`/`UNIQUE`) que serializa la carrera, y un campo que distingue "en vuelo" de "terminada".
- [ ] El flujo usa **INSERT-primero** (no "leer y luego escribir") y explica quién gana la carrera y qué le pasa al que pierde.
- [ ] La tabla de status mapea cada caso correctamente, con el **409** para el "en vuelo".
- [ ] Justificas que el pago es **fail-closed** y por qué.
- [ ] Respondes, sin notas, por qué la clave la genera el cliente y por qué INSERT-primero cierra la ventana de carrera.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

La clave es la PK (o un `UNIQUE` sobre `(clave, usuario_id)`). El campo `respuesta jsonb` arranca en `NULL` (en vuelo) y se llena al terminar. El árbitro de la carrera es que **el `INSERT` falla por violación de unicidad** para el segundo request: ahí lees la fila y decides según `respuesta` esté llena (devuelves el resultado, 200/201) o `NULL` (409 "procesando"). Repasa la sección 4.2–4.3 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `diseno.md` + `esquema.sql` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/disenar-pago-idempotente.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/disenar-pago-idempotente.md` — no la mires antes de intentarlo.
