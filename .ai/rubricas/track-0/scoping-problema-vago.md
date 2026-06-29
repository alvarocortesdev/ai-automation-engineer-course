---
ejercicio_id: track-0/scoping-problema-vago
fase: track-0
sub_unidad: "T0.8"
version: 1
---

# Rúbrica — Convierte un pedido vago en un mini-spec (discovery)

> Rúbrica analítica para un ejercicio de **diseño/razonamiento**. Lo que se evalúa es el **criterio de
> discovery**: separar la solución imaginada del problema, hacer las preguntas correctas, y acotar un MVP
> entregable. No hay un único spec correcto, pero sí criterios correctos: un alumno puede scopear distinto
> y estar bien si lo justifica; puede "entregar un spec" que en realidad codea la solución imaginada del
> cliente y estar mal.

## Objetivos evaluados
- **O1** — Convertir un problema vago en un mini-spec aplicando el banco de 7 preguntas antes de codear.
- **O2** — Separar la solución imaginada del problema real y acotar una rebanada mínima de valor.

## Criterios y niveles

### C1 — Separar solución imaginada del problema · mapea: O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Toma el pedido literal ("asistente por WhatsApp") como el problema y diseña sobre eso. |
| **en-progreso** | Intuye que hay algo más detrás, pero el spec sigue centrado en la solución que pidió el cliente. |
| **competente** | Nombra la solución imaginada y reformula el problema en términos de outcome (no-shows / horas de confirmación), no de "chatbot/WhatsApp". |
| **excelente** | El mini-spec **no menciona** la solución imaginada; el problema queda planteado de forma que admite varias soluciones, y deja "WhatsApp" como una opción de implementación, no como el objetivo. |

### C2 — Calidad del discovery (las 7 preguntas) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Faltan la mayoría de las preguntas, o son genéricas sin conectar con el caso. |
| **en-progreso** | Cubre algunas dimensiones pero omite las críticas (costo de error, rebanada mínima), o no distingue pregunta de supuesto. |
| **competente** | Cubre las 7 dimensiones con preguntas pertinentes y marca las respuestas como **supuestos**, no como hechos. |
| **excelente** | Las preguntas son afiladas (revelan el proceso manual real), el costo de error se traduce a una decisión técnica (human-in-the-loop), y detecta el dato gratis (citas históricas) como activo de evaluación. |

### C3 — Mini-spec y rebanada mínima · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay spec, o no tiene métrica de éxito ni fuera-de-scope. |
| **en-progreso** | Spec presente pero la métrica no tiene número, o el "MVP" es en realidad todo el sistema (no acota nada). |
| **competente** | Spec completo con métrica numérica, en-scope y fuera-de-scope explícitos, y una rebanada mínima entregable. |
| **excelente** | El MVP es genuinamente pequeño (resuelve el dolor #1 primero), el fuera-de-scope incluye explícitamente la solución imaginada, y la métrica tiene línea base y meta. |

### C4 — Identificación del riesgo (metacognición) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **competente** | Nombra una pregunta cuya respuesta cambiaría el diseño y explica por qué. |
| **excelente** | Elige el riesgo de verdad dominante (p. ej. calidad de los datos históricos, o el volumen real de urgentes) y lo liga a una decisión concreta que tomaría distinto. |

## Errores típicos a marcar
- **Codear la solución imaginada:** el spec dice "chatbot/WhatsApp" en vez de plantear el problema (no-shows, clasificación). Es el error central.
- **Saltarse el costo de error:** no preguntar qué pasa si el sistema se equivoca → se pierde la justificación del human-in-the-loop.
- **MVP que no acota:** el "en-scope" es el sistema completo; no hay rebanada mínima real.
- **Métrica sin número:** "que funcione mejor" no es métrica de éxito.
- **Confundir supuesto con hecho:** presentar respuestas inventadas como datos confirmados del cliente.
- (transversal) no registrar las preguntas abiertas/supuestos (rompe la disciplina spec-driven); ignorar que un dato existente (citas históricas) sirve para evaluar.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Spec impecable y exhaustivo pero que **codea la solución imaginada** (un LLM tiende a complacer el pedido literal del cliente).
- Las 7 preguntas perfectamente formateadas pero los supuestos no calzan con el caso concreto (genéricos, intercambiables con cualquier pedido).
- **Verificación sugerida:** pedir al alumno que, sin notas, diga cuál es la **rebanada mínima** y por qué esa y no otra. Si hizo el discovery, lo justifica con el dolor #1; si lo generó, recita el spec sin priorizar.

## Feedback sugerido (graduado)
> Nunca escribir el spec por el alumno.
- **Pista (nivel 1):** "Lee tu problem statement: ¿menciona la palabra 'WhatsApp' o 'chatbot'? Si sí, todavía estás describiendo la solución que el cliente se imaginó, no su problema."
- **Pregunta socrática (nivel 2):** "Si el cliente pudiera resolver UNA sola cosa primero, ¿cuál duele más? ¿Tu MVP es esa, o es todo a la vez? ¿Qué pasa si el sistema se equivoca en el peor caso?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Reformula el problem statement en términos del número que el cliente quiere mover (no-shows, horas de confirmación). Luego define como MVP la rebanada que ataca el dolor #1, y manda el resto a fuera-de-scope."

## Conexión con el proyecto / capstone
- Es el músculo que diferencia el write-up de tus capstones de [T0.5]: contar el **discovery** (qué pediste vago, cómo lo acotaste) hace tu proyecto único frente al "80% idéntico". Es también la STAR de ambigüedad de [T0.3] y la disciplina spec-driven aplicada a un humano que no sabe lo que quiere.
