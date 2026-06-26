---
ejercicio_id: fase-1/tdd-total-propina
fase: fase-1
sub_unidad: "1.6"
version: 1
---

# Rúbrica — Tu primer ciclo red-green-refactor (TDD)

> Rúbrica **analítica** atada a los `objetivos`. El corazón del ejercicio NO es la función
> `total_con_propina` (es trivial), sino el **método**: tests escritos antes del código,
> caso feliz parametrizado, errores con `pytest.raises`. Evaluar el proceso TDD y la calidad
> de los tests tanto como la corrección de la implementación.

## Objetivos evaluados
- **O1** — Aplicar red-green-refactor: test que falla primero, mínimo código para el verde, refactor con red puesta.
- **O2** — Estructurar tests con AAA y nombres que describen el comportamiento.
- **O3** — Cubrir el camino feliz con `parametrize` y los errores con `pytest.raises`.

## Criterios y niveles

### C1 — Corrección de la implementación · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | La función no calcula bien la propina, o usa `float` en el resultado, o no maneja `pct = 0`. |
| **en-progreso** | Camino feliz correcto pero falta una de las guardas de error (monto negativo o pct fuera de rango). |
| **competente** | Las cuatro reglas del contrato correctas: cálculo entero, `pct = 0` → monto, ambos `ValueError`. |
| **excelente** | Además evita el `float` por diseño (entero) y comenta/explica el redondeo (`round` usa "banker's rounding"); guardas con mensajes claros. |

### C2 — Proceso TDD y calidad de los tests · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Solo está la semilla, o no hay tests propios; la suite no cubre los errores. Ningún indicio de rojo-primero. |
| **en-progreso** | Tests para el camino feliz pero copiados/pegados (sin `parametrize`), o falta un caso de error, o nombres tipo `test_1`. |
| **competente** | Camino feliz con `@pytest.mark.parametrize`, **ambos** errores con `pytest.raises`, AAA y nombres descriptivos, +1 caso borde propio. |
| **excelente** | Evidencia clara del ciclo (commits o nota de "vi rojo, luego verde"); casos borde bien elegidos (pct=100, monto=0); tests que aíslan un comportamiento por test. |

## Errores típicos a marcar
- **Escribir la función primero y los tests después**: contradice el objetivo; suele delatarse porque los tests solo confirman lo que el código ya hace y no hay caso de error que falle.
- **Resultado en `float`**: comparar `total == 11000.0` o arrastrar decimales; el contrato pide pesos enteros. Trabajar en entero es la jugada correcta.
- **No ver el rojo**: implementar todo de una y escribir los tests al final; se pierde la verificación de que el test prueba algo.
- **Copiar y pegar el mismo test cambiando números** en vez de `parametrize`: funciona, pero es el smell que `parametrize` resuelve.
- **`assert total_con_propina(...)` sin `==`**: un assert de un valor truthy (`assert total_con_propina(10000, 10)`) pasa con cualquier número distinto de cero — no verifica nada útil.
- **Usar `pytest.raises` sin el tipo** o sin llamar la función dentro del `with`.
- (transversal spec-driven) no traducir todos los puntos del contrato a tests: un punto del contrato sin test es un agujero.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Suite "perfecta y completa" de golpe, sin ningún rastro del ciclo incremental (todos los casos a la vez, incluida sofisticación no pedida como `pytest.approx`, `hypothesis` o fixtures innecesarias para una función pura).
- Implementación que maneja casos que ningún test cubre (over-engineering): señal de código pegado, no derivado de tests.
- No puede explicar por qué se ve el test en rojo antes de implementar.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué pasa si cambia `round` por `int()` (truncar) en un caso como `(15, 10)`, y que escriba el test que distinguiría ambos comportamientos.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Antes de tocar `solucion.py`, ¿tienes un test que falle? Empieza por el más simple y míralo en rojo. El rojo es el permiso para escribir código."
- **Pregunta socrática (nivel 2):** "Tienes el camino feliz verde. ¿Qué entrada NO probaste todavía? ¿Qué debería pasar con un `monto` negativo, y cómo escribirías un test que lo verifique sin un `==`?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Para los errores, usa `with pytest.raises(ValueError): total_con_propina(-1, 10)` — y míralo en rojo antes de agregar la guarda `if monto < 0: raise ValueError(...)`. Para el camino feliz, junta tus casos en un `@pytest.mark.parametrize('monto, pct, esperado', [...])`. Revisa secciones 4.3–4.5 y reintenta antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Es el primer eslabón del hilo de testing del curso: el ciclo red-green-refactor que practicas aquí es el método con que se construye cada función del **Capstone F1** y se vuelve práctica obligatoria en la Fase 2.
