---
ejercicio_id: fase-2/tdd-dividir-gasto
fase: fase-2
sub_unidad: "2.7"
version: 1
---

# Rúbrica — Dividir un gasto en partes justas (TDD de una regla real)

> Rúbrica **analítica** atada a los `objetivos`. La pieza única de este ejercicio: el
> **comportamiento 2 debe haber forzado el diseño**. Si la `bitacora.md` muestra el reparto
> del resto programado "de una" en el ciclo 1 (sin un rojo del caso no-exacto que lo pida),
> el alumno adivinó en vez de diseñar — exactamente lo que TDD evita. Evaluar `bitacora.md`,
> `test_solucion.py` y `solucion.py` juntos.

## Objetivos evaluados
- **O1** — Red-green-refactor estricto, dejando que el test del resto fuerce el diseño.
- **O2** — Traducir comportamientos **y un invariante** en tests; distinguir caso concreto de propiedad.
- **O3** — Diseñar los caminos de error (`personas <= 0`, `monto < 0`) con tests que los exijan.

## Criterios y niveles

### C1 — Corrección del reparto · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | El reparto no suma el monto (dejó `[33,33,33]`), o el resto va a las personas equivocadas; `acceptance_test.py` en rojo. |
| **en-progreso** | Casos exactos bien, pero algún no-exacto falla la invariante `max-min <= 1` (reparte el resto todo a una persona). |
| **competente** | `acceptance_test.py` en **verde**: suma exacta, una parte por persona, diferencia ≤ 1. |
| **excelente** | Verde + implementación limpia (`divmod` + comprensión o equivalente), sin ramas muertas. |

### C2 — Disciplina de TDD: el diseño lo dirigió el test · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin `bitacora.md`, o un test único que prueba todo: no hay ciclos. |
| **en-progreso** | Bitácora presente pero el reparto del resto aparece ya en el ciclo 1 (sin rojo del caso no-exacto): adivinó, no trianguló. |
| **competente** | Un test por comportamiento; el ciclo 2 muestra el rojo de `[33,33,33]` que motivó el `divmod`. |
| **excelente** | Además incluye el **test de invariante** (8) y articula por qué es más fuerte que un caso suelto (puente a property-based de 2.8). |

### C3 — Caminos de error y aserción · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `personas=0` revienta con `ZeroDivisionError` crudo (no `ValueError`), o monto negativo pasa silencioso. |
| **en-progreso** | Lanza `ValueError` pero sin test con `pytest.raises`, o cubre solo uno de los dos errores. |
| **competente** | Ambos errores lanzan `ValueError`, testeados con `pytest.raises`, escritos en rojo primero. |
| **excelente** | Mensajes de error con intención (qué argumento y por qué), y validación antes de cualquier cálculo. |

## Errores típicos a marcar
- **Adivinar el diseño:** programar `divmod` + reparto del resto en el ciclo 1, sin pasar por el rojo de `[33,33,33]`. Funciona, pero contradice O1: el objetivo es que el test fuerce el diseño.
- **Repartir el resto mal:** sumar todo el resto a la última persona (`[33,33,34]`) o a una sola, rompiendo `max-min <= 1`. La regla pide repartir de a 1 peso a las primeras `resto` personas.
- **`ZeroDivisionError` en vez de `ValueError`:** no validar `personas` antes de dividir. El camino de error es comportamiento, no un crash.
- **Confundir caso con propiedad:** no escribir el test de invariante, o escribir `assert dividir_gasto(100,3) == [34,33,33]` y llamarlo "invariante". El invariante es `sum(...) == monto` para *cualquier* entrada válida.
- **Floats donde deben ir ints:** usar `/` en vez de `//`/`divmod` y devolver `33.33...`; el contrato es pesos enteros.
- (transversal spec-driven) ciclos no visibles en el historial / un commit gigante.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `solucion.py` que aparece ya con `divmod` y la comprensión perfecta, mientras la `bitacora.md` no registra el rojo del caso no-exacto: el diseño no se derivó, se pegó.
- Generalizaciones no pedidas (soporte de pesos ponderados por persona, redondeo configurable, `Decimal`): sofisticación impropia del enunciado.
- No sabe explicar **por qué** `[33,33,33]` falla el comportamiento 2 (suma 99) ni por qué el resto va a las *primeras* personas.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, `dividir_gasto(7, 3)` y justifique el reparto del resto; luego que diga qué invariante atraparía un bug donde el resto se sumara dos veces.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Tu bitácora tiene un rojo en el ciclo 2? Antes de `[34,33,33]`, ¿viste fallar `[33,33,33]` por no sumar 100? Ese rojo es el que justifica todo el reparto del resto."
- **Pregunta socrática (nivel 2):** "Si divides 100 entre 3 con división entera, te sobran pesos. ¿Cuántos? ¿Hay una operación que te dé el cociente y ese sobrante a la vez? ¿A quién, exactamente, le toca cada peso sobrante para que nadie pague más de 1 peso de diferencia?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "`base, resto = divmod(monto, personas)`. Las primeras `resto` personas reciben `base + 1`, las demás `base`: `[base + 1 if i < resto else base for i in range(personas)]`. Valida `personas <= 0` y `monto < 0` con `raise ValueError` ANTES, y testea ambos con `pytest.raises`. Repasa la sección 7 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- El reparto justo es la clase de regla que el módulo Splitwise del capstone HomeBase necesita correcta al peso. Practicar el invariante `sum == monto` aquí es el primer paso hacia las property-based tests de 2.8 y hacia medir la *calidad* de los tests (no su coverage) en 2.9.
