# validar-salida-llm-pydantic — Validar la salida de un LLM con pydantic

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.4` Type hints, mypy y pydantic
**Ruta:** crítica · **Modalidad:** código · **Timebox:** 35–45 min

## 🎯 Objetivo

Diseñar un modelo **pydantic v2** que valide, en la **frontera**, un JSON producido por un LLM:
acepta los datos limpios y tipados, o los rechaza con `ValidationError`. Esto es el patrón que se
repite en cada feature de IA: **nunca confíes en la salida del modelo sin validarla**.

## 📋 Contexto

Un LLM te devuelve texto. Le pediste un JSON con cinco campos y a veces te lo da bien, a veces
manda el `monto` como string, deja un campo en blanco, devuelve `items` vacío, o **alucina** un
campo que nunca pediste. Validar en la frontera —el punto exacto donde el dato no confiable entra a
tu sistema— es lo que separa un script de juguete de un servicio que no explota con el primer dato
raro. Lo formalizarás en `6.4` (structured outputs) y `6.14` (seguridad LLM); el músculo se forma aquí.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, sin IA (timebox arriba). Diseña el contrato **antes** de codear (spec-first).
2. Solo entonces consulta la **documentación oficial** de pydantic v2 si la necesitas.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* el modelo.
4. Mañana, reescribe el modelo **de memoria** y explica por qué `extra="forbid"` importa con LLMs.

## 🛠️ Instrucciones

Instala pydantic una vez (si no lo tienes):

```bash
uv add pydantic        # o:  pip install pydantic
```

Luego:

1. **Diseña el modelo** `Compra` en `compra.py` según el contrato del docstring (cinco campos, con
   sus tipos y constraints). Decide qué `Field(...)` y qué `@field_validator` necesita cada uno.
2. **Cierra la puerta** a campos alucinados con `model_config = ConfigDict(extra="forbid")`.
3. **Implementa** `parsear_compra(raw_json)` para que **parsee y valide en un solo paso**
   (un método de pydantic v2 hace ambas cosas; no uses `json.loads` por separado).
4. **Verifica** hasta que pasen todos los tests:

   ```bash
   uv run pytest
   ```

5. **Cierra el loop.** Agrega en `test_compra.py` **un test tuyo** para un caso borde realista de un
   LLM (monto como `"12990.5"`, un item vacío en la lista, un campo faltante, etc.).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `Compra` valida el JSON correcto y **coacciona** `monto` de `"12990"` a `12990` (int).
- [ ] Rechaza con `ValidationError`: `monto <= 0`, `comercio`/`categoria` vacíos o de solo espacios,
      `items` vacío, fecha inválida y **campos alucinados** (extra).
- [ ] `parsear_compra` usa el método de pydantic v2 que **parsea JSON y valida a la vez**.
- [ ] Agregaste al menos un test propio de un caso borde realista de un LLM.
- [ ] Puedes explicar **sin notas** qué es "validar en la frontera" y por qué `extra="forbid"` importa.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Piensa el contrato antes de codear: `monto` es `int` con `Field(gt=0)`; `items` es `list[str]` con
`Field(min_length=1)`; `fecha` es `date` (pydantic parsea la cadena ISO solo). Para los strings de
solo espacios, `Field(min_length=1)` **no** alcanza —`"   "` tiene largo 3—: necesitas un
`@field_validator("comercio", "categoria")` (con `@classmethod` justo debajo) que haga `strip` y
lance `ValueError` si queda vacío. Para los campos alucinados,
`model_config = ConfigDict(extra="forbid")`. Para parsear+validar en un paso,
`Compra.model_validate_json(raw_json)`. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `compra.py`, `test_compra.py`),
- la **rúbrica**: `.ai/rubricas/fase-1/validar-salida-llm-pydantic.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/validar-salida-llm-pydantic.md` — no la
mires antes de intentarlo de verdad.
