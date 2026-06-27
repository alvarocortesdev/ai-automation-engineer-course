---
ejercicio_id: fase-6/context-window-budget
fase: fase-6
sub_unidad: "6.2"
version: 1
---

# Rúbrica — Token budget: arma el contexto que cabe

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector evalúa el
> **proceso** (¿predijo antes de medir?) y la **comprensión** (¿la reflexión nombra
> el context rot?), no solo si los tests pasan. Lee la solución de referencia **al
> final**, cuando ya formaste tu propio juicio.

## Objetivos evaluados

- **O1** — Implementar la política de token budgeting (system fijo + recientes).
- **O2** — Predecir qué turnos entran/salen sin ejecutar.
- **O3** — Explicar por qué descartar los viejos mitiga el context rot.

## Criterios y niveles

### C1 — Corrección de la política · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No pasa los tests; o "hace caber" descartando recientes en vez de viejos, o parte mensajes. |
| **en-progreso** | Pasa la mayoría pero falla un caso borde (system que excede, historial vacío, o el corte del sufijo). |
| **competente** | Todos los tests verdes: system siempre primero, recientes conservados, orden cronológico, no parte mensajes, `ValueError` cuando el system excede. |
| **excelente** | Además deja la lógica legible y comenta por qué recorre de atrás hacia adelante; o añade un test propio (p. ej. presupuesto exacto al borde). |

### C2 — Proceso Primero-Sin-IA (predicción antes de medir) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`, o se escribió después de correr los tests (números calcados sin razonamiento). |
| **en-progreso** | Predice el resultado pero sin justificar (solo "entran t2,t3,t4"). |
| **competente** | `prediccion.md` existe antes de ejecutar, predice los 3 turnos recientes y razona el cálculo (35 − 5 system = 30 → 3 turnos de 10). |
| **excelente** | Anticipa también un caso borde (p. ej. qué pasa si el system solo ya excede) sin que se lo pidan. |

### C3 — Comprensión demostrada (context rot) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `verificacion.md` ausente, o justifica el descarte solo con "para que quepa". |
| **en-progreso** | Menciona costo/tokens pero no conecta con la **calidad** de recuperación. |
| **competente** | Explica que conservar lo reciente mantiene la señal alta y que llenar la ventana de historial viejo degrada la recuperación (context rot / atención finita). |
| **excelente** | Conecta con compactación (resumir lo descartado en vez de tirarlo) y/o con el capstone RAG. |

## Errores típicos a marcar

- **Descartar los recientes en vez de los viejos** (recorrer el historial al derecho y cortar al final): mata la recencia, contradice el objetivo.
- **Partir un mensaje** para que "quepa el pedacito": confunde más al modelo; un turno entra entero o no entra.
- **Olvidar reinvertir** la lista → la salida queda en orden inverso (más reciente primero), que no es lo que la API espera.
- **No contemplar `ValueError`** cuando el system solo excede el presupuesto (devuelve algo inválido en silencio).
- **Hardcodear un tokenizer** (tiktoken/API) en vez de usar el `contar` inyectado → acopla el ejercicio a la red y rompe la testabilidad.
- (transversal) Justificar el descarte solo por costo y no por calidad (context rot).

## Señales de dependencia-IA

> Describir sin acusar; proponer una verificación.

- Implementación correcta pero `prediccion.md` ausente o idéntica a la salida real (predijo "después").
- `verificacion.md` usa el término "context rot" con precisión de manual pero no puede explicar, en una pregunta de seguimiento, por qué la recencia ayuda.
- **Verificación sugerida:** pedir que prediga a mano un caso nuevo (p. ej. budget 25) y que explique por qué recorre `reversed(historial)` y no al derecho.

## Feedback sugerido (graduado)

> Nunca pegar el código de la solución.

- **Pista (nivel 1):** "¿En qué orden recorres el historial? Si quieres conservar lo más reciente, ¿desde qué punta conviene empezar a sumar?"
- **Pregunta socrática (nivel 2):** "Si sumas turnos del más viejo al más nuevo y cortas al llenarte, ¿qué turnos te quedan? ¿Son los que un usuario querría que el modelo recuerde?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Recorre `reversed(historial)`, resta el costo de cada turno del presupuesto restante y corta en cuanto uno no cabe; al final reinvierte la lista para devolver el orden cronológico. El `system` se cuenta aparte y nunca pasa por ese bucle."

## Conexión con el proyecto / capstone

- Esta política es el módulo que, en el **Capstone F6 (RAG de producción)**, decide cuántos chunks recuperados caben junto al historial sin reventar el budget de costo/latencia — y la base sobre la que se monta la compactación.
