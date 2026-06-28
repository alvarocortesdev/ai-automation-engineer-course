"""Tests de la verificación de webhook — definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

No edites estos tests para "hacerlos pasar" cambiando el contrato: implementa
`verificador.py` hasta que pasen en verde. El helper `_firmar` te muestra
EXACTAMENTE cómo se construye una firma válida (es tu "spec" del esquema).
"""

import hashlib
import hmac

from verificador import verificar_webhook

SECRETO = "whsec_test_123"
AHORA = 1_718_900_000  # un "ahora" fijo para que los tests sean deterministas


def _firmar(payload: bytes, t: int, secreto: str = SECRETO) -> str:
    """Construye una cabecera de firma válida: 't=<t>,v1=<hmac_hex>'."""
    base = f"{t}.".encode() + payload
    firma = hmac.new(secreto.encode(), base, hashlib.sha256).hexdigest()
    return f"t={t},v1={firma}"


def test_firma_valida_y_fresca_es_valido():
    payload = b'{"id":"evt_1","monto":1000}'
    header = _firmar(payload, AHORA)
    assert verificar_webhook(payload, header, SECRETO, AHORA) == "VALIDO"


def test_payload_manipulado_es_firma_invalida():
    payload_original = b'{"id":"evt_1","monto":1000}'
    header = _firmar(payload_original, AHORA)
    payload_alterado = b'{"id":"evt_1","monto":9999}'  # atacante cambia el monto
    assert verificar_webhook(payload_alterado, header, SECRETO, AHORA) == "FIRMA_INVALIDA"


def test_secreto_equivocado_es_firma_invalida():
    payload = b'{"id":"evt_1","monto":1000}'
    header = _firmar(payload, AHORA, secreto="otro_secreto")  # firmado con otro secreto
    assert verificar_webhook(payload, header, SECRETO, AHORA) == "FIRMA_INVALIDA"


def test_timestamp_viejo_con_firma_valida_es_expirado():
    payload = b'{"id":"evt_1","monto":1000}'
    t_viejo = AHORA - 600  # 10 minutos atrás; tolerancia por defecto = 300
    header = _firmar(payload, t_viejo)  # firma VÁLIDA, pero vieja
    assert verificar_webhook(payload, header, SECRETO, AHORA) == "EXPIRADO"


def test_dentro_de_la_tolerancia_es_valido():
    payload = b'{"id":"evt_1","monto":1000}'
    t = AHORA - 120  # 2 minutos atrás, dentro de los 5 de tolerancia
    header = _firmar(payload, t)
    assert verificar_webhook(payload, header, SECRETO, AHORA) == "VALIDO"


def test_tolerancia_personalizada():
    payload = b'{"id":"evt_1"}'
    t = AHORA - 120  # 2 minutos
    header = _firmar(payload, t)
    # con tolerancia de 60s, 120s atrás ya expiró
    assert verificar_webhook(payload, header, SECRETO, AHORA, tolerancia_seg=60) == "EXPIRADO"


def test_cabecera_sin_v1_es_malformado():
    payload = b'{"id":"evt_1"}'
    header = f"t={AHORA}"  # falta v1
    assert verificar_webhook(payload, header, SECRETO, AHORA) == "MALFORMADO"


def test_cabecera_sin_t_es_malformado():
    payload = b'{"id":"evt_1"}'
    header = "v1=deadbeef"  # falta t
    assert verificar_webhook(payload, header, SECRETO, AHORA) == "MALFORMADO"


def test_cabecera_con_t_no_entero_es_malformado():
    payload = b'{"id":"evt_1"}'
    header = "t=ayer,v1=deadbeef"  # t no es un entero
    assert verificar_webhook(payload, header, SECRETO, AHORA) == "MALFORMADO"


def test_cabecera_basura_es_malformado():
    payload = b'{"id":"evt_1"}'
    assert verificar_webhook(payload, "basura-sin-formato", SECRETO, AHORA) == "MALFORMADO"


# TODO(estudiante): añade al menos un caso borde tuyo. Sugerencia: un timestamp
# en el FUTURO (ahora - t negativo) más allá de la tolerancia, que también debería
# tratarse como sospechoso (relojes desincronizados o manipulación).
# def test_timestamp_muy_en_el_futuro():
#     ...
