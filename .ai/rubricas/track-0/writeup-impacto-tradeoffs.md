---
ejercicio_id: track-0/writeup-impacto-tradeoffs
fase: track-0
sub_unidad: "T0.5"
version: 1
---

# Rúbrica — Del "hice X" al "X redujo Y" + write-up de trade-offs

> Rúbrica analítica para un ejercicio de **diseño/razonamiento**. Se evalúan dos cosas: (1) si las
> decisiones del write-up son **decisiones reales** —con alternativa visible y un porqué defendible, no
> elecciones sin trade-off— y (2) si los bullets de impacto usan la **fórmula correcta con métricas
> honestas**, sin inflar. El contenido exacto varía según el proyecto del alumno; lo que se mide es el
> criterio, no la coincidencia con un ejemplo.

## Objetivos evaluados
- **O2** — Write-up de trade-offs: decisión → alternativa descartada → por qué; tocar un hilo de producción.
- **O3** — Lenguaje de impacto: acción + métrica + resultado, con números medidos o estimados honestos.
- **O2b** — Checklist de los tres no-negociables con estado real y acción de cierre.

## Criterios y niveles

### C1 — Calidad de las decisiones (write-up de trade-offs) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Menos de dos decisiones, o "decisiones" sin alternativa ("usé FastAPI" sin trade-off). |
| **en-progreso** | Dos decisiones con alternativa, pero el "por qué" es débil o circular ("porque es mejor") sin nombrar el costo/beneficio real. |
| **competente** | ≥2 decisiones, cada una con alternativa razonable descartada y un porqué defendible; ≥1 toca un hilo de producción (HITL, costo-latencia, observabilidad). |
| **excelente** | Las decisiones citan el costo concreto de la falla que previenen (p. ej. "cerrar el ticket de un cliente cuesta más que la latencia de validar") y/o un punto del Definition of Done de la fase (least-privilege + HITL). |

### C2 — Lenguaje de impacto (bullets) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Bullets que describen tarea ("usé dos modelos") sin resultado, o menos de tres. |
| **en-progreso** | Algún bullet con la fórmula, pero otros siguen siendo "hice X"; o un número sin marcar medido/estimado. |
| **competente** | Los 3 bullets con acción + métrica + resultado; cada número marcado como medido o estimado. |
| **excelente** | Métricas claramente honestas (rangos, "estimado" donde corresponde) y conectadas a un trade-off del write-up (p. ej. el ruteo de modelos del costo aparece como decisión *y* como impacto). |

### C3 — Honestidad de las métricas (señal crítica) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Números impresionantes pero indefendibles ("ahorré muchísima plata", "10x más rápido") sin base. |
| **en-progreso** | Números plausibles pero sin marcar si son medidos o estimados (ambigüedad que en una entrevista se cae). |
| **competente** | Cada número marcado; los estimados se presentan como estimados, no como medidos. |
| **excelente** | El alumno distingue qué *podría* medir de verdad y qué solo estima, y lo dice; nada que no pueda defender en vivo. |

### C4 — Checklist de los tres no-negociables · mapea: O2b
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Falta el checklist, o marca "sí" en todo sin evidencia (un screenshot contado como demo que corre). |
| **en-progreso** | Checklist presente pero sin acción de cierre para lo que falta. |
| **competente** | Estado real de los tres; acción concreta de cierre para los que faltan (p. ej. "grabar video de 60 s"). |
| **excelente** | Distingue correctamente screenshot de demo que corre y prioriza el write-up como el no-negociable más raro. |

## Errores típicos a marcar
- **Falsa decisión**: "elegí Python/FastAPI/Postgres" sin alternativa ni trade-off (no es un cruce de diseño).
- **Por qué circular**: "lo elegí porque es la mejor opción" sin nombrar el costo/beneficio concreto.
- **Número inflado o sin marcar**: "10x más rápido" indefendible, o una métrica sin decir si se midió.
- **Screenshot contado como demo que corre**: viola el no-negociable.
- **Ningún hilo de producción**: dos decisiones puramente cosméticas (color del botón, nombre de variable).
- (transversal) write-up que no podría defenderse en una entrevista (T0.3): si no aguanta un "¿por qué no
  lo hiciste al revés?", no es una decisión articulada.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Write-up pulido y genérico que encaja con *cualquier* proyecto (no menciona detalles concretos del suyo).
- Métricas redondas y perfectas ("exactamente 60%", "exactamente 90%") presentadas como medidas sin que el
  proyecto del alumno tenga forma de haberlas medido.
- Decisiones sofisticadas que el alumno no puede defender si se le pregunta "¿y si hubieras elegido la
  alternativa?".
- **Verificación sugerida:** pedir que defienda **una** de sus decisiones contra su alternativa en voz
  alta, y que diga cuál de sus tres números mediría de verdad y cómo. Si lo articuló él, responde; si
  dependió de la IA, se nota en la defensa.

## Feedback sugerido (graduado)
> Nunca reescribir el write-up por el alumno.
- **Pista (nivel 1):** "Tu decisión 1 dice qué usaste, pero no contra qué. ¿Había otra forma razonable de
  hacerlo? Si no la había, no es una decisión —es la única opción. Busca un cruce con dos caminos."
- **Pregunta socrática (nivel 2):** "Para tu agente: ¿qué pasa si el LLM clasifica mal y el sistema ya
  ejecutó la acción? ¿Cuánto cuesta esa falla comparado con validar antes? Esa comparación *es* tu porqué."
- **Dirección concreta (nivel 3, sólo tras intento real):** "El patrón a corregir es separar 'elección sin
  trade-off' de 'decisión con alternativa'. Reescribe cada decisión con el molde explícito: elegí A,
  descarté B, porque el costo de [la falla que B no previene] supera a [lo que A cuesta]. Y marca cada
  número como medido o estimado."

## Conexión con el proyecto / capstone
- El write-up de trade-offs es lo que defiendes en vivo en [T0.3 Práctica de entrevista] y la materia prima
  del CV de impacto en [T0.7]. El manejo de fallas que articulas aquí es la historia de
  [T0.4 Falla en producción]. Es el no-negociable que casi nadie tiene: dominarlo te diferencia solo.
