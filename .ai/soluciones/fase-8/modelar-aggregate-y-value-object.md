---
ejercicio_id: fase-8/modelar-aggregate-y-value-object
fase: fase-8
sub_unidad: "8.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Hay **variantes válidas**
> (cómo guarda los movimientos, si modela `Movimiento` como enum+Dinero o dos listas): lo que
> mide la rúbrica es que las **invariantes sean imposibles de violar**, no que el código sea idéntico.

# Solución de referencia — Refactor a aggregate + value object

## Cómo usar esta solución
El alumno entrega `billetera.py` + `test_billetera.py` + `bitacora.md`. Corre
`acceptance_test.py` (11 tests) como primer filtro objetivo. Luego contrasta el diseño contra
lo de abajo, buscando **fugas** que los tests no cubren (colección expuesta, `assert` en vez de
`raise`, evento antes de validar).

## Respuesta canónica (una versión que pasa los 11 tests)

```python
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Dinero:
    centavos: int
    moneda: str = "CLP"

    def __post_init__(self) -> None:
        if self.centavos < 0:
            raise ValueError("Dinero no puede ser negativo")

    def __add__(self, otro: "Dinero") -> "Dinero":
        if self.moneda != otro.moneda:
            raise ValueError("No se suman monedas distintas")
        return Dinero(self.centavos + otro.centavos, self.moneda)


class TipoMovimiento(Enum):
    CARGA = "carga"
    PAGO = "pago"


@dataclass(frozen=True)
class Movimiento:
    tipo: TipoMovimiento
    monto: Dinero


@dataclass(frozen=True)
class PagoRealizado:           # domain event: pasado, inmutable
    monto: Dinero


class SaldoInsuficiente(Exception):
    """Excepción de dominio: no hay saldo para el pago."""


class Billetera:               # aggregate root
    def __init__(self) -> None:
        self._movimientos: list[Movimiento] = []
        self._eventos: list[object] = []

    def cargar(self, monto: Dinero) -> None:
        self._movimientos.append(Movimiento(TipoMovimiento.CARGA, monto))

    def pagar(self, monto: Dinero) -> None:
        if monto.centavos > self.saldo().centavos:    # 1) VALIDA primero
            raise SaldoInsuficiente(monto.centavos)
        self._movimientos.append(Movimiento(TipoMovimiento.PAGO, monto))  # 2) muta
        self._eventos.append(PagoRealizado(monto=monto))                  # 3) emite

    def saldo(self) -> Dinero:                         # FUNCIÓN, no campo
        total = 0
        for m in self._movimientos:
            total += m.monto.centavos if m.tipo is TipoMovimiento.CARGA else -m.monto.centavos
        return Dinero(total)

    def eventos_no_publicados(self) -> list:
        return list(self._eventos)                     # copia: no filtra lo interno
```

## Razonamiento paso a paso
1. **`Dinero` carga su invariante.** `frozen=True` da inmutabilidad + igualdad por valor + hash. `__post_init__` hace **imposible** construir un negativo. `__add__` bloquea cross-currency. El dinero va en **centavos enteros** (nunca `float`).
2. **El saldo se calcula, no se guarda.** Es el corazón del ejercicio: al eliminar el campo `saldo`, se elimina *por construcción* el bug de desincronización. No hay forma de que el saldo "mienta" porque no existe como estado independiente.
3. **La invariante "no negativo" se protege en `pagar()`**, validando antes de mutar. El orden validar → mutar → emitir garantiza que `PagoRealizado` solo se registra si el pago de verdad ocurrió.
4. **No se filtra lo interno.** `eventos_no_publicados()` devuelve copia; los movimientos no se exponen por referencia.

## Puntos resbalosos / variantes
- **Variante válida:** dos listas separadas (`_cargas`, `_pagos`) en vez de una de `Movimiento`. Correcto si el saldo sigue siendo función y nada se filtra.
- **Variante válida:** `Movimiento` con signo en el `Dinero` no sirve (Dinero no admite negativos); por eso el tipo (CARGA/PAGO) va aparte. Si el alumno usó un campo `delta: int`, aceptable si protege el no-negativo del saldo.
- **Fuga típica que los tests NO atrapan:** un `def movimientos(self): return self._movimientos` (sin copiar) permite mutar desde fuera. Márcalo aunque `acceptance_test.py` pase.
- **`assert self.centavos >= 0`** en vez de `raise`: se desactiva con `python -O`. No es robusto; márcalo.

## Rango de soluciones aceptables
Cualquier diseño donde: (a) `Dinero` sea inmutable/no-negativo/no-cross-currency, (b) el saldo sea **función** de los movimientos (no un campo mutable), (c) `pagar` valide antes de mutar y no deje saldo negativo, (d) no se filtre la colección interna, y (e) el evento se emita solo en pago exitoso. Nombres internos, estructura de datos y si usa `Enum` o constantes son libres.
