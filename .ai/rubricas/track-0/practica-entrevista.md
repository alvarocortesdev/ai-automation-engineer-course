---
ejercicio_id: track-0/practica-entrevista
fase: track-0
sub_unidad: "T0.3"
version: 1
---

# Rúbrica — Cadencia de entrevistas + banco STAR + autoevaluación de mock

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. Este ejercicio es de **diseño + autoevaluación**, no de código: lo que se evalúa es la calidad y honestidad de los artefactos, no que las historias sean "impresionantes".

## Objetivos evaluados

- O1: Diseñar e implementar una cadencia semanal de mock interviews (3 formatos) con grabación y autoevaluación por rúbrica, desde el mes 2.
- O2: Construir un banco de historias STAR reutilizables en inglés (semilla de 3 → meta 8-10), con Action dominante y Result con número, mapeadas a preguntas behavioral.
- O3: Demostrar el thinking out loud (vía la grabación) y diagnosticar el propio desempeño con rúbrica, extrayendo una mejora accionable.

## Criterios y niveles

### C1 — Cadencia como sistema ejecutable · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay plan, o es aspiracional ("practicaré cuando pueda"); no cubre los 3 formatos. |
| **en-progreso** | Cubre los formatos pero sin día/hora fijos, o falta la regla (inglés/grabado/autoevaluado). |
| **competente** | Día y hora **concretos** para los 3 formatos + herramientas + regla explícita de inglés/grabación/autoevaluación el mismo día. |
| **excelente** | Lo anterior + un disparador anti-excusa creíble y un sistema de archivo de grabaciones (trazabilidad semana a semana). |

### C2 — Calidad de las historias STAR · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Menos de 3 historias, sin estructura STAR, o no están en inglés. |
| **en-progreso** | 3 historias en inglés pero con S inflada y A/R pobres, o Result sin número, o cada una mapea a menos de 3 preguntas. |
| **competente** | 3 historias en inglés, S/T/A/R etiquetados, **Action dominante (~60%)**, **Result con número**, cada una mapeada a ≥3 preguntas. |
| **excelente** | Lo anterior + al menos una historia **demuestra** un hábito de ingeniería (testing/idempotencia/observabilidad/seguridad) sin nombrarlo; backlog hacia 8-10 esbozado. |

### C3 — Autoevaluación honesta y accionable (comprensión demostrada) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No grabó, o la "autoevaluación" no evidencia que se escuchó (genérica, sin datos del audio). |
| **en-progreso** | Grabó y rellenó la rúbrica, pero la mejora es vaga ("hablar mejor", "estar menos nervioso"). |
| **competente** | Autoevaluación basada en lo que **escuchó** (muletillas, silencios, si clarificó), con **1 mejora concreta y accionable**. |
| **excelente** | Mejora atada a un criterio observable (p. ej. "clarificar requisitos antes de codear; me lancé en el min 1") + reconoce una sorpresa real del audio. |

### C4 — Comunicación e inglés técnico · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Artefactos en español donde debían ir en inglés; STAR ilegible. |
| **en-progreso** | Inglés con errores que entorpecen, o estructura difícil de seguir. |
| **competente** | Historias y mock en inglés comprensible; STAR claro y conciso. |
| **excelente** | Inglés fluido y natural; las historias se leen como respuestas listas para decir en voz alta. |

## Errores típicos a marcar

- "Practicaré cuando me sienta listo": cadencia esporádica en vez de día/hora fijos (mata el objetivo O1).
- _Situation_ inflada que se come el tiempo; _Action_ y _Result_ raquíticos.
- _Result_ sin número ("quedó mejor", "el cliente quedó contento") — es opinión, no resultado.
- Una historia por pregunta en vez de una historia que cubre varias (no entendió la reutilización).
- No grabarse, o "autoevaluarse" sin evidencia de haberse escuchado.
- Mejora no accionable ("hablar mejor") en vez de un comportamiento concreto.
- Historias en español "porque después las traduzco" — el gate es hablar en inglés bajo presión.
- (transversal) historias que afirman calidad ("soy muy ordenado") en vez de demostrarla con hechos y números.

## Señales de dependencia-IA

- Tres historias STAR pulidas y genéricas, sin números específicos ni detalle técnico que solo el alumno podría conocer (probable que la IA las redactara).
- Autoevaluación que describe una grabación que no parece existir (no hay archivo, ni datos concretos del audio).
- Inglés impecablemente uniforme en las historias pero el alumno no puede contarlas en voz alta sin leer (verificación: pedir que cuente una sin mirar).
- Verificación sugerida: pídele que cuente **una** historia del banco en voz alta, en inglés, y que responda "¿por qué hiciste ESE cambio y no otro?". Si no puede defender la Action, la historia no es suya o no la interiorizó.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca incluir el texto de la solución de referencia.**

- **Pista (nivel 1):** "Mira la proporción de tu mejor historia: ¿cuánto ocupa la _Situation_ vs la _Action_? ¿Dónde está el número del _Result_?"
- **Pregunta socrática (nivel 2):** "Si yo te pregunto '¿por qué hiciste ese cambio y no otro?', ¿tu Action ya lo responde, o tendrías que improvisar? ¿Y tu cadencia: qué te impide hacer el primer mock esta semana, exactamente?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Reescribe la Action de la historia 1 empezando por cómo **mediste/diagnosticaste** antes de actuar, y cierra el Result con la métrica del objetivo. En la cadencia, fija un día y hora específicos para el primer formato y agenda la grabación; sin eso, el objetivo O1 no se cumple."

## Conexión con el proyecto / capstone

- Alimenta el portafolio (T0.5): cada capstone terminado son 2-3 historias STAR nuevas; la historia de falla en producción (T0.4) es la más potente del banco. El system design de RAG que ensaya aquí es explicar la arquitectura de su capstone de Fase 6.
