# Ejercicio 0.7 — Recursión y scope, trazados a mano

> **Modalidad: a mano (sin ejecutar, sin IA).** Entrena tu *notional machine* en las dos piezas
> que más se oxidan: la **pila de llamadas** de una función recursiva y el **scope** (alcance) de
> las variables. Si las predices sin ejecutar, piensas como ingeniero.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.7` Fundamentos de programación sin IA
**Ruta:** crítica · **Timebox:** 25–35 min

## 🎯 Objetivo

- **O1** — Predecir, **sin ejecutar**, las tres salidas del programa de abajo.
- **O2** — Trazar la **pila de llamadas** de `suma_hasta(4)`, mostrando la bajada (hasta el caso
  base) y la subida (cómo se resuelve cada nivel).
- **O3** — Explicar, vía **scope (LEGB)**, por qué `print(x)` imprime `10` y no `6`.

## El programa a trazar

```python
def suma_hasta(n):
    if n == 0:
        return 0
    return n + suma_hasta(n - 1)

x = 10
def f(n):
    x = n * 2
    return x

print(f(3))
print(x)
print(suma_hasta(4))
```

## 📏 Tu tarea (en este orden — Primero-Sin-IA)

1. **Predice** las tres líneas que imprime, **sin ejecutar y sin IA**, a mano o en `.md`.
2. **Dibuja la pila** de `suma_hasta(4)`: una fila por nivel de llamada, mostrando qué queda
   pendiente de sumar en cada uno y qué valor devuelve cada nivel al volver.
3. **Explica el scope**: ¿la `x` de dentro de `f` es la misma que la `x = 10` de afuera, o una
   nueva? ¿Por qué `print(x)` da `10`?
4. **Solo después**, ejecuta el programa y **verifica**.
5. **Reflexiona**: si fallaste, escribe en 2–3 frases *qué idea de fondo* tenías equivocada (no
   "me equivoqué en un número": la idea — el caso base, el orden de la subida, el shadowing).

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — las 3 salidas predichas **antes** de ejecutar + la **pila de llamadas** de
  `suma_hasta(4)` + tu explicación del scope.
- `verificacion.md` — la salida real al ejecutar + si coincidió.
- `reflexion.md` — qué idea equivocada tenías (o por qué acertaste).

> No incluyas la salida ejecutada en `prediccion.md`. El valor del ejercicio está en **predecir
> primero**. Si ejecutas antes de predecir, el ejercicio no sirve.

## ✅ Criterios de "hecho"

- [ ] Predijiste las **tres** líneas antes de ejecutar.
- [ ] La pila de `suma_hasta(4)` muestra bajada **y** subida (no solo el resultado).
- [ ] Explicaste por qué `print(x)` da `10` usando la idea de scope local vs. global.
- [ ] Si fallaste, nombraste la **idea** equivocada, no el número.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para la recursión: baja anotando qué queda "pendiente" en cada nivel (`4 + ?`, `3 + ?`, …) hasta
tocar el caso base (`n == 0`), y recién ahí empieza a subir resolviendo de adentro hacia afuera.
Para el scope: pregúntate si asignar `x = n * 2` **dentro** de `f` crea una variable nueva local o
modifica la de afuera (revisa la regla LEGB y la sección 4.3 de la lección). Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

> "Corrige `ejercicios/fase-0/fundamentos-programacion-recursion-scope/` usando el framework de
> `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (la pila, la explicación del scope), no solo si los números
finales coinciden.
