"""Auto-verificación del contrato (8.2). Corre SOLO al final:

    uv run pytest acceptance_test.py

Verifica el comportamiento observable del modelo DDD, sin atarte a nombres internos
(cómo guardas los movimientos es decisión tuya). Si pasa en verde, tu aggregate
protege sus invariantes y tu value object carga las suyas.
"""

import pytest

from billetera import Dinero, Billetera, SaldoInsuficiente


# ---------- Value object: Dinero ----------

def test_dinero_igualdad_por_valor():
    assert Dinero(1000) == Dinero(1000)
    assert Dinero(1000) != Dinero(999)


def test_dinero_es_inmutable():
    d = Dinero(1000)
    with pytest.raises(Exception):       # FrozenInstanceError (subclase de AttributeError)
        d.centavos = 5


def test_dinero_no_negativo():
    with pytest.raises(ValueError):
        Dinero(-1)


def test_dinero_suma_misma_moneda():
    assert Dinero(1000) + Dinero(500) == Dinero(1500)


def test_dinero_no_suma_monedas_distintas():
    with pytest.raises(ValueError):
        Dinero(1000, "CLP") + Dinero(1000, "USD")


# ---------- Aggregate root: Billetera ----------

def test_billetera_arranca_en_cero():
    assert Billetera().saldo() == Dinero(0)


def test_cargar_aumenta_el_saldo():
    b = Billetera()
    b.cargar(Dinero(1000))
    b.cargar(Dinero(500))
    assert b.saldo() == Dinero(1500)


def test_pagar_descuenta_del_saldo():
    b = Billetera()
    b.cargar(Dinero(1000))
    b.pagar(Dinero(300))
    assert b.saldo() == Dinero(700)


def test_pagar_de_mas_rechaza_y_no_deja_saldo_negativo():
    b = Billetera()
    b.cargar(Dinero(500))
    with pytest.raises(SaldoInsuficiente):
        b.pagar(Dinero(800))
    assert b.saldo() == Dinero(500)      # saldo intacto: la invariante se respetó


# ---------- Domain event: PagoRealizado ----------

def test_pago_exitoso_emite_evento():
    b = Billetera()
    b.cargar(Dinero(1000))
    b.pagar(Dinero(400))
    eventos = b.eventos_no_publicados()
    assert len(eventos) == 1
    assert type(eventos[0]).__name__ == "PagoRealizado"
    assert eventos[0].monto == Dinero(400)


def test_pago_rechazado_no_emite_evento():
    b = Billetera()
    b.cargar(Dinero(100))
    with pytest.raises(SaldoInsuficiente):
        b.pagar(Dinero(999))
    assert b.eventos_no_publicados() == []
