---
ejercicio_id: fase-6/eval-harness-a-mano
fase: fase-6
sub_unidad: "6.9"
version: 1
---

# Rúbrica — Un eval harness con gate de regresión, a mano

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo central no es "pasan los
> tests", es que el alumno **entienda las 4 piezas de un eval harness** (dataset → scorer →
> agregación → gate) y la diferencia precision/recall, más por qué el **gate de regresión**
> bloquea aunque el umbral absoluto esté ok. Un harness que pasa los tests pero confunde el
> denominador de precision con el de recall, o que no atrapa la regresión, no demuestra el
> objetivo.

## Objetivos evaluados
- **O1** — Implementar precision@k y recall@k a mano (deterministas, teoría de conjuntos).
- **O2** — Construir el harness: dataset → scorer → agregación → guardar casos malos.
- **O3** — Gate de regresión: umbral absoluto **y** regresión vs baseline + tolerancia.
- **O4** — Explicar qué métricas son deterministas y cuál (faithfulness) necesita un juez.

## Criterios y niveles

### C1 — Corrección de las métricas (¿hace lo que el objetivo pide?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `precision_recall_at_k` no corre, o devuelve lo mismo para precision y recall (confunde los denominadores). |
| **en-progreso** | Una de las dos métricas correcta; falla el truncado a `k` o el caso `relevantes` vacío. |
| **competente** | precision = hits/k, recall = hits/len(relevantes), trunca a `recuperados[:k]`, y recall=1.0 con `relevantes` vacío. Tests verdes. |
| **excelente** | Maneja además bordes por iniciativa (k mayor que la lista recuperada) y agregó un test propio que los ejercita. |

### C2 — Harness y gate (calidad de ingeniería) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `correr_eval` no agrega bien, o el gate solo chequea el umbral y **no** la regresión. |
| **en-progreso** | Agrega medias pero `fallos` está vacío/mal poblado, o el gate confunde umbral con regresión (off-by una comparación). |
| **competente** | Medias correctas; `fallos` guarda exactamente los casos con recall < 1.0; el gate bloquea por umbral **y** por `baseline - tolerancia`. |
| **excelente** | El `razon` del gate es legible para logging (distingue "umbral" de "regresión"); explica por qué existe la tolerancia. |

### C3 — Comprensión demostrada (write-up calza con el código) · mapea: O1, O3, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`, o las predicciones se escribieron después de ejecutar (calzan perfecto, sin conteo de conjuntos visible). |
| **en-progreso** | `verificacion.md` no distingue lo determinista de lo que necesita juez, o no explica precision vs recall. |
| **competente** | `prediccion.md` muestra los conjuntos contados a mano; `verificacion.md` dice que recall/precision son set math (sin LLM) y faithfulness necesita un juez. |
| **excelente** | Explica el árbol de diagnóstico (recall alto + faithfulness bajo → arreglar generación, no retrieval) y por qué el gate de regresión atrapa lo que el umbral deja pasar. |

## Errores típicos a marcar
- **Confundir los denominadores** — usar `/k` para recall o `/len(relevantes)` para precision. Es EL error conceptual del ejercicio.
- **No truncar a `k`** — contar hits sobre toda la lista recuperada en vez de `recuperados[:k]`; precision y recall salen inflados.
- **Gate sin chequeo de regresión** — solo comparar contra el umbral absoluto; deja pasar una versión que empeoró respecto a prod (el test `test_gate_bloquea_por_regresion...` lo fija).
- **`fallos` mal definido** — guardar todos los casos, o ninguno, en vez de los de recall < 1.0; o solo guardar el promedio y perder la lista de casos malos.
- **Dividir por cero** — `relevantes` vacío sin la convención recall=1.0, o `k=0`.
- (transversales) reporta solo el número agregado sin los casos malos; persigue "que pase el test" sin entender qué mide; trata el LLM-as-judge como objetivo sin nombrar sesgos.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Implementación impecable con type hints pulidos pero un `verificacion.md` que no sabe explicar **por qué** recall necesita el total de relevantes en el denominador y precision no.
- `prediccion.md` con los resultados correctos pero sin los conjuntos contados, o usando vocabulario ("nDCG", "MRR") por encima del nivel sin poder defenderlo.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué pasa con `k=2` sobre `["c1","c2","c3"]` y `relevantes={"c3"}`. Si entendió el truncado, responde precision=0, recall=0 y explica que c3 quedó fuera del top-k; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Precision y recall comparten el numerador (hits) pero NO el denominador. ¿Cuál divide por `k` y cuál por el total de relevantes? ¿Qué castiga cada uno?"
- **Pregunta socrática (nivel 2):** "Tu gate deja pasar un recall de 0.86 cuando la versión en prod tenía 0.90. ¿Eso es una mejora o una regresión? ¿Qué chequeo te falta además del umbral?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Trunca con `recuperados[:k]`, cuenta `hits` con intersección de conjuntos, `precision = hits/k`, `recall = hits/len(relevantes)` (1.0 si vacío). En el gate: primero `if score < umbral`, luego `if baseline is not None and score < baseline - tolerancia`. Guarda en `fallos` los casos con recall < 1.0."

## Conexión con el proyecto / capstone
- Este harness —métricas de retrieval + gate de regresión— es el entregable "eval harness versionado + número + gate de regresión" del Definition of Done del capstone RAG de la fase. El `gate_de_regresion` es lo que, llevado a CI (DeepEval/promptfoo), bloquea un merge que empeora la calidad: el ship-gate del sistema.
