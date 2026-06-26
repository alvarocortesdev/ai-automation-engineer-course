"""Tests del ejercicio 2.12 — de print a logging estructurado.

ESTADO INICIAL (con el starter de print):
- `test_logica_intacta` PASA (no tocas la lógica).
- los demás FALLAN: hay print en stdout y no hay records de logging.
Cuando conviertas a logging con niveles + contexto, todos pasan a verde.

Nota: estos tests usan `caplog` (captura records de logging) y `capsys` (captura
stdout). NO llaman a configurar_logging() a propósito: caplog instala su propio
handler, así que un `print` aterriza en stdout (capsys lo ve) y un `logger.*` en
los records (caplog los ve). Esa es justo la diferencia que estás aprendiendo.
"""

import logging

from solucion import procesar_pedidos

PEDIDOS = [
    {"id": 1, "cantidad": 2, "precio": 5000},
    {"id": 2, "cantidad": 0, "precio": 9990},   # inválido
    {"id": 3, "cantidad": 1, "precio": 7000},
]


def test_logica_intacta():
    # La lógica de negocio NO cambia: dos válidos procesados, el inválido omitido.
    r = procesar_pedidos(PEDIDOS, correlation_id="req-1")
    assert r == [{"id": 1, "total": 10000}, {"id": 3, "total": 7000}]


def test_no_quedan_prints(capsys):
    procesar_pedidos(PEDIDOS, correlation_id="req-1")
    salida = capsys.readouterr().out
    assert salida == "", f"quedan print sueltos en stdout: {salida!r}"


def test_pedido_valido_emite_info_con_contexto(caplog):
    caplog.set_level(logging.INFO)
    procesar_pedidos([{"id": 1, "cantidad": 2, "precio": 5000}], correlation_id="req-xyz")
    infos = [r for r in caplog.records if r.levelno == logging.INFO]
    assert infos, "esperaba al menos un log INFO por cada pedido procesado"
    rec = infos[-1]
    assert getattr(rec, "pedido_id", None) == 1, "el INFO debe llevar pedido_id en extra="
    assert getattr(rec, "correlation_id", None) == "req-xyz", "y el correlation_id"


def test_pedido_invalido_emite_warning(caplog):
    caplog.set_level(logging.WARNING)
    r = procesar_pedidos([{"id": 9, "cantidad": 0, "precio": 100}], correlation_id="req-1")
    assert r == [], "el pedido inválido debe omitirse, no procesarse"
    warns = [rec for rec in caplog.records if rec.levelno == logging.WARNING]
    assert warns, "un pedido inválido debe emitir WARNING (no print, no crash)"
    assert getattr(warns[-1], "pedido_id", None) == 9


def test_detalle_interno_va_en_debug(caplog):
    caplog.set_level(logging.DEBUG)
    procesar_pedidos([{"id": 1, "cantidad": 2, "precio": 5000}], correlation_id="req-1")
    debugs = [r for r in caplog.records if r.levelno == logging.DEBUG]
    assert debugs, "el detalle interno (procesando/total) debe ir en nivel DEBUG, no INFO"
