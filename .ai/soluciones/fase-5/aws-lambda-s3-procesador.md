---
ejercicio_id: fase-5/aws-lambda-s3-procesador
fase: fase-5
sub_unidad: "5.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una implementación de referencia;
> hay variaciones válidas (cómo se valida `Records`, nombres de variables). Úsala para graduar pistas
> y verificar que el verde de `pytest` viene de un diseño testeable real, no de un atajo.

# Solución de referencia — Lambda S3-triggered

## `handler.py`

```python
from __future__ import annotations


def parsear_evento(event: dict) -> tuple[str, str]:
    if not event.get("Records"):
        raise ValueError("evento de S3 sin 'Records'")
    s3 = event["Records"][0]["s3"]
    return s3["bucket"]["name"], s3["object"]["key"]


def handler(event: dict, context=None, s3_client=None) -> dict:
    if s3_client is None:
        import boto3  # import perezoso: el test inyecta un cliente falso

        s3_client = boto3.client("s3")

    bucket, key = parsear_evento(event)
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return {
        "status": "ok",
        "bucket": bucket,
        "key": key,
        "bytes": obj["ContentLength"],
    }
```

## `policy.json` (execution role, least privilege)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LeerUploads",
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::donpelusa-app-uploads-prod/*"
    },
    {
      "Sid": "EscribirLogs",
      "Effect": "Allow",
      "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "arn:aws:logs:*:*:log-group:/aws/lambda/*"
    }
  ]
}
```

## Ejemplo de test propio (lo que el alumno debe agregar)

```python
def test_records_vacio_lanza_valueerror():
    with pytest.raises(ValueError):
        parsear_evento({"Records": []})


def test_bytes_refleja_content_length():
    fake = FakeS3Client(content_length=999)
    resultado = handler(EVENTO, s3_client=fake)
    assert resultado["bytes"] == 999
```

## Puntos clave que el corrector debe verificar

1. **Testeabilidad por inyección.** `handler(event, context=None, s3_client=None)` con fallback
   `if s3_client is None: import boto3; s3_client = boto3.client("s3")`. El import de boto3 es
   **perezoso** (dentro de la función), si no el test falla cuando boto3 no está instalado.
2. **Caso borde.** `parsear_evento` valida `Records` y lanza `ValueError` **antes** de indexar
   (no dejar que reviente con `KeyError`/`IndexError`).
3. **Least privilege real.** Dos statements, acciones enumeradas, `Resource` por ARN. Ningún `*` en
   `Action` ni en `Resource` de S3. Permiso de logs presente.
4. **Cero access keys.** No debe haber ninguna credencial escrita; en la nube las da el execution role.
5. **`pytest` verde** con los 4 tests dados + al menos 1 propio con aserción real.

## Verificación rápida (corrector)

```bash
cd ejercicios/fase-5/aws-lambda-s3-procesador && pytest -q
# esperado: todos los tests en verde, sin tocar AWS ni la red
```
