"""Módulo legado (#412) — resumen de una cuenta. ESTABA EN PRODUCCIÓN.

NO reescribas el módulo. Tu trabajo es DEPURAR con método:
  reproducir → leer el stack trace → hipótesis → confirmar con pdb →
  test de regresión que falle PRIMERO → arreglar SOLO la causa raíz.

Bug reportado (ticket #412):
  "El resumen revienta para cuentas que solo tienen abonos."

Cada movimiento es un dict: {"tipo": "abono" | "cargo", "monto": int}.
  saldo       = suma de abonos - suma de cargos
  mayor_cargo = el cargo más grande
"""


def _solo(movimientos, tipo):
    """Devuelve los montos de los movimientos de un tipo dado."""
    return [m["monto"] for m in movimientos if m["tipo"] == tipo]


def resumen_cuenta(movimientos):
    abonos = _solo(movimientos, "abono")
    cargos = _solo(movimientos, "cargo")
    saldo = sum(abonos) - sum(cargos)
    return {
        "saldo": saldo,
        "n_movimientos": len(movimientos),
        "mayor_cargo": max(cargos),  # <-- el reporte #412 apunta por aquí
    }


if __name__ == "__main__":
    # Caso "normal" (funciona hoy):
    normales = [
        {"tipo": "abono", "monto": 1000},
        {"tipo": "cargo", "monto": 300},
        {"tipo": "cargo", "monto": 700},
    ]
    print(resumen_cuenta(normales))

    # Caso del ticket #412 (revienta hoy): descomenta y córrelo bajo pdb.
    # solo_abonos = [{"tipo": "abono", "monto": 1000}, {"tipo": "abono", "monto": 500}]
    # print(resumen_cuenta(solo_abonos))
