---
ejercicio_id: fase-3/cazar-n1
fase: fase-3
sub_unidad: "3.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Caza y mata el N+1 con eager loading

## Implementación canónica (`solucion.py`)

Estrategia recomendada: `selectinload` (la relación `Autor.libros` es **to-many** / colección).

```python
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from modelos import Autor


def listar_autores_con_libros(session: Session) -> list[dict]:
    autores = session.scalars(
        select(Autor).options(selectinload(Autor.libros))  # eager: 1 query extra con IN(...)
    ).all()
    return [
        {"autor": autor.nombre, "libros": [libro.titulo for libro in autor.libros]}
        for autor in autores
    ]
```

Ejecuta exactamente **2 queries** sin importar el número de autores: una `SELECT ... FROM autores` y una `SELECT ... FROM libros WHERE autor_id IN (...)`. Verificado contra `test_acceptance.py`: ambos tests en verde.

## Variante igualmente válida: `joinedload` (1 query)

```python
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from modelos import Autor


def listar_autores_con_libros(session: Session) -> list[dict]:
    autores = session.scalars(
        select(Autor).options(joinedload(Autor.libros))
    ).unique().all()   # .unique() OBLIGATORIO: joinedload de colección lo exige en 2.0
    return [
        {"autor": autor.nombre, "libros": [libro.titulo for libro in autor.libros]}
        for autor in autores
    ]
```

Ejecuta **1 query** (un `LEFT OUTER JOIN`). También pasa el test (≤ 2). El `.unique()` no es opcional: sin él, `session.scalars(...)` con `joinedload` de colección **lanza `InvalidRequestError`** en SQLAlchemy 2.0.

## Por qué la versión ingenua falla

```python
# ❌ N+1: 1 + N queries
autores = session.scalars(select(Autor)).all()           # 1 query
return [
    {"autor": a.nombre, "libros": [l.titulo for l in a.libros]}  # N queries (lazy, una por autor)
    for a in autores
]
```

Con 10 autores: 1 (autores) + 10 (un `SELECT libros WHERE autor_id = ?` por cada `a.libros`) = **11 queries**. `test_no_hay_n_mas_1` falla con "se ejecutaron 11 SELECTs". El `relationship` es lazy por defecto: cada acceso a `a.libros` materializa la colección con su propia query.

## Elección esperada en la bitácora
- **`selectinload`** es la respuesta de partida para colecciones: 2 queries fijas, no multiplica filas, escala parejo. Es lo que se espera por defecto.
- **`joinedload`** (1 query) es aceptable y correcto aquí (la colección es chica), siempre que use `.unique()`. Para colecciones grandes o varias relaciones anidadas, `selectinload` suele ganar (el JOIN ancho repite datos).
- La bitácora **competente** reporta el conteo medido: ingenua = 11, curada = 1 o 2.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`.unique()` con `joinedload` de colección.** Si el alumno usó `joinedload` sin `.unique()`, su test ni siquiera corre (lanza `InvalidRequestError`). Marca que debe encadenarlo.
2. **Eager por consulta, no global.** Configurar `lazy="selectin"` en el `relationship` del modelo "pasa" el test pero penaliza todas las consultas; el enunciado pide resolverlo en la **consulta** con `.options(...)`. Acéptalo como funcional pero señala el matiz.
3. **El acceso a `.libros` después de cerrar la sesión.** Si construyen los dicts fuera del `with Session(...)`, los objetos están expirados/detached. La referencia construye los dicts **dentro** de la sesión (o materializa con eager loading antes de salir). El test usa la sesión abierta, así que esto no falla el test, pero es un error a marcar si aparece.
4. **Diagnóstico por conteo, no por tiempo.** La bitácora debe hablar de número de queries, no de milisegundos.

## Rango de soluciones aceptables
- `selectinload(Autor.libros)` → ✅ recomendada.
- `joinedload(Autor.libros)` + `.unique()` → ✅ válida.
- Devolver objetos en vez de dicts → ❌ el test espera la estructura de dicts; debe cumplir el contrato.
- `lazy="selectin"` en el modelo → ⚠️ funciona pero no es lo pedido; competente con observación.
- ❌ **No aceptable como competente:** dejar lazy (N+1), o `joinedload` de colección sin `.unique()`.
