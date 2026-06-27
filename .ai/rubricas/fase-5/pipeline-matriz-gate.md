---
ejercicio_id: fase-5/pipeline-matriz-gate
fase: fase-5
sub_unidad: "5.3"
version: 1
---

# Rúbrica — Diseña el pipeline completo: matriz, caché, gate y trade-offs

> Rúbrica **analítica** atada a los `objetivos` del contrato. El test estructural (`test_workflow.py`) da la señal objetiva del YAML; **el write-up es el corazón de este ejercicio** y se corrige por la calidad del razonamiento, no por una respuesta única.

## Objetivos evaluados

- O1: Configurar un pipeline con matriz, caché y jobs encadenados con `needs` (test → build → deploy).
- O2: Gatear el deploy por rama (`if`) y por `environment: production` con su secret; distinguir secret de repo de secret de environment.
- O3: Explicar por qué el workflow no bloquea un merge (lo hace la branch protection) y razonar el trade-off costo/latencia de la matriz.

## Criterios y niveles

### C1 — Corrección del workflow (¿hace lo que el objetivo pide?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_workflow.py` falla en varios asserts: falta algún job, la matriz no tiene las 3 versiones, o no hay `needs`. |
| **en-progreso** | Pasa parcialmente: matriz correcta pero sin caché, o `build`/`deploy` sin `needs`, o `deploy` sin `if:`/sin `environment`. |
| **competente** | `test_workflow.py` verde: matriz de 3, caché, `needs` correctos, deploy gated (`if:` de rama + `environment: production`), secret por referencia. |
| **excelente** | Lo anterior + `fail-fast: false` en la matriz (ver todos los rojos), `permissions` mínimos, `concurrency`, nombres de job/step claros en inglés. |

### C2 — Seguridad (OWASP / supply chain) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Secret en texto plano en el YAML, o actions a `@main`. |
| **en-progreso** | Referencia el secret pero el deploy no está realmente gated (corre en PRs), o falta `environment`. |
| **competente** | Secret vía `${{ secrets.DEPLOY_TOKEN }}`, deploy solo en push a main, `environment: production` como puerta. |
| **excelente** | Explica que el `environment` permite reglas de protección (aprobación manual, secrets propios) y que el deploy desde un PR de fork sería un riesgo; conecta con 5.4. |

### C3 — Comprensión del modelo de gate (write-up c) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Cree que el `if:` o el workflow bloquea el merge. No menciona branch protection. |
| **en-progreso** | Intuye que "hay algo más" pero no lo nombra con precisión. |
| **competente** | Nombra **branch protection / ruleset con required status checks** como el mecanismo que bloquea el merge, y dice que vive en la config del repo, no en el YAML. |
| **excelente** | Articula el modelo "workflow reporta / branch protection bloquea" con una analogía propia y entiende que sin el check requerido el pipeline es decorativo. |

### C4 — Razonamiento de trade-offs (write-up a, b, d) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Respuestas vacías o circulares ("uso matriz porque es mejor"). No distingue `needs` de `if`. |
| **en-progreso** | Distingue `needs`/`if` pero la respuesta de la matriz es "más versiones = más seguro" sin pesar el costo. |
| **competente** | (a) `needs` = orden, `if` = condición, ortogonales. (b) secret de repo vs de environment con un caso de uso. (d) matriz justificada por riesgo real (librería pública) vs desperdicio (servicio interno en un solo runtime). |
| **excelente** | Cuantifica el costo (3× minutos), da ejemplos concretos propios, y conecta con costos cloud (5.8). Defiende cuándo NO usar matriz. |

## Errores típicos a marcar

- Confundir `needs` (ejecución) con `if` (condición): creer que son redundantes.
- Creer que el `if:` del deploy "protege main" — es la misconception central; el gate es la branch protection.
- Secret en texto plano, o referenciarlo mal (`$secrets.X`, `${secrets.X}` en vez de `${{ secrets.X }}`).
- Matriz justificada por reflejo ("más es mejor") sin pesar el costo de minutos.
- Confundir caché (entradas, best-effort) con artefacto (salidas, conservar) en el write-up.
- `deploy` que corre en PRs (sin `if:` de rama) → un PR de fork podría deployar a prod.
- (transversal) No mencionar `permissions` mínimos ni el pin de actions cuando se pregunta por seguridad.

## Señales de dependencia-IA

- YAML impecable pero write-up vago o contradictorio: señal de que generó el workflow y no razonó.
- Write-up que usa términos correctos (OIDC, reusable workflows) sin que el YAML los use y sin poder defenderlos.
- Respuesta a (c) "el if/needs bloquea el merge" con seguridad, pese a tener el YAML perfecto: copió, no entendió.
- Las cuatro respuestas del write-up suenan a documentación parafraseada, sin un ejemplo concreto propio.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `pytest test_workflow.py` y atiende el primer assert que falla. Para el write-up, relee tu (c): ¿de verdad el `if:` impide que alguien apriete 'Merge'?"
- **Pregunta socrática (nivel 2):** "Si quito la matriz y dejo solo Python 3.13, ¿qué riesgo concreto dejo de cubrir? ¿Ese riesgo existe en tu caso?" / "Tu CI muestra rojo en un PR. Físicamente, ¿qué impide hoy que el botón verde de merge se pueda apretar?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El gate de merge es la branch protection / ruleset con required status checks (Settings → Rules), no el YAML. Y la matriz se justifica por riesgo (librería pública multi-versión), no por reflejo. Reescribe (c) y (d) con eso y un ejemplo propio; revisa la sección 4.6 y 5 de la lección."

## Conexión con el proyecto / capstone

- Este es el pipeline del Capstone F5 en miniatura: matriz/caché/gate/deploy gated son justo lo que el capstone exige, y el write-up (c) evita arrastrar al capstone la creencia de que el workflow basta para proteger `main`.
</content>
