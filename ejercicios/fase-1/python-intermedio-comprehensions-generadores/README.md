# Ejercicio 1.2 — Procesar transacciones con comprehensions y un generador

> **Modalidad: código (Primero-Sin-IA).** Practicas las dos primeras herramientas de la
> sub-unidad 1.2: **comprehensions** (transformar/filtrar en una línea legible) y
> **generadores** (producir datos de a uno, sin materializar la colección). Sin IA hasta
> cerrar tu intento.

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.2` Python intermedio
**Ruta:** crítica · **Timebox:** 35–45 min

## 🎯 Objetivo

Implementar tres funciones que procesan una lista de transacciones, **usando la herramienta
correcta para cada caso**: una `set` comprehension, una `dict` comprehension y un **generador**
con `yield`.

## 📋 Contexto

Transformar y filtrar datos es la mitad del trabajo de un ingeniero de IA y de datos. Aquí lo
haces con las herramientas idiomáticas de Python, y eliges **generador** cuando los datos no
deberían materializarse de golpe (el mismo criterio que aplicarás al transmitir tokens de un LLM
o procesar archivos enormes en fases siguientes).

## 📏 Primero-Sin-IA

1. **Antes de programar**, escribe el **contrato** de cada función en una línea: ¿qué entra?,
   ¿qué sale?, ¿qué pasa con la lista vacía?
2. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
3. Solo entonces consulta la **documentación oficial** (comprehensions, generadores).
4. **Solo al final**, usa IA para *revisar y explicar* — nunca para *generar*.
5. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `transacciones.py` y completa las tres funciones (no cambies sus firmas).
2. Corre los tests:

   ```bash
   uv run pytest        # recomendado
   # o, si ya tienes pytest:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test borde tuyo** en `test_transacciones.py` (¿transacciones con `id`
   repetido?, ¿montos iguales al `minimo`?, ¿una sola transacción?).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `categorias_unicas` y `indexar_por_id` usan **comprehensions** (no un `for` con `append`/asignación).
- [ ] `stream_montos` es un **generador** (usa `yield`), produce los montos `>= minimo` **en orden**, y **no** construye una lista.
- [ ] Lista vacía: `set()`, `{}` y un generador que no produce nada, respectivamente.
- [ ] Todos los tests pasan y agregaste **un test propio**.
- [ ] Puedes **explicar sin notas** por qué `stream_montos` no debería devolver una lista.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Una `set` comprehension es `{expr for x in iterable}`; una `dict` comprehension es
`{clave: valor for x in iterable}`. Para `stream_montos`, un generador **no construye** la
colección: recorres con un `for`, y cuando un monto cumple el filtro lo entregas con `yield`
(la función se pausa hasta que le pidan el siguiente). Si escribiste `return [m for m in ...]`,
eso es una **lista**, no un generador. Revisa las secciones 4.1 y 4.2 de la lección antes de
mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-1/python-intermedio-comprehensions-generadores/` usando el framework
> de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-1/` — no la mires antes de intentarlo
de verdad.
