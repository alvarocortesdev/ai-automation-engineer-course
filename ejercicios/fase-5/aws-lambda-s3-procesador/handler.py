"""AWS Lambda disparada por un evento de S3 (subida de objeto).

Objetivo del ejercicio: dejar la Lambda TESTEABLE sin AWS ni red, separando
la lógica pura (parsear el evento) del efecto (hablar con S3, que se inyecta).

NO cambies las firmas de `parsear_evento` ni de `handler`.
Implementa lo marcado con TODO. Corre `pytest` hasta el verde.
"""

from __future__ import annotations


def parsear_evento(event: dict) -> tuple[str, str]:
    """Extrae (bucket, key) de un evento de S3.

    La forma del evento es:
        event["Records"][0]["s3"]["bucket"]["name"]   -> bucket
        event["Records"][0]["s3"]["object"]["key"]    -> key

    Si el evento no trae `Records`, lanza ValueError (caso borde).
    """
    # TODO: valida que exista 'Records' (si no, raise ValueError)
    # TODO: extrae bucket y key y devuélvelos como tupla
    raise NotImplementedError


def handler(event: dict, context=None, s3_client=None) -> dict:
    """Punto de entrada de la Lambda.

    - Usa `parsear_evento` para sacar bucket y key.
    - Llama a `s3_client.get_object(Bucket=..., Key=...)` y lee 'ContentLength'.
    - Devuelve {"status": "ok", "bucket": ..., "key": ..., "bytes": ...}.

    `s3_client` se inyecta para poder testear sin AWS. Si viene None, créalo
    con boto3 (en la nube real, boto3 resuelve credenciales del execution role;
    NO se escribe ninguna access key).
    """
    if s3_client is None:
        import boto3  # import perezoso: el test inyecta un cliente falso y no necesita boto3

        s3_client = boto3.client("s3")

    # TODO: parsea el evento, consulta el objeto, arma y devuelve el resumen.
    raise NotImplementedError
