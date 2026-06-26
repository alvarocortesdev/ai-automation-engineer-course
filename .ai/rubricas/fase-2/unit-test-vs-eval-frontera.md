---
ejercicio_id: fase-2/unit-test-vs-eval-frontera
fase: fase-2
sub_unidad: "2.11"
version: 1
---

# Rúbrica — La frontera: unit test, eval o ninguno

> Rúbrica **analítica** atada a los `objetivos`. El ejercicio no se ejecuta: se
> evalúa el **razonamiento**. La señal central es si el alumno traza bien la línea
> "¿mi código…?" (unit test) vs. "¿el modelo…?" (eval), y si reconoce lo que no se
> debe afirmar de un sistema no determinista.

## Objetivos evaluados
- **O1** — Clasificar cada afirmación (unit test / eval / ninguno) con justificación correcta.
- **O2** — Entender que la calidad del modelo es un eval y que no se afirma igualdad exacta de salidas no deterministas.
- **O3** — Diseñar la frontera: qué se inyecta/mockea, qué corre real, cómo se ve el eval.

## Criterios y niveles

### C1 — Clasificación correcta de las 8 afirmaciones · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan veredictos, o clasifica como "eval" cosas que son del propio código (p. ej. el truncado o el parseo), o como "unit test" la corrección de categoría del modelo. |
| **en-progreso** | Acierta los unit tests obvios (1, 2, 6) pero confunde el reintento (3) o no distingue eval (4, 5) de seguridad (8), o trata la 7 como test válido. |
| **competente** | 1/2/3/6 = unit test; 4/5 = eval; 7 = ninguno; 8 = eval de seguridad. Cada veredicto con justificación de una frase coherente. |
| **excelente** | Además matiza ramas vecinas (p. ej. la 3 son dos unit tests: "reintenta una vez" y "tras dos fallos lanza"), y nombra la métrica del eval (accuracy/F1 para 4, faithfulness/LLM-as-judge para 5). |

### C2 — Razonamiento sobre la frontera (Sección 2) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No define qué se mockea, o propone mockear `json.loads`/la validación/el truncado (sobre-mockeo), o llamaría al modelo real en los unit tests. |
| **en-progreso** | Dice que mockea `generar` pero no especifica el tipo de doble ni qué queda real, o no esboza el eval. |
| **competente** | Inyecta `generar` y lo mockea (stub para respuestas fijas; spy para afirmar el prompt y contar reintentos); deja `json.loads`, validación, truncado y bucle de reintento **reales**; esboza un eval (dataset etiquetado → métrica → gate, no en cada commit). |
| **excelente** | Además justifica por qué el eval no va en CI (costo/latencia/no-determinismo) y conecta con Fase 6 (ragas / LLM-as-judge / promptfoo como gate). |

### C3 — Comprensión conceptual demostrada · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue "mi pegamento" de "el modelo"; cree que mockear el LLM permite verificar su corrección. |
| **competente** | Articula que el assert prueba el código que rodea al modelo, y que la calidad del modelo se mide con un eval. |
| **excelente** | Explica por qué afirmar igualdad exacta de una salida no determinista (afirmación 7) es un test inútil y flaky por diseño, y por qué la 8 necesita muestreo repetido (un solo intento no prueba robustez). |

## Errores típicos a marcar
- Clasificar el **truncado (6)** o el **parseo (2)** como eval: son código determinista del alumno → unit test.
- Clasificar la **corrección de categoría (4)** como unit test "mockeando el modelo": el mock devuelve la categoría que el alumno escribió, no prueba que el modelo acierte.
- Tratar la **afirmación 7** como un test válido: pedir igualdad exacta de una salida no determinista es flaky por diseño; no se afirma.
- Reducir la **afirmación 8** a un solo assert: la robustez frente a prompt injection se evalúa con muestreo repetido / red-team (OWASP LLM), no con un caso.
- En la frontera: proponer **mockear de más** (parser, validación, truncado) o **llamar al modelo real** en los unit tests.
- (transversal) no notar que el eval cuesta tokens y por eso corre como gate ocasional, no en cada commit.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Veredictos correctos pero justificaciones genéricas que no mencionan el *porqué* específico (p. ej. "es un eval" sin decir qué se mide).
- Clasifica la 7 y la 8 "de libro" pero no puede explicar el muestreo repetido ni el no-determinismo si se le pregunta.
- **Verificación sugerida:** pedir que invente dos afirmaciones nuevas para esta misma feature —una unit test y una eval— y las justifique; y que explique por qué la 4 no se puede convertir en unit test mockeando el modelo.

## Feedback sugerido (graduado)
> Nunca dar la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Lee cada afirmación: ¿empieza con '¿mi código…?' o con '¿el modelo…?'. Eso casi siempre decide unit test vs. eval. ¿Dónde caen el truncado (6) y la categoría correcta (4)?"
- **Pregunta socrática (nivel 2):** "Si mockeas el modelo para que devuelva 'facturación', ¿tu assert prueba que el modelo clasifica bien, o que tu código propaga lo que tú escribiste? ¿Qué tipo de prueba mide lo primero?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "1/2/3/6 son unit tests (tu pegamento, con fake). 4/5 son evals (dataset + métrica). 7 no se testea (no determinismo). 8 es un eval de seguridad con muestreo. En la frontera, mockea solo `generar`; deja parseo/validación/truncado/reintento reales. Repasa la tabla 6.3 de la lección antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Fija el criterio que usarás en el **Capstone F2** y en toda la **Fase 6**: qué entra en la suite unitaria (determinista, gratis, en cada commit) y qué se reserva para el eval harness (caro, ocasional, como gate). Sin esta línea clara, los proyectos de IA terminan con tests que parecen probar la IA y no prueban nada.
