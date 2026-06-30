"""Tests del handler de Lambda. Corren SIN AWS ni red: el cliente S3 se inyecta.

Ejecuta desde la carpeta del ejercicio:
    uv run pytest        # o:  pytest
"""

import json
from pathlib import Path

import pytest

from handler import handler, parsear_evento

EVENTO = json.loads((Path(__file__).parent.parent / "evento_s3.json").read_text())


class FakeS3Client:
    """Cliente S3 falso: registra la llamada y devuelve un ContentLength fijo.

    Sustituye a boto3 en los tests para no tocar AWS ni la red.
    """

    def __init__(self, content_length: int = 2048):
        self.content_length = content_length
        self.llamadas: list[dict] = []

    def get_object(self, **kwargs):
        self.llamadas.append(kwargs)
        return {"ContentLength": self.content_length}


def test_parsear_evento_extrae_bucket_y_key():
    bucket, key = parsear_evento(EVENTO)
    assert bucket == "acme-app-uploads-prod"
    assert key == "facturas/factura.pdf"


def test_parsear_evento_sin_records_lanza_valueerror():
    with pytest.raises(ValueError):
        parsear_evento({})


def test_handler_devuelve_resumen_con_cliente_falso():
    fake = FakeS3Client(content_length=2048)
    resultado = handler(EVENTO, context=None, s3_client=fake)

    assert resultado["status"] == "ok"
    assert resultado["bucket"] == "acme-app-uploads-prod"
    assert resultado["key"] == "facturas/factura.pdf"
    assert resultado["bytes"] == 2048


def test_handler_consulta_el_objeto_correcto():
    fake = FakeS3Client()
    handler(EVENTO, context=None, s3_client=fake)

    # El handler debe haber consultado el objeto exacto del evento (least surprise).
    assert fake.llamadas == [
        {"Bucket": "acme-app-uploads-prod", "Key": "facturas/factura.pdf"}
    ]


# TODO (tú): agrega al menos un caso de prueba propio.
# Sugerencia: un evento con "Records": [] o sin la clave, y verifica el ValueError;
# o un ContentLength distinto y verifica que 'bytes' lo refleja.
