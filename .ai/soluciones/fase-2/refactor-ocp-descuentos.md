---
ejercicio_id: fase-2/refactor-ocp-descuentos
fase: fase-2
sub_unidad: "2.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Refactor a Open/Closed con red de tests

## Respuesta canónica

Una abstracción `Descuento` con una clase por tipo, y un **registro** (`dict`) que mapea el string del tipo a
una instancia. La función pública conserva su firma y delega al registro; agregar un tipo es **una clase + una
entrada**, sin reabrir la lógica de precio.

```python
"""descuentos.py — refactorizado a Open/Closed."""
from typing import Protocol


class Descuento(Protocol):
    def calcular(self, monto: int) -> int: ...


class SinDescuento:
    def calcular(self, monto: int) -> int:
        return 0


class DescuentoPorcentaje:
    """Estrategia parametrizada por porcentaje: evita 5 clases casi idénticas."""

    def __init__(self, pct: int) -> None:
        self._pct = pct

    def calcular(self, monto: int) -> int:
        return monto * self._pct // 100


# Registro: único punto de extensión. Agregar un tipo = una entrada nueva.
_REGISTRO: dict[str, Descuento] = {
    "regular": SinDescuento(),
    "vip": DescuentoPorcentaje(10),
    "empleado": DescuentoPorcentaje(30),
    "estudiante": DescuentoPorcentaje(15),
    "jubilado": DescuentoPorcentaje(20),
    "mayorista": DescuentoPorcentaje(25),   # ← la extensión, sin tocar nada más
}


def calcular_descuento(cliente_tipo: str, monto: int) -> int:
    """Firma pública intacta: delega al registro; tipo desconocido → 0."""
    estrategia = _REGISTRO.get(cliente_tipo, SinDescuento())
    return estrategia.calcular(monto)
```

Test del tipo nuevo que el alumno agrega (sin tocar las clases existentes):

```python
def test_descuento_mayorista():
    assert calcular_descuento("mayorista", 10_000) == 2_500
```

## Razonamiento paso a paso

1. **El contrato común** es `calcular(self, monto: int) -> int`. Es lo que comparten las cinco ramas del
   `if/elif`. Declararlo como `Protocol` (o `ABC`) elimina la necesidad de preguntar el tipo.
2. **El despacho** pasa de `if/elif` a un `dict` string→instancia. Esto es clave: un `dict`-registro **no es** el
   smell `switch`, porque agregar un caso no introduce una rama condicional nueva en la lógica —solo una entrada
   de datos. La función `calcular_descuento` queda **cerrada a modificación**.
3. **La extensión** (`mayorista`) es literalmente una línea en el registro. Eso es OCP demostrado: el código
   probado no se reabre.

## Variantes aceptables (NO penalizar)
- **`abc.ABC` + `@abstractmethod`** en vez de `Protocol`: igual de válido. `Protocol` es más "pythónico" (duck
  typing tipado, sin herencia obligatoria); `ABC` es más explícito. Ambos son `competente`.
- **Una clase por tipo** (`DescuentoVip`, `DescuentoEmpleado`, …) en vez de la `DescuentoPorcentaje`
  parametrizada: es **igualmente correcto** y más fiel al enunciado literal ("una clase por tipo"). La versión
  parametrizada es un refinamiento (evita 5 clases casi clonadas, aplica DRY) y cuenta como `excelente` si el
  alumno lo justifica —pero **no es obligatoria**; una clase por tipo es perfectamente competente.
- **Auto-registro** vía decorador o `__init_subclass__`: técnicamente válido, pero para 6 casos es
  **sobre-ingeniería** (justo la crítica de la lección). Si aparece, el corrector lo nota como señal de
  dependencia-IA o de celo dogmático, no como mérito —salvo que el alumno lo defienda con un trade-off real.
- **Función pública que recibe la estrategia inyectada** (`precio_final(monto, descuento)`): es el diseño DIP
  puro de la lección, pero **rompe la firma `calcular_descuento(cliente_tipo, monto)`** que los tests usan. Si el
  alumno fue por ahí, debió mantener además un wrapper que respete la firma original. Sin el wrapper, los tests
  no pasan → `en-progreso` en C1.

## Puntos resbalosos (donde el corrector debe mirar)
1. **¿Modificó los tests?** Si cambió valores esperados o la firma, el comportamiento cambió → no es un refactor.
2. **¿El despacho sigue ramificando por tipo?** Un `if tipo == "vip": return DescuentoVip()` disfraza el smell,
   no lo elimina. El registro `dict` es la señal de OCP real.
3. **Truncado a entero:** `vip` de 999 = 99 (no 100). Si usó `round`, falla `test_redondeo_a_entero`.
4. **Tipo desconocido → 0:** debe preservarse con `.get(..., SinDescuento())` o equivalente.
5. **Agregar `mayorista` sin tocar lo demás:** si para agregarlo editó otra clase o una rama, no demostró OCP.
