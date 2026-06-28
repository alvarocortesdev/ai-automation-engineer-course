---
ejercicio_id: fase-7/endurecer-workflow-n8n
fase: fase-7
sub_unidad: "7.1"
version: 1
---

# Rúbrica — Endurece un workflow frágil de n8n

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar. El test estructural (`test_workflow.py`) da la señal objetiva; la comprensión se mide en `hardening.md` y en cómo el alumno **explica** las decisiones.

## Objetivos evaluados

- O1: Implementar idempotencia — barrera de deduplicación con clave estable, **corriente arriba** del nodo con efecto secundario.
- O2: Configurar reintentos (`retryOnFail`, `maxTries` 2-5, `waitBetweenTries` > 0) en el nodo peligroso y asociar un **error workflow**.
- O3: Explicar por qué reintentar sin idempotencia duplica efectos y por qué el dedup va antes, no después.

## Criterios y niveles

### C1 — Corrección del workflow (¿hace lo que el objetivo pide?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_workflow.py` no pasa; falta el dedup, o no hay reintentos, o no hay `errorWorkflow`. El JSON no parsea. |
| **en-progreso** | Pasa parcialmente: añadió el dedup pero **después** del efecto secundario (orden invertido), o puso reintentos sin `errorWorkflow`, o `maxTries` fuera de rango. |
| **competente** | `test_workflow.py` verde: dedup corriente arriba (Webhook → dedup → "Crear factura"), reintentos sanos en "Crear factura", `settings.errorWorkflow` presente. |
| **excelente** | Lo anterior + iniciativa: clave de dedup estable y bien elegida (`payment_id`, no el item entero), `onError: stopWorkflow` explícito, y/o nota de que el error workflow debe incluir el id de la execution para depurar. |

### C2 — Idempotencia bien razonada (hilo: confiabilidad) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Cree que reintentar basta; no distingue fallo transitorio de efecto duplicado. |
| **en-progreso** | Pone el dedup pero no sabe explicar por qué va antes; o usa una clave inestable (timestamp, id generado por corrida). |
| **competente** | Ubica la barrera antes del efecto secundario y explica que protege la acción peligrosa; elige una clave estable del evento. |
| **excelente** | Articula que **reintentar sin idempotencia agrava** los duplicados (timeout tras crear la factura → reintento crea otra) y conecta con at-least-once de 7.2 / 3.14. |

### C3 — Comprensión demostrada (`hardening.md` calza con el JSON) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `hardening.md`, o repite el enunciado sin explicar el porqué. |
| **en-progreso** | Explica el orden pero no el riesgo de reintentar sin idempotencia (o viceversa). |
| **competente** | Explica ambos: dedup-antes-del-efecto y reintento-sin-idempotencia-duplica, con sus palabras. |
| **excelente** | Distingue con precisión "tolerar fallos transitorios" (reintentos) de "no duplicar efectos" (idempotencia) y nombra el error workflow como observabilidad (5.10) en automatización. |

## Errores típicos a marcar

- Dedup **después** del nodo de efecto secundario → la factura duplicada ya se creó; deduplicar el Slack no la borra.
- Activar reintentos **sin** barrera de idempotencia → ante un timeout post-creación, el reintento duplica la factura.
- Clave de dedup **inestable** (timestamp de llegada, id generado en cada corrida) → no deduplica nada.
- `waitBetweenTries: 0` o muy bajo → reintentos agresivos martillan la API justo cuando está sobrecargada.
- Falta `errorWorkflow` → el flujo falla en silencio.
- Error workflow que "avisa que algo falló" sin el id de la execution → inútil para depurar.
- (transversal) Romper la conexión "Crear factura" → "Notificar Slack" al reconectar el dedup.

## Señales de dependencia-IA

- Un `workflow.json` perfecto pero un `hardening.md` que no puede defender el **orden** del dedup (lo más probable que una IA acierta en estructura y el alumno no entiende).
- Explica con vocabulario que no aparece en la lección (p. ej. "outbox pattern", "saga") sin poder decir qué problema resuelve aquí.
- Dice "los reintentos hacen el flujo idempotente": confusión exacta que la lección desarma; señal de copiar sin internalizar.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `pytest test_workflow.py` y lee el primer assert que falla: te nombra la propiedad que falta (¿el dedup está antes o después del efecto secundario?)."
- **Pregunta socrática (nivel 2):** "Si el primer webhook sufre un timeout justo **después** de crear la factura, ¿qué hace su reintento? ¿Y qué hace tu dedup con el segundo webhook idéntico? ¿En qué orden tienen que estar para que eso no duplique?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "La barrera de idempotencia va corriente arriba del efecto secundario (Webhook → dedup → Crear factura) porque protege la acción peligrosa; los reintentos solo cubren fallos transitorios de una ejecución. Ajusta tu `hardening.md` para que explique ambos, no solo la estructura. Revisa 4.3–4.4 de la lección."

## Conexión con el proyecto / capstone

- Este workflow endurecido es el **patrón de confiabilidad** del Capstone F7 (idempotente, manejo de errores, observable): un agente que ejecuta acciones externas no puede duplicar efectos ni fallar en silencio. Entender aquí el orden dedup-antes-del-efecto evita arrastrar la misconception al capstone.
