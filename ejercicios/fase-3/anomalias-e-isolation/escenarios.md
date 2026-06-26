# Escenarios a analizar

> Tres entrelazados de dos sesiones concurrentes (A y B) sobre una base de Postgres.
> Los pasos están en **orden temporal**: la línea de más arriba ocurre primero.
> Tablas usadas:
>
> - `cuentas(id, saldo)` — saldo en pesos enteros.
> - `eventos(id, stock)` — tickets disponibles.
> - `turnos(medico_id, de_turno)` — `de_turno` es booleano; **invariante de negocio: siempre debe haber al menos 1 médico con `de_turno = true`.**
>
> Para cada escenario: nombra la anomalía, di si ocurre bajo `READ COMMITTED` y bajo `REPEATABLE READ`, elige el nivel/técnica mínimo que la resuelve, y justifica el trade-off. Escribe tus respuestas en `analisis.md`.

---

## Escenario 1 — Reporte que no cuadra

Estado inicial: `cuentas` tiene id=1 con saldo=1000 y id=2 con saldo=0.

```text
A: BEGIN;
A:   SELECT saldo FROM cuentas WHERE id = 1;         -- lee 1000
B: BEGIN;
B:   UPDATE cuentas SET saldo = saldo - 1000 WHERE id = 1;
B:   UPDATE cuentas SET saldo = saldo + 1000 WHERE id = 2;
B: COMMIT;
A:   SELECT saldo FROM cuentas WHERE id = 1;         -- ¿qué lee ahora?
A: COMMIT;
```

Pregunta clave: dentro de la transacción de A, las dos lecturas de la misma fila ¿dan el mismo valor?

---

## Escenario 2 — El último ticket

Estado inicial: `eventos` tiene id=1 con stock=1. El código de cada sesión hace la lógica **en la aplicación**.

```text
A: BEGIN;
A:   SELECT stock FROM eventos WHERE id = 1;         -- lee 1
B: BEGIN;
B:   SELECT stock FROM eventos WHERE id = 1;         -- lee 1
A:   -- la app calcula 1 - 1 = 0
A:   UPDATE eventos SET stock = 0 WHERE id = 1;
A: COMMIT;
B:   -- la app calcula 1 - 1 = 0  (con el valor que leyó antes)
B:   UPDATE eventos SET stock = 0 WHERE id = 1;
B: COMMIT;
```

Pregunta clave: ¿cuántos tickets se vendieron y cuántos había?

---

## Escenario 3 — Los dos médicos de turno

Estado inicial: `turnos` tiene a Ana (`medico_id=1, de_turno=true`) y a Beto (`medico_id=2, de_turno=true`). La regla: cada uno puede darse de baja **solo si queda al menos otro de turno**. Ambos quieren irse a la vez.

```text
A: BEGIN;
A:   SELECT count(*) FROM turnos WHERE de_turno = true;   -- Ana lee 2 -> "hay otro, puedo irme"
B: BEGIN;
B:   SELECT count(*) FROM turnos WHERE de_turno = true;   -- Beto lee 2 -> "hay otro, puedo irme"
A:   UPDATE turnos SET de_turno = false WHERE medico_id = 1;
A: COMMIT;
B:   UPDATE turnos SET de_turno = false WHERE medico_id = 2;
B: COMMIT;
```

Pregunta clave: cada `UPDATE` toca una fila **distinta**, así que no se pisan. ¿Se respetó la invariante de "al menos 1 de turno"? ¿Qué isolation level lo habría impedido?
