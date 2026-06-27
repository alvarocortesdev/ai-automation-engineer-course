---
ejercicio_id: fase-5/primer-pipeline-ci
fase: fase-5
sub_unidad: "5.3"
version: 1
---

# Rúbrica — Tu primer pipeline: lint → test en cada PR

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. El test estructural (`test_workflow.py`) da una señal objetiva; la comprensión se mide en cómo el alumno **explica** el workflow.

## Objetivos evaluados

- O1: Implementar un workflow que se dispare en `push` a `main` y en `pull_request`, con `permissions: contents: read`.
- O2: Ordenar los steps del job de CI (checkout → setup-uv → `uv sync --frozen` → ruff → pytest) y justificar por qué el `checkout` va primero.
- O3: Pinear las actions a un tag de versión (nunca `@main`) y explicar qué se necesita **además** del workflow (branch protection) para bloquear un merge con CI en rojo.

## Criterios y niveles

### C1 — Corrección del workflow (¿hace lo que el objetivo pide?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_workflow.py` no pasa; falta el bloque `on:`, el job `test`, o el `checkout`. El YAML no parsea o no tiene jobs. |
| **en-progreso** | Pasa parcialmente: corre los tests pero el orden de steps está mal (p. ej. `checkout` no es el primero), o falta uno de los triggers (solo `push` o solo `pull_request`), o falta `uv sync --frozen`. |
| **competente** | `test_workflow.py` verde: dos triggers correctos, `permissions: contents: read`, job `test` en `ubuntu-latest`, steps en el orden correcto, actions pineadas a versión. |
| **excelente** | Lo anterior + detalles de iniciativa: `concurrency` con `cancel-in-progress`, nombres de step descriptivos, o un comentario que explica una decisión. Sabe que la matriz/caché vendrían después y no las mete porque sí. |

### C2 — Seguridad y reproducibilidad (hilo transversal) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Action pineada a `@main`/`@latest`; sin bloque `permissions` (token con permisos por defecto amplios); instala deps sin `--frozen`. |
| **en-progreso** | Pinea a versión pero olvida `permissions`, o usa `uv sync` sin `--frozen` (no reproducible). |
| **competente** | Actions pineadas a tag, `permissions: contents: read`, `uv sync --frozen` (instala exactamente el lockfile). |
| **excelente** | Menciona (o aplica) el pin a commit SHA como paso siguiente, y/o explica por qué el mínimo privilegio importa aunque "sea solo CI". Conecta con 5.4. |

### C3 — Comprensión demostrada (el alumno explica, no solo copia) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar por qué el `checkout` va primero ni qué hace `--frozen`. Cree que el `if:`/el workflow bloquea el merge. |
| **en-progreso** | Explica el orden de steps pero no distingue "el workflow reporta" de "la branch protection bloquea". |
| **competente** | Explica cada step y su orden; nombra que para bloquear un merge rojo hace falta **branch protection / required status check**, fuera del YAML. |
| **excelente** | Articula el modelo completo (workflow = examen, branch protection = reglamento) y razona el costo de los minutos de CI / por qué `concurrency` ahorra plata. |

## Errores típicos a marcar

- `checkout` no es el primer step → el runner está vacío, todo lo demás falla con "no such file".
- Olvidar `uv sync --frozen` (o usarlo sin `--frozen`): el pipeline "funciona" pero no es reproducible.
- Pinear una action a `@main` o `@latest` (riesgo de supply chain).
- Secret/valor sensible en texto plano (aunque este ejercicio no tiene deploy, marcarlo si aparece).
- Creer que el workflow, el `if:` o el `needs:` bloquea el merge: lo bloquea la branch protection.
- Olvidar uno de los dos triggers (solo `push` deja los PRs sin check; solo `pull_request` deja `main` sin verificación tras el merge).
- (transversal) Meter matriz/caché/artefactos "porque sí" en el pipeline más simple: complejidad sin riesgo que la justifique.

## Señales de dependencia-IA

- Un YAML perfecto y "sobre-ingenierizado" (matriz, varios OS, caché manual, `workflow_dispatch`) que el alumno no puede explicar paso a paso → copiado, no entendido.
- Explica el workflow con vocabulario que no aparece en la lección y no sabe defenderlo (p. ej. `reusable workflows`, `composite actions`) sin poder decir qué problema resuelven.
- Dice "el pipeline bloquea el merge" con seguridad: señal de que reprodujo un tutorial sin internalizar el modelo (es justo la misconception central de la lección).

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `pytest test_workflow.py` y lee el primer assert que falla: te nombra exactamente qué propiedad del YAML no se cumple."
- **Pregunta socrática (nivel 2):** "Si borraras el step de `checkout`, ¿qué tendría el runner cuando intente correr `pytest`? ¿Por qué eso fija el orden?" / "Tu `ci.yml` muestra rojo en un PR malo — ¿qué impide, hoy, que un compañero igual lo mergee?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El orden correcto es checkout → setup → sync --frozen → lint → test, y el gate de merge no vive en el YAML sino en Settings → Rules (required status checks). Revisa la sección 4.6 de la lección y ajusta tu explicación, no solo el archivo."

## Conexión con el proyecto / capstone

- Este `ci.yml` es el esqueleto literal del pipeline del Capstone F5; sobre él se montan los gates de seguridad (5.4), el build de la imagen (5.1) y el deploy (5.9). Entender el orden y el modelo de gate aquí evita arrastrar la misconception al capstone.
</content>
