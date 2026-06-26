# Ejercicio 0.3 — Traza una inversión in-place con aliasing

> **Modalidad: a mano (sin ejecutar, sin IA).** Este ejercicio entrena tu *notional machine*: el modelo mental de cómo la máquina ejecuta el código, paso a paso. Si predices la salida antes de correrla, estás pensando como ingeniero. Si necesitas ejecutar para saber qué hace, todavía no.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.3` Notional machine y trazado a mano
**Ruta:** crítica · **Timebox:** 30 min

## 🎯 Objetivos

- **O1** — Predecir la salida **exacta** de un programa con un bucle `while`, índices y mutación *in-place*, **sin ejecutar**.
- **O2** — Construir una **tabla de estado** (variable × paso) que justifique la predicción.
- **O3** — Explicar, con el modelo *"nombres → objetos"*, por qué el `is` final da lo que da (aliasing).

## El código a trazar

```python
def reordenar(xs):
    izquierda = 0
    derecha = len(xs) - 1
    while izquierda < derecha:
        xs[izquierda], xs[derecha] = xs[derecha], xs[izquierda]
        izquierda = izquierda + 1
        derecha = derecha - 1
    return xs

original = [5, 8, 2, 1]
copia = original
resultado = reordenar(copia)
print(original)
print(resultado)
print(original is resultado)
```

## 📏 Primero-Sin-IA (en este orden, timebox 30 min)

1. **Predice** las tres líneas que imprime el programa, **sin ejecutar y sin IA**. A mano, en papel o en un `.md`.
2. **Construye la tabla de estado** del bucle: una fila por cada vuelta del `while`, con columnas para `izquierda`, `derecha` y el contenido de `xs` *después* de esa vuelta.
3. **Sólo después**, ejecuta el código y **verifica**.
4. **Reflexiona**: si fallaste, ¿en qué fila se rompió tu modelo? ¿Era el aliasing (`copia = original`), la mutación *in-place* del swap, o el `is`?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` con la **tabla de estado** del `while` y las **tres** líneas predichas (antes de ejecutar).
- [ ] `verificacion.md` con la salida real al ejecutar y si coincidió o no.
- [ ] `reflexion.md` con la **idea de fondo** que tenías mal (o por qué acertaste) — no "me equivoqué en un número".
- [ ] Puedes explicar sin notas por qué `original is resultado` da `True`.

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — tu predicción de las 3 líneas + la tabla de estado.
- `verificacion.md` — la salida real + si coincidió.
- `reflexion.md` — la idea equivocada (si la hubo) o por qué acertaste.

> No incluyas la salida ejecutada en `prediccion.md`. El valor del ejercicio está en **predecir primero**. Si ejecutas antes de predecir, no sirve.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Cuenta **cuántos objetos lista** existen en todo el programa. `original = [5, 8, 2, 1]` crea uno. `copia = original` **no** crea otro: es la misma etiqueta sobre el mismo objeto. `reordenar` muta ese objeto *in-place* (el swap cambia posiciones dentro de la lista, no crea una nueva) y `return xs` devuelve el mismo objeto. Si solo hay **un** objeto lista, ¿qué pasa con `is`?

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-0/notional-machine-trazado/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (la tabla de estado y el razonamiento del `is`), no solo si las tres líneas coinciden. La **solución de referencia** vive en `.ai/soluciones/fase-0/notional-machine-trazado.md` — no la mires antes de intentarlo de verdad.
