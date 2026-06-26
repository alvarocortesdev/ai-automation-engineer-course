"""Tests de aceptación — Verifica un JWT a mano.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Estos tests definen el contrato de `verificar_jwt`. Solo usan la librería
estándar (no PyJWT). NO abras este archivo para "adivinar" la solución:
solo verifica la tuya. Añade al menos un caso borde tuyo al final.
"""

import json

import pytest

from verificador import (
    AlgoritmoNoPermitido,
    FirmaInvalida,
    TokenExpirado,
    TokenMalformado,
    _b64url_encode,
    firmar_jwt,
    verificar_jwt,
)

SECRET = "secreto-de-pruebas-no-usar-en-prod"


def test_token_valido_devuelve_claims():
    token = firmar_jwt({"sub": "ana", "role": "user", "exp": 2000}, SECRET)
    claims = verificar_jwt(token, SECRET, ahora=1000)
    assert claims["sub"] == "ana"
    assert claims["role"] == "user"


def test_firma_invalida_con_secreto_distinto():
    token = firmar_jwt({"sub": "ana", "exp": 2000}, SECRET)
    with pytest.raises(FirmaInvalida):
        verificar_jwt(token, "otro-secreto", ahora=1000)


def test_payload_manipulado_rompe_la_firma():
    # Un atacante toma un token válido y cambia role:user -> role:admin
    # SIN volver a firmarlo (no tiene el secreto). Debe ser rechazado.
    token = firmar_jwt({"sub": "ana", "role": "user", "exp": 2000}, SECRET)
    h, _p, s = token.split(".")
    payload_malicioso = _b64url_encode(
        json.dumps({"sub": "ana", "role": "admin", "exp": 2000}).encode("utf-8")
    )
    token_trucado = f"{h}.{payload_malicioso}.{s}"
    with pytest.raises(FirmaInvalida):
        verificar_jwt(token_trucado, SECRET, ahora=1000)


def test_token_expirado():
    token = firmar_jwt({"sub": "ana", "exp": 1000}, SECRET)
    # ahora == exp: ya expiró (la frontera cuenta como expirado).
    with pytest.raises(TokenExpirado):
        verificar_jwt(token, SECRET, ahora=1000)


def test_justo_antes_de_expirar_es_valido():
    token = firmar_jwt({"sub": "ana", "exp": 1000}, SECRET)
    assert verificar_jwt(token, SECRET, ahora=999)["sub"] == "ana"


def test_ataque_alg_none_es_rechazado():
    # Ataque clásico: header con alg=none y firma vacía.
    header = _b64url_encode(json.dumps({"alg": "none", "typ": "JWT"}).encode("utf-8"))
    payload = _b64url_encode(json.dumps({"sub": "admin", "exp": 2000}).encode("utf-8"))
    token = f"{header}.{payload}."
    with pytest.raises(AlgoritmoNoPermitido):
        verificar_jwt(token, SECRET, ahora=1000)


def test_estructura_malformada():
    with pytest.raises(TokenMalformado):
        verificar_jwt("solo.dos", SECRET, ahora=1000)
    with pytest.raises(TokenMalformado):
        verificar_jwt("una-sola-parte", SECRET, ahora=1000)


def test_base64_o_json_invalido_es_malformado():
    with pytest.raises(TokenMalformado):
        verificar_jwt("@@@.@@@.@@@", SECRET, ahora=1000)


def test_sin_exp_no_expira_nunca():
    token = firmar_jwt({"sub": "ana"}, SECRET)  # sin claim exp
    assert verificar_jwt(token, SECRET, ahora=10**12)["sub"] == "ana"


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Ideas: un token con `exp` no numérico, un header sin `alg`, un secreto vacío.
