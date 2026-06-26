---
ejercicio_id: fase-2/mockear-llm-extractor
fase: fase-2
sub_unidad: "2.11"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Mockear el LLM: suite para un extractor de pedidos

## Suite canónica (`test_solucion.py`)

```python
import pytest
from unittest.mock import Mock

from solucion import (
    Pedido,
    ExtraccionInvalida,
    extraer_pedido,
    construir_prompt,
    INSTRUCCION,
)


def fake_llm(respuesta):
    """Stub: ignora el prompt y devuelve siempre `respuesta` (un STRING)."""
    def generar(prompt):
        return respuesta
    return generar


# TODO 1 — happy path
def test_extrae_pedido_valido():
    pedido = extraer_pedido("quiero 2 cafés", fake_llm('{"producto": "café", "cantidad": 2}'))
    assert pedido == Pedido(producto="café", cantidad=2)


# TODO 2 — el prompt incluye el mensaje (spy con Mock)
def test_el_prompt_incluye_el_mensaje():
    generar = Mock(return_value='{"producto": "café", "cantidad": 2}')
    extraer_pedido("quiero 2 cafés", generar)
    prompt_enviado = generar.call_args.args[0]
    assert "quiero 2 cafés" in prompt_enviado
    assert INSTRUCCION in prompt_enviado
    generar.assert_called_once()


# TODO 3 — respuesta no-JSON
def test_respuesta_no_json_lanza_error():
    with pytest.raises(ExtraccionInvalida):
        extraer_pedido("...", fake_llm("Claro, el cliente quiere 2 cafés :)"))


# TODO 4 — cantidad inválida (caza al mutante_a)
@pytest.mark.parametrize("cuerpo", [
    '{"producto": "café", "cantidad": -3}',   # ≤ 0
    '{"producto": "café", "cantidad": 0}',    # ≤ 0
    '{"producto": "café", "cantidad": "2"}',  # no es entero (string)
    '{"producto": "café", "cantidad": true}', # bool no cuenta como entero
])
def test_cantidad_invalida_lanza_error(cuerpo):
    with pytest.raises(ExtraccionInvalida):
        extraer_pedido("...", fake_llm(cuerpo))


# TODO 5 — mensaje vacío: NO se llama al modelo
def test_mensaje_vacio_no_llama_al_modelo():
    generar = Mock()
    with pytest.raises(ExtraccionInvalida):
        extraer_pedido("   ", generar)
    generar.assert_not_called()


# Extra defendible (sube a "excelente"): clave faltante es otra rama de error
def test_clave_faltante_lanza_error():
    with pytest.raises(ExtraccionInvalida):
        extraer_pedido("...", fake_llm('{"producto": "café"}'))
```

## Por qué cada test prueba lo que dice probar
- **Happy path**: la respuesta `café/2` la escribió el autor del test → el assert prueba que el código **parsea y construye el `Pedido`**, no que el modelo extraiga bien.
- **Prompt (spy)**: verifica la **interacción** con la frontera. El prompt debe acarrear el mensaje del usuario; si no, el modelo recibiría una instrucción sin datos. `INSTRUCCION in prompt` fija que la plantilla no se rompió.
- **No-JSON**: `json.loads("Claro, ...")` lanza `JSONDecodeError`, que el SUT envuelve en `ExtraccionInvalida`. Sin este test, un modelo charlatán tumbaría producción con un error crudo.
- **Cantidad inválida**: ejercita la rama de validación. Es **el caso que caza al `mutante_a`** (que omite esa validación). `"2"` (string) y `true` (bool) son trampas reales: `json.loads` los acepta como tipos JSON pero no son cantidades válidas.
- **Vacío sin llamar**: el `assert_not_called()` comprueba la optimización/regla de negocio de no gastar una llamada (tokens) en entrada vacía.

## Autochequeo con el mutante (el corrector debe pedir evidencia)
- Apuntar el import a `mutantes.mutante_a` (omite la validación de cantidad): el caso `cantidad: -3` (y `0`, `"2"`, `true`) pasa de esperar `ExtraccionInvalida` a **recibir un `Pedido`** → la suite se pone **ROJA**. Si la suite no tiene el caso de cantidad inválida, queda verde y el mutante "sobrevive".
- Revertir el import a `solucion` y confirmar verde.

## Por qué se mockea la frontera y NO el resto
- `generar` (la llamada al LLM) es la **frontera**: red, costo, no determinismo. Se reemplaza por un fake/Mock.
- `json.loads`, la validación de claves y la de cantidad son **lógica pura**: se prueban reales, por su efecto. Mockearlas sería sobre-mockeo: el test dejaría de probar el parseo/validación, que es justo lo que se quiere cubrir.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Fake string vs. dict**: el fake DEBE devolver un string (la frontera real devuelve texto). Si devuelve un dict, el parser nunca corre — penalizar en C1 y comentar.
2. **No mockear `json.loads`**: si lo hace, el test no prueba el parseo (sobre-mockeo).
3. **`bool` como cantidad**: `isinstance(True, int)` es `True` en Python; el SUT lo rechaza explícitamente. No es obligatorio que el alumno tenga ese caso, pero suma.
4. **Spy del prompt**: aceptar `Mock(return_value=...)` + `call_args`, o una función espía casera que guarda el prompt en una lista. Ambas válidas.
5. **Calidad del modelo**: ningún test debe pretender probarla. Si el alumno cree que el happy path "prueba que el modelo clasifica/extrae bien", corregir el concepto: eso es un eval.

## Rango de soluciones aceptables
- **Tests separados** por cada caso de cantidad inválida en vez de `parametrize`: funciona; el `parametrize` es más limpio (mejor para "excelente").
- **Stub casero** (`lambda`/función) en vez de `Mock` para el happy path y los errores: válido. El `Mock` es necesario solo para el spy del prompt y el `assert_not_called`.
- **Sin el test extra de clave faltante**: aceptable para "competente"; tenerlo sube a "excelente" por distinguir ramas de error vecinas.
- **`notas.md`** con el análisis del mutante: no obligatorio, suma.
- **Probar `construir_prompt` por separado** como función pura: bienvenido, no exigido.
