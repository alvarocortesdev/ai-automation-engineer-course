# Ejercicio 7.2 — Procesador idempotente con dead-letter queue

> **Modalidad: código + write-up (verificado por `pytest` + razonamiento).** Un canal de mensajes
> entrega *at-least-once*: el mismo evento puede llegar varias veces, y algunos fallan siempre.
> Este procesador es la pieza que vuelve ese canal seguro: deduplica y aparta los venenosos.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.2` Ingeniería de integración + confiabilidad
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

- **O1** — Implementar **idempotencia**: deduplicar por el id del evento de modo que el side-effect corra **una sola vez** ante duplicados.
- **O2** — Implementar una **DLQ**: enrutar un *poison message* a una cola lateral tras `max_intentos`, en vez de reintentarlo para siempre.
- **O3** — Explicar por escrito el **dual-write**, el **patrón outbox** y el rol de la **reconciliación** (write-up).

## 📋 Contexto

Es el motor de procesamiento detrás del receptor de tu [capstone F7](/fase-7-automatizacion/proyecto/):
el agente recibe un input, y este procesador garantiza que un reintento no ejecute dos veces la acción,
y que un input venenoso no paralice el flujo. Es el punto 6 del Definition of Done (manejo de fallas)
aplicado a la entrada.

## 📏 Primero-Sin-IA (en este orden, timebox 45 min)

1. Resuélvelo **solo**, a mano. Lee el contrato en `procesador.py` y hazlo pasar test por test.
2. Escribe el `write-up.md` con **tus palabras** (no copies la lección).
3. **Solo al final**, usa IA para *revisar* —no para generar.
4. Mañana, reescribe la clase de memoria. Si no puedes, no la aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `procesador.py` e implementa `ProcesadorIdempotente` (no cambies firmas ni claves de salida).
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos pasen en verde**. El caso clave: un evento que falla y luego tiene éxito **no** es un duplicado.
4. Escribe `write-up.md` respondiendo, en prosa breve y defendible:
   - **(a)** ¿Por qué un evento que falla y luego tiene éxito **no** debe contar como "duplicado" en el intento exitoso?
   - **(b)** Explica el problema del **dual-write** y cómo el **patrón outbox** lo resuelve. ¿Por qué los consumidores del outbox deben ser idempotentes?
   - **(c)** ¿Qué aporta la **reconciliación** que la entrega en tiempo real (webhooks/eventos) no garantiza por sí sola?
5. Añade **al menos un test propio** (sugerencia: dos eventos venenosos distintos, ambos a la DLQ sin interferir).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` pasa: dedup (efecto una sola vez en duplicados), poison → DLQ tras `max_intentos`, eventos distintos por separado.
- [ ] Un evento que falla y luego se reintenta con éxito se procesa de verdad (no marcado como duplicado).
- [ ] Un evento ya en la DLQ no re-ejecuta el efecto.
- [ ] El `write-up.md` distingue **entrega at-least-once** de **procesamiento idempotente**.
- [ ] El write-up nombra el **dual-write** y explica el **outbox** con la idea de la transacción única.
- [ ] Agregaste al menos un test propio.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Lleva dos estructuras internas: `completados: {id: resultado}` (solo entran los **éxitos**) e
`intentos: {id: int}`. En `procesar`: si el id está en `completados` → `duplicado`; si está en la DLQ →
`dlq`; si no, llama a `efecto` dentro de `try`. En éxito, guarda en `completados` → `procesado`. En
excepción, incrementa `intentos[id]` y compara con `max_intentos` para decidir `reintentable` vs `dlq`.
La clave del punto (a): marca como completado **solo** en la rama de éxito.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, incluido `write-up.md`),
- la **rúbrica**: `.ai/rubricas/fase-7/procesador-idempotente-dlq.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/procesador-idempotente-dlq.md` — no la mires
antes de intentarlo de verdad.
