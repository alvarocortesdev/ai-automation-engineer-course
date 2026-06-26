---
ejercicio_id: fase-2/flujo-pr-commits-code-review
fase: fase-2
sub_unidad: "2.13"
version: 1
---

# Rúbrica — Reescribe el historial: Conventional Commits + PR + code review

> Rúbrica **analítica** atada a los `objetivos`. Se evalúa **comunicación de ingeniería**: commits con
> tipo correcto (y el breaking bien marcado), una descripción de PR que comunica el *por qué*, y un code
> review que **comenta el código, no a la persona**, etiqueta intención, separa lo bloqueante de la
> preferencia, y **caza el bug plantado**. No hay redacción "única" correcta; hay decisiones mejor y peor
> fundadas.

## Objetivos evaluados
- **O1** — Conventional Commits válidos (tipo/scope/imperativo) + identificar el `BREAKING CHANGE`.
- **O2** — Descripción de PR que comunica **por qué** y **cómo probarlo**, no solo el qué.
- **O3** — Code review que comenta el código (no a la persona), **etiqueta** intención, separa bloqueante de preferencia, e **identifica el bug** del diff.

## Criterios y niveles

### C1 — Conventional Commits + breaking change · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Mantiene mensajes vagos, o pone el mismo tipo a todo (`feat:` para todo), o no usa el formato `tipo: desc`. |
| **en-progreso** | Formato correcto en la mayoría pero **se le escapa el breaking change** (commit 4 como `feat`/`fix` sin `!`/`BREAKING CHANGE`), o descripciones en pasado/gerundio ("añadí"/"añadiendo"). |
| **competente** | Los 5 con tipo válido y descripción en imperativo: `feat` (1), `fix` (2), `test` (3), el `feat!`/`fix!` con `BREAKING CHANGE` (4), `chore`/`build` (5). |
| **excelente** | Además nota que el commit 5 mezcla dos cosas (deps + lint) y propone partirlo; usa scope (`feat(descuentos):`); footer `Closes #42` donde corresponde. |

### C2 — Descripción del PR · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin descripción, o repite el título; no dice cómo probar ni por qué. |
| **en-progreso** | Dice el **qué** pero no el **por qué**, o falta "cómo probarlo", o no enlaza el issue. |
| **competente** | Secciones Qué / Por qué / Cómo probarlo / Trade-offs; enlaza `Closes #42`; el revisor podría empezar sin preguntar nada. |
| **excelente** | El "por qué" es concreto (problema de negocio/usuario), el "cómo probarlo" es ejecutable, y los trade-offs nombran una decisión real (p. ej. cupón inválido → error). |

### C3 — Calidad del code review · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "lgtm 👍", o comentarios que atacan a la persona ("no pensaste"), o no encuentra el bug. |
| **en-progreso** | Encuentra algún problema pero sin etiquetar intención ni distinguir bloqueante de nit; o caza el bug pero sin `praise`; o solo nitpickea estilo. |
| **competente** | 3-4 comentarios **etiquetados** (`praise`/`issue`/`suggestion`/`question`); **identifica el bug del porcentaje** como `issue` bloqueante; comenta el código, no a la persona; hay un `praise` concreto. |
| **excelente** | Además nota que el test `test_cupones_validos` **fallaría** con el código actual (el `9000` esperado no cuadra), propone el fix conceptual sin imponerlo, y plantea la pregunta de diseño (total negativo / clamp a 0) como `suggestion`/`question`. |

## Errores típicos a marcar
- **Breaking change sin marcar** (commit 4): cambiar el comportamiento público (ignorar → lanzar `ValueError`) sin `!`/`BREAKING CHANGE` es el error más caro del ejercicio.
- **Descripciones en pasado/gerundio**: Conventional Commits van en **imperativo** ("añade", no "añadí"/"añadiendo").
- **PR que dice el qué pero no el por qué**: el diff ya muestra el qué; la descripción existe para el por qué y el cómo probar.
- **Review tóxico o vacío**: "no pensaste en X" (ataca a la persona) y "lgtm" (no revisó) son los dos extremos malos.
- **No etiquetar intención**: mezclar un bug bloqueante con un nit de estilo sin distinguirlos le quita al autor la señal de qué *debe* arreglar.
- **No encontrar el bug**: `descuento = subtotal * pct` (sin `/100`) hace que `BIENVENIDO10` reste 10× el subtotal → total negativo. Es el `issue` bloqueante central.
- **Olvidar el `praise`**: el test parametrizado de cupones válidos + el `ValueError` claro del cupón inválido son lo bien hecho; señalarlo enseña al equipo.
- (transversal testing) no notar que el test **codifica el comportamiento correcto** (`9000`) y por tanto **estaría rojo** con el código del diff: la suite ya delata el bug.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Review pulidísimo con jerga de Conventional Comments pero que **no detecta el bug del porcentaje**: copió la forma, no leyó el código.
- Commits "perfectos" pero el alumno no sabe defender por qué el 4 es breaking y el 2 no.
- PR description genérica de plantilla ("This PR adds…") sin nada específico del cupón.
- **Verificación sugerida:** pedir que **traduzca a mano** `aplicar_cupon(10000, "BIENVENIDO10")` con el código del diff (da `10000 - 100000 = -90000`); si no lo hace o no ve el problema, no revisó de verdad. Pedir que explique por qué el commit 4 rompe a quien dependía del comportamiento viejo.

## Feedback sugerido (graduado)
> Nunca dar el artefacto de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Traduce a mano `aplicar_cupon(10000, 'BIENVENIDO10')` con el código tal cual. ¿El número que sale tiene sentido como total? Y mira el `9000` que espera el test."
- **Pregunta socrática (nivel 2):** "El commit 4 cambia qué pasa con un cupón inexistente. Si yo tenía código que dependía de que se ignorara, ¿mi código sigue funcionando tras tu cambio? ¿Cómo se llama ese tipo de cambio?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Marca el commit 4 como breaking (`feat!`/`fix!` + `BREAKING CHANGE`). En el review, el bug del porcentaje es un `issue` bloqueante (falta `/100`); etiqueta cada comentario por intención y añade un `praise` por el test parametrizado. Repasa las secciones 4.4–4.6 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- El **[Capstone F2](/fase-2-ingenieria/proyecto/)** exige Conventional Commits en todo el historial y que el trabajo entre por PRs revisables. Este ejercicio entrena las tres mitades de eso: commits legibles, descripción que respeta al revisor, y review que mejora sin lastimar — el hábito de colaboración que escala a todas las fases.
