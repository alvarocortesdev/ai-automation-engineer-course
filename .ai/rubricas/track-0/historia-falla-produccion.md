---
ejercicio_id: track-0/historia-falla-produccion
fase: track-0
sub_unidad: "T0.4"
version: 1
---

# Rúbrica — Historia de falla en producción: instrumentar, romper, post-mortem público

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. Este ejercicio es de **instrumentación + escritura**, no de código: lo que se evalúa es que el incidente sea **real**, que la causa raíz sea **blameless y sistémica**, y que el loop se cierre con una **señal nueva**. NO se evalúa que el incidente sea "espectacular".

## Objetivos evaluados

- O1: Instrumentar una app con usuarios reales (logs estructurados + al menos una alerta) para que un fallo se detecte por una señal, no por la queja del usuario.
- O2: Escribir un post-mortem público y blameless de un incidente real con las 7 secciones (summary, impact, timeline, detection, root cause por 5 whys, remediation, action items con dueño y fecha).
- O3: Derivar una métrica/alerta/SLO que cierre el loop y destilar el incidente en una historia STAR en inglés.

## Criterios y niveles

### C1 — Realidad del incidente y de los usuarios (corrección) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Incidente de juguete: usuarios inventados, números redondos sin rastro, sin logs ni evidencia; o no hay incidente real. |
| **en-progreso** | Incidente plausible pero con señales de fabricación (sin impacto humano concreto, sin línea de log real, "100k usuarios"). |
| **competente** | Incidente **real** con usuarios reales nombrados (aunque sean 3) e impacto humano concreto; `instrumentacion.md` muestra un log estructurado real (o un plan honesto del "todavía no"). |
| **excelente** | Lo anterior + correlación clara entre la línea de log (`request_id`) y el evento del timeline; la instrumentación ya existía o se agregó como parte del aprendizaje. |

### C2 — Causa raíz blameless y sistémica (5 whys) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | La causa raíz nombra a una persona ("fui descuidado", "el dev no testeó") o culpa al usuario; o se queda en el síntoma ("había un typo"). |
| **en-progreso** | Intenta los 5 whys pero se detiene en el trigger (el bug puntual) sin llegar a lo sistémico; o la cadena no encadena de verdad. |
| **competente** | Cadena de 5 whys que llega a una causa **sistémica y accionable** (test/alerta/review/deploy que faltaba), **sin** nombres como causa. |
| **excelente** | Lo anterior + reconoce más de un factor contribuyente sistémico y los distingue del trigger; lenguaje genuinamente blameless en todo el documento. |

### C3 — Detección y cierre del loop (observabilidad) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay sección _Detection_, o no reconoce que "me avisó el usuario" es un hueco; no agrega ninguna señal nueva. |
| **en-progreso** | Dice qué alertó pero no **qué NO** alertó; la remediación arregla el bug pero no agrega métrica/alerta/SLO. |
| **competente** | _Detection_ nombra explícitamente el hueco (qué debió alertar y no lo hizo) + agrega una **métrica/alerta/SLO concreta** que detectaría el fallo la próxima vez. |
| **excelente** | Lo anterior + la nueva señal es defendible (umbral/SLO razonado, no inventado) y hay plan de **probar** que la alerta de verdad se dispara. |

### C4 — Estructura, action items y testing · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Faltan secciones de las 7; sin action items, o action items sin dueño/fecha; termina en "ya lo arreglé". |
| **en-progreso** | Las 7 secciones están pero alguna es decorativa; action items vagos o sin dueño/fecha; sin test de regresión. |
| **competente** | Las **7 secciones** completas; action items con **dueño y fecha**; al menos uno es un **test de regresión** que reproduce el fallo. |
| **excelente** | Lo anterior + action items priorizados y atados a la causa raíz (no a síntomas), con el test de regresión descrito de forma que reproduce el fallo específico. |

### C5 — Comunicación e inglés (STAR) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Post-mortem/STAR en español donde debían ir en inglés, o STAR sin estructura/sin número en el Result. |
| **en-progreso** | Inglés con errores que entorpecen, o el STAR no deriva del mismo incidente, o mapea a menos de 3 preguntas. |
| **competente** | Post-mortem y STAR en inglés comprensible; STAR con S/T/A/R, _Action_ dominante, _Result_ con número (la alerta/SLO), ≥3 preguntas mapeadas. |
| **excelente** | Inglés fluido y natural; el STAR se lee como respuesta lista para decir en voz alta y el _Result_ cierra en la señal nueva. |

## Errores típicos a marcar

- Incidente de juguete: usuarios y números inventados, sin impacto humano, sin rastro de logs (mata C1).
- Causa raíz con nombre propio ("fui descuidado", "el usuario hizo algo raro") en vez de algo sistémico — no es blameless.
- Detenerse en el trigger ("había un bug en la línea X") sin preguntar por qué llegó a producción sin que nada lo detectara.
- Sección _Detection_ ausente o que no admite que "me avisó el usuario" es una falla de detección.
- Terminar en "ya lo arreglé" sin agregar métrica/alerta/SLO (remediación ≠ prevención).
- Action items sin dueño ni fecha (es un diario, no un documento de ingeniería).
- No incluir un test de regresión entre los action items (el reflejo de testing del curso).
- Post-mortem o STAR en español ("después lo traduzco") — el gate es el inglés.
- Medir solo "está arriba" (200 OK) e ignorar _gray failures_ (responde pero entrega vacío/incorrecto).
- (transversal) si el incidente fue de seguridad o de costo, no reconocer la dimensión OWASP / techo de costo.

## Señales de dependencia-IA

- Post-mortem pulido y genérico, sin detalle técnico que solo el alumno podría conocer (sin línea de log real, sin nombres de sus usuarios, números sospechosamente redondos).
- Causa raíz "de manual" que no calza con el impacto descrito ni con el timeline (señal de texto generado sin un incidente detrás).
- STAR impecable pero el alumno no puede contar el incidente en voz alta ni responder "¿por qué hiciste ESE cambio y no otro?".
- Verificación sugerida: pídele que muestre **la línea de log real** que correlaciona el fallo, y que cuente el incidente en voz alta en inglés respondiendo "¿qué habría alertado y por qué no lo hizo?". Si no puede, el incidente no es suyo o lo inventó.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca incluir el texto de la solución de referencia.**

- **Pista (nivel 1):** "Lee tu sección _Root cause_: ¿alguno de tus 'por qué' termina en una persona o en el usuario? ¿Y tu _Detection_: dice qué NO alertó?"
- **Pregunta socrática (nivel 2):** "Si esto vuelve a pasar mañana, ¿qué señal del sistema te avisaría, y en cuántos minutos? Si la respuesta sigue siendo 'me avisaría el usuario', ¿cuál es entonces el action item que falta?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Extiende la cadena de 5 whys un paso más allá del bug puntual hasta lo que el sistema permitió (test/alerta/deploy que faltaba), y cierra el post-mortem con una alerta o SLO concreto y un test de regresión. Sin la señal nueva, el objetivo O3 no se cumple."

## Conexión con el proyecto / capstone

- Alimenta el portafolio (T0.5) con la pieza más difícil de falsificar y la historia STAR más potente del banco (T0.3). El post-mortem ES el "write-up público de qué falló" que exige el Definition of Done de los capstones de Fase 5 y Fase 7; la instrumentación es el hábito de observabilidad del curso aplicado.
