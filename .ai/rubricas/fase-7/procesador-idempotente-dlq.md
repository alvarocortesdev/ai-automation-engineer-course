---
ejercicio_id: fase-7/procesador-idempotente-dlq
fase: fase-7
sub_unidad: "7.2"
version: 1
---

# Rúbrica — Procesador idempotente con dead-letter queue

> Rúbrica **analítica** atada a los `objetivos` del contrato. Es un ejercicio **mixto**: hay tests
> automáticos (`test_procesador.py`) **y** un `write-up.md`. El verde de los tests es necesario, no
> suficiente: el corrector evalúa también si el write-up demuestra que el alumno entiende *por qué*
> at-least-once obliga a la idempotencia y qué resuelve el outbox. Pasar los tests sin un write-up
> defendible es `competente` a lo sumo.

## Objetivos evaluados

- O1: Idempotencia — el side-effect corre una sola vez ante duplicados.
- O2: DLQ — un poison message va a la cola lateral tras `max_intentos`.
- O3: Explicar dual-write, outbox y reconciliación (write-up).

## Criterios y niveles

### C1 — Corrección del procesador · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo; el efecto se re-ejecuta en duplicados, o el poison nunca llega a la DLQ. |
| **en-progreso** | Dedup funciona pero la DLQ falla (cuenta mal los intentos), o marca como duplicado un evento que falló y aún no tuvo éxito. |
| **competente** | Los 8 tests en verde: dedup (efecto una sola vez), poison → DLQ tras `max_intentos`, eventos distintos por separado, evento en DLQ no re-ejecuta. |
| **excelente** | Además, separación limpia de estado (completados solo en éxito), y un caso propio significativo (dos poison distintos sin interferir). |

### C2 — Comprensión de at-least-once vs. idempotencia (el corazón) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El write-up confunde "no reintentar" con "idempotencia", o cree que se puede lograr exactly-once delivery. |
| **en-progreso** | Distingue entrega de procesamiento pero no explica por qué un fallo previo no debe marcar duplicado. |
| **competente** | Explica que la entrega es at-least-once y que la idempotencia (dedup por id) vuelve el procesamiento effectively-once; justifica el punto (a). |
| **excelente** | Conecta: el relay del outbox entrega at-least-once → por eso los consumidores deben ser idempotentes → el mismo procesador sirve para webhooks, colas y replay. |

### C3 — Comprensión de outbox y reconciliación · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona el dual-write, o describe el outbox como "una tabla más" sin la idea de atomicidad. |
| **en-progreso** | Nombra el dual-write pero no explica la transacción única que lo resuelve. |
| **competente** | Explica el dual-write (DB + publicar pueden divergir si hay crash en medio) y el outbox (escribir el evento en la MISMA transacción; un relay lo publica después). |
| **excelente** | Articula "entrega en vivo = velocidad falible, reconciliación = corrección lenta" y por qué un sistema serio usa las dos. |

## Errores típicos a marcar

- Re-ejecutar el efecto en un duplicado (no separar "ya completado" del flujo de procesamiento).
- Marcar como completado en un intento **fallido** → el reintento exitoso posterior se trata como duplicado y nunca se ejecuta.
- DLQ sin límite real (reintenta infinito) o que cuenta los intentos de eventos distintos juntos.
- Afirmar en el write-up que se garantiza "exactly-once delivery" (mito en sistemas distribuidos).
- Describir el outbox sin la idea clave: **misma transacción** que el cambio de negocio (sin eso, no resuelve nada).
- (transversal) Pasar los tests sin poder defender por qué reconciliar es necesario si ya hay webhooks.

## Señales de dependencia-IA

- Clase impecable pero el alumno no puede explicar por qué un fallo previo no convierte el éxito en duplicado.
- Write-up que usa el vocabulario exacto de la lección (transcrito) sin ejemplos propios ni capacidad de defenderlo.
- Sofisticación impropia (menciona CDC, 2PC, sagas) sin poder explicar el caso simple del dual-write.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué devuelve `procesar` para un evento que falló dos veces (max=3) y luego tiene éxito. Si entendió, dice "procesado"; si dependió de IA, duda.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "¿En qué momento exactamente marcas un evento como 'ya hecho'? Corre mentalmente el caso 'falla, falla, éxito': ¿tu código lo procesa o lo descarta como duplicado?"
- **Pregunta socrática (nivel 2):** "Si la entrega es at-least-once y no puedes evitar los duplicados en el canal, ¿dónde tiene que vivir la garantía de 'una sola vez'? ¿Qué pieza la provee?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Guarda en `completados` **solo** en la rama de éxito; lleva `intentos` aparte para decidir la DLQ. Un fallo incrementa intentos pero no marca completado, así el éxito posterior sí se procesa. Para el write-up, el outbox vive en 4.7 y la reconciliación en 4.8 de la lección."

## Conexión con el proyecto / capstone

- Este procesador es el **motor de fallas** del [capstone F7](/fase-7-automatizacion/proyecto/): garantiza que un reintento del input no dispare dos veces la acción del agente, y que un input venenoso no paralice el flujo. Es el punto 6 del Definition of Done (manejo de fallas + techo de costo) hecho código.
