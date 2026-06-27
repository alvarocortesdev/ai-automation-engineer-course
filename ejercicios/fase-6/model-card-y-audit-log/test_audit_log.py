"""Tests del audit log. Definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Los tests NO asumen un algoritmo de hash concreto: solo exigen que sea determinista,
que dependa del contenido y que registrar/verificar_cadena estén de acuerdo. Lo que SÍ
exigen es el comportamiento de gobernanza: redactar PII, no guardar el crudo, y detectar
manipulación.
"""

import pytest

from audit_log import GENESIS, redactar, registrar, verificar_cadena


def _evento(decision="ok", **extra):
    base = {
        "request_id": "req-1",
        "timestamp": "2026-06-27T14:03:11Z",
        "actor": "user-7f3a",
        "modelo": "claude-sonnet-4-5@2026-05",
        "prompt_version": "v12",
        "decision": decision,
    }
    base.update(extra)
    return base


# --- redactar -------------------------------------------------------------

def test_redactar_email():
    out = redactar("escríbeme a ana.perez@example.com hoy")
    assert "ana.perez@example.com" not in out
    assert "<REDACTADO>" in out
    assert "hoy" in out  # no borra el resto del texto


def test_redactar_digitos():
    out = redactar("mi RUT es 12.345.678-9 y mi fono 987654321")
    assert "12.345.678-9" not in out
    assert "987654321" not in out
    assert out.count("<REDACTADO>") >= 2


def test_redactar_no_toca_numeros_cortos():
    # 4 dígitos (un año) no es PII y no se redacta
    assert "2026" in redactar("nos vemos en 2026")


# --- registrar ------------------------------------------------------------

def test_registrar_incluye_requeridos():
    r = registrar(_evento(), GENESIS)
    for campo in CAMPOS:
        assert campo in r
    assert r["prev_hash"] == GENESIS
    assert isinstance(r["record_hash"], str) and r["record_hash"]


def test_registrar_falta_campo_lanza():
    evento = _evento()
    del evento["actor"]
    with pytest.raises(ValueError):
        registrar(evento, GENESIS)


def test_registrar_redacta_y_no_guarda_crudo():
    evento = _evento(input_text="mi correo es ana@example.com, gracias")
    r = registrar(evento, GENESIS)
    assert "input_text" not in r                 # nunca el crudo
    assert "input_redacted" in r
    assert "ana@example.com" not in r["input_redacted"]


def test_registrar_distintos_eventos_distinto_hash():
    a = registrar(_evento(decision="aprobado"), GENESIS)
    b = registrar(_evento(decision="rechazado"), GENESIS)
    assert a["record_hash"] != b["record_hash"]


# --- verificar_cadena -----------------------------------------------------

def _cadena(n=3):
    registros = []
    prev = GENESIS
    for i in range(n):
        r = registrar(_evento(decision=f"d{i}", request_id=f"req-{i}"), prev)
        registros.append(r)
        prev = r["record_hash"]
    return registros


def test_cadena_integra():
    assert verificar_cadena(_cadena()) is True


def test_cadena_detecta_tamper_de_campo():
    registros = _cadena()
    registros[1]["decision"] = "MANIPULADO"  # editan un registro viejo, sin recomputar el hash
    assert verificar_cadena(registros) is False


def test_cadena_detecta_reordenamiento():
    registros = _cadena()
    registros[0], registros[1] = registros[1], registros[0]
    assert verificar_cadena(registros) is False


CAMPOS = (
    "request_id",
    "timestamp",
    "actor",
    "modelo",
    "prompt_version",
    "decision",
)


# TODO(estudiante): añade al menos un caso borde tuyo. Ideas:
#  - ¿qué devuelve verificar_cadena([]) ? (decide el contrato y testéalo)
#  - si alguien manipula un campo Y recomputa su record_hash, ¿se detecta igual?
#    (pista: el enlace del registro SIGUIENTE deja de cuadrar)
# def test_mi_caso_borde():
#     ...
