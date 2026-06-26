# Ejercicio 3.5 — Caza y mata el N+1 con eager loading

> **Modalidad: código (Python + SQLAlchemy 2.0, sin IA).** El antipatrón #1 de los ORMs —disparar una query por cada resultado— diagnosticado contando queries y resuelto con eager loading. SQLite **en memoria**: no necesitas Postgres ni configurar nada.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.5` ORMs y el problema N+1
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

Implementar `listar_autores_con_libros(session)` para que devuelva cada autor con los títulos de sus libros **sin caer en el N+1**: a lo más **2 queries**, sin importar cuántos autores haya. Y justificar por escrito si elegiste `joinedload` o `selectinload` y por qué.

## 📋 Contexto

Cada endpoint del capstone que liste recursos con sus relaciones (pedidos con cliente, autor con libros, carrito con items) corre el riesgo de un N+1. Es el bug que no se nota con 10 filas de prueba y mata la API con 10.000 en producción. Saber diagnosticarlo (contando queries) y curarlo (eager loading) es exactamente lo que un reviewer mira primero —y una pregunta de entrevista de backend casi garantizada.

## ⚙️ Requisitos

Solo necesitas SQLAlchemy y pytest (la base es SQLite **en memoria**, incluida en Python):

```bash
uv add "sqlalchemy>=2.0" pytest      # o:  pip install "sqlalchemy>=2.0" pytest
```

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Implementa primero la versión **ingenua** (lazy) y **mira el test fallar** por exceso de queries: ver el bug es parte del aprendizaje.
2. Solo entonces, consulta la **documentación oficial** (SQLAlchemy 2.0 — Relationship Loading Techniques).
3. **Solo al final**, usa IA para *revisar* tu solución y tu bitácora — no para generarlas.
4. Mañana, reescribe de memoria la versión curada.

## 🛠️ Instrucciones

1. Abre `solucion.py` e implementa `listar_autores_con_libros(session)` **sin cambiar la firma**. Debe devolver:

   ```python
   [{"autor": "Autor 0", "libros": ["Libro 0-0", "Libro 0-1", "Libro 0-2"]}, ...]
   ```

2. `modelos.py` ya define `Autor`/`Libro` (uno-a-muchos, relación lazy). No lo toques.
3. Corre el test:

   ```bash
   uv run pytest        # o:  pytest
   ```

   `test_datos_correctos` verifica la estructura y los datos. `test_no_hay_n_mas_1` **cuenta las queries** con un event listener y exige ≤ 2.
4. Escribe `bitacora.md`: qué estrategia elegiste (`joinedload` o `selectinload`), **por qué**, y cuántas queries ejecuta la versión ingenua frente a la curada.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: datos correctos **y** conteo de queries ≤ 2.
- [ ] Usaste eager loading explícito (`selectinload` o `joinedload` con `.unique()` si es colección), no lazy.
- [ ] `bitacora.md` justifica la elección y reporta el conteo ingenua (1+N) vs curada (≤ 2).
- [ ] Puedes explicar **sin notas** por qué la versión lazy dispara 1+N queries y en qué línea exacta nace cada query extra.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El N+1 nace cuando accedes a `autor.libros` dentro del bucle: cada acceso a una relación **lazy** dispara su propia query. La cura es pedir la relación **por adelantado** en el `select`:

- `select(Autor).options(selectinload(Autor.libros))` → 2 queries (una de autores, una de libros con `WHERE autor_id IN (...)`). Ideal para colecciones (to-many).
- `select(Autor).options(joinedload(Autor.libros))` → 1 query (un `LEFT JOIN`), pero **debes** encadenar `.unique()` antes de `.all()` o SQLAlchemy 2.0 lanza `InvalidRequestError`.

Repasa la sección 4.6–4.8 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `solucion.py` + `bitacora.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/cazar-n1.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/cazar-n1.md` — no la mires antes de intentarlo de verdad.
