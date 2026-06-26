# Ejercicio 3.2 — Lee y diagnostica: JOINs, NULLs y window functions

> **Modalidad: a mano (predice sin ejecutar), verifica al final.** Este ejercicio entrena lo que más harás revisando código: leer una query ajena y *saber qué devuelve* sin correrla. Si predices la salida antes de ejecutarla, estás razonando como ingeniero de backend. Si necesitas ejecutar para saber qué hace, todavía no.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.2` Queries avanzadas
**Ruta:** crítica · **Timebox:** 35–40 min

## Objetivos

- **O1** — Predecir la salida de queries con `LEFT JOIN` + `COUNT`, y con window functions (`RANK`, `SUM OVER`), **sin ejecutar**.
- **O2** — Diagnosticar por qué un `WHERE` sobre la tabla derecha convierte un `LEFT JOIN` en `INNER`, y corregirlo moviendo la condición al `ON`.
- **O3** — Decidir el tipo de JOIN correcto según **qué filas sin pareja deben sobrevivir**.

## Las tablas (una biblioteca)

```sql
-- socios
id | nombre
 1 | Ana
 2 | Beto
 3 | Cora
 4 | Dani          -- Dani NO tiene préstamos

-- prestamos  (fecha_devolucion NULL = el libro sigue prestado)
 id | socio_id | libro        | fecha_devolucion
 10 |    1     | 'Dune'       | 2026-05-01
 11 |    1     | 'Hyperion'   | NULL
 12 |    2     | 'Solaris'    | 2026-04-20
 13 |    3     | 'Dune'       | 2026-05-10
 14 |    3     | 'Neuromante' | 2026-05-12

-- ventas (monto en miles)
 mes | region  | monto
  1  | 'Norte' | 100
  2  | 'Norte' | 150
  3  | 'Norte' | 120
  1  | 'Sur'   | 200
  2  | 'Sur'   | 180
```

(El esquema completo con `INSERT`s está en `datos.sql`, por si quieres verificar al final.)

## Tu tarea (en este orden — Primero-Sin-IA, sin ejecutar)

Crea un archivo `respuestas.md` y resuelve **a mano**:

### 1. Predice la salida (tabla completa, ordenada)

```sql
SELECT s.nombre, COUNT(p.id) AS total
FROM socios s
LEFT JOIN prestamos p ON p.socio_id = s.id
GROUP BY s.nombre
ORDER BY s.nombre;
```

### 2. Diagnostica el bug y corrígelo

Esta query pretendía listar a **todos** los socios junto con sus préstamos ya devueltos, **incluyendo a los socios sin préstamos**. Pero Dani desaparece del resultado. Explica **por qué** y **reescríbela** para que Dani vuelva a aparecer (con `libro` en NULL):

```sql
SELECT s.nombre, p.libro
FROM socios s
LEFT JOIN prestamos p ON p.socio_id = s.id
WHERE p.fecha_devolucion IS NOT NULL;
```

### 3. Decide el JOIN (una línea de justificación cada uno)

Para cada pedido, di qué tipo de JOIN usarías y **por qué**:

- **(a)** "Todos los socios y cuántos libros tienen prestados ahora mismo (los no devueltos), incluso los que tienen 0."
- **(b)** "Solo los préstamos que ya fueron devueltos, con el nombre del socio."
- **(c)** "Reconciliar `socios` con una tabla `tarjetas` para detectar socios sin tarjeta **y** tarjetas sin socio, todo de una vez."

### 4. Predice la salida (ordenada por region, luego mes)

```sql
SELECT region, mes, monto,
       RANK() OVER (PARTITION BY region ORDER BY monto DESC) AS rnk,
       SUM(monto) OVER (PARTITION BY region ORDER BY mes) AS acumulado
FROM ventas;
```

## Verifica (solo después de predecir)

```bash
# Levanta un PostgreSQL efímero y carga los datos + tus queries:
docker run --rm -e POSTGRES_PASSWORD=x -p 5433:5432 -d --name pg-ej postgres:16
sleep 4
docker exec -i pg-ej psql -U postgres < datos.sql
# luego pega cada query con: docker exec -i pg-ej psql -U postgres -c "SELECT ..."
docker rm -f pg-ej   # al terminar
```

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Diste la **tabla completa** (con el orden pedido) en las preguntas 1 y 4, no una descripción vaga.
- [ ] En la 2 explicaste que el `WHERE` sobre la columna de la tabla derecha eliminó la fila NULL de Dani (degradó el `LEFT` a `INNER`) y moviste la condición al `ON`.
- [ ] En la 3 justificaste cada elección por **qué filas sin pareja deben sobrevivir**.
- [ ] Puedes **explicar sin notas** la diferencia entre `RANK` y `ROW_NUMBER` ante un empate.

## Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **1:** `COUNT(p.id)` ignora NULL → Dani da 0, no 1.
- **2:** la fila fantasma de Dani tiene `fecha_devolucion = NULL`; `NULL IS NOT NULL` es falso, así que el `WHERE` la elimina. La condición que describe la tabla derecha y debe preservar las filas sin pareja va en el `ON`: `LEFT JOIN prestamos p ON p.socio_id = s.id AND p.fecha_devolucion IS NOT NULL`.
- **4:** en Norte, `RANK` por monto desc: 150→1, 120→2, 100→3; `acumulado` con `ORDER BY mes` es un total corriente: 100, 250, 370. En Sur: 200→1, 180→2; acumulado 200, 380.

Es una pista, no la solución de referencia.

</details>

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-3/queries-avanzadas-lectura/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **razonamiento** (el porqué del bug, la justificación del JOIN), no solo si el número final coincide. La **solución de referencia** vive en `.ai/soluciones/fase-3/` — no la mires antes de intentarlo de verdad.
