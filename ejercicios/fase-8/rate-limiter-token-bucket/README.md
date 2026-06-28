# Ejercicio 8.1 — Rate limiter token bucket (testeable y determinista)

> **Modalidad: código (Primero-Sin-IA, con tests).** Implementas el algoritmo de rate limiting más
> usado en producción. El reto técnico de fondo no es el algoritmo (es corto): es diseñarlo para que
> sea **determinista y testeable** inyectando el reloj, en vez de leer la hora dentro de la clase.

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.1` Fundamentos de System Design
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar un `TokenBucket` que decida si un request se permite o se rechaza según un presupuesto de
tokens que se recarga con el tiempo. A escala, un rate limiter protege tu capacidad (un cliente no
tumba el sistema para todos), da equidad y **controla el costo** —crítico en APIs de LLM, donde un
cliente en loop puede quemar miles de dólares.

## 📋 Contexto

El **token bucket** es el algoritmo canónico de rate limiting (lo usan API gateways, nubes y CDNs):
un balde con capacidad fija de tokens que se rellena a una tasa constante. Cada request consume
tokens; si no hay suficientes, se rechaza. Permite **ráfagas** (hasta la capacidad) pero acota la
tasa sostenida (el refill rate). Lo conectas con el capstone de la fase: los dos sistemas con IA
necesitan rate limiting para no dispararse en costo.

## 📏 Primero-Sin-IA

1. Lee `rate_limiter.py` y `test_rate_limiter.py`. **A mano**, sin IA, dibuja en papel cómo cambia
   el número de tokens en el tiempo (recarga lineal con tope). Solo entonces escribe código.
2. Consulta la **documentación oficial** si necesitas (no hace falta una librería: es Python puro).
3. **Solo al final**, usa IA para *revisar y explicar* tu solución —no para generarla.
4. Mañana, **reescríbelo de memoria**. Si no te sale el orden recargar→decidir, no lo aprendiste.

## 🛠️ Instrucciones

1. Abre `rate_limiter.py` y completa la clase `TokenBucket` (no cambies las firmas):
   - `__init__`: el bucket arranca **lleno** (capacity tokens) y guarda la marca de tiempo inicial.
   - `allow(ahora, cost=1.0)`: primero **recarga** según el tiempo transcurrido (sin pasar de la
     capacidad; si `ahora` no avanzó, no recargues), luego **consume** `cost` si alcanza y devuelve
     `True`, o devuelve `False` **sin consumir**.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos pasen en verde**.
4. Añade **al menos un test propio** (un caso borde que se te ocurra).

> Regla innegociable del ejercicio: **el reloj se inyecta** (`ahora`). Prohibido llamar a
> `time.monotonic()` / `time.time()` dentro de la clase. Esa es la diferencia entre un rate limiter
> testeable y uno que solo puedes probar con `sleep` (lento y flaky).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `uv run pytest` (o `pytest`) en verde: todos los tests pasan.
- [ ] Cero llamadas a un reloj real dentro de `TokenBucket` (el tiempo entra por `ahora`).
- [ ] El orden es **recargar primero, decidir después**; los tokens nunca superan la capacidad.
- [ ] Un `cost` que no alcanza devuelve `False` **sin** consumir tokens.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar por qué** el rate limiting protege capacidad y costo, sin notas.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Guarda dos cosas de estado: `tokens` (cuántos quedan) y `ultima_recarga` (el `ahora` de la última
vez que recargaste). En `allow`, calcula `transcurrido = ahora - ultima_recarga`; si es positivo,
`tokens = min(capacity, tokens + transcurrido * refill_rate)` y actualiza `ultima_recarga`. El `min`
es lo que impide acumular tokens infinitos. Recién entonces compara `tokens >= cost`. El orden
importa: si decides antes de recargar, rechazas requests que sí deberían pasar.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (esta carpeta),
- la **rúbrica**: `.ai/rubricas/fase-8/rate-limiter-token-bucket.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-8/rate-limiter-token-bucket.md` — no la
mires antes de intentarlo de verdad.
