---
ejercicio_id: fase-6/defensa-contenido-no-confiable
fase: fase-6
sub_unidad: "6.2"
version: 1
---

# Rúbrica — Defensa de prompt injection + versionado (diseño)

> Rúbrica analítica para un ejercicio **de diseño**. No hay respuesta única: se evalúa
> la **coherencia** del diseño con la amenaza y la **honestidad** sobre lo que la
> defensa básica NO cubre. Un diseño "no estándar" bien argumentado vale más que el
> "correcto" sin defensa. Lee la solución de referencia al final.

## Objetivos evaluados

- **O1** — Segregar contenido no confiable del canal de instrucciones.
- **O2** — Distinguir vectores mitigados de no mitigados (honestidad).
- **O3** — Versionado + trazabilidad para auditar una falla.

## Criterios y niveles

### C1 — Segregación de datos vs. instrucciones · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No cambia el flujo, o "arregla" filtrando palabras ("ignora") del documento, o pone el documento en el `system`. |
| **en-progreso** | Delimita el documento pero no declara que es contenido no confiable, o no prohíbe revelar el system. |
| **competente** | `system` con rol de autoridad que (a) delimita el documento (p. ej. `<DOCUMENTO>...</DOCUMENTO>`), (b) declara ese texto como DATOS no instrucciones, (c) ordena ignorar órdenes internas, (d) prohíbe revelar el system. El documento va en `user`. |
| **excelente** | Además menciona el canal de autoridad del rol `system` (instrucciones del operador ≠ texto del usuario) y/o normaliza/escapa los delimitadores para que el atacante no los falsifique. |

### C2 — Honestidad sobre los límites (vectores mitigados / no) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Afirma que el diseño "bloquea todo" / "es seguro": señal de no entender el problema. |
| **en-progreso** | Nombra mitigados pero no logra nombrar uno no mitigado, o el "no mitigado" es trivial. |
| **competente** | Dos vectores mitigados bien explicados (p. ej. inyección directa de "ignora", intento de exfiltrar el system) **y** uno no mitigado real (p. ej. inyección indirecta sofisticada, ofuscación, instrucciones en otro idioma/codificación). |
| **excelente** | Prioriza por impacto y enlaza la defensa en profundidad a `6.14` (guardrails, validación de salida). |

### C3 — Acción peligrosa (no ejecutar salida cruda) · mapea: O1/seguridad
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No aborda la acción "enviar correo" o cree que basta con el prompt. |
| **en-progreso** | Dice "validar" vagamente sin nombrar la regla. |
| **competente** | Nombra la regla: **nunca ejecutar una acción con efectos sobre la salida cruda del LLM** sin validación/confirmación; el correo se dispara solo tras una verificación en código (o HITL). |
| **excelente** | Conecta con least-privilege de herramientas / human-in-the-loop (6.14, 6.8). |

### C4 — Versionado y trazabilidad · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No versiona, o "guardo el prompt en el código" sin identificador. |
| **en-progreso** | Versiona el prompt pero no registra qué versión produjo cada salida. |
| **competente** | Identificador estable (semver/`@vN`/hash) **y** registro por respuesta de al menos {prompt_version, model, input, output} para auditar después. |
| **excelente** | Conecta la trazabilidad (prompt+modelo+dataset→score) con el eval harness de `6.9`. |

## Errores típicos a marcar

- **"Filtrar la palabra ignora con regex"** como defensa: trivial de evadir (mayúsculas, sinónimos, otro idioma, base64).
- **Meter el documento en el `system`**: lo eleva a instrucción — empeora el problema.
- **Declarar el diseño "100% seguro"**: el prompt injection no se elimina con delimitadores; afirmarlo es la señal #1 de inmadurez.
- **Olvidar la acción peligrosa**: enfocarse solo en "no revelar el system" e ignorar que la salida no debe disparar efectos sin validar.
- **Versionar el prompt pero no registrar qué versión generó cada salida**: sin eso no hay auditoría posible.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- Diseño que usa vocabulario de seguridad avanzado (p. ej. "spotlighting", "dual LLM pattern") pero no puede explicar, en una pregunta de seguimiento, por qué un filtro de palabras no sirve.
- Afirmación tajante de seguridad total (un humano que entendió el tema casi siempre añade un "pero esto no es blindaje").
- **Verificación sugerida:** "Dame una inyección que TU diseño NO frena" — si no puede inventar ninguna, no interiorizó los límites.

## Feedback sugerido (graduado)

> Nunca redactar el `system` completo por el alumno.

- **Pista (nivel 1):** "¿En qué rol están hoy las instrucciones y en cuál el documento? Si el modelo trata todo como instrucciones, ¿qué pasa con el texto del atacante?"
- **Pregunta socrática (nivel 2):** "Si delimitas el documento y le dices al modelo que lo ignore como orden, ¿qué tipo de inyección más astuta podría colarse igual? Nómbrala."
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu `system` delimita bien, pero no aborda el correo. Aunque el modelo resista la inyección, la regla es que **ninguna acción con efectos se dispara sobre la salida cruda del LLM**: el correo solo sale tras una validación en código o una confirmación humana. Añade esa capa."

## Conexión con el proyecto / capstone

- Esta defensa es la que protege el **Capstone F6 (RAG de producción)** cuando un documento del corpus contiene una inyección indirecta; el versionado + trazabilidad es lo que el eval harness (6.9) usa para atribuir regresiones a un cambio de prompt.
