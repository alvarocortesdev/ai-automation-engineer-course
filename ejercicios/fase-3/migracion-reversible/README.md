# Ejercicio 3.4 — Escribe una migración reversible con backfill

> **Modalidad: código (Primero-Sin-IA).** Esto es una migración de verdad, en miniatura. Para que no
> tengas que instalar Alembic ni levantar Postgres, trabajas sobre `sqlite3` de la librería estándar
> de Python: la mecánica (cambiar esquema + mover datos + poder revertir) es **exactamente la misma**
> que la de una migración Alembic real.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.4` Migraciones de esquema
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

Implementar las dos mitades de una migración —`upgrade` y `downgrade`— que separan una columna
`nombre_completo` en `nombre` y `apellido`, **rellenando** (backfill) los datos existentes, y que se
puede **revertir** dejando la tabla idéntica a como estaba.

## 📋 Contexto

Toda app real evoluciona su esquema sin perder datos. Este es el patrón más común que vas a escribir:
agregar columnas y poblarlas desde lo que ya existe. Saber hacerlo reversible es lo que te deja dormir
tranquilo cuando una migración sale mal en staging. Alimenta directamente el Capstone F3 (API de
producción), que exige el esquema versionado con migraciones.

## El estado inicial

La tabla ya existe cuando tu migración corre (el test la crea):

```sql
CREATE TABLE usuarios (
    id              INTEGER PRIMARY KEY,
    nombre_completo TEXT NOT NULL
);
```

Con datos como: `"Ada Lovelace"`, `"Grace Murray Hopper"`, `"Cher"`.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox 35 min). Está bien que sea lento.
2. Solo entonces, consulta **documentación oficial** (`sqlite3`, `str.split`).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**.

## 🛠️ Instrucciones

1. Abre `migracion.py` e implementa `upgrade(conn)` y `downgrade(conn)` (no cambies sus firmas).
   - **`upgrade(conn)`**: agrega las columnas `nombre` y `apellido` a `usuarios`, y rellena sus
     valores desde `nombre_completo`. **Contrato del split**: la primera palabra es `nombre`; el resto
     (si lo hay) es `apellido`; si no hay resto, `apellido = ""`.
     - `"Ada Lovelace"` → `nombre="Ada"`, `apellido="Lovelace"`
     - `"Grace Murray Hopper"` → `nombre="Grace"`, `apellido="Murray Hopper"`
     - `"Cher"` → `nombre="Cher"`, `apellido=""`
   - **`downgrade(conn)`**: deja la tabla **exactamente** como estaba (solo `id` y `nombre_completo`,
     con sus datos intactos). No toques `nombre_completo` en ningún momento.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos pasen en verde** (incluido el test de round-trip).
4. Añade al menos **un caso de prueba tuyo** en `test_migracion.py` (un nombre borde: ¿espacios
   dobles?, ¿string con solo espacios?, ¿un nombre con tres palabras?).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` pasa en verde, incluido el round-trip (`upgrade` → `downgrade` deja la tabla idéntica).
- [ ] El backfill maneja el caso de un solo nombre sin apellido (`apellido = ""`).
- [ ] El `downgrade` no pierde ni altera `nombre_completo`.
- [ ] Agregaste al menos un test propio con un caso borde.
- [ ] Puedes **explicar sin notas** por qué `upgrade` agrega las columnas antes de rellenarlas.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`upgrade` tiene dos fases en orden: primero `ALTER TABLE usuarios ADD COLUMN nombre TEXT` (y otro para
`apellido`), **luego** un `SELECT id, nombre_completo FROM usuarios` y, por cada fila, un
`UPDATE usuarios SET nombre = ?, apellido = ? WHERE id = ?`. Para partir el nombre,
`str.split(None, 1)` divide en la primera racha de espacios y devuelve una lista de 1 o 2 elementos
(maneja gratis el caso "sin apellido"). Para `downgrade`, `ALTER TABLE usuarios DROP COLUMN nombre`
(existe en SQLite 3.35+, incluido en Python 3.12+). Recuerda hacer `conn.commit()`.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/migracion-reversible.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/migracion-reversible.md` — no la mires
antes de intentarlo de verdad.
