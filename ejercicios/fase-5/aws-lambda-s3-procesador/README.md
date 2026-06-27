# Lambda S3-triggered: handler + política IAM mínima, testeado sin AWS

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.7` AWS profundización
**Ruta:** opcional / profundización · **Timebox:** 40–45 min · **Modalidad:** código

## 🎯 Objetivo

Implementar una **AWS Lambda** (Python) que se dispara al subir un objeto a S3: extrae `bucket` y
`key` del evento, consulta el tamaño del objeto y devuelve un resumen. La gracia pedagógica:
dejarla **testeable sin AWS ni red**, separando la **lógica pura** (parsear el evento) del **efecto**
(hablar con S3, que se **inyecta**). Además, escribir su **policy IAM de least privilege**.

## 📋 Contexto

"Una Lambda es solo una función con la firma `handler(event, context)`" — verlo así te quita el
miedo y te deja **testearla como cualquier función**. La inyección del cliente S3 es el patrón que
hace eso posible (y el mismo que usarás para testear código que llama a APIs externas y a LLMs en la
Fase 6). La policy te ancla el reflejo de **least privilege** del hilo de seguridad (lección 5.4).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Navega el dict del evento sin copiar nada.
2. Solo entonces, consulta **documentación oficial** (Lambda Python handler, eventos de S3).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* el handler.
4. Mañana, **reescribe `parsear_evento` de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `handler.py`. Implementa (sin cambiar firmas):
   - `parsear_evento(event) -> tuple[str, str]`: extrae `(bucket, key)`; lanza `ValueError` si no
     hay `Records`.
   - `handler(event, context=None, s3_client=None) -> dict`: usa `parsear_evento`, llama a
     `s3_client.get_object(Bucket=..., Key=...)`, lee `ContentLength`, y devuelve
     `{"status": "ok", "bucket": ..., "key": ..., "bytes": ...}`. Si `s3_client` es `None`, créalo con
     `boto3.client("s3")` (en la nube real las credenciales vienen del **execution role**, no de
     access keys).
2. Completa `policy.json` con la **policy de least privilege** del execution role: solo `s3:GetObject`
   sobre el ARN del bucket + permisos de escribir logs. **Nada de `*`.**
3. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

4. Itera hasta el **verde** y agrega **al menos un test propio** en `tests/test_handler.py`.

> Los tests **no tocan AWS**: inyectan un `FakeS3Client`. No necesitas cuenta de AWS ni boto3
> instalado para que pasen (boto3 solo se importa si no inyectas cliente).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` pasa: `parsear_evento` y `handler` funcionan con el cliente falso, sin tocar AWS.
- [ ] `parsear_evento` lanza `ValueError` ante un evento sin `Records` (caso borde).
- [ ] `handler` acepta `s3_client` inyectable y **no escribe ninguna access key**.
- [ ] `policy.json` es **least privilege**: `s3:GetObject` acotado a ARN + permisos de logs; sin `*`.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar sin notas** por qué inyectar el cliente hace la Lambda testeable y qué role
      necesita en AWS.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

La forma del evento es `event["Records"][0]["s3"]["bucket"]["name"]` y `...["object"]["key"]`
(ábrela en `evento_s3.json` y navega el dict). En `parsear_evento`, valida
`if not event.get("Records"): raise ValueError(...)` **antes** de indexar. El truco de testeabilidad
es la **inyección de dependencia**: `def handler(event, context=None, s3_client=None)` y dentro
`if s3_client is None: ... s3_client = boto3.client("s3")`; el test te pasa un objeto falso con
`get_object(**kwargs)` que devuelve `{"ContentLength": 2048}`. Para `policy.json`, son dos
statements (leer S3 + escribir logs), como el ejercicio 6.3 de la lección.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `handler.py`, `policy.json`, tus tests),
- la **rúbrica**: `.ai/rubricas/fase-5/aws-lambda-s3-procesador.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/aws-lambda-s3-procesador/` — no la mires
antes de intentarlo de verdad.
