# tipar-y-pasar-mypy — Tipar un módulo y hacer pasar `mypy --strict`

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.4` Type hints, mypy y pydantic
**Ruta:** crítica · **Modalidad:** código · **Timebox:** 30–40 min

## 🎯 Objetivo

Anotar un módulo Python **sin tipos** hasta que `mypy --strict` reporte **0 errores**, y en el
camino dejar que mypy te muestre un **bug latente** (un campo opcional tratado como si siempre
estuviera). El arreglo nace del aviso de mypy, no de un parche a ciegas.

## 📋 Contexto

Los type hints son la mini-spec que una herramienta puede verificar **antes de ejecutar**. `mypy
--strict` es esa herramienta en modo exigente: el mismo que corre en el CI de un equipo profesional.
Aquí ves su valor real: atrapar, en tu editor, la clase de bug más común (pasar `None` donde
esperabas un número) **antes** de que un dato incompleto lo dispare en producción.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, sin IA (timebox arriba). Lee el error de mypy con calma: te dice el tipo exacto.
2. Solo entonces consulta **documentación oficial** de mypy/typing si la necesitas.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* las anotaciones.
4. Mañana, vuelve a anotar el módulo **de memoria** y explica por qué `int | None` no es asignable a `int`.

## 🛠️ Instrucciones

Instala las herramientas una vez (si no las tienes):

```bash
uv add pydantic mypy      # o:  pip install mypy
```

Luego, **en este orden**:

1. **Anota** `despensa.py`: parámetros y retorno de **ambas** funciones, y el acumulador local.
   - Los precios son enteros (pesos): una lista de items es `list[dict[str, int]]`.
   - La división `/` devuelve `float`: piensa qué tipo tiene el retorno de `descuento` y el acumulador.
2. **Verifica estáticamente** y lee el aviso:

   ```bash
   uv run mypy --strict despensa.py
   ```

3. **Arregla** el bug que mypy revela (un **default** para el campo opcional). Nada de `# type: ignore`.
4. **Corre los tests** hasta que pasen todos:

   ```bash
   uv run pytest
   ```

5. **Cierra el loop.** Agrega en `test_despensa.py` **un test tuyo** para otro caso borde (p. ej. lista vacía).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `uv run mypy --strict despensa.py` reporta **0 errores** (todas las funciones y el acumulador anotados).
- [ ] Los 4 tests pasan, incluido `test_item_sin_descuento_se_trata_como_cero`.
- [ ] El arreglo del bug es un **default** (`.get("descuento_pct", 0)`), no un `# type: ignore` ni un cast forzado.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes explicar **sin notas** por qué mypy marcó el error y por qué `int | None` no es asignable a `int`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

mypy --strict te marcará **dos** cosas. (1) `item.get("descuento_pct")` tiene tipo `int | None`
—`.get` devuelve `None` cuando la clave falta— y se lo pasas a un parámetro que pediste `int`. El
arreglo correcto es darle un **default** al `.get` para que jamás devuelva `None`. (2) Si arrancas
el acumulador con `suma = 0`, mypy lo infiere `int`, pero le sumas el `float` que devuelve la
división; anótalo `suma: float = 0`. Ambos avisos desaparecen solos cuando los tipos quedan
coherentes. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `despensa.py`, `test_despensa.py`),
- la **rúbrica**: `.ai/rubricas/fase-1/tipar-y-pasar-mypy.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/tipar-y-pasar-mypy.md` — no la mires
antes de intentarlo de verdad.
