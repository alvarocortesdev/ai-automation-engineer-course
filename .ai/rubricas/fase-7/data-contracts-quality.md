---
ejercicio_id: fase-7/data-contracts-quality
fase: fase-7
sub_unidad: "7.5d"
version: 1
---

# Rúbrica — Gate de calidad shift-left: valida un lote contra un data contract

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. **Nunca entregar el código de la solución de referencia.**

## Objetivos evaluados

- **O1:** Explicar y escribir un data contract, distinguiéndolo de un test de datos y de la observabilidad; argumentar por qué un contrato versionado en el borde previene el schema drift.
- **O2:** Implementar un gate shift-left que detecta las violaciones (schema/tipo/nulo/duplicado/dominio/rango + freshness/volumen) y bloquea el lote con un reporte estructurado.
- **O3:** Explicar la data observability (5 pilares + OpenLineage) y por qué los datos malos rompen igual la analítica y un RAG (asimetría del fallo silencioso).

## Criterios y niveles

### C1 — Corrección: el gate detecta las violaciones obligatorias · mapea: O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `pytest -v` no llega a verde; `validar_lote` corta en la primera violación, o no acumula, o lanza `TypeError` al evaluar tipo/rango sobre un `None`. |
| **en-progreso** | Pasa algunos casos pero faltan reglas (p. ej. no detecta `campo_extra` o `duplicado`), o las `Violacion` no traen los índices de `filas`. |
| **competente** | Las 7 reglas obligatorias detectadas; cada `Violacion` con `regla` + `campo` + `filas`; `ok` es True solo con cero violaciones; todos los tests provistos en verde. |
| **excelente** | Lo anterior + `frescura` y `volumen` (profundización) correctos, con el manejo de zona horaria de `ts` (ISO 8601) y `bool` excluido de `number`. |

### C2 — Calidad de ingeniería: tests reales + caso borde propio · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó ningún test propio; o "arregló" un test rojo cambiando el dato del test en vez de la lógica. |
| **en-progreso** | Agregó un test trivial que no aporta (re-testea un caso ya cubierto). |
| **competente** | Agregó ≥1 test de caso borde con valor real (lote vacío, `bool` como number, fila con varias violaciones a la vez). |
| **excelente** | Tests que aíslan bien (un caso = una regla), nombres claros, y un test que verifica que el gate **acumula** múltiples violaciones de una sola fila mala. |

### C3 — Comprensión demostrada: contract vs test vs observability · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay WRITEUP, o usa "contrato/test/observabilidad" como sinónimos. |
| **en-progreso** | Distingue test de contrato pero no ubica la observabilidad, o no explica shift-left. |
| **competente** | Articula las tres piezas (qué pregunta responde cada una, cuándo corre) y por qué el gate va en el **borde** (shift-left), no antes del dashboard. |
| **excelente** | Lo anterior + conecta con RAG: nombra una patología concreta de su gate que, colada, produciría una **alucinación silenciosa**, y explica por qué no salta ningún error (asimetría del fallo). |

## Errores típicos a marcar

- **`TypeError` al evaluar `min`/`max` o tipo sobre un valor `None`** → no respetó el orden (nulo primero, luego tipo/rango).
- **`bool` aceptado como `number`** (`isinstance(True, int)` es `True` en Python) → falta el `and not isinstance(v, bool)`.
- **Corta en la primera violación** en vez de acumular todas → reporte parcial, inútil para el productor (mismo antipatrón que un linter que para en el primer error).
- **`Violacion` sin índices de `filas`** → "falló algo" no sirve para diagnosticar; el productor necesita saber qué filas.
- **No detecta `campo_extra`** → cree que validar es solo "están los campos que espero", cuando el schema drift más sutil es un campo *de más*.
- **Confunde validar el tipo con validar la semántica** en el WRITEUP (cree que "tipo correcto = dato correcto") — el caso del cambio de unidad (centavos→pesos) lo desmiente.
- (transversales) Persigue *cantidad* de reglas sin pensar qué decisión protege cada una (equivalente a perseguir coverage%); confía en que "exit 0 = datos sanos" (confunde observabilidad de proceso con de dato); olvida que un gate de entrada es también una **defensa de seguridad** (datos no confiables del exterior, OWASP).

## Señales de dependencia-IA

- Solución que importa **Great Expectations / pandera / pydantic** y delega todo a la librería, cuando el ejercicio pide implementar el motor **a mano** — y el alumno no sabe explicar qué hace por debajo (`"¿qué query/predicado corre un ExpectColumnValuesToBeUnique?"` → silencio).
- WRITEUP pulido con el vocabulario exacto de la lección pero que **no calza** con el código (p. ej. afirma "acumulo todas las violaciones" pero el código tiene un `return` temprano).
- Manejo de zona horaria / `fromisoformat` sofisticado e impecable junto a una lógica de duplicados torpe — inconsistencia de nivel que sugiere copiar-pegar parcial.
- Explica los 5 pilares de observabilidad de memoria pero no sabe responder "¿freshness es de proceso o de dato?".

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `pytest -v` y mira el primer rojo. ¿El test espera que detectes una regla que no implementaste, o tu código se cae con un error (p. ej. `TypeError` sobre un `None`)? Empieza por ahí."
- **Pregunta socrática (nivel 2):** "¿Tu `validar_lote` recorre las **filas** o los **campos del contrato**? Si recorres el contrato campo por campo, ¿de dónde sacas naturalmente el `campo` y los índices de cada `Violacion`? Y cuando un valor es `None`, ¿tiene sentido preguntar si es mayor que `min`?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Te cae un `TypeError` porque evalúas `valor < min` sobre un `None`. Reordena: detecta `nulo` primero y, para tipo/rango, salta los valores `None`. Aparte: `isinstance(True, int)` es `True` en Python, así que `monto=True` pasa tu chequeo de `number`; añade `and not isinstance(v, bool)`. No cambies los tests — están señalando justo esto."

## Conexión con el proyecto / capstone

- Este gate **es** la primera línea de defensa del capstone de F7: lo que el agente extrae es un lote de datos que pasa por el gate de contrato antes de aterrizar o disparar una acción (potencialmente irreversible) en un sistema externo. Es el mismo *ship-gate* que aplicarás a los evals del agente en [7.7](/fase-7-automatizacion/7-7-agentes-automatizacion-ia/): si el lote no cumple el contrato, se bloquea y va a cuarentena (DLQ de 7.2), no contamina ni el warehouse ni el RAG.
