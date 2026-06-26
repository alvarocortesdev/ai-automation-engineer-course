"""Tests del ejercicio 2.12 — depurar con método.

ESTADO INICIAL:
- `test_caso_normal_funciona` PASA hoy (el bug está aislado: no rompe todo).
- `test_regresion_412_solo_abonos` FALLA hoy con un ValueError (reproduce #412).
  Ese fallo es el "rojo" que DEBE existir antes de que arregles nada.

Flujo: corre `pytest` y mira el rojo. Recién después de confirmar la causa con
pdb (ver README), arregla `solucion.py` y completa el TODO del test de regresión.
"""

import pytest

from solucion import resumen_cuenta


def test_caso_normal_funciona():
    movs = [
        {"tipo": "abono", "monto": 1000},
        {"tipo": "cargo", "monto": 300},
        {"tipo": "cargo", "monto": 700},
    ]
    r = resumen_cuenta(movs)
    assert r["saldo"] == 0
    assert r["n_movimientos"] == 3
    assert r["mayor_cargo"] == 700


def test_regresion_412_solo_abonos():
    """Ticket #412: una cuenta con solo abonos NO debe reventar.

    HOY este test falla (ValueError: max() ... is empty). Esa es la prueba
    objetiva del bug. Cuando arregles la causa raíz, debe pasar.
    """
    movs = [{"tipo": "abono", "monto": 1000}, {"tipo": "abono", "monto": 500}]
    r = resumen_cuenta(movs)
    assert r["saldo"] == 1500
    # TODO: afirma cuánto vale "mayor_cargo" cuando NO hay cargos.
    #       Declara tu decisión de diseño (0 o None) en traza.md y fíjala aquí.
    # assert r["mayor_cargo"] == ...


# ---------------------------------------------------------------------------
# DEUDA SEPARADA (dos sombreros): el módulo IGNORA en silencio un movimiento
# cuyo `tipo` no es "abono" ni "cargo". Eso quizá sea un bug, pero NO es el
# ticket #412 y NO se arregla aquí. Lo dejamos pintado como comportamiento
# deseado FUTURO con xfail, para registrar la deuda sin "arreglar de paso".
# ---------------------------------------------------------------------------
@pytest.mark.xfail(reason="deuda: hoy un tipo desconocido se ignora; fix en ticket aparte")
def test_deuda_tipo_desconocido_no_se_ignora_en_silencio():
    movs = [{"tipo": "abono", "monto": 1000}, {"tipo": "comision", "monto": 200}]
    r = resumen_cuenta(movs)
    # Comportamiento DESEADO (todavía no implementado): que el desconocido
    # no desaparezca sin dejar rastro. Hoy n_movimientos los cuenta pero el
    # monto de "comision" no entra a ningún lado. Define en el ticket futuro
    # qué debería pasar (¿warning? ¿categoría "otros"?) y testéalo ALLÁ.
    assert r.get("ignorados") == 1
