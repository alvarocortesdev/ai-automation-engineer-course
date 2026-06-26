# Ejercicio 3.1 — Escribe SQL contra una base que corre

> **Modalidad: código (SQL), Primero-Sin-IA.** Escribes consultas reales contra una base de datos que se ejecuta de verdad (SQLite, sin instalar nada). Una consulta por archivo; un test la corre y compara el resultado. La disciplina es **predecir el resultado a mano antes de correr el test**: si aciertas en tu cabeza, ya entendiste la consulta.

## La base de datos

Una sola tabla `productos` (sin `JOIN` en esta lección: los `JOIN` llegan en la sub-unidad 3.2, Queries avanzadas). Está definida y sembrada en `seed.sql` —no la edites—:

| columna | tipo | qué es |
|---|---|---|
| `id` | INTEGER PK | identificador autoincremental |
| `nombre` | TEXT | nombre del producto |
| `categoria` | TEXT | `periféricos`, `pantallas`, `cables`, `accesorios` |
| `precio` | INTEGER | precio en pesos |
| `stock` | INTEGER | unidades disponibles |

## Tu tarea (Primero-Sin-IA, timebox 30–40 min)

Escribe **una consulta por archivo** en `consultas/`. Cada archivo trae el enunciado como comentario:

- **q1** — `SELECT` + `WHERE`: nombre y stock de los productos de `'periféricos'` con stock mayor que 0.
- **q2** — `ORDER BY` + `LIMIT`: nombre y precio de los **3 más caros**, del más caro al más barato.
- **q3** — `GROUP BY` + `COUNT`: cuántos productos hay por categoría.
- **q4** — `GROUP BY` + `SUM`: la suma de `stock` por categoría.
- **q5** — `INSERT`: agrega `'Alfombrilla'`, `'accesorios'`, precio `9990`, stock `50` (deja que la base asigne el `id`).
- **q6** — `UPDATE`: sube en `1000` el precio de todos los productos de `'cables'`.
- **q7** — `DELETE`: elimina los productos sin stock (`stock = 0`).

## Cómo correr los tests

Desde esta carpeta:

```bash
uv run pytest        # recomendado
pytest               # si ya tienes pytest en el entorno
```

Cada test arma una base nueva en memoria (no se pisan entre sí). En q5/q6/q7 el test verifica el **estado de la base** después de tu operación.

## Criterios de "hecho"

- [ ] `pytest` pasa en verde: las 7 consultas dan el resultado esperado.
- [ ] En q5/q6/q7 escribiste primero el `SELECT` con el mismo `WHERE` (en una línea de comentario) para ver qué filas ibas a tocar **antes** de ejecutar el verbo destructivo.
- [ ] No usaste `JOIN` (todo es una sola tabla).
- [ ] Puedes explicar **sin notas** por qué `GROUP BY categoria` te deja poner `categoria` y `COUNT(*)` en el `SELECT`, pero no `nombre`.

## Pedir corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-3/consultas-sql-tienda/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará que tus consultas sean correctas **y** que entiendas por qué —no solo que el test pase.
