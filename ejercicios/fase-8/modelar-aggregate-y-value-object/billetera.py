"""Ejercicio 8.2 — Refactor de modelo anémico a aggregate + value object.

PUNTO DE PARTIDA: abajo está el modelo ANÉMICO de una billetera de pre-pago.
Funciona en el caso feliz, pero tiene agujeros (marcados). Tu trabajo es BORRARLO
y reescribir este archivo a DDD táctico, test-driven, cerrando los agujeros.

Contrato final al que debes llegar (lo verifica acceptance_test.py):

  Dinero(centavos: int, moneda: str = "CLP")
      - @dataclass(frozen=True): inmutable + igualdad por valor.
      - centavos negativo -> ValueError.
      - a + b suma si misma moneda; monedas distintas -> ValueError.

  class SaldoInsuficiente(Exception): ...   # excepción de DOMINIO

  class Billetera:                          # aggregate root
      cargar(monto: Dinero) -> None
      pagar(monto: Dinero) -> None          # saldo insuficiente -> SaldoInsuficiente
      saldo() -> Dinero                     # FUNCIÓN de los movimientos, no un campo
      eventos_no_publicados() -> list       # sin exponer lo interno por referencia

  PagoRealizado                             # domain event, inmutable, con monto: Dinero
      - pagar() exitoso lo registra; pago rechazado NO registra evento.

Reescribe TODO lo de abajo. Hazlo crecer una invariante a la vez (bitacora.md).
"""

# ============================================================================
# MODELO ANÉMICO DE PARTIDA  —  BÓRRALO y reescríbelo como DDD táctico.
# ============================================================================
# Agujeros (los que tu refactor debe volver IMPOSIBLES):
#   (1) `saldo` es un campo que se mantiene a mano -> se desincroniza de los movimientos.
#   (2) `pagar` no valida nada -> el saldo puede quedar NEGATIVO.
#   (3) el dinero es un `int` pelado -> nada impide montos negativos ni mezcla de monedas.
#   (4) las reglas viven AFUERA del objeto (en funciones) -> fáciles de saltarse u olvidar.


class BilleteraAnemica:
    def __init__(self):
        self.saldo = 0          # (1) fuente de verdad duplicada
        self.movimientos = []


def cargar(billetera, monto):
    billetera.movimientos.append(("carga", monto))
    billetera.saldo += monto    # (1) si alguien toca .movimientos directo, miente


def pagar(billetera, monto):
    billetera.saldo -= monto    # (2) NADA impide saldo < 0
    billetera.movimientos.append(("pago", monto))


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que pasa ANTES de correrlo? (el anémico lo permite)
    b = BilleteraAnemica()
    cargar(b, 500)
    pagar(b, 800)
    print("saldo anémico tras pagar 800 sobre 500:", b.saldo)  # ... queda en -300
