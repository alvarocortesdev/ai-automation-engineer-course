"""Tests del gate de calidad. Corre: `pytest -v`

Estos tests definen el comportamiento obligatorio (nivel "competente"): cada caso
de violación + el caso feliz + la semántica del gate. NO cubren freshness ni
volumen (profundización): para esos, agrega tu propio test.
"""

from gate import CONTRATO_EVENTOS_PAGO, Reporte, validar_lote

CONTRATO = CONTRATO_EVENTOS_PAGO


def _fila_valida(**overrides):
    fila = {
        "evento_id": "e1",
        "usuario_id": "u1",
        "monto": 1990,
        "estado": "pagado",
        "ts": "2026-06-27T10:00:00+00:00",
    }
    fila.update(overrides)
    return fila


def _lote_limpio():
    return [
        _fila_valida(evento_id="e1", usuario_id="u1", monto=1990, estado="pagado"),
        _fila_valida(evento_id="e2", usuario_id="u2", monto=0, estado="creado"),
    ]


def _reglas(reporte: Reporte) -> set[str]:
    return {v.regla for v in reporte.violaciones}


# --- Caso feliz -------------------------------------------------------------
def test_lote_limpio_pasa_el_gate():
    reporte = validar_lote(_lote_limpio(), CONTRATO)
    assert reporte.ok is True
    assert reporte.violaciones == []
    assert reporte.filas_totales == 2


# --- Schema ------------------------------------------------------------------
def test_campo_requerido_faltante():
    lote = _lote_limpio()
    del lote[1]["estado"]  # falta un campo requerido
    reporte = validar_lote(lote, CONTRATO)
    assert reporte.ok is False
    assert "campo_faltante" in _reglas(reporte)
    viol = next(v for v in reporte.violaciones if v.regla == "campo_faltante")
    assert viol.campo == "estado"
    assert viol.filas == [1]


def test_campo_extra_no_declarado():
    lote = _lote_limpio()
    lote[0]["columna_fantasma"] = 42  # campo no declarado = schema drift
    reporte = validar_lote(lote, CONTRATO)
    assert reporte.ok is False
    assert "campo_extra" in _reglas(reporte)


# --- Valores -----------------------------------------------------------------
def test_tipo_incorrecto():
    lote = _lote_limpio()
    lote[0]["monto"] = "mil novecientos"  # debería ser number
    reporte = validar_lote(lote, CONTRATO)
    assert reporte.ok is False
    assert "tipo" in _reglas(reporte)


def test_nulo_en_campo_requerido():
    lote = _lote_limpio()
    lote[1]["monto"] = None
    reporte = validar_lote(lote, CONTRATO)
    assert reporte.ok is False
    assert "nulo" in _reglas(reporte)


def test_duplicado_en_campo_unico():
    lote = _lote_limpio()
    lote[1]["evento_id"] = "e1"  # evento_id es unico -> e1 repetido
    reporte = validar_lote(lote, CONTRATO)
    assert reporte.ok is False
    assert "duplicado" in _reglas(reporte)
    viol = next(v for v in reporte.violaciones if v.regla == "duplicado")
    assert set(viol.filas) == {0, 1}


def test_valor_fuera_de_dominio():
    lote = _lote_limpio()
    lote[0]["estado"] = "reembolsado"  # no está en valores aceptados
    reporte = validar_lote(lote, CONTRATO)
    assert reporte.ok is False
    assert "valor_no_aceptado" in _reglas(reporte)


def test_valor_fuera_de_rango():
    lote = _lote_limpio()
    lote[1]["monto"] = -50  # viola min: 0
    reporte = validar_lote(lote, CONTRATO)
    assert reporte.ok is False
    assert "fuera_de_rango" in _reglas(reporte)
    viol = next(v for v in reporte.violaciones if v.regla == "fuera_de_rango")
    assert viol.filas == [1]


# --- Semántica del gate / reporte -------------------------------------------
def test_gate_acumula_varias_violaciones():
    # Una sola fila mala dispara varias reglas a la vez.
    lote = _lote_limpio()
    lote[1] = _fila_valida(evento_id="e1", monto=-50, estado="x")
    reporte = validar_lote(lote, CONTRATO)
    assert reporte.ok is False
    # duplicado (e1), fuera_de_rango (-50), valor_no_aceptado ("x")
    assert {"duplicado", "fuera_de_rango", "valor_no_aceptado"} <= _reglas(reporte)


def test_resumen_cuenta_filas_rechazadas():
    lote = _lote_limpio()
    lote[1]["monto"] = -50  # solo la fila 1 es mala
    resumen = validar_lote(lote, CONTRATO).resumen()
    assert resumen["ok"] is False
    assert resumen["filas_totales"] == 2
    assert resumen["filas_rechazadas"] == 1


# TODO (tuyo): agrega al menos un test de caso borde. Sugerencias:
#   - lote vacío,
#   - bool donde se espera number (recuerda: True NO es un number válido),
#   - (profundización) freshness con `ahora` y volumen fuera de banda.
