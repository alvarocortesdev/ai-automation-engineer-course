---
ejercicio_id: fase-0/disena-tu-sistema-de-estudio
fase: fase-0
sub_unidad: "0.1"
version: 1
---

# Rúbrica — Diseña tu sistema de estudio

> Rúbrica **analítica** para un ejercicio de **diseño/razonamiento** (sin tests).
> Lo que se evalúa es la **coherencia y la justificación** del sistema que el
> alumno diseñó, no que coincida con una "respuesta correcta". Dos alumnos pueden
> tener horarios y clasificaciones distintos y ambos estar `excelente` si cada
> decisión está bien fundada. El corrector busca **entendimiento del método**, no
> conformidad con una plantilla.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Aplicar el Primero-Sin-IA **escalado por novedad**: clasificar tareas y
  justificar el punto de partida (worked example vs. intento solo).
- **O2** — Diseñar un sistema con **active recall + spaced repetition** como
  ritual, con drill diario y bloques fijos.
- **O3** — Explicar por qué depender de la IA para *pensar* atrofia la autonomía
  y distinguir usar IA para aprender vs. para evitarlo.

## Criterios y niveles

### C1 — Clasificación por novedad con justificación · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay tabla, o clasifica sin justificar, o copia las etiquetas del enunciado sin razonar. |
| **en-progreso** | Clasifica las 6 tareas pero las justificaciones son genéricas ("porque sí", "es fácil") o confunde la primera acción con la etiqueta (marca `nuevo` y luego "Primero-Sin-IA de entrada"). |
| **competente** | Las 6 tareas clasificadas **coherentemente con su experiencia**; primera acción correcta para cada etiqueta; al menos una `nuevo` y una `repaso`; justificación de 1 línea defendible. |
| **excelente** | Además explicita el criterio rector ("¿la he hecho antes con éxito?") y reconoce que la etiqueta depende de _su_ historia, no de la tarea en abstracto; señala algún caso ambiguo y lo razona. |

### C2 — Diseño del sistema: active recall + spacing + ritual · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin horario, o "cuando pueda"; sin drill diario; sin cadencia de repaso. |
| **en-progreso** | Tiene bloques pero vagos; incluye spacing _o_ recall pero no ambos; el drill es decorativo (no dice qué/cuándo/cómo se registra). |
| **competente** | Bloques **concretos** (día+hora+duración); drill diario definido (qué/cuándo/registro); cadencia de spaced repetition con al menos 3 hitos (p. ej. +1/+3/+7) basada en **recuperación de memoria**, no en relectura. |
| **excelente** | El sistema es **ejecutable y realista** para su disponibilidad (10–15 h/sem), prefiere sesiones distribuidas sobre maratones, y el repaso es recall activo explícito (reescribir/enseñar/predecir), no "releer". |

### C4 — Comprensión demostrada (el write-up calza con el método) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay sección de protocolo con sus palabras, o repite los 4 pasos textuales sin entenderlos (orden equivocado, IA antes del intento). |
| **en-progreso** | Reproduce los pasos pero no puede explicar _por qué_ la IA va al final, o confunde "no usar IA" con "no necesitarla para pensar". |
| **competente** | Explica con sus palabras por qué el intento propio va primero y la IA al final (para revisar/explicar), y por qué releer es ilusión de fluidez frente al recall. |
| **excelente** | Da un ejemplo propio y concreto de cuándo usó la IA para *evitar* pensar y qué hará distinto; distingue con nitidez aprender-con-IA de evitar-aprender. |

<!-- C3 (Seguridad) y C5 (Observabilidad/eval) no aplican: ejercicio conceptual de Fase 0. -->

## Errores típicos a marcar
- **Confundir etiqueta con acción:** marca una tarea como `repaso` pero pone
  "worked example primero" (o al revés). La etiqueta determina la primera acción.
- **Clasificar la tarea en abstracto**, no "para mí": dice que `git rebase` es
  `nuevo` "porque es difícil" en vez de "porque yo nunca lo he hecho".
- **Horario-deseo:** "estudiar más", "cuando tenga tiempo" — sin bloques concretos.
- **Spacing ausente o falso:** repasar "releyendo notas" en vez de recuperar de
  memoria; o todo el repaso el mismo día (massing disfrazado).
- **Drill decorativo:** menciona el drill diario pero no dice qué, cuándo, ni
  cómo lo registra.
- **Malentender la regla:** escribe "no usar IA" en vez de "no necesitarla para
  pensar"; o pone la IA antes del intento propio.
- (transversal spec-driven) No versiona `metodo.md` ni usa el commit pedido;
  trata el documento como descartable y no como su primer spec.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- `metodo.md` con prosa pulida y vocabulario de _learning science_ (encoding,
  interleaving, retrieval strength) que el alumno **no puede explicar** si se le
  pregunta — sofisticación impropia del nivel F0.1 sin defensa.
- Tabla de novedad "perfecta" pero idéntica a la del enunciado/lección, sin
  rastro de la historia personal del alumno (no hay ambigüedad, no hay un "esto
  para mí es repaso porque…").
- Reflexión genérica que no nombra una situación real y concreta.
- **Verificación sugerida:** pedir que clasifique en voz alta **una tarea nueva
  no listada** (p. ej. "configurar un webhook") y justifique el punto de partida.
  Si interiorizó el método, lo hace en segundos; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca redactar el método por el alumno. Ordenado de menos a más directo.

- **Pista (nivel 1):** "Mira tu tabla: en al menos una fila, la etiqueta y la
  primera acción no concuerdan. ¿Cuál manda sobre cuál?"
- **Pregunta socrática (nivel 2):** "Para clasificar `git rebase`, ¿qué pregunta
  exacta te tienes que hacer? ¿La respuesta depende de la tarea o de _tu_
  historia con ella?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu cadencia de
  repaso usa 'releer notas': ese es justo el hábito que la lección desmonta.
  Cámbialo por una acción de **recuperación** (reescribir de memoria, predecir,
  enseñarlo) en cada hito, y explica en una línea por qué recuperar le gana a
  reconocer."

## Conexión con el proyecto / capstone
- Este `metodo.md` es la infraestructura del **Capstone F0 — CLI sin IA** y el
  primer documento-spec del alumno: el hábito de _planear antes de codear_ y de
  _repasar con recall_ es lo que sostendrá la disciplina de escribir esa CLI sin
  apoyarse en la IA.
