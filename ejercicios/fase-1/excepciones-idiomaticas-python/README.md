# excepciones-idiomaticas-python — Excepciones de dominio en Python (parser de gastos)

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.9` Manejo de errores idiomático comparado
**Ruta:** opcional/profundización · **Modalidad:** código · **Timebox:** 30–40 min

## 🎯 Objetivo

Escribir un parser de gastos con **dos niveles** de manejo de error idiomático: la **unidad
lanza** una excepción de dominio (con encadenamiento), el **lote devuelve** los errores como datos.
Es el patrón que decide, a conciencia, **cuándo lanzar vs cuándo devolver** un fallo.

## 📋 Contexto

Las líneas vienen de afuera (un archivo, un correo, un LLM): pueden estar rotas. `parsear_linea`
tiene el contrato "una línea válida o nada" → ante una mala, **lanza** `LineaInvalida`.
`parsear_archivo` tiene el contrato "procesa todo lo que puedas y repórtame qué falló" → **no se
cae** en la primera línea mala, junta los válidos y los errores por separado. Este contraste —misma
operación, distinto nivel, distinta decisión— es el corazón de la lección, y la semilla del manejo
de errores que mapearás a códigos HTTP en FastAPI (Fase 3).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, sin IA (timebox arriba). Diseña los modos de fallo **antes** de codear.
2. Solo entonces consulta la **documentación oficial** de excepciones de Python si la necesitas.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, reescribe `parsear_linea` **de memoria** y explica qué gana el `from e`.

## 🛠️ Instrucciones

1. Abre `gastos.py`. Las `dataclass` (`Gasto`, `ErrorLinea`) y la excepción `LineaInvalida` ya están
   definidas: ese es el contrato. Tu trabajo es implementar `parsear_linea` y `parsear_archivo`.
2. `parsear_linea` debe **lanzar** `LineaInvalida` ante los 4 modos de fallo, y **encadenar**
   (`raise ... from e`) el `ValueError` cuando el monto no es entero (estilo EAFP).
3. `parsear_archivo` debe recorrer las líneas, **ignorar las blancas**, y por cada línea mala
   acumular un `ErrorLinea(numero, contenido, motivo)` — sin caerse.
4. Verifica hasta que pasen todos los tests:

   ```bash
   uv run pytest        # o:  pytest
   ```

5. **Cierra el loop.** Agrega en `test_gastos.py` **un test tuyo** para un caso borde realista.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `parsear_linea` lanza `LineaInvalida` ante campos ≠ 3, monto no entero, monto ≤ 0 y
      `comercio`/`categoria` vacíos (tras `strip`).
- [ ] Con monto no entero, la excepción está **encadenada**: `exc.__cause__` es el `ValueError`.
- [ ] `parsear_archivo` devuelve `(list[Gasto], list[ErrorLinea])`, ignora blancas y no se cae.
- [ ] Los números de línea en `ErrorLinea` son correctos (1-based, contando las blancas).
- [ ] Agregaste al menos un test propio.
- [ ] Puedes explicar **sin notas** por qué la unidad lanza pero el lote devuelve, y qué gana el `from e`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`parsear_linea`: `partes = [p.strip() for p in linea.split(";")]`; si `len(partes) != 3` lanza; si
`comercio`/`categoria` son falsy (vacíos) lanza; para el monto, `try: monto = int(monto_raw) except
ValueError as e: raise LineaInvalida(...) from e`; si `monto <= 0` lanza. `parsear_archivo`:
`for numero, linea in enumerate(texto.splitlines(), start=1)`, salta si `not linea.strip()`, y un
`try: gastos.append(parsear_linea(linea)) except LineaInvalida as e: errores.append(ErrorLinea(...))`.
La unidad lanza porque su contrato es "válido o nada"; el lote devuelve porque el suyo es "todo lo
que puedas + reporte". Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `gastos.py`, `test_gastos.py`),
- la **rúbrica**: `.ai/rubricas/fase-1/excepciones-idiomaticas-python.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/excepciones-idiomaticas-python.md` — no
la mires antes de intentarlo de verdad.
