# Ejercicio 3.2 — Reemplaza el self-join: window functions sobre transacciones

> **Modalidad: código SQL (Primero-Sin-IA).** Escribirás tres queries contra una base de cuentas y transacciones. El corazón del ejercicio es reescribir "lo último por grupo" como una window function y **defender por qué reemplaza al self-join**.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.2` Queries avanzadas
**Ruta:** crítica · **Timebox:** 45 min

## Objetivos

- **O1** — Escribir una window function de **agregación** (`SUM OVER`) que calcule un saldo acumulado por grupo **sin colapsar las filas**.
- **O2** — Resolver "la transacción más reciente de cada cuenta" con `ROW_NUMBER()` filtrado en una subquery/CTE.
- **O3** — Explicar **por qué** la versión window reemplaza al self-join O(n²) (una pasada ordenada vs re-escaneo por fila).

## La base (en `esquema.sql`)

```sql
-- cuentas
id | titular
 1 | Ana
 2 | Beto
 3 | Cora

-- transacciones (monto: positivo = ingreso, negativo = gasto)
 id | cuenta_id | fecha      | monto
  1 |     1     | 2026-01-02 |  100
  2 |     1     | 2026-01-05 |  -30
  3 |     1     | 2026-01-10 |   50
  4 |     2     | 2026-01-03 |  200
  5 |     2     | 2026-01-08 |  -50
  6 |     3     | 2026-01-04 |   80
```

## Tu tarea (Primero-Sin-IA, en este orden)

1. Piensa **el contrato** de cada query antes de escribirla: ¿qué columnas salen, cuántas filas, en qué orden?
2. Escribe las tres queries en `consultas.sql`, cada una etiquetada con `-- A`, `-- B`, `-- C`.
3. Cárgalas y verifica contra los **resultados esperados** de abajo.
4. Completa `NOTAS.md`.

### A) Saldo acumulado por cuenta (sin colapsar filas)

Cada transacción con su `saldo_corriente`: la suma de **esa cuenta** desde su primera transacción hasta la fila actual, ordenado por fecha. Deben salir las **6 filas**. Usa una window function de agregación.

### B) La transacción más reciente de cada cuenta

El `id`, `cuenta_id`, `fecha` y `monto` de la transacción de **fecha máxima** de cada cuenta. Primero piénsala con un self-join o subquery correlacionada (la forma "obvia"); luego **entrega la versión con `ROW_NUMBER()`**, filtrada en una subquery o CTE (`WHERE rn = 1` **afuera**).

### C) Cada transacción con el monto de la anterior

Columnas `cuenta_id`, `fecha`, `monto`, `monto_anterior`: el monto de la transacción **anterior de la misma cuenta** (ordenadas por fecha). Usa `LAG`. La primera de cada cuenta tiene `monto_anterior` en NULL.

## Resultados esperados (para auto-verificación)

**A** — saldo corriente por cuenta:

| cuenta_id | fecha | monto | saldo_corriente |
|---|---|---|---|
| 1 | 2026-01-02 | 100 | 100 |
| 1 | 2026-01-05 | -30 | 70 |
| 1 | 2026-01-10 | 50 | 120 |
| 2 | 2026-01-03 | 200 | 200 |
| 2 | 2026-01-08 | -50 | 150 |
| 3 | 2026-01-04 | 80 | 80 |

**B** — la más reciente de cada cuenta:

| id | cuenta_id | fecha | monto |
|---|---|---|---|
| 3 | 1 | 2026-01-10 | 50 |
| 5 | 2 | 2026-01-08 | -50 |
| 6 | 3 | 2026-01-04 | 80 |

**C** — monto anterior (LAG):

| cuenta_id | fecha | monto | monto_anterior |
|---|---|---|---|
| 1 | 2026-01-02 | 100 | NULL |
| 1 | 2026-01-05 | -30 | 100 |
| 1 | 2026-01-10 | 50 | -30 |
| 2 | 2026-01-03 | 200 | NULL |
| 2 | 2026-01-08 | -50 | 200 |
| 3 | 2026-01-04 | 80 | NULL |

## Cómo correr

```bash
docker run --rm -e POSTGRES_PASSWORD=x -p 5433:5432 -d --name pg-ej postgres:16
sleep 4
docker exec -i pg-ej psql -U postgres < esquema.sql
docker exec -i pg-ej psql -U postgres < consultas.sql
docker rm -f pg-ej   # al terminar
```

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las tres queries corren sin error sobre `esquema.sql` y dan los resultados esperados.
- [ ] (A) conserva las 6 filas (no las colapsa) y el saldo de Ana es 100, 70, 120.
- [ ] (B) se entrega con `ROW_NUMBER()` filtrado **afuera** (subquery o CTE), no con `WHERE ROW_NUMBER()...`.
- [ ] `NOTAS.md` nombra el trade-off de costo (una pasada ordenada vs re-escaneo por fila) y lo liga al bucle anidado O(n²) de DSA.
- [ ] Puedes **explicar sin notas** por qué `WHERE rn = 1` no puede ir en el mismo nivel que calcula `rn`.

## Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **A:** `SUM(monto) OVER (PARTITION BY cuenta_id ORDER BY fecha)` — con `ORDER BY` dentro del `OVER`, el marco por defecto suma desde el inicio de la partición hasta la fila actual (total corriente).
- **B:** numera con `ROW_NUMBER() OVER (PARTITION BY cuenta_id ORDER BY fecha DESC)` en una subquery (o CTE), y afuera `WHERE rn = 1`.
- **C:** `LAG(monto) OVER (PARTITION BY cuenta_id ORDER BY fecha)`.

Es una pista, no la solución de referencia.

</details>

## Cómo pedir la corrección

> "Corrige `ejercicios/fase-3/window-vs-self-join/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-3/` — no la mires antes de intentarlo de verdad.
