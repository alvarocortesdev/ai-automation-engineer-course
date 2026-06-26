# Ejercicio 1.2 — Un decorador de reintento y un context manager con limpieza garantizada

> **Modalidad: código (Primero-Sin-IA).** Practicas las dos herramientas más difíciles de la
> sub-unidad 1.2: **decoradores** (envolver comportamiento sin tocar la función) y **context
> managers** (garantizar la limpieza pase lo que pase). Ambas reaparecen en cada fase con IA.
> Sin IA hasta cerrar tu intento.

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.2` Python intermedio
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

Implementar un **decorador parametrizado** `reintentar(veces)` (el patrón con el que se envuelve
cada llamada a una API o a un LLM) y un **context manager** `conexion(registro)` que garantice la
liberación del recurso aunque el bloque lance una excepción.

## 📋 Contexto

El decorador `reintentar` es **literalmente** lo que usarás en la Fase 6 para que una llamada a un
LLM no se caiga ante el primer error de red (hilo de **costo/latencia y robustez**). El context
manager es el patrón estándar para abrir y cerrar recursos (archivos, conexiones a base de datos,
locks) sin filtrarlos. Dominarlos aquí es construir esas fases por adelantado.

## 📏 Primero-Sin-IA

1. **Antes de programar**, escribe el **contrato** de cada pieza: ¿qué entra?, ¿qué pasa cuando
   la función falla todas las veces?, ¿qué debe ocurrir en el `with` si el bloque revienta?
2. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
3. Solo entonces consulta la **documentación oficial** (`functools.wraps`, `contextlib`).
4. **Solo al final**, usa IA para *revisar y explicar* — nunca para *generar*.
5. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `robustez.py` y completa `reintentar` y `conexion` (no cambies sus firmas).
2. Corre los tests:

   ```bash
   uv run pytest        # recomendado
   # o, si ya tienes pytest:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test borde tuyo** en `test_robustez.py` (¿`reintentar(veces=1)`?,
   ¿qué excepción exacta se re-lanza?, ¿el recurso del `with` se cierra dos veces?).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `reintentar` funciona como `@reintentar(veces=3)` (es un decorador **parametrizado**).
- [ ] Una función que falla y luego acierta devuelve el resultado; una que siempre falla **re-lanza** la última excepción tras `veces` intentos.
- [ ] La función decorada **conserva su `__name__`** (usaste `functools.wraps`).
- [ ] `conexion` agrega `"desconectado"` al `registro` **aunque el bloque lance una excepción**, y la excepción **se propaga** (no se la traga).
- [ ] Todos los tests pasan y agregaste **un test propio**.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Un decorador **parametrizado** tiene **tres** niveles anidados: `reintentar(veces)` devuelve un
decorador; ese decorador recibe `func` y devuelve `envoltura`; `envoltura` hace el trabajo. Para
el reintento: un `for intento in range(veces)` con `try/except` dentro; si la llamada funciona,
`return` corta; guarda la excepción en una variable y, si el bucle termina sin éxito, hazle
`raise` afuera. Para el context manager con `@contextmanager`: lo que va en el `finally` **después
del `yield`** corre siempre — ahí agregas `"desconectado"`. **No** envuelvas el `yield` en un
`except` que se trague la excepción. Revisa las secciones 4.3 y 4.4 de la lección antes de mirar
la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-1/python-intermedio-decorador-context-manager/` usando el framework de
> `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-1/` — no la mires antes de intentarlo
de verdad.
