---
ejercicio_id: fase-1/index
fase: fase-1
sub_unidad: "1.0"
version: 1
---

# Rúbrica — Diagnóstico de entrada y plan de Fase 1

> Rúbrica analítica para un ejercicio **a-mano** de placement/metacognición. No
> hay "respuesta correcta": se evalúa la **honestidad** del autodiagnóstico, la
> **concreción** del plan (que además **alterne las dos pistas** y agende la
> victoria-IA) y la **claridad** de la justificación de por qué dos lenguajes. Un
> plan precioso pero irreal vale menos que uno modesto y sostenible. El corrector
> premia el realismo, no la ambición.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Autoevaluar el punto de partida por sub-unidad (1.1–1.10) en las dos
  pistas, distinguiendo "lo sé hacer sin notas" de "lo reconozco".
- **O2** — Diseñar un plan con bloques concretos que **alterne** Python y TS y
  **agende** la victoria-IA (1.10), con ritual de repaso.
- **O3** — Justificar el porqué de los dos lenguajes (rol de cada uno) y cuándo
  usarlos.

## Criterios y niveles

### C1 — Honestidad y cobertura del diagnóstico · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta la tabla, o cubre menos de las 10 sub-unidades, o no asigna niveles. |
| **en-progreso** | Cubre las 10 pero el nivel no es defendible (todo en "lo sé hacer" sin evidencia, o todo "nuevo" pese a experiencia previa declarada), o falta la razón por fila, o no distingue a qué pista pertenece cada una. |
| **competente** | Las 10 sub-unidades con pista, nivel **y** una razón coherente; aplica la prueba de "¿podría resolverlo sin notas ahora?" de forma consistente. |
| **excelente** | Además matiza ("reconozco las comprehensions pero nunca escribí un generador") y **usa el diagnóstico para priorizar** el plan (más tiempo donde marcó `nuevo`). |

### C2 — Concreción, realismo y diseño de las dos pistas · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay plan, o son intenciones ("estudiaré más", "le dedicaré tiempo") sin días/horas. |
| **en-progreso** | Hay bloques pero irreales (p. ej. 3 h diarias con trabajo de tiempo completo); **o** no alterna las pistas (planea toda Python y luego todo TS); **o** no agenda la victoria-IA; **o** falta el ritual de repaso. |
| **competente** | Bloques concretos (día/hora/duración) plausibles para su vida; **alterna** las dos pistas de forma explícita; **agenda** la 1.10; ritual de repaso presente. |
| **excelente** | El plan ata el repaso al *spacing* (revisar al día siguiente + a los pocos días con **recuperación**, no relectura); pondera bien (más a Python por ser la pista larga, sin enfriar TS); agenda la victoria-IA **temprano** (tras 1.5) como ancla de motivación y lo justifica. |

### C4 — Comprensión demostrada (por qué dos lenguajes) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay texto, o no nombra un rol para cada lenguaje. |
| **en-progreso** | Menciona ambos pero con frases genéricas ("son populares", "los piden") sin un rol concreto, o asigna el rol al revés (TS para IA, Python para front) sin justificar. |
| **competente** | Asigna a cada lenguaje su rol concreto: **Python** = puente a IA / APIs / datos; **TypeScript** = frontend + filtro de las ofertas fullstack; y da un caso de cuándo usar cada uno. |
| **excelente** | Conecta con su propio perfil/meta (AI + automatización) y reconoce que el valor está en **construir de punta a punta**, no solo en orquestar modelos; señala que `pydantic`↔`zod` es el mismo hábito de validación en dos idiomas. |

<!-- C3 (Seguridad) y C5 (Observabilidad/eval) no aplican: ejercicio conceptual de placement de Fase 1. -->

## Errores típicos a marcar
- **Sobreconfianza:** marca casi todo "lo sé hacer sin notas" sin haber tocado
  `pytest`, generadores, `async` o TypeScript. La prueba es "¿ahora, sin notas?".
- **Bloques no alternados:** planea toda la pista Python y *después* toda la de TS
  —pierde el efecto del *interleaving* y deja TS enfriándose semanas.
- **Victoria-IA tardía o ausente:** no agenda la 1.10, o la deja para el final.
  Es la zanahoria de motivación; va temprano (tras 1.5), no de postre.
- **Horario-deseo:** "estudiar más", "cuando tenga tiempo" — sin bloques concretos.
- **Spacing falso:** repasar "releyendo notas" en vez de recuperar de memoria; o
  todo el repaso el mismo día (massing disfrazado).
- **Roles de lenguaje vagos o invertidos:** "los dos porque están de moda", o
  asignar Python al front y TS a la IA sin razón.
- **Saltar la base:** plan que arranca por "Python avanzado" (decoradores/`async`)
  antes de 1.1–1.2, ignorando la secuencia básico→intermedio→avanzado.
- (transversal spec-driven) No versiona estos archivos ni los trata como su primer
  documento de planificación de la fase.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- Plan con prosa pulida y vocabulario de *learning science* (encoding,
  interleaving, retrieval strength) que el alumno **no puede explicar** si se le
  pregunta — sofisticación impropia del nivel F1.0 sin defensa.
- Tabla de diagnóstico "perfecta" pero sin rastro de su historia personal: ningún
  matiz, ninguna fila ambigua, niveles idénticos a un patrón genérico.
- Texto de "por qué dos lenguajes" que repite el argumentario de la portada
  palabra por palabra, sin un caso propio.
- **Verificación sugerida:** pedir que clasifique en voz alta **un tema no listado**
  (p. ej. "list comprehensions con condición" o "narrowing de un union en TS") y
  justifique su punto de partida. Si interiorizó el método, lo hace en segundos; si
  dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca redactar el plan por el alumno. Ordenado de menos a más directo.

- **Pista (nivel 1):** "Mira tu plan: ¿en qué semana tocas TypeScript por primera
  vez? Si la respuesta es 'después de toda Python', algo se va a enfriar."
- **Pregunta socrática (nivel 2):** "¿Cuál es la prueba exacta para escribir 'lo sé
  hacer sin notas' en una fila? Aplícala a 1.6 (primer test con pytest): ¿la
  pasas?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu cadencia de repaso
  usa 'releer notas': ese es justo el hábito que el curso desmonta. Cámbialo por
  una acción de **recuperación** (reescribir de memoria, predecir la salida,
  enseñarlo) en cada hito. Y adelanta la 1.10: ponla en cuanto cierres 1.5, para
  que la motivación no dependa de llegar al final de la fase."

## Conexión con el proyecto / capstone
- Estos tres archivos son el primer documento de planificación de la fase y la
  antesala del **Capstone F1 — La misma app, dos lenguajes**: el orden de pistas
  que diseñes aquí y la disciplina de repaso son lo que sostendrá escribir la
  misma mini-API en Python y TypeScript sin apoyarte en la IA para pensar.
