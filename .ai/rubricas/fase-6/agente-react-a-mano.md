---
ejercicio_id: fase-6/agente-react-a-mano
fase: fase-6
sub_unidad: "6.8"
version: 1
---

# Rúbrica — El agent loop ReAct, a mano

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo central no es "pasan los
> tests", es que el alumno **entienda que un agente es el tool use de 6.4 en un bucle**,
> con un techo de costo y un gate de seguridad en cada vuelta. Un loop que pasa los tests
> pero ejecuta tools fuera de la allowlist, o que no tiene techo real, no demuestra el
> objetivo.

## Objetivos evaluados
- **O1** — Implementar el agent loop ReAct (razonar → observar → gate → actuar → repetir).
- **O2** — Techo de pasos como guardrail de costo/latencia (sin loop infinito).
- **O3** — Gate de allowlist antes de ejecutar (least privilege / Excessive Agency, LLM06).
- **O4** — Devolver observaciones como `tool_result` y explicar la memoria de corto plazo.

## Criterios y niveles

### C1 — Corrección del loop (¿hace lo que el objetivo pide?) · mapea: O1, O4
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No corre, o no devuelve `ResultadoAgente`; varios tests en rojo. |
| **en-progreso** | Pasa algunos tests pero el conteo de `pasos` está mal, o no guarda el turno del modelo antes de ramificar (rompe el caso de 2 tools). |
| **competente** | Los 5 tests en verde; respuesta directa, tool-luego-responde y 2-tools-secuenciales salen con el conteo de pasos correcto. |
| **excelente** | Además procesa **varios** `tool_use` de un mismo turno (tool use en paralelo) y agregó un test propio que lo ejercita. |

### C2 — Guardrails: techo + gate (calidad de ingeniería) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay techo (un `while True` sin corte) o no hay allowlist real; la tool no permitida se ejecuta. |
| **en-progreso** | Hay techo pero off-by-one (el modelo se llama de más), o el gate va **después** de ejecutar la tool. |
| **competente** | `range(MAX_PASOS)` corta exacto (modelo llamado `MAX_PASOS` veces en el caso terco); allowlist comprobada **antes** de ejecutar; tool no permitida → `es_error=True` sin correr. |
| **excelente** | El motivo de rechazo es legible para logging y el alumno explica el techo como guardrail de **costo + seguridad** a la vez. |

### C3 — Comprensión demostrada (write-up calza con el código) · mapea: O2, O3, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`, o las predicciones se escribieron después de ejecutar (calzan perfecto, sin razonamiento). |
| **en-progreso** | `verificacion.md` dice "por si acaso" sin nombrar costo vs seguridad ni LLM06. |
| **competente** | Distingue costo (tokens por vuelta + rate limit) de seguridad (cortar un agente descontrolado), y liga la allowlist a least privilege / Excessive Agency. |
| **excelente** | Explica por qué la última vuelta de ReAct (3 vueltas para 2 tools) no pide tool, y da un ejemplo propio de acción que exigiría HITL. |

## Errores típicos a marcar
- **Ejecutar la tool antes del chequeo de allowlist** — la tool no permitida corre; fallo de seguridad aunque algún test pase. El permiso va primero.
- **No guardar `resp.content` en `mensajes` antes de ramificar** — la siguiente vuelta pierde el `tool_use` que se está respondiendo (la API real rechaza el `tool_result` huérfano).
- **Techo off-by-one** — `while True` mal cortado o `range(MAX_PASOS + 1)`: el modelo se llama de más; el test del modelo terco lo fija.
- **Conteo de `pasos` equivocado** — devolver desde dentro del bloque de tools en vez de dejar que el loop vuelva a llamar al modelo (2 tools deben dar 3 pasos).
- **`tool_result` sin `tool_use_id`** — pierde la correlación pregunta-respuesta de la tool.
- (transversales) confía en la salida del LLM sin validar; agente con exceso de tools/permisos; falta un trade-off defendible en el write-up.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Loop impecable con manejo de tool use en paralelo y `dataclasses` pulidas, pero un `verificacion.md` que no sabe explicar **por qué** el orden (observar → gate → actuar) importa.
- `prediccion.md` con los 3 resultados correctos pero sin razón, o usando vocabulario ("recursion limit", "trajectory eval") por encima del nivel sin poder defenderlo.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué pasa si el modelo pide en un mismo turno **dos** tools, una permitida y otra no. Si entendió el loop y el gate, responde (una corre, la otra se rechaza, ambas observaciones vuelven); si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu loop ejecuta una tool que no está en la allowlist. ¿En qué orden corren: guardar el turno, ¿terminó?, comprobar permiso, ejecutar? ¿Qué no quieres ni tocar?"
- **Pregunta socrática (nivel 2):** "Si el modelo nunca devuelve `end_turn`, ¿qué corta tu loop? ¿Y por qué ese corte es a la vez un tema de plata y de seguridad?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Estructura la vuelta así: (1) `resp = llamar_modelo(mensajes)`; (2) `mensajes.append({'rol':'assistant','contenido':resp.content})` SIEMPRE; (3) `if resp.stop_reason != 'tool_use': return ...end_turn`; (4) por bloque tool_use: `if nombre not in HERRAMIENTAS_PERMITIDAS:` error, else `invocar(...)`; (5) append de los tool_result. El techo es `range(MAX_PASOS)`."

## Conexión con el proyecto / capstone
- Este loop —con techo de costo, gate de allowlist y la base del HITL— es exactamente el entregable "validación de salida antes de ejecutar + least-privilege + techo de costo" del Definition of Done del capstone de la fase, y el esqueleto del capstone agéntico estrella de la Fase 7. Sin él, un agente que actúa es un incidente esperando ocurrir.
