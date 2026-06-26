---
ejercicio_id: fase-0/capstone-cli-sin-ia
fase: fase-0
sub_unidad: "0.P"
version: 1
---

# Rúbrica — Capstone Fase 0: CLI sin IA

> Rúbrica analítica para el **capstone integrador** de la Fase 0. No hay una única
> respuesta correcta: el alumno elige su propio problema y diseño. Lo que se evalúa
> es la **disciplina de ingeniería** (spec antes del código, ADR, errores honestos,
> Conventional Commits, demo que corre) y la **autonomía** (lo pensó sin delegar en
> una IA y puede defender cada decisión). Un CLI funcional sin spec/ADR/commits
> limpios **no** cumple el objetivo del capstone, aunque "funcione".
>
> Este capstone se mide contra el **Definition of Done único** (§B de
> `CURRICULUM-REVIEW.md`). En la Fase 0 aplican los puntos **1** (spec + ADR),
> **8** (demo + README + write-up) y **9** (Conventional Commits), más el **gate
> de la fase**: escrito 100% sin IA para razonar. El resto del DoD se *siembra*
> aquí y se *exige* en fases posteriores —no lo penalices si falta.

## Objetivos evaluados
> De `objetivos` en `ejercicio.yml`.

- **O1** — Diseñar una herramienta pequeña partiendo de una **mini-spec** (entradas/salidas/casos borde) escrita *antes* de codear, y justificar la decisión técnica principal en un **ADR**.
- **O2** — Implementar un CLI que parsee argumentos, ejecute comandos, valide entradas y devuelva **exit codes honestos** con mensajes a `stderr`, 100% sin IA para razonar.
- **O3** — Entregar al estándar mínimo del mercado: **demo que corre**, **README** usable, historial de **Conventional Commits** y un **write-up de trade-offs**.

## Criterios y niveles

### C1 — Diseño spec-first + ADR · mapea: O1 · DoD 1 · hilo: spec-driven
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay `SPEC.md`, o se escribió **después** del código (su commit es posterior a la primera función), o no hay ADR. La spec describe lo ya hecho en vez de diseñar lo que falta. |
| **en-progreso** | Hay spec, pero le faltan los casos borde (solo el "happy path"), o el ADR no justifica nada real ("elegí Python porque sí"). |
| **competente** | `SPEC.md` con entradas, salidas y **≥3 casos borde**, commiteada **antes** de la primera función; ADR con contexto / decisión / consecuencias sobre una decisión técnica real. |
| **excelente** | Además: cada caso borde de la spec tiene su rama/validación trazable en el código; el ADR nombra alternativas descartadas y el costo aceptado. La spec se lee como la lista de tests futura. |

### C2 — Corrección y robustez del CLI · mapea: O2 · DoD 8
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El CLI no corre, o solo el camino feliz; cualquier entrada inesperada lo hace explotar con un traceback crudo. |
| **en-progreso** | Corre el happy path y algún borde, pero falla en otros (no valida argumento faltante, o asume que un archivo/carpeta siempre existe). |
| **competente** | Hace lo que el README promete y maneja sus casos borde declarados: argumento faltante, entrada inválida y un caso "vacío" se atienden con mensajes claros, sin tracebacks. |
| **excelente** | Maneja bordes que el enunciado no pidió (datos corruptos, permisos, duplicados), y separa **decidir** de **actuar** (p. ej. un `--dry-run`/`simular` para operaciones destructivas). |

### C3 — Calidad de ingeniería y observabilidad-semilla · mapea: O2 · hilo: observabilidad
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Todo va a `stdout` (incluidos los errores); `exit` siempre 0 (o siempre 1); funciones gigantes que mezclan parseo, lógica y E/S. |
| **en-progreso** | Distingue éxito de error en el exit code, pero manda errores a `stdout`, o el código está poco descompuesto (una sola función hace todo). |
| **competente** | **stdout = dato útil, stderr = diagnósticos**; exit codes honestos (0 éxito, ≠0 error, con códigos distintos para "uso" vs "ejecución"); el código está partido en funciones con una responsabilidad cada una. |
| **excelente** | Los mensajes de error son accionables (dicen *qué* dato falló y *qué* hacer); los exit codes están documentados en la spec y son consistentes. Es la semilla honesta de la observabilidad de la Fase 5. |

### C4 — Entregables y comunicación · mapea: O3 · DoD 8 y 9
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin README usable, o sin demo, o el historial tiene `wip`/`arregla cosas`/un commit gigante "todo el CLI". No hay write-up de trade-offs. |
| **en-progreso** | README incompleto (falta cómo instalar o un ejemplo copiable), o demo sin pegar, o algunos commits no son Conventional Commits. |
| **competente** | README que un desconocido puede seguir (qué es, instalar, usar) con **demo pegada que corre**; historial 100% Conventional Commits (validados por el hook); write-up de 3–5 líneas con trade-offs. |
| **excelente** | El historial se lee como un resumen del proyecto (spec → ADR → feat pequeños → fix de bordes → docs); el write-up nombra un trade-off **defendible** (qué dejó fuera y por qué) y la demo es reproducible (asciinema/GIF o sesión exacta). |

### C5 — Autonomía y comprensión demostrada · gate F0 (sin IA) · señal anti-dependencia
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar partes de su propio código; la sofisticación no calza con el nivel F0 (estructura "de libro" indefendible). Indicios de diseño delegado a una IA. |
| **en-progreso** | Explica el qué pero no el porqué de sus decisiones; titubea al justificar un caso borde o el exit code elegido. |
| **competente** | Explica **cada línea y cada commit sin notas**; defiende por qué validó antes de actuar y por qué eligió su herramienta (su ADR). |
| **excelente** | Reflexiona sobre dónde sintió el impulso de pedirle a una IA y cómo lo resolvió solo; convierte una dificultad en una regla reutilizable para el próximo proyecto. |

## Errores típicos a marcar
- **Spec escrita después del código** (misma fecha/commit que la última función): se saltó el ejercicio; la spec documenta, no diseña.
- **Proyecto demasiado ambicioso a medias**: un "framework" de 2000 líneas que no corre vale menos que un CLI de 80 que sí. Premiar lo terminado.
- **Errores a `stdout` y exit siempre 0**: rompe la composición con pipes y miente sobre qué pasó. Es el antipatrón de observabilidad más común aquí.
- **`commit` gigante único** ("feat: todo el CLI"): impide leer la historia y delata que no se construyó por pasos.
- **README que asume contexto**: "corre el script" sin decir cómo instalar ni un ejemplo. Si un desconocido no puede usarlo, no cumple DoD 8.
- **Confundir "100% sin IA" con "sin autocompletado"**: lo prohibido es delegar el *pensamiento* (diseño/estructura/lógica), no usar `man`, docs oficiales o autocompletado básico.
- **`argparse` "decorativo"**: define sub-comandos pero no valida nada y deja que la primera excepción reviente en crudo.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación. Nunca dar la solución.
- Código con un estilo o patrones (typing avanzado, abstracciones "limpias") **muy por encima** del nivel F0 que el alumno no puede explicar línea a línea.
- `SPEC.md`/`ADR` con prosa pulida pero **desconectada** del código real (la spec menciona casos borde que el código no atiende, o al revés).
- Historial con **un solo commit grande** o mensajes genéricos: señal de que pegó un resultado completo en vez de construirlo por pasos.
- Explicación del "porqué" de una decisión que repite frases de manual sin aterrizarlas en *su* problema concreto.
- **Verificación sugerida:** pídele que agregue **en vivo** un caso borde nuevo que no estaba en la spec (con su commit `feat:`/`fix:`) y que explique dónde va la rama y por qué ese exit code. Si lo construyó de verdad, lo hace en minutos; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca entregar diseño ni código de la solución de referencia. El alumno eligió su propio problema: el feedback se ancla en *su* spec.
- **Pista (nivel 1):** "Mira las fechas de tus commits: ¿tu `SPEC.md` llegó antes o después de tu primera función? Eso te dice si la spec **guió** el diseño o solo lo describió."
- **Pregunta socrática (nivel 2):** "Toma un caso borde de tu spec (p. ej. el argumento faltante). Sígueme el camino en tu código: ¿en qué línea se atiende?, ¿a qué flujo va el mensaje?, ¿con qué exit code termina? Si alguno no tiene respuesta, ahí está el hueco."
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón a aplicar es **separar decidir de actuar y validar antes de tocar nada**: primero valida la entrada y devuelve un exit code honesto (2 para uso, ≠0 para error), recién después ejecuta. Reescribe ese comando con esa forma y vuelve a correr tu demo antes de seguir."

## Conexión con el proyecto / capstone
- Este **es** el capstone de la Fase 0: cierra el constructive alignment de toda la fase (spec-first de `0.8`, descomposición de `0.2`, trazado de `0.3`, funciones/validación de `0.7`, terminal/exit codes de `0.5`, Git/Conventional Commits de `0.6`). El hábito **spec + ADR + Conventional Commits** que se mide aquí es el punto 1 y 9 del DoD de **todos** los capstones del curso, hasta la plataforma RAG (F6) y la automatización agéntica (F7).
