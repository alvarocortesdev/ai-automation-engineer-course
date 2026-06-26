# Ejercicio 0.3 — Trazado a mano de un bucle anidado

> **Modalidad: a mano (sin ejecutar, sin IA).** Este ejercicio entrena tu *notional machine*: el modelo mental de cómo la máquina ejecuta el código, paso a paso. Si predices la salida antes de correrla, estás pensando como ingeniero. Si necesitas ejecutar para saber qué hace, todavía no.

## Objetivos

- **O1** — Predecir la salida de un bucle anidado con acumulador, línea a línea, **sin ejecutar**.
- **O2** — Construir una **tabla de traza** (variable × iteración) que justifique la predicción.
- **O3** — Diagnosticar tu propio error contrastando predicción vs. ejecución real.

## El código a trazar

```python
def misterio(n):
    total = 0
    for i in range(1, n + 1):
        fila = 0
        for j in range(i):
            fila = fila + j
        total = total + fila
    return total
```

## Tu tarea (en este orden — Primero-Sin-IA, timebox 30 min)

1. **Predice** el valor que devuelve `misterio(4)` **sin ejecutar el código y sin IA**. A mano, en papel o en un `.md`.
2. **Construye la tabla de traza**: una fila por cada paso relevante, columnas para `i`, `j`, `fila`, `total`. Anota cómo cambia cada variable en cada iteración del bucle externo e interno.
3. **Sólo después**, ejecuta el código (`python -c "..."` o un archivo) y **verifica**.
4. **Reflexiona**: si tu predicción falló, escribe en 2–3 frases *qué* idea tenías equivocada (no "me equivoché en un número" — la idea de fondo).

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — tu valor predicho **antes** de ejecutar + la **tabla de traza**.
- `verificacion.md` — la salida real al ejecutar + si coincidió o no.
- `reflexion.md` — qué idea equivocada tenías (si la hubo), o por qué acertaste.

> No incluyas la salida ejecutada en `prediccion.md`. El valor de este ejercicio está en **predecir primero**. Si ejecutas antes de predecir, el ejercicio no sirve.

## Pedir corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-0/trazado-a-mano-bucle/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (la tabla de traza), no sólo si el número final es correcto.
