---
ejercicio_id: fase-6/diseno-multiagente-hitl
fase: fase-6
sub_unidad: "6.8"
version: 1
---

# Rúbrica — Diseño: sistema agéntico con patrón, framework y HITL

> Rúbrica **analítica** atada a los `objetivos` del contrato. **Hay más de un diseño
> correcto.** Lo que se evalúa NO es que el alumno coincida con la referencia, sino la
> **calidad de la justificación**: cada decisión atada a una restricción dominante, no a un
> gusto. Un diseño que elige "5 agentes con LangGraph" sin defender por qué un single-agent
> no alcanza es peor que un single-agent bien justificado.

## Objetivos evaluados
- **O1** — Elegir patrón por la restricción dominante (y justificar single vs multi).
- **O2** — Elegir framework por restricción, nombrando qué se pierde.
- **O3** — Ubicar HITL en lo irreversible y definir un techo de costo.
- **O4** — Distinguir memoria corto/largo plazo; 3 riesgos OWASP con mitigación.

## Criterios y niveles

### C1 — Decisión de patrón y framework (¿justifica por restricción?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige patrón/framework sin razón, o "el mejor", o multi-agente "porque es más potente". |
| **en-progreso** | Da una razón vaga ("LangGraph es completo") sin atarla a una restricción del escenario; no dice qué pierde. |
| **competente** | Patrón y framework atados a una restricción concreta del caso (volumen, especialización, control de estado), y nombra al menos un trade-off del framework. |
| **excelente** | Defiende explícitamente single-agent como default y por qué (o por qué no alcanza aquí), y el trade-off del framework es específico (no "tiene curva de aprendizaje"). |

### C2 — Seguridad y HITL (OWASP aplicado al escenario) · mapea: O3, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No marca el reembolso como HITL, o lista riesgos OWASP genéricos sin aterrizarlos en este escenario. |
| **en-progreso** | Marca el HITL del reembolso pero las mitigaciones son "ten cuidado" / "valida bien" sin acción concreta. |
| **competente** | Reembolso → HITL justificado por irreversibilidad; ≥1 acción reversible automática; 3 riesgos OWASP **distintos** con mitigación accionable y específica al caso. |
| **excelente** | Identifica el **prompt injection vía el texto del ticket** (contenido no confiable, LLM01) como el riesgo no obvio, y separa el `escalar_a_humano` (semi-irreversible) con criterio propio. |

### C3 — Memoria y costo (modelo mental correcto) · mapea: O3, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Confunde memoria de corto y largo plazo, o no define el techo de costo. |
| **en-progreso** | Distingue las dos memorias pero sin ejemplo concreto, o el techo no dice qué pasa al alcanzarse. |
| **competente** | Corto plazo = conversación del ticket actual con ejemplo; largo plazo = store entre tickets del cliente con ejemplo; techo con ubicación y comportamiento de corte. |
| **excelente** | Conecta el techo de pasos con costo (tokens por vuelta) **y** con un fallback razonable (escalar a humano al agotarse), no solo "cortar". |

## Errores típicos a marcar
- **Multi-agente por defecto** — proponer un enjambre de agentes sin justificar por qué un single-agent con buenas tools no resuelve el caso. El default correcto es single-agent.
- **"El mejor framework"** — elegir sin una restricción dominante identificada; señal de que no entendió el problema.
- **Reembolso automático** — dejar `emitir_reembolso` sin HITL es el fallo de seguridad central del ejercicio (Excessive Agency, LLM06).
- **Riesgos OWASP genéricos** — citar "prompt injection" sin aterrizarlo en que el **texto del ticket es contenido no confiable** que entra al contexto del agente.
- **Confundir las memorias** — meter "el nombre del cliente entre tickets" en la lista de mensajes (corto plazo) en vez de un store.
- (transversales) confía en la salida del LLM sin validar; agente con exceso de tools/permisos; falta un solo trade-off defendible.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diseño que enumera los 5 patrones y los 10 riesgos OWASP con prosa pulida pero no **elige** ni justifica por qué uno y no otro (volcado de catálogo, no decisión).
- Mitigaciones genéricas que servirían para cualquier agente, sin tocar las acciones concretas del escenario (reembolso, ticket no confiable, base de clientes recurrente).
- **Verificación sugerida:** pedir que defienda, en voz alta, por qué **no** eligió uno de los otros patrones (p. ej. "¿por qué no handoffs?"). Si entendió, contrasta restricciones; si dependió de la IA, repite el catálogo.

## Feedback sugerido (graduado)
> Nunca dar el diseño "correcto" antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu diseño elige multi-agente. ¿Qué restricción concreta de este escenario hace que un solo agente con estas 5 tools no alcance? Si no la encuentras, quizás single-agent es la respuesta."
- **Pregunta socrática (nivel 2):** "De las 5 acciones, ¿cuál no podrías deshacer si el agente se equivoca? ¿Qué pasa si la ejecuta por una instrucción escondida en el texto de un ticket?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Ata cada decisión a una restricción: patrón ← ¿volumen o especialización?; framework ← ¿control de estado, tipado, o menor fricción?; HITL ← reversibilidad de cada acción; memoria ← ¿dato del run o dato entre runs? Y para seguridad parte por: el texto del ticket es contenido no confiable (LLM01), el reembolso es Excessive Agency (LLM06)."

## Conexión con el proyecto / capstone
- Este diseño es el boceto del **capstone agéntico estrella de la Fase 7** (input → clasifica/extrae → decide → ejecuta) y alimenta el Definition of Done: least-privilege de tools, HITL para acciones sensibles, techo de costo y observabilidad. Defenderlo por restricciones es justo lo que se evalúa en una entrevista de system design de IA.
