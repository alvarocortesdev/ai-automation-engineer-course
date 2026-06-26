# Ejercicio 3.14 — Reintentos con backoff exponencial + jitter (a mano)

> **Modalidad: código (Python, sin IA).** Implementas el patrón de reintentos que todo backend de producción necesita —y que toda librería de retry (tenacity, etc.) implementa por dentro— para entender la mecánica una vez, a mano.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.14` Idempotencia y resiliencia
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

Implementar `reintentar(fn, ...)` que reintente **solo** errores transitorios (los permanentes se propagan de inmediato), con **backoff exponencial acotado por un tope** y **full jitter**, hasta un tope de intentos; y relanzar la última excepción transitoria si se agotan. Sin tenacity ni ninguna librería de retry.

## 📋 Contexto

Toda llamada saliente del capstone (al proveedor de pagos, a otra API) necesita reintentar los fallos pasajeros sin amplificar la carga ni reintentar lo que no se arregla. Este es el ladrillo de resiliencia más reutilizable que vas a escribir, y entenderlo por dentro te deja usar bien la librería real después.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Razona la secuencia de esperas en papel antes de teclear.
2. Solo entonces consulta la **documentación oficial** (AWS Builders' Library: timeouts/retries/backoff; `random`).
3. **Solo al final**, usa IA para *revisar* — no para generar la función.
4. Mañana, reescríbela de memoria.

## 🛠️ Instrucciones

1. Abre `solucion.py` e implementa `reintentar` **sin cambiar su firma**. Las excepciones `ErrorTransitorio` y `ErrorPermanente` ya están definidas ahí.
2. Recuerda: `dormir` y `aleatorio` se **inyectan** (defaults `time.sleep` y `random.random`) para que los tests sean deterministas. La espera del intento `n` (empezando en 0) es `aleatorio() * min(tope, base * 2**n)`.
3. Corre el test:

   ```bash
   uv run pytest        # o: pytest
   ```

4. Escribe `bitacora.md`: por qué el jitter evita la retry storm y por qué los 4xx no se reintentan.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: éxito al primer intento (sin dormir), falla N veces y acierta, error permanente sin reintentar, agotar intentos relanza el transitorio, backoff exponencial con tope, jitter por debajo del delay.
- [ ] No reintentas errores que no están en `transitorias`; no duermes después del último intento.
- [ ] `bitacora.md` explica jitter/retry-storm y por qué no se reintentan los permanentes.
- [ ] Agregaste **un test borde tuyo** (p. ej. `max_intentos=1`).
- [ ] Puedes explicar **sin notas** por qué reintentar un `POST` no idempotente duplica el efecto.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Un bucle `for intento in range(max_intentos):` con `try: return fn()`. En el `except transitorias as exc:`, si es el último intento (`intento + 1 >= max_intentos`) haz `raise`; si no, calcula `espera = aleatorio() * min(tope, base * (2 ** intento))` y `dormir(espera)`. Las excepciones **no** transitorias no las atrapas: se propagan solas. Repasa la sección 4.4 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `solucion.py` + `bitacora.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/retry-backoff-jitter.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/retry-backoff-jitter.md` — no la mires antes de intentarlo.
