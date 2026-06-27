"""Tests para armar_contexto.

Estrategia: usamos un contador de tokens determinista (palabras) inyectado, así los
tests no dependen de ninguna API ni librería externa. Verifican la POLÍTICA, no
números mágicos de un tokenizer real.
"""

import pytest

from presupuesto import armar_contexto


def palabras(texto: str) -> int:
    return len(texto.split())


def _turno(rol: str, n: int, etiqueta: str) -> dict:
    """Un turno con n palabras, todas iguales a `etiqueta` (para identificarlo)."""
    return {"role": rol, "content": " ".join([etiqueta] * n)}


SYSTEM = " ".join(["sys"] * 5)  # 5 palabras


def _historial_5():
    return [
        _turno("user", 10, "t0"),
        _turno("assistant", 10, "t1"),
        _turno("user", 10, "t2"),
        _turno("assistant", 10, "t3"),
        _turno("user", 10, "t4"),
    ]


def test_system_siempre_presente():
    ctx = armar_contexto(SYSTEM, _historial_5(), 35, palabras)
    assert ctx["system"] == SYSTEM


def test_total_dentro_del_presupuesto():
    ctx = armar_contexto(SYSTEM, _historial_5(), 35, palabras)
    total = palabras(ctx["system"]) + sum(palabras(m["content"]) for m in ctx["messages"])
    assert total <= 35


def test_conserva_los_mas_recientes():
    # budget 35: system(5) deja 30 -> caben 3 turnos de 10 -> los 3 MÁS recientes.
    ctx = armar_contexto(SYSTEM, _historial_5(), 35, palabras)
    etiquetas = [m["content"].split()[0] for m in ctx["messages"]]
    assert etiquetas == ["t2", "t3", "t4"]


def test_orden_cronologico_en_la_salida():
    # La salida va del más viejo al más reciente, no invertida.
    ctx = armar_contexto(SYSTEM, _historial_5(), 35, palabras)
    etiquetas = [m["content"].split()[0] for m in ctx["messages"]]
    assert etiquetas == sorted(etiquetas)  # t2 < t3 < t4


def test_incluidos_son_un_sufijo_del_historial():
    # "no partir mensajes" + "recencia": lo incluido es un sufijo contiguo.
    historial = _historial_5()
    ctx = armar_contexto(SYSTEM, historial, 35, palabras)
    n = len(ctx["messages"])
    assert historial[-n:] == ctx["messages"]


def test_solo_el_mas_reciente_cuando_apenas_cabe_uno():
    # budget 15: system(5) deja 10 -> cabe exactamente 1 turno (el más reciente).
    ctx = armar_contexto(SYSTEM, _historial_5(), 15, palabras)
    etiquetas = [m["content"].split()[0] for m in ctx["messages"]]
    assert etiquetas == ["t4"]


def test_ningun_turno_cabe_pero_system_si():
    # budget 10: system(5) deja 5, pero cada turno cuesta 10 -> messages vacío.
    ctx = armar_contexto(SYSTEM, _historial_5(), 10, palabras)
    assert ctx["system"] == SYSTEM
    assert ctx["messages"] == []


def test_historial_vacio():
    ctx = armar_contexto(SYSTEM, [], 100, palabras)
    assert ctx["messages"] == []


def test_system_solo_excede_lanza_valueerror():
    with pytest.raises(ValueError):
        armar_contexto(SYSTEM, _historial_5(), 3, palabras)  # system cuesta 5 > 3


def test_usa_el_contador_inyectado():
    # Un contador que cuenta 1 por mensaje sin importar el contenido.
    uno = lambda s: 1
    # system cuesta 1, deja 2 -> caben 2 turnos (los 2 más recientes).
    ctx = armar_contexto(SYSTEM, _historial_5(), 3, uno)
    etiquetas = [m["content"].split()[0] for m in ctx["messages"]]
    assert etiquetas == ["t3", "t4"]
