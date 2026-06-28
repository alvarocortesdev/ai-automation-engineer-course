"""Tus tests — crécelos una invariante a la vez (red -> green -> refactor).

Empieza por el value object Dinero (lo más pequeño), luego la Billetera, luego el evento.
El primer test ya está escrito y arranca en ROJO (Dinero todavía no existe en billetera.py
hasta que lo escribas). NO copies acceptance_test.py: el ejercicio es que TÚ traduzcas el
contrato a tests.
"""

import pytest

# Cuando escribas el value object en billetera.py, este import dejará de fallar.
from billetera import Dinero


def test_dinero_no_puede_ser_negativo():
    # Comportamiento 1 (rojo): un Dinero negativo debe ser IMPOSIBLE de construir.
    with pytest.raises(ValueError):
        Dinero(-1)


# Sigue tú: igualdad por valor, suma misma moneda, ValueError entre monedas distintas,
# saldo inicial 0, cargar aumenta, pagar descuenta, pagar de más lanza SaldoInsuficiente
# y NO deja saldo negativo, pago exitoso emite PagoRealizado, pago rechazado no emite.
