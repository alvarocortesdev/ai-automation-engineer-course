---
ejercicio_id: <fase>/<slug>        # debe coincidir con el id de ejercicio.yml
fase: <fase>
sub_unidad: "<x.y>"
version: 1
---

# Rúbrica — <Título del ejercicio>

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback.

## Objetivos evaluados
> Copiados (o derivados) de `objetivos` en `ejercicio.yml`. Cada criterio de abajo mapea a uno o más.

- O1: <objetivo observable, verbo de Bloom>
- O2: <…>

## Criterios y niveles

> Para cada criterio: qué es observable y cómo se ve en cada nivel. Incluye sólo los criterios que apliquen a este ejercicio (un ejercicio `a-mano` de Fase 0 no tiene "seguridad" ni "eval").

### C1 — Corrección (¿hace lo que el objetivo pide?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | <no cumple el objetivo: …> |
| **en-progreso** | <lo intenta pero falla en algo sustancial: …> |
| **competente** | <cumple el objetivo con calidad aceptable: …> |
| **excelente** | <cumple + algo que demuestra dominio / hilo transversal por iniciativa: …> |

### C2 — Calidad de ingeniería (tests/aserciones reales, clean code, manejo de errores) · mapea: O?
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | … |
| **en-progreso** | … |
| **competente** | … |
| **excelente** | … |

<!-- Criterios opcionales según el ejercicio; borra los que no apliquen:
### C3 — Seguridad (OWASP web/LLM según aplique)
### C4 — Comprensión demostrada (el write-up calza con el código/razonamiento)
### C5 — Observabilidad / eval (si toca IA: eval harness + número)
### C6 — Comunicación (README/ADR claros; inglés en fases tardías)
-->

## Errores típicos a marcar
> Lista concreta para este ejercicio. El corrector la contrasta contra la entrega.

- <error frecuente 1 + por qué está mal>
- <error frecuente 2 …>
- (transversales, si aplican) persigue coverage% en vez de aserciones; mockea de más; confía en la salida del LLM sin validar; agente con exceso de tools/permisos; falta un trade-off defendible.

## Señales de dependencia-IA
> Indicios de que el alumno usó IA para *pensar* en vez de *aprender*. El corrector las describe sin acusar y propone una verificación.

- <p. ej. resultado correcto sin proceso/razonamiento visible>
- <explicación que no calza con el trabajo>
- <sofisticación impropia del nivel de la fase, indefendible>

## Feedback sugerido (graduado)
> Plantilla de pistas para que el corrector no improvise el spoiler. Ordenadas de menos a más directas. **Nunca incluir el código de la solución.**

- **Pista (nivel 1):** <apunta a la región del error sin resolverlo>
- **Pregunta socrática (nivel 2):** <que el alumno reconstruya el razonamiento>
- **Dirección concreta (nivel 3, sólo tras intento real):** <qué corregir y por qué, sin dar la solución>

## Conexión con el proyecto / capstone
> Cómo este ejercicio alimenta el capstone de la fase (constructive alignment).

- <una línea>
