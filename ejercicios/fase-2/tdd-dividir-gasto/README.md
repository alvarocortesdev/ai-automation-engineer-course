# 2.7 — Dividir un gasto en partes justas (TDD de una regla real)

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.7` TDD obligatorio
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** código

## 🎯 Objetivo

Construir, **test-driven**, `dividir_gasto(monto_clp: int, personas: int) -> list[int]`
que reparte un gasto entero entre varias personas lo más parejo posible. A diferencia
del kata del sumador, aquí la **regla del reparto del resto** no es obvia: vas a *descubrir*
el diseño cuando un test te muestre que la división entera, sola, no suma el total.

## 📋 Contexto

Es la lógica que vive dentro de un Splitwise: divides una cuenta de `$100` entre 3 y no
da exacto — alguien tiene que asumir el peso que sobra. La función decide eso de forma
determinista y justa (las partes difieren en a lo más 1 peso y suman *exactamente* el
total). El módulo Splitwise del capstone HomeBase usa exactamente esta clase de regla.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Un comportamiento a la vez.
2. Solo entonces, consulta la [documentación oficial de pytest](https://docs.pytest.org/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* tests ni código.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Trabaja los comportamientos **en este orden**, un ciclo red-green-refactor por cada uno,
anotándolo en `bitacora.md`:

1. `dividir_gasto(100, 2)` → `[50, 50]` (división exacta).
2. `dividir_gasto(100, 3)` → `[34, 33, 33]` (sobra 1 peso → a la primera; suma 100).
3. `dividir_gasto(10, 4)` → `[3, 3, 2, 2]` (sobran 2 → a las dos primeras).
4. `dividir_gasto(0, 3)` → `[0, 0, 0]`.
5. `dividir_gasto(100, 1)` → `[100]`.
6. `dividir_gasto(100, 0)` lanza `ValueError` (no se reparte entre cero personas).
7. `dividir_gasto(-100, 2)` lanza `ValueError` (monto negativo no tiene sentido aquí).

Y, además de los 7, **al menos un test de invariante**:

8. Para algún caso no exacto, `sum(dividir_gasto(m, p)) == m`. Es el puente a las
   *property-based tests* de [`2.8`](/fase-2-ingenieria/2-8-diseno-de-tests/): no fijas un
   resultado concreto, fijas una **propiedad** que debe cumplirse siempre.

> ⚠️ **El comportamiento 2 es el que diseña la función.** Con división entera sola,
> `dividir_gasto(100, 3)` daría `[33, 33, 33]`, que suma **99**, no 100. Resístete a
> programar el reparto del resto antes de tener ese test en rojo: deja que el test te lo pida.
> El starter trae **el test 1** escrito y `solucion.py` en rojo (`NotImplementedError`). Sigue tú.

### Auto-verificación (solo al final)

```bash
uv run pytest acceptance_test.py
```

No la abras antes de cerrar tus ciclos: te quita el trabajo de traducir la spec a tests.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Un test por comportamiento (1–7) **más** al menos un test de invariante (8), escritos por ti.
- [ ] `bitacora.md` muestra el `🔴` **antes** del `🟢` en cada ciclo.
- [ ] `uv run pytest` (tuyos) y `uv run pytest acceptance_test.py` en **verde**.
- [ ] El reparto del resto lo dirigió el test 2/3, no lo programaste "de una" sin rojo.
- [ ] Los dos caminos de error (`personas <= 0`, `monto < 0`) lanzan `ValueError`, con `pytest.raises`.
- [ ] Puedes explicar **sin notas** por qué `sum(resultado) == monto` es una propiedad más fuerte que cualquier caso suelto.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `solucion.py` — tu implementación, crecida test a test.
- `test_solucion.py` — tus tests (comportamientos + invariante).
- `bitacora.md` — el log de ciclos: por cada comportamiento, una línea
  `🔴 <qué probé> → 🟢 <qué código mínimo> → 🔵 <refactor o "nada">`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el test 1, `[monto // personas] * personas` pasa. El test 2 lo rompe (suma 99).
Ahí está el insight: `base, resto = divmod(monto, personas)` te da el cociente entero y
cuántos pesos sobran. Las primeras `resto` personas reciben `base + 1`; las demás, `base`.
Una comprensión lo expresa entero:
`[base + 1 if i < resto else base for i in range(personas)]`.
Valida primero (`if personas <= 0: raise ...`, `if monto_clp < 0: raise ...`) y escribe
esos tests de error **en rojo** antes de la guarda. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `bitacora.md`**),
- la **rúbrica**: `.ai/rubricas/fase-2/tdd-dividir-gasto.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/tdd-dividir-gasto.md`
— no la mires antes de intentarlo de verdad.
