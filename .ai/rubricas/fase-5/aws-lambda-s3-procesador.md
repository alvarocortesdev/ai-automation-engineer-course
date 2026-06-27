---
ejercicio_id: fase-5/aws-lambda-s3-procesador
fase: fase-5
sub_unidad: "5.7"
version: 1
---

# Rúbrica — Lambda S3-triggered: handler + policy IAM mínima, testeado sin AWS

> Rúbrica **analítica** atada a los `objetivos` del contrato. Hay test automático
> (`tests/test_handler.py`): el verde es necesario pero **no suficiente** — se evalúa también el
> diseño testeable (inyección), el manejo del caso borde, la policy de least privilege y el test
> propio. El corrector corre `pytest` y lee el código y la `policy.json`.

## Objetivos evaluados

- O1: Implementar la Lambda (`handler(event, context)`) que parsea el evento de S3 y resume el objeto.
- O2: Separar lógica pura (`parsear_evento`) del efecto (S3) inyectando el cliente → testeable sin AWS.
- O3: Manejar el caso borde (evento sin `Records` → `ValueError`).
- O4: Escribir la policy IAM de least privilege del execution role (sin access keys).

## Criterios y niveles

### C1 — Corrección (¿pasa y hace lo pedido?) · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `pytest` no pasa; `parsear_evento` o `handler` sin implementar o con `NotImplementedError`. |
| **en-progreso** | Pasa el caso feliz pero no el `ValueError` del evento sin `Records`, o el dict de retorno no tiene las 4 claves. |
| **competente** | Los 4 tests dados pasan: extrae bucket/key, lanza `ValueError` sin `Records`, devuelve `{status, bucket, key, bytes}` y consulta el objeto correcto. |
| **excelente** | Además el código es limpio (sin indexar a ciegas; valida antes), y `parsear_evento` es una función pura reutilizable. |

### C2 — Diseño testeable (inyección de dependencia) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Crea `boto3.client("s3")` dentro sin permitir inyección → el test tocaría AWS (o falla por falta de credenciales). |
| **en-progreso** | Acepta `s3_client` pero no usa el patrón `s3_client or boto3.client(...)`, o importa boto3 a nivel de módulo (rompe el test si no está instalado). |
| **competente** | `handler(event, context=None, s3_client=None)` con fallback a boto3 e import perezoso; el test inyecta el `FakeS3Client` sin red. |
| **excelente** | Explica (en comentario o write-up) por qué la inyección hace la Lambda testeable como cualquier función, y conecta con testear llamadas a APIs/LLMs (F6). |

### C3 — Seguridad / least privilege (policy + sin secretos) · mapea: O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `policy.json` con `Action: "*"` / `Resource: "*"`, o hay una access key escrita en el código. |
| **en-progreso** | Usa role pero la policy es amplia (`s3:*` o `Resource: *` en S3), o le falta el permiso de logs. |
| **competente** | Dos statements: `s3:GetObject` acotado al ARN del bucket + `logs:CreateLogStream`/`logs:PutLogEvents`; ninguna access key en el código. |
| **excelente** | ARNs precisos (incluye `/aws/lambda/...` para el log group), `Sid` descriptivos, y articula por qué el código no lleva credenciales (execution role + credenciales temporales). |

### C4 — Calidad de tests (¿aserciones reales? ¿test propio?) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó test propio, o su test no asercia nada útil (p. ej. `assert True`). |
| **en-progreso** | Agregó un test pero duplica uno existente sin aportar un caso nuevo. |
| **competente** | Agregó un caso borde propio real (p. ej. `Records: []` → `ValueError`, o un `ContentLength` distinto reflejado en `bytes`). |
| **excelente** | Su test cubre un caso que los dados no cubren y tiene una aserción precisa con mensaje claro. |

## Errores típicos a marcar

- Crear `boto3.client("s3")` rígido dentro del handler → acopla a AWS y rompe la testeabilidad (no inyectable).
- Importar boto3 a nivel de módulo: el test (que inyecta el falso) falla si boto3 no está instalado.
- Indexar `event["Records"][0]` sin validar → `KeyError`/`IndexError` en vez del `ValueError` pedido.
- Policy con `*` presentada como mínima; o pegar una access key "para que funcione".
- Olvidar el permiso de logs en la policy (la Lambda no podría escribir a CloudWatch).
- (transversal) `assert True` o test que pasa siempre; perseguir "que pase pytest" sin aserciones reales.

## Señales de dependencia-IA

- Handler con manejo de errores y typing sofisticados pero el alumno no sabe explicar **por qué** se inyecta el cliente.
- Policy IAM perfecta pero con un `Action: "*"` que delata copy-paste sin entender least privilege.
- Comentarios genéricos ("# get the object from s3") que no calzan con un diseño testeable pensado.
- Tests extra impecables pero que no añaden ningún caso nuevo (relleno).

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "¿Tu `handler` se puede testear sin tocar AWS? Si dentro haces `boto3.client('s3')` sin permitir pasar un cliente, el test no puede inyectar el falso. Mira la firma sugerida."
- **Pregunta socrática (nivel 2):** "Si separas 'parsear el evento' de 'hablar con S3', ¿cuál de las dos partes necesita la red para testearse? ¿Cómo le pasas a la función un S3 de mentira en el test?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Usa `def handler(event, context=None, s3_client=None)` y dentro `if s3_client is None: import boto3; s3_client = boto3.client('s3')`. Valida `Records` en `parsear_evento` antes de indexar (`raise ValueError`). En `policy.json`, enumera `s3:GetObject` sobre el ARN del bucket + los dos permisos de logs; nada de `*`. Revisa secciones 4.7 y 6.3 de la lección."

## Conexión con el proyecto / capstone

- La tarea por evento del Capstone F5 (procesar un archivo recién subido) **es** esta Lambda. El patrón de inyección reaparece en F6 para testear código que llama a LLMs sin gastar tokens, y la policy de least privilege es la base de la seguridad de agentes en F7 (*Excessive Agency*).
