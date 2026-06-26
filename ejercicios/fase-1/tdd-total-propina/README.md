# 1.6 — Tu primer ciclo red-green-refactor (TDD)

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.6` Primer test unitario con pytest
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** código

## 🎯 Objetivo

Construir `total_con_propina(monto, pct_propina)` **dirigido por tests**: el test
primero (rojo), luego el mínimo código (verde), luego refactor. El entregable real
no es solo la función: es **tu suite de tests** y la evidencia de que recorriste el
ciclo en pasos chicos.

## 📋 Contexto

`total_con_propina` calcula el total de una cuenta de restaurante sumando la propina.
Es deliberadamente simple para que el foco esté en el **método**, no en el algoritmo.
Este es el ejercicio donde el TDD deja de ser teoría: vas a sentir cómo el test que
escribes *antes* te empuja a manejar los casos borde que tu cabeza, sola, se saltaría.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Escribe el test antes que el código.
2. Solo entonces, consulta la documentación oficial de [pytest](https://docs.pytest.org/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `test_solucion.py`. Hay una **semilla** (un test simple). Córrela:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

   Verás **ROJO**: la función aún no está implementada. Ese es el paso, no un error.

2. Abre `solucion.py` e implementa el **mínimo** para poner la semilla en **VERDE**.
   No te adelantes a casos que ningún test pide todavía.
3. Agrega el siguiente test (camino feliz parametrizado), míralo rojo, ponlo verde.
   Repite por cada punto del contrato. Cierra con un **refactor** (tests siguen verdes).
4. Añade al menos **un caso borde tuyo**.

### Contrato de `total_con_propina(monto, pct_propina)`

| Condición | Comportamiento esperado |
|---|---|
| caso normal | devuelve `monto + round(monto * pct_propina / 100)`, en **pesos enteros** |
| `pct_propina == 0` | total `==` `monto` (propina cero) |
| `monto` negativo | lanza `ValueError` |
| `pct_propina` fuera de `[0, 100]` | lanza `ValueError` |

> 💡 Trabaja en **enteros** (pesos), no en `float`. Así evitas el problema de
> precisión de los decimales y tus `assert` con `==` son exactos. `round()` basta.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Escribiste cada test **antes** del código que lo hace pasar (lo viste en rojo primero).
- [ ] Tus tests siguen **AAA** (Arrange-Act-Assert) y tienen nombres que describen el comportamiento.
- [ ] Cubres el camino feliz con `@pytest.mark.parametrize` y **ambos** errores con `pytest.raises`.
- [ ] Todos los tests pasan en verde y agregaste al menos un caso borde propio.
- [ ] Puedes explicar **sin notas** por qué ver el test en rojo primero importa.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Empieza por el test más simple (la semilla ya lo es) y míralo fallar porque la
función no existe. Implementa el mínimo para pasarlo. Recién entonces agrega un test
con `pytest.raises(ValueError)` para `monto` negativo —y obsérvalo en **rojo** antes
de añadir la guarda `if monto < 0: raise ValueError(...)`. Para validar el rango de
`pct_propina`, una sola condición lo cubre: `if not 0 <= pct_propina <= 100`. El
cálculo es una línea con `round(...)`. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `test_solucion.py`**),
- la **rúbrica**: `.ai/rubricas/fase-1/tdd-total-propina.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/tdd-total-propina.md` —
no la mires antes de intentarlo de verdad.
