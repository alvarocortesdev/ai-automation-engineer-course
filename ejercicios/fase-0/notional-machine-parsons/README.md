# Ejercicio 0.3 — Parsons: ordena la función `promedio`

> **Modalidad: mixta (reordenar a mano → verificar con tests).** Un *Parsons problem* te da las líneas correctas pero **desordenadas**. No escribes código nuevo: razonas la **estructura** — qué depende de qué, qué vive dentro del bucle, qué va al final. Es trazado a mano aplicado a la *forma* del programa.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.3` Notional machine y trazado a mano
**Ruta:** crítica · **Timebox:** 25 min

## 🎯 Objetivos

- **O1** — Reordenar las líneas de una función pequeña (incluida la **indentación**) hasta que su comportamiento sea correcto.
- **O2** — Justificar el orden por **dependencias** de datos y de control, no por estética.
- **O3** — Verificar con una suite de tests que la función cumple su contrato, incluido el **caso borde** (lista vacía).

## El problema

La función `promedio(numeros)` debe devolver el promedio de la lista. Si la lista está **vacía**, debe devolver `0.0` (sin reventar por división entre cero).

Estas son sus líneas, **desordenadas**:

```text
    total = 0
def promedio(numeros):
    if not numeros:
        return 0.0
    for n in numeros:
        total = total + n
    return total / len(numeros)
```

Tu trabajo: ponerlas en el orden correcto, con la indentación correcta, dentro de `solucion.py`.

## 📏 Primero-Sin-IA (en este orden, timebox 25 min)

1. **A mano, sin ejecutar:** escribe el orden que crees correcto. Pregúntate por cada línea: *¿qué necesita que ya exista antes que ella?*
2. Pásalo a `solucion.py` (reemplaza el stub).
3. **Recién ahí** ejecuta los tests. Itera hasta verde.
4. En `orden.md`, justifica el orden: ¿por qué `total = 0` no puede ir después del `for`? ¿Por qué el `return total / len(numeros)` va al final?

## 🛠️ Instrucciones

1. Abre `solucion.py` y reemplaza el stub por las líneas reordenadas (no agregues líneas nuevas ni cambies nombres).
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade **un test tuyo** en `tests/test_solucion.py`: un caso borde que se te ocurra (p. ej. números negativos, o un solo elemento).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `solucion.py` con la función reordenada, ejecutable, sin líneas sobrantes.
- [ ] `pytest` en verde (incluido el caso de lista vacía).
- [ ] Agregaste al menos **un test propio**.
- [ ] `orden.md` con 3–4 frases justificando el orden por dependencias.
- [ ] Puedes explicar sin notas por qué la indentación *es* la estructura (qué vive dentro del `for`).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Piensa en **dependencias**, no en cómo se ve. ¿Qué línea *usa* `total`? Esa línea no puede ir antes de la que crea `total`. ¿Conviene chequear la lista vacía **antes** o **después** de calcular `len(numeros)`? La indentación te dice qué está *dentro* del `for` (se ejecuta una vez por elemento) y qué está al nivel de la función (se ejecuta una vez).

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-0/notional-machine-parsons/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-0/notional-machine-parsons.md` — no la mires antes de intentarlo de verdad.
