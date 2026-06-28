---
ejercicio_id: fase-7/criterio-de-salida-n8n
fase: fase-7
sub_unidad: "7.1"
version: 1
---

# Rúbrica — Criterio de salida: ¿n8n, código o Temporal?

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio de razonamiento/diseño: **no hay test**. No existe una única respuesta correcta; se evalúa que cada elección esté **justificada por una restricción** y que el alumno reconozca los límites reales del low-code. El corrector mide el razonamiento, no la coincidencia con la solución de referencia.

## Objetivos evaluados

- O1: Decidir por la **restricción dominante** (no por gusto) si cada caso se queda en n8n o se gradúa.
- O2: Identificar los **límites reales del low-code** que obligan a graduar, y reconocer el **patrón híbrido**.
- O3: Documentar la decisión de graduar en un **ADR** con un trade-off honesto.

## Criterios y niveles

### C1 — Decisiones justificadas por restricción · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige por gusto ("código siempre es mejor") o deja celdas vacías; no nombra restricciones. |
| **en-progreso** | Acierta algunas elecciones pero la "restricción dominante" es vaga ("es más complejo") o la "señal que cambiaría la decisión" falta. |
| **competente** | Las 4 filas tienen elección + restricción concreta + señal de cambio defendible. Las elecciones son razonables (ver solución de referencia para el rango aceptable). |
| **excelente** | Además matiza: reconoce que más de una opción es viable en algún caso y argumenta el corte; nombra costo/latencia o mantenibilidad por ops como factor. |

### C2 — Reconoce los límites del low-code y el híbrido · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No identifica ningún límite real de n8n; manda el caso durable a n8n o a un script. |
| **en-progreso** | Identifica un límite pero no asigna bien el caso durable, o trata el caso de IA como "todo n8n" o "todo código". |
| **competente** | El caso con estado durable/esperas largas/reanudar-exacto va a **Temporal**; el de IA reconoce el **patrón híbrido** (n8n delgado + servicio en código). |
| **excelente** | Explica *por qué* "reanudar exactamente tras crash" y "exactamente una vez" son la firma de durable execution, y por qué el híbrido da lo mejor de ambos (visibilidad para ops + testabilidad del core). |

### C3 — ADR con trade-off honesto · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay ADR, o solo dice "elijo X porque es mejor". |
| **en-progreso** | ADR con contexto y decisión, pero sin alternativas o sin trade-off (solo ventajas). |
| **competente** | ADR completo: contexto, decisión, alternativas descartadas y un trade-off real (qué pierde al graduar). |
| **excelente** | El trade-off es honesto y específico: menos visibilidad para ops, más infra que operar, curva de aprendizaje del equipo; no vende la graduación como gratis. |

## Errores típicos a marcar

- "Código siempre es mejor que low-code" → ignora que a veces n8n gana **porque** un no-dev debe mantenerlo.
- Mandar el onboarding multi-día (estado durable) a n8n con un nodo Wait, creyendo que basta → n8n no garantiza replay determinista ni durabilidad de estado.
- Tratar el caso de IA como dicotomía (todo n8n / todo código) en vez de híbrido.
- ADR que solo lista ventajas: graduar también **cuesta** (infra, visibilidad, mantenimiento).
- "Restricción dominante" vaga ("es complejo") sin nombrar QUÉ restricción (lógica/branching, testabilidad, estado durable, volumen/latencia, mantenedor no-dev).

## Señales de dependencia-IA

- Cuatro decisiones impecables pero sin una sola "señal que cambiaría mi decisión" pensada por el alumno → respuesta plausible generada, no razonada.
- ADR genérico que no menciona ninguna restricción concreta del escenario elegido.
- Usa el patrón híbrido como muletilla en los 4 casos sin defender por qué cada uno lo necesita o no.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Para cada fila, completa la columna 'restricción dominante' con UNA palabra clave: ¿es la lógica, la testabilidad, el estado durable, el volumen, o quién la mantiene? Esa palabra decide casi sola."
- **Pregunta socrática (nivel 2):** "En el onboarding de proveedor, ¿qué pasa con tu solución si el servidor se reinicia al día 4, durante la espera de la firma? ¿Reanuda exactamente donde quedó? ¿Qué herramienta te garantiza eso?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El caso con esperas de días + reanudar exacto + exactamente-una-vez es durable execution (Temporal, 7.3); el de IA es híbrido (n8n orquesta, un servicio en código extrae y se evalúa). Tu ADR debe nombrar qué PIERDES al graduar, no solo lo que ganas. Revisa 4.7 de la lección."

## Conexión con el proyecto / capstone

- Esta decisión define la **arquitectura del Capstone F7**: qué vive en n8n (orquestación visible) y qué se gradúa a código o Temporal. El ADR que escribes aquí es, literalmente, una de las decisiones que el capstone exige documentar.
