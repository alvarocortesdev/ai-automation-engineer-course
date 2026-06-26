---
ejercicio_id: fase-1/tdd-total-propina
fase: fase-1
sub_unidad: "1.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Tu primer ciclo red-green-refactor (TDD)

## Implementación canónica (`solucion.py`)

```python
def total_con_propina(monto, pct_propina):
    if monto < 0:
        raise ValueError(f"monto no puede ser negativo: {monto}")
    if not 0 <= pct_propina <= 100:
        raise ValueError(f"pct_propina fuera de [0,100]: {pct_propina}")
    propina = round(monto * pct_propina / 100)
    return monto + propina
```

## Suite canónica (`test_solucion.py`)

```python
import pytest
from solucion import total_con_propina


@pytest.mark.parametrize("monto, pct, esperado", [
    (10000, 10, 11000),   # caso típico
    ( 5000,  0,  5000),   # pct 0 -> total == monto
    ( 8000, 100, 16000),  # pct máximo -> dobla
    (    0, 10,     0),   # monto 0
    (12340, 10, 13574),   # 12340 + round(1234.0)
])
def test_total_camino_feliz(monto, pct, esperado):
    assert total_con_propina(monto, pct) == esperado


@pytest.mark.parametrize("monto_invalido", [-1, -100])
def test_monto_negativo_lanza_value_error(monto_invalido):
    with pytest.raises(ValueError):
        total_con_propina(monto_invalido, 10)


@pytest.mark.parametrize("pct_invalido", [-1, 101, 200])
def test_pct_fuera_de_rango_lanza_value_error(pct_invalido):
    with pytest.raises(ValueError):
        total_con_propina(10000, pct_invalido)
```

## Razonamiento paso a paso (el ciclo que debió recorrer)

1. **RED #1:** escribe `test_propina_10_pct_de_10000` (la semilla). Corre `pytest` → falla
   con `NotImplementedError`. Eso confirma que el test ejerce la función.
2. **GREEN #1:** implementa el mínimo: `return monto + round(monto * pct_propina / 100)`.
   Corre → verde.
3. **RED #2:** agrega el caso `pct == 0`. Como el cálculo ya lo cubre (propina 0), puede salir
   verde de inmediato — está bien; lo importante es haber escrito el test.
4. **RED #3:** agrega `test_monto_negativo_lanza_value_error` con `pytest.raises`. Hoy la función
   NO lanza nada (devuelve un número negativo) → **rojo**. GREEN: agrega la guarda `if monto < 0`.
5. **RED #4:** agrega `test_pct_fuera_de_rango...` → rojo → GREEN con `if not 0 <= pct_propina <= 100`.
6. **REFACTOR:** junta los casos felices en un `parametrize`, mejora nombres/mensajes. Tests siguen verdes.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Orden de las guardas vs. el cálculo.** Las validaciones van **antes** del cálculo: no tiene
   sentido calcular sobre un input inválido.
2. **`round` y "banker's rounding".** En Python 3, `round(0.5) == 0` y `round(2.5) == 2` (redondeo
   al par). Por eso el caso `(12340, 10)` se eligió sin `.5` (da `1234.0` exacto). Si el alumno usa
   un caso como `(15, 10)` → `round(1.5) == 2`, el esperado correcto es `17`, no `16`. No es un bug:
   es la regla de `round`. Marcar solo si el alumno afirma un esperado equivocado por no conocerla.
3. **Entero, no `float`.** El resultado debe ser entero. `monto * pct_propina / 100` es `float`; el
   `round(...)` lo vuelve `int`, y `monto + int` es `int`. Correcto.
4. **`assert` sin comparación.** `assert total_con_propina(10000, 10)` (sin `== 11000`) pasa con
   cualquier número distinto de cero: no verifica nada. Cazar.

## Rango de soluciones aceptables
- **Validar `pct` con dos `if` separados** (`< 0` y `> 100`) en vez de la cadena `0 <= pct <= 100`:
  igual de válido.
- **`int(round(...))` explícito**: redundante (`round` de un float ya da `int` con un solo argumento),
  pero correcto.
- **No usar `parametrize`** y tener varios tests separados bien nombrados: baja a `competente` en C2;
  el objetivo explícito pide `parametrize`, pero la cobertura sigue siendo válida.
- **Mensajes de excepción:** cualquier texto razonable; no se exige redacción concreta.
- **`pytest.approx`:** innecesario aquí (trabajamos en enteros). Si aparece, no es error, pero puede
  señalar receta pegada; contrastar con el resto.
- **Caso borde propio:** se acepta cualquiera defendible (pct=50, monto muy grande, `round` con `.5`
  bien razonado, etc.).
