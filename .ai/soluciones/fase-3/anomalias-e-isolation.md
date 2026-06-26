---
ejercicio_id: fase-3/anomalias-e-isolation
fase: fase-3
sub_unidad: "3.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnosticar anomalías y elegir el isolation level

## Respuesta canónica por escenario

### Escenario 1 — Reporte que no cuadra
- **Anomalía:** **non-repeatable read**. A lee `saldo = 1000`; B transfiere y confirma; A vuelve a leer la **misma fila** y obtiene `0`. Dos lecturas de la misma fila dentro de una transacción dan valores distintos.
- **¿`READ COMMITTED`?** Sí, ocurre (cada `SELECT` ve lo último confirmado al momento de ejecutarse).
- **¿`REPEATABLE READ`?** No ocurre: el snapshot se fija al inicio de la transacción de A, así que ambas lecturas devuelven `1000`.
- **Solución mínima:** `REPEATABLE READ`.
- **Trade-off:** A lee datos "viejos" (consistentes con su snapshot) y puede chocar con `40001` si intentara **escribir** una fila que cambió; para un reporte de solo lectura, el costo es despreciable.

### Escenario 2 — El último ticket
- **Anomalía:** **lost update**. Ambas sesiones leen `stock = 1`, calculan `0` **en la aplicación**, y ambas escriben `0`. Se vendieron 2 tickets habiendo 1.
- **¿`READ COMMITTED`?** Sí, ocurre (el bug silencioso por defecto).
- **¿`REPEATABLE READ`?** El lost update silencioso NO ocurre, pero a cambio la segunda transacción que escribe la fila ya modificada **aborta con `40001`** y debe reintentarse.
- **Solución mínima:** la **aritmética atómica** `UPDATE eventos SET stock = stock - 1 WHERE id = 1 AND stock > 0` resuelve sin subir el nivel ni tomar locks explícitos. Si la lógica necesita leer y decidir en la app, `SELECT ... FOR UPDATE`.
- **Trade-off:** la aritmética atómica es la más barata (un statement, sin reintentos). `FOR UPDATE` serializa el acceso a la fila (menos paralelismo, riesgo de deadlock si hay varias filas). Subir a `REPEATABLE READ` obliga a un loop de reintento.

### Escenario 3 — Los dos médicos de turno
- **Anomalía:** **write skew**. Ana y Beto leen `count = 2` ("hay otro de turno, puedo irme"), y cada uno actualiza una fila **distinta**. No se pisan, pero juntos dejan `count = 0`, violando la invariante "al menos 1 de turno".
- **¿`READ COMMITTED`?** Sí, ocurre.
- **¿`REPEATABLE READ`?** **También ocurre** — cada uno tocó una fila distinta, así que no hay conflicto de actualización que dispare `40001`. `REPEATABLE READ` NO protege del write skew.
- **Solución mínima:** **`SERIALIZABLE`**. SSI detecta la dependencia read/write cruzada y aborta una de las dos con `40001`; al reintentar, esa transacción ve `count = 1` y ya no se da de baja.
- **Trade-off:** `SERIALIZABLE` exige un loop de reintento y tiene algo más de overhead de seguimiento; es el precio de la correctitud cuando la regla cruza varias filas. (Alternativa sin subir nivel: tomar un lock explícito sobre una fila "guardiana", o `SELECT ... FOR UPDATE` sobre todos los médicos de turno — más manual y propenso a error.)

## Razonamiento paso a paso (lo que delata comprensión)
1. El alumno debe separar **lost update** (misma fila, se pisan) de **write skew** (filas distintas, invariante cruzada). Es la distinción clave de la lección.
2. Debe saber que en Postgres `REPEATABLE READ` ya elimina non-repeatable **y** phantom (más estricto que el estándar), pero **no** el write skew.
3. Debe reconocer que subir el isolation level no es "transparente": cambia un bug silencioso por un `40001` que la app maneja.
4. Debe preferir la solución **mínima**: aritmética atómica antes que `FOR UPDATE` antes que subir el nivel, cuando bastan.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Escenario 2 con aritmética en la DB vs en la app.** Si el escenario hiciera `UPDATE ... SET stock = stock - 1` (aritmética en la DB) en vez de calcular `0` en la app, bajo `READ COMMITTED` **no** habría lost update (el `UPDATE` re-evalúa sobre el valor confirmado). El enunciado especifica "la app calcula", así que sí hay lost update. Un alumno fino puede notar esta diferencia — es excelente, no error.
2. **Escenario 3 y `REPEATABLE READ`.** El error más común es decir que `REPEATABLE READ` lo arregla. No: filas distintas, sin conflicto de actualización. Solo `SERIALIZABLE`.
3. **"Mínimo" no es "máximo por si acaso".** Responder `SERIALIZABLE` a los tres es técnicamente correcto pero falla O3 (no es el mínimo, y paga reintentos donde no hacían falta).

## Rango de soluciones aceptables
- **Escenario 1:** `REPEATABLE READ` o `SERIALIZABLE` evitan el non-repeatable; `REPEATABLE READ` es el mínimo. Ambos aceptables si justifica por qué eligió.
- **Escenario 2:** aritmética atómica, `FOR UPDATE`, o subir a `REPEATABLE READ`/`SERIALIZABLE` con retry — todos válidos; la aritmética atómica es la "mejor" por simplicidad, pero cualquiera bien justificado es competente.
- **Escenario 3:** `SERIALIZABLE` (canónico). Un lock explícito que serialice a los médicos de turno (`FOR UPDATE` sobre el `SELECT count`-equivalente con las filas) también es aceptable si está bien razonado; es más frágil.
- ❌ **No aceptable:** afirmar que `REPEATABLE READ` arregla el escenario 3, o que `READ COMMITTED` evita el non-repeatable del escenario 1.
