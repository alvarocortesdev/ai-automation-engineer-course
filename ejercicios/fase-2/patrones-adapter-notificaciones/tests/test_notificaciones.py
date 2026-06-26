"""Tests del Adapter — definen el contrato.

Ejecuta desde la carpeta del ejercicio:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Estos tests arrancan en ROJO (los adapters aún no existen: lanzan
NotImplementedError). Implementa `SmsAdapter` hasta ponerlos en verde, y
luego AGREGA tu `EmailAdapter` + su test (TODO al final): es la prueba de
Open/Closed —agregar un proveedor sin tocar `enviar_alerta` ni `SmsAdapter`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notificaciones import (  # noqa: E402
    GatewaySmsLegacy,
    SmsAdapter,
    enviar_alerta,
)


def test_sms_adapter_traduce_la_llamada():
    # El Adapter cumple `Notificador.enviar` por fuera y llama a la API ajena
    # (send_text con sender) por dentro, sin perder ni renombrar datos.
    gateway = GatewaySmsLegacy()
    adapter = SmsAdapter(gateway, remitente="+56900000000")

    adapter.enviar("+56911111111", "hola")

    assert gateway.enviados == [
        {"to": "+56911111111", "body": "hola", "from": "+56900000000"}
    ]


def test_negocio_usa_solo_el_contrato():
    # `enviar_alerta` no conoce al proveedor: recibe cualquier `Notificador`.
    gateway = GatewaySmsLegacy()

    enviar_alerta(SmsAdapter(gateway, remitente="+56900000000"), "+56922222222")

    enviado = gateway.enviados[0]
    assert enviado["to"] == "+56922222222"
    assert enviado["body"] == "Tu pedido fue confirmado"
    assert enviado["from"] == "+56900000000"


# TODO(estudiante): demuestra Open/Closed.
# 1. Implementa `EmailAdapter` en notificaciones.py (adapta ClienteEmailV2.dispatch).
# 2. Escribe aquí `test_email_adapter_traduce_la_llamada` que pruebe que
#    `enviar_alerta(EmailAdapter(cliente), "ana@correo.cl")` deja en
#    `cliente.bandeja` un payload con recipient/subject/html correctos,
#    SIN haber tocado `enviar_alerta` ni `SmsAdapter`.
