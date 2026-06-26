---
ejercicio_id: fase-3/migracion-reversible
fase: fase-3
sub_unidad: "3.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Escribe una migración reversible con backfill

## Respuesta canónica

```python
import sqlite3


def upgrade(conn: sqlite3.Connection) -> None:
    # 1) ESQUEMA: agrega las columnas (nullable; aún vacías).
    conn.execute("ALTER TABLE usuarios ADD COLUMN nombre TEXT")
    conn.execute("ALTER TABLE usuarios ADD COLUMN apellido TEXT")

    # 2) DATOS: backfill desde nombre_completo.
    filas = conn.execute("SELECT id, nombre_completo FROM usuarios").fetchall()
    for id_, completo in filas:
        partes = (completo or "").split(None, 1)   # 1 o 2 elementos
        nombre = partes[0] if partes else ""
        apellido = partes[1] if len(partes) > 1 else ""
        conn.execute(
            "UPDATE usuarios SET nombre = ?, apellido = ? WHERE id = ?",
            (nombre, apellido, id_),
        )
    conn.commit()


def downgrade(conn: sqlite3.Connection) -> None:
    # Reversible porque nombre_completo nunca se tocó: basta quitar lo nuevo.
    conn.execute("ALTER TABLE usuarios DROP COLUMN nombre")
    conn.execute("ALTER TABLE usuarios DROP COLUMN apellido")
    conn.commit()
```

Verificado: pasa los 8 tests de `test_migracion.py` (Python 3.12 / SQLite 3.51).

## Razonamiento paso a paso

1. **El orden es ley.** `upgrade` hace primero el cambio de **esquema** (`ADD COLUMN`) y después la migración de **datos** (`SELECT` + `UPDATE`). Invertirlo da `sqlite3.OperationalError: no such column: nombre`. Esta separación esquema→datos es exactamente la de una migración Alembic real.
2. **`split(None, 1)` es la pieza clave.** Dividir en la *primera* racha de espacios (`None` = cualquier whitespace, `1` = como máximo un corte) devuelve una lista de 1 o 2 elementos: maneja gratis los nombres de una sola palabra y los apellidos compuestos ("Murray Hopper"), y colapsa espacios dobles. `split(" ")` o `split(" ")[1]` rompen estos casos.
3. **`apellido = ""` y no `None`.** El contrato pide string vacío para el caso sin apellido; el test lo verifica explícitamente. Un `None` (NULL) fallaría `test_upgrade_apellido_vacio_no_es_null`.
4. **El `downgrade` es reversible *porque no destruimos nada*.** `nombre_completo` permanece intacto durante toda la migración, así que revertir es simplemente quitar las dos columnas derivadas. Los datos originales nunca se perdieron.
5. **`commit()`** en ambas funciones: sin él, en un flujo real los cambios no se persisten y los tests serían intermitentes.

## Por qué este ejercicio enseña lo que enseña

- **Borrar la columna vieja sería el error grave.** Si `upgrade` hiciera `DROP COLUMN nombre_completo`, el `downgrade` sería **imposible de hacer fiel**: no se reconstruye "Ada Lovelace" desde "Ada" + "Lovelace" sin asumir el separador, y se perderían los espacios/casos originales. En una migración real, el borrado de la columna vieja se difiere a una migración *posterior* (la fase **contract** de expand/contract), nunca en la misma que rellena.
- **Tabla "ligera" vs. modelo real.** En Alembic, este mismo backfill se escribe con `op.get_bind()` y una `sa.table(...)` ad-hoc (no el modelo vivo), por la misma razón por la que aquí usamos SQL directo: la migración congela el esquema de su momento histórico.

## Rango de soluciones aceptables

- Usar `executemany` para los `UPDATE`, o un único `UPDATE ... SET nombre = substr(...)` con funciones SQL de string, es **válido** si el resultado pasa los tests (aunque hacerlo en Python es más legible aquí).
- Hacer un `for` con `conn.execute(...)` o construir una lista de tuplas y `executemany` son equivalentes.
- En `downgrade`, el orden de los dos `DROP COLUMN` da igual.
- Llamar `commit` una sola vez al final de cada función es suficiente (no hace falta por fila).
- **Variante de control para detectar dependencia-IA:** pedir que prediga la salida si se invierte el orden (UPDATE antes de ADD COLUMN). La respuesta correcta es "falla con no such column". Quien copió de la IA suele no anticiparlo.

## Test propio esperado (ejemplos de buen borde)

```python
def test_tres_palabras():
    conn = _db_inicial()
    conn.execute("INSERT INTO usuarios (id, nombre_completo) VALUES (9, 'Juan Carlos Pérez')")
    conn.commit()
    upgrade(conn)
    fila = conn.execute("SELECT nombre, apellido FROM usuarios WHERE id = 9").fetchone()
    assert fila == ("Juan", "Carlos Pérez")   # primera palabra = nombre, resto = apellido
```

Otros bordes válidos: espacios dobles (`"Margaret  Hamilton"` → `("Margaret", "Hamilton")`), o un valor solo-espacios (que con `split(None, 1)` da `nombre=""`, `apellido=""`).
