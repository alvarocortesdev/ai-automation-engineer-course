"""Tests del procesador idempotente — definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

No edites estos tests para "hacerlos pasar" cambiando el contrato: implementa
`procesador.py` hasta que pasen en verde. El patrón de los tests usa un contador
de side-effects para comprobar que un duplicado NO re-ejecuta el efecto.
"""

import pytest

from procesador import ProcesadorIdempotente


def _efecto_contador():
    """Devuelve (efecto, llamadas) donde llamadas['n'] cuenta cuántas veces corrió."""
    llamadas = {"n": 0}

    def efecto(evento):
        llamadas["n"] += 1
        return f"ok:{evento['id']}"

    return efecto, llamadas


def test_evento_nuevo_se_procesa_una_vez():
    p = ProcesadorIdempotente()
    efecto, llamadas = _efecto_contador()
    out = p.procesar({"id": "evt_1"}, efecto)
    assert out["status"] == "procesado"
    assert out["resultado"] == "ok:evt_1"
    assert llamadas["n"] == 1


def test_duplicado_no_reejecuta_el_efecto():
    p = ProcesadorIdempotente()
    efecto, llamadas = _efecto_contador()
    primero = p.procesar({"id": "evt_1"}, efecto)
    segundo = p.procesar({"id": "evt_1"}, efecto)  # MISMO id
    assert primero["status"] == "procesado"
    assert segundo["status"] == "duplicado"
    assert segundo["resultado"] == "ok:evt_1"      # devuelve el resultado guardado
    assert llamadas["n"] == 1                       # el efecto corrió UNA sola vez


def test_eventos_distintos_se_procesan_por_separado():
    p = ProcesadorIdempotente()
    efecto, llamadas = _efecto_contador()
    a = p.procesar({"id": "evt_a"}, efecto)
    b = p.procesar({"id": "evt_b"}, efecto)
    assert a["status"] == "procesado"
    assert b["status"] == "procesado"
    assert llamadas["n"] == 2


def test_poison_message_va_a_dlq_tras_max_intentos():
    p = ProcesadorIdempotente(max_intentos=3)

    def efecto_venenoso(evento):
        raise ValueError("siempre falla")

    r1 = p.procesar({"id": "evt_malo"}, efecto_venenoso)
    r2 = p.procesar({"id": "evt_malo"}, efecto_venenoso)
    r3 = p.procesar({"id": "evt_malo"}, efecto_venenoso)
    assert r1["status"] == "reintentable"
    assert r2["status"] == "reintentable"
    assert r3["status"] == "dlq"
    assert any(e["id"] == "evt_malo" for e in p.dlq)


def test_evento_en_dlq_no_reejecuta_el_efecto():
    p = ProcesadorIdempotente(max_intentos=1)
    llamadas = {"n": 0}

    def efecto_venenoso(evento):
        llamadas["n"] += 1
        raise ValueError("siempre falla")

    p.procesar({"id": "evt_malo"}, efecto_venenoso)   # 1er intento -> dlq (max=1)
    despues = p.procesar({"id": "evt_malo"}, efecto_venenoso)
    assert despues["status"] == "dlq"
    assert llamadas["n"] == 1                           # no se reejecuta estando en DLQ


def test_falla_y_luego_exito_no_es_duplicado():
    p = ProcesadorIdempotente(max_intentos=3)
    estado = {"fallar": True, "n": 0}

    def efecto_inestable(evento):
        estado["n"] += 1
        if estado["fallar"]:
            raise ConnectionError("transitorio")
        return "ok"

    r1 = p.procesar({"id": "evt_x"}, efecto_inestable)  # falla -> reintentable
    estado["fallar"] = False
    r2 = p.procesar({"id": "evt_x"}, efecto_inestable)  # ahora SÍ se procesa
    assert r1["status"] == "reintentable"
    assert r2["status"] == "procesado"                  # NO "duplicado"
    assert estado["n"] == 2                              # el efecto corrió en ambos


def test_exito_despues_no_se_reprocesa():
    p = ProcesadorIdempotente()
    efecto, llamadas = _efecto_contador()
    p.procesar({"id": "evt_1"}, efecto)
    p.procesar({"id": "evt_1"}, efecto)
    tercero = p.procesar({"id": "evt_1"}, efecto)
    assert tercero["status"] == "duplicado"
    assert llamadas["n"] == 1


def test_dlq_arranca_vacia():
    p = ProcesadorIdempotente()
    assert p.dlq == []


# TODO(estudiante): añade un caso tuyo. Sugerencia: dos eventos venenosos
# distintos deben terminar AMBOS en la DLQ sin interferir entre sí.
# def test_dos_poison_distintos():
#     ...
