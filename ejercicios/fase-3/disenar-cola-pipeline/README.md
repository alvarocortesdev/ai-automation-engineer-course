# Ejercicio 3.16a — Diseña el pipeline: qué encolar, cómo reintentar, qué va a la DLQ

> **Modalidad: razonamiento + diseño (sin código, sin IA).** No se ejecuta nada. Decides, para cinco operaciones reales, **síncrono vs cola**, y para las encoladas defines reintentos, idempotency key y DLQ. Se evalúa la **calidad del criterio**, no una respuesta única.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.16` Colas y procesamiento async
**Ruta:** opcional / profundización · **Timebox:** 35–45 min

## 🎯 Objetivo

Decidir, para cada operación de una app, si va **síncrona** (dentro del request) o **a una cola** (worker aparte), justificando con criterio (lento / frágil / no-crítico-para-la-respuesta); y para las encoladas, diseñar la política de **reintentos** (backoff + jitter + tope), la **idempotency key**, y qué cuenta como **poison message** que va a la **DLQ** y cómo se monitorea.

## 📋 Contexto

"¿Esto va en el request o a una cola?" es una decisión de diseño que aparece en cada backend serio y en entrevistas de system design. El error de junior es meter todo a una cola ("más escalable") o nada ("más simple"). El semi-senior decide por **contexto**, nombra el costo de la cola (un broker que operar, consistencia eventual) y sabe que reintentar **obliga** a idempotencia. Este patrón —reintentos + idempotencia + DLQ— es además la columna de la confiabilidad que verás en la Fase 7.

## 📏 Primero-Sin-IA

1. Decide y diseña **solo**, a mano (timebox arriba). A papel o en el `.md` directo.
2. Solo entonces, consulta documentación oficial (Celery tasks/retry, BullMQ attempts/backoff) si necesitas confirmar una característica.
3. **Solo al final**, usa IA para *cuestionar* tu diseño (pídele que ataque una de tus decisiones) — no para que diseñe por ti.
4. Mañana, reescribe de memoria los dos criterios que más pesan al decidir síncrono vs cola, y por qué at-least-once obliga a idempotencia.

## 🧩 La app: "Postal" (SaaS de campañas de email)

Cinco operaciones. Para cada una vas a decidir y, si aplica, diseñar:

- **A. `POST /signup`** — crea el usuario en Postgres (~20 ms) y le envía un **email de bienvenida** vía un SMTP externo que a veces tarda o se cae.
- **B. `POST /campaigns`** — el usuario sube un **CSV de 50.000 contactos**; el sistema valida el archivo, y envía **un email a cada contacto** (50.000 envíos a SMTP). El usuario no puede esperar a que terminen los 50.000.
- **C. `GET /campaigns/{id}`** — devuelve el estado de una campaña (cuántos enviados, fallidos, pendientes). Lectura simple en la base.
- **D. `POST /webhooks/payment`** — recibe un webhook del proveedor de pagos, **valida la firma HMAC**, y a partir de ahí debe marcar la factura pagada y notificar al usuario. El proveedor **reintenta el webhook** si tu respuesta tarda más de unos segundos o no es 2xx.
- **E. Recálculo nocturno de analítica** — todas las noches a las 03:00 recalcula métricas agregadas de todos los usuarios. Pesado, pero nadie lo dispara ni lo espera en vivo.

## 🛠️ Instrucciones

Crea un archivo **`DISENO.md`** con:

1. **Tabla de decisión** — una fila por operación (A–E) con columnas: `operación` · `síncrono o cola` · `por qué` (criterio: lento / frágil / no-crítico) · `status que devuelve el endpoint`.
2. **Política por operación encolada** — para **cada** operación que mandes a la cola, especifica:
   - `max_attempts` y la **fórmula de backoff + jitter** (puedes usar la de `3.14`),
   - la **idempotency key** concreta (qué campos la forman y por qué),
   - qué fallo es **transitorio** (reintentar) y cuál es **poison message** (a la DLQ), con un ejemplo del dominio,
   - cómo **monitorearías la DLQ** (alerta + qué harías al revisarla).
3. **Diagrama Mermaid** del flujo de la **campaña (B)**: producer → broker → worker(s) → (Hecho | DLQ).
4. **Párrafo de cierre** — nombra **un** costo real de haber metido una cola (no la vendas como gratis) y di cuál operación **NO** debería ir a una cola y por qué.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las cinco operaciones tienen decisión **síncrono vs cola** justificada con criterio (no "más escalable" / "más simple" a secas).
- [ ] Cada operación encolada define `max_attempts`, backoff **con jitter**, idempotency key concreta y qué cuenta como poison message (DLQ).
- [ ] Distingues al menos un fallo **transitorio** de un **poison message** con ejemplo del dominio.
- [ ] Reconoces al menos una operación que **NO** debería ir a una cola (over-engineering) y lo explicas.
- [ ] El caso del webhook (D) refleja la sutileza: responder **rápido** (2xx) y delegar el trabajo pesado a la cola, porque el proveedor reintenta si tardas.
- [ ] El diagrama de la campaña muestra producer/broker/worker/(Hecho|DLQ) y el cierre nombra un costo real de la cola.
- [ ] Puedes explicar, sin notas, por qué at-least-once obliga a idempotencia en los 50.000 envíos.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **Heurística sync vs cola:** ¿es lento (más de ~100–200 ms)? ¿es frágil (llama a un tercero que puede fallar)? ¿el usuario necesita el resultado **antes** de la respuesta? Lento + frágil + no-necesario-en-la-respuesta → cola.
- **A (signup + email):** crea el usuario síncrono (rápido, crítico para la respuesta), encola el email (lento + frágil + no crítico). Status `202` o `201` con estado "email en camino".
- **B (campaña 50k):** clarísimo a la cola, idealmente **un job por contacto** (no un job gigante). Idempotency key natural: `(campaign_id, contacto_id)` para no enviar dos veces a la misma persona si un worker muere a mitad. Poison message: un email con formato inválido → DLQ, no reintentar 5 veces.
- **C (GET estado):** lectura rápida, síncrona. Meterla a una cola es over-engineering.
- **D (webhook):** el caso fino. Valida la firma y responde **2xx rápido** (el proveedor reintenta si tardas → at-least-once desde afuera, ¡tu handler del webhook también debe ser idempotente por `event_id`!). El trabajo pesado (marcar pagado, notificar) va a la cola.
- **E (nocturno):** trabajo **programado** (cron / scheduler), no encolado por un request. Distínguelo de una cola disparada por usuario.

El eje dominante: encola lo **lento + frágil** que el usuario **no necesita** antes de responderle; deja síncrono lo rápido o crítico para la respuesta. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA tu `DISENO.md`, la **rúbrica** (`.ai/rubricas/fase-3/disenar-cola-pipeline.md`) y las instrucciones (`.ai/INSTRUCCIONES-CORRECTOR.md`). La **solución de referencia** vive en `.ai/soluciones/fase-3/disenar-cola-pipeline.md` — no la mires antes de intentarlo.
