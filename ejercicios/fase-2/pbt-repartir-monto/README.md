# Ejercicio 2.8 — Property-based testing: caza el bug del remanente

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.8` Diseño de tests
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** código (Python + Hypothesis)

> **Primero-Sin-IA.** Implementa la función y diseña las propiedades **a mano, sin IA**. La IA solo
> revisa y explica al final — nunca genera las propiedades por ti. El valor del ejercicio es que *tú*
> descubras qué invariante afirmar.

## 🎯 Objetivo

Escribir **property-based tests** con Hypothesis que afirman invariantes sobre *cientos* de entradas
generadas, y entender por qué cazan bugs de borde que tres ejemplos a mano no cazan.

## 📋 Contexto

`repartir_monto(total, partes)` reparte un entero `total ≥ 0` en `partes` partes lo más parejo posible:
las partes difieren a lo más en 1 y **suman exactamente `total`** (piensa en dividir una cuenta en
centavos sin perder ni inventar plata). Una implementación ingenua como `[total // partes] * partes`
pasa los ejemplos "redondos" (100/4) y **pierde plata** en cuanto hay resto (101/4). El ejemplo a mano
no lo nota; una propiedad bien escrita lo caza al primer intento. Esta función es la semilla del refactor
de rendimiento y de los invariantes de negocio que blindarás en el **Capstone F2**.

## 📏 Primero-Sin-IA

1. Implementa `repartir_monto` **solo**, a mano (timebox arriba). Está bien que sea feo.
2. Solo entonces consulta la **documentación oficial** de Hypothesis para la sintaxis de `@given`.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* tus propiedades.
4. Mañana, **reescribe una de tus propiedades de memoria.** Si no puedes, no la aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.py` y completa `repartir_monto` (no cambies su firma). El starter lanza
   `NotImplementedError`.
2. Instala Hypothesis si no lo tienes:

   ```bash
   uv add --dev hypothesis        # o:  pip install hypothesis
   ```

3. Corre los tests de ejemplo provistos y confirma el **verde** de partida:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

4. En `test_solucion.py`, escribe **al menos tres** property-based tests con `@given`:
   - **P1 — conservación:** `sum(repartir_monto(total, partes)) == total`.
   - **P2 — equidad:** `max(partes_resultado) - min(partes_resultado) <= 1`.
   - **P3 — cantidad:** `len(repartir_monto(total, partes)) == partes`.

   Usa estrategias **acotadas**: `st.integers(min_value=0, max_value=10**9)` para el total y
   `st.integers(min_value=1, max_value=1000)` para las partes.
5. Añade una prueba con `pytest.raises(ValueError)` para `partes <= 0`.
6. Escribe `propiedades.md`: por cada propiedad, una frase con **qué invariante** afirma y **qué bug
   atraparía** que un ejemplo no.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `repartir_monto` implementada; los tests de ejemplo provistos pasan en **verde**.
- [ ] Al menos **tres** propiedades con `@given` y estrategias acotadas, todas verdes.
- [ ] En `propiedades.md` demuestras que **P1 falla** contra la versión ingenua `[total // partes] * partes`.
- [ ] Cubriste `partes <= 0` con `pytest.raises(ValueError)`.
- [ ] Puedes explicar **sin notas** qué es el *shrinking* y por qué una propiedad **tautológica** (que
      reimplementa la función en el assert) no sirve.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para la implementación, `divmod` es la clave: `base, resto = divmod(total, partes)` te da el piso y
cuántas partes deben llevar **una unidad extra**. Repártelo a las primeras: `base + 1` para `i < resto`,
`base` para el resto. Para las propiedades, recuerda que una propiedad **no** compara contra un valor
esperado fijo: afirma una **relación** que debe valer siempre (la suma se conserva). La tautología a
evitar: NO escribas `assert repartir_monto(t, n) == [base+1 if ...]` recomputando el algoritmo en el
test — eso solo prueba que tu código es igual a sí mismo, no que es correcto. Revisa la sección 4.5 de
la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `solucion.py`, `test_solucion.py`, `propiedades.md`),
- la **rúbrica**: `.ai/rubricas/fase-2/pbt-repartir-monto.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/pbt-repartir-monto.md` — no la mires antes
de intentarlo de verdad.
