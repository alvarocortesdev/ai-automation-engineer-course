"""Tests de aceptación del mini-dispatcher de cola.

Verifican la SEMÁNTICA de una cola real: reintentos hasta un tope, DLQ para
poison messages, y deduplicación por job.id bajo entrega at-least-once.

NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
Corre:  uv run pytest   (o: pytest)
"""

import collections

from solucion import Job, procesar_cola


def _handler_que_falla(fail_until: dict[str, int]):
    """Devuelve un handler que falla las primeras `fail_until[id]` llamadas de
    cada id y luego tiene éxito. `handler.calls` cuenta las llamadas por id.
    Si un id no está en `fail_until`, el handler nunca falla para ese id.
    """
    calls: collections.Counter = collections.Counter()

    def handler(job: Job) -> None:
        calls[job.id] += 1
        if calls[job.id] <= fail_until.get(job.id, 0):
            raise RuntimeError(f"fallo simulado #{calls[job.id]} para {job.id}")

    handler.calls = calls  # type: ignore[attr-defined]
    return handler


def test_exito_al_primer_intento() -> None:
    handler = _handler_que_falla({})  # nunca falla
    res = procesar_cola([Job(id="j1", max_attempts=3)], handler)

    assert res["done"] == ["j1"]
    assert res["dlq"] == []
    assert handler.calls["j1"] == 1  # se llamó una sola vez


def test_flaky_se_recupera_dentro_del_tope() -> None:
    # Falla las 2 primeras veces, funciona en la 3a; con max_attempts=3 alcanza.
    handler = _handler_que_falla({"j1": 2})
    res = procesar_cola([Job(id="j1", max_attempts=3)], handler)

    assert res["done"] == ["j1"], "debería completarse al 3er intento"
    assert res["dlq"] == [], "no debería ir a la DLQ: se recuperó a tiempo"
    assert handler.calls["j1"] == 3, "handler llamado exactamente max_attempts veces"


def test_siempre_falla_va_a_la_dlq() -> None:
    handler = _handler_que_falla({"j1": 99})  # falla siempre
    res = procesar_cola([Job(id="j1", max_attempts=3)], handler)

    assert res["done"] == [], "no debería completarse nunca"
    assert len(res["dlq"]) == 1, "el poison message debe terminar en la DLQ"
    assert res["dlq"][0].id == "j1"
    assert res["dlq"][0].attempts == 3, "agotó exactamente max_attempts intentos"
    assert handler.calls["j1"] == 3, "ni un intento de más (sin loop infinito)"


def test_at_least_once_dedup_por_id() -> None:
    # La cola trae el MISMO id dos veces (entrega at-least-once). Ambos
    # tendrían éxito, pero el handler debe correr UNA sola vez para ese id.
    handler = _handler_que_falla({})  # nunca falla
    res = procesar_cola(
        [Job(id="dup", max_attempts=3), Job(id="dup", max_attempts=3)],
        handler,
    )

    assert res["done"] == ["dup"], "el id completado aparece una sola vez"
    assert res["dlq"] == []
    assert handler.calls["dup"] == 1, "idempotencia: el handler NO corre dos veces"


def test_mezcla_done_y_dlq() -> None:
    # ok1 funciona al primer intento; bad falla siempre (DLQ); ok2 funciona.
    handler = _handler_que_falla({"bad": 99})
    res = procesar_cola(
        [
            Job(id="ok1", max_attempts=3),
            Job(id="bad", max_attempts=3),
            Job(id="ok2", max_attempts=3),
        ],
        handler,
    )

    assert set(res["done"]) == {"ok1", "ok2"}
    assert [j.id for j in res["dlq"]] == ["bad"]
    assert handler.calls["bad"] == 3
    assert handler.calls["ok1"] == 1
    assert handler.calls["ok2"] == 1
