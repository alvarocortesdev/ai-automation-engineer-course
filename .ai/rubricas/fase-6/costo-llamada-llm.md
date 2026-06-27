---
ejercicio_id: fase-6/costo-llamada-llm
fase: fase-6
sub_unidad: "6.3"
version: 1
---

# Rúbrica — Calculadora de costo y elección de modelo

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector evalúa el
> **proceso** (¿calculó a mano antes de codear?) y la **comprensión** (¿la reflexión
> explica por qué la salida pesa más?), no solo si los tests pasan. Lee la solución de
> referencia **al final**, cuando ya formaste tu propio juicio.

## Objetivos evaluados

- **O1** — Calcular el costo en USD con la fórmula por millón de tokens.
- **O2** — Predecir a mano el costo en varios modelos y cuál es el más barato.
- **O3** — Explicar por qué la salida pesa más que la entrada en el costo.

## Criterios y niveles

### C1 — Corrección del cálculo · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No pasa los tests; o confunde entrada/salida, o divide por 1000 en vez de 1e6, o devuelve 0 para un modelo desconocido. |
| **en-progreso** | Pasa la mayoría pero falla un borde (0 tokens, o el modelo desconocido no lanza excepción, o `modelo_mas_barato` con tabla vacía). |
| **competente** | Todos los tests verdes: fórmula por millón correcta, 0 tokens = 0.0, modelo desconocido lanza, `modelo_mas_barato` elige bien según la carga. |
| **excelente** | Además `modelo_mas_barato` se apoya en `calcular_costo` (no duplica la fórmula) y la lógica queda legible; o añade un test propio (p. ej. empate). |

### C2 — Proceso Primero-Sin-IA (predicción antes de medir) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`, o se escribió después de correr los tests (números calcados sin cuenta). |
| **en-progreso** | Da los costos pero sin mostrar la cuenta, o no dice cuál es el más barato. |
| **competente** | `prediccion.md` existe antes de ejecutar, con la cuenta de los 3 modelos (opus 0.10, sonnet 0.06, haiku 0.02) y haiku como el más barato. |
| **excelente** | Anticipa que el "más barato" puede cambiar con la proporción in/out (no es siempre el mismo modelo) sin que se lo pidan. |

### C3 — Comprensión demostrada (salida pesa más) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `verificacion.md` ausente, o dice "la salida cuesta más" sin el porqué (el precio out > in). |
| **en-progreso** | Menciona que out cuesta más pero no conecta con la respuesta verbosa. |
| **competente** | Explica que el precio por millón de salida es mayor (p. ej. $25 vs $5) y que un modelo verboso genera más tokens de salida → más caro por request. |
| **excelente** | Conecta con model routing / control de `max_tokens` o con el budget de costo del capstone. |

## Errores típicos a marcar

- **Dividir por 1000 en vez de 1e6** (confundir "por mil" con "por millón"): costo 1000x mal.
- **Sumar entrada y salida con el mismo precio** (usar solo `in` o promediar): ignora que out cuesta más.
- **Devolver 0 (o `None`) para un modelo desconocido** en vez de lanzar: un bug silencioso que en prod factura mal sin avisar.
- **`modelo_mas_barato` que ignora la carga** (devuelve el de menor precio de salida fijo): falla cuando la proporción in/out cambia.
- **Reimplementar la fórmula dentro de `modelo_mas_barato`** en vez de reusar `calcular_costo`: duplicación que se desincroniza.
- (transversal) Hardcodear precios reales dentro de la función en vez de usar el `precios` inyectado → acopla a precios que cambian.

## Señales de dependencia-IA

> Describir sin acusar; proponer una verificación.

- Implementación correcta pero `prediccion.md` ausente o idéntica a la salida real (calculó "después").
- `verificacion.md` usa "la salida cuesta más" como eslogan pero no puede decir, en una pregunta de seguimiento, **cuánto** más (la relación de precios) ni por qué.
- **Verificación sugerida:** pedir que calcule a mano un caso nuevo (p. ej. 15k in / 3k out en los 3 modelos) y que diga cuál gana si la salida fuera 10x la entrada.

## Feedback sugerido (graduado)

> Nunca pegar el código de la solución.

- **Pista (nivel 1):** "¿Por cuánto divides los tokens? El pricing está dado **por millón** — revisa la potencia de 10."
- **Pregunta socrática (nivel 2):** "Si un modelo cobra $5 por millón de entrada y $25 por millón de salida, ¿qué pesa más en una respuesta larga: lo que mandaste o lo que generó?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Calcula cada lado por separado (`tokens/1e6 * precio_de_ese_lado`) y súmalos. Para el más barato, evalúa `calcular_costo` sobre **cada** modelo de la tabla y quédate con el menor — `min(precios, key=...)`."

## Conexión con el proyecto / capstone

- Esta calculadora es la base del **budget de costo/latencia** que el **Capstone F6 (RAG de producción)** exige como entregable de primera clase: medir el USD por consulta (embedding + generación) y justificar la elección de modelo por tarea en un ADR.
