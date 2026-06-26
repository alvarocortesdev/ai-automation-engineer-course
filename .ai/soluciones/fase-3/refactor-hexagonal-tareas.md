---
ejercicio_id: fase-3/refactor-hexagonal-tareas
fase: fase-3
sub_unidad: "3.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Refactor a dominio + puerto + adaptadores

> Verificada: las 17 pruebas (`test_dominio_sin_infra.py`, `test_contrato_repositorio.py`, `test_api.py`) pasan en verde contra esta implementación.

## `dominio.py` (puro — sin `fastapi` ni `sqlalchemy`)

```python
from dataclasses import dataclass
from typing import Protocol

MAX_PENDIENTES = 5


@dataclass
class Tarea:
    titulo: str
    completada: bool = False
    id: int | None = None


class LimiteTareasPendientes(Exception):
    pass


class RepositorioTareas(Protocol):
    def agregar(self, tarea: Tarea) -> Tarea: ...
    def obtener(self, id: int) -> Tarea | None: ...
    def listar(self) -> list[Tarea]: ...
    def contar_pendientes(self) -> int: ...


class ServicioTareas:
    def __init__(self, repo: RepositorioTareas) -> None:
        self._repo = repo

    def crear_tarea(self, titulo: str) -> Tarea:
        if self._repo.contar_pendientes() >= MAX_PENDIENTES:
            raise LimiteTareasPendientes(
                f"No se permiten mas de {MAX_PENDIENTES} tareas pendientes"
            )
        return self._repo.agregar(Tarea(titulo=titulo))

    def listar_tareas(self) -> list[Tarea]:
        return self._repo.listar()
```

## `adaptador_memoria.py`

```python
from dominio import Tarea


class RepositorioTareasMemoria:
    def __init__(self) -> None:
        self._items: list[Tarea] = []
        self._next_id = 1

    def agregar(self, tarea: Tarea) -> Tarea:
        tarea.id = self._next_id
        self._next_id += 1
        self._items.append(tarea)
        return tarea

    def obtener(self, id: int) -> Tarea | None:
        return next((t for t in self._items if t.id == id), None)

    def listar(self) -> list[Tarea]:
        return list(self._items)

    def contar_pendientes(self) -> int:
        return sum(1 for t in self._items if not t.completada)
```

## `adaptador_sqlalchemy.py` (traduce `TareaORM` ↔ `Tarea`)

```python
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from dominio import Tarea
from modelos import TareaORM


def _a_dominio(fila: TareaORM) -> Tarea:
    return Tarea(id=fila.id, titulo=fila.titulo, completada=fila.completada)


class RepositorioTareasSQLAlchemy:
    def __init__(self, session: Session) -> None:
        self._session = session

    def agregar(self, tarea: Tarea) -> Tarea:
        fila = TareaORM(titulo=tarea.titulo, completada=tarea.completada)
        self._session.add(fila)
        self._session.flush()          # asigna el id sin cerrar la transacción
        return _a_dominio(fila)

    def obtener(self, id: int) -> Tarea | None:
        fila = self._session.get(TareaORM, id)
        return _a_dominio(fila) if fila is not None else None

    def listar(self) -> list[Tarea]:
        return [_a_dominio(f) for f in self._session.scalars(select(TareaORM)).all()]

    def contar_pendientes(self) -> int:
        return self._session.scalar(
            select(func.count()).select_from(TareaORM).where(TareaORM.completada == False)  # noqa: E712
        ) or 0
```

## `api.py` (endpoint flaco; traduce excepción de dominio a 409)

```python
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from adaptador_sqlalchemy import RepositorioTareasSQLAlchemy
from dominio import LimiteTareasPendientes, RepositorioTareas, ServicioTareas

engine = create_engine("postgresql+psycopg://usuario:clave@localhost/tareas")
app = FastAPI()


def obtener_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
        session.commit()


def obtener_repo(
    session: Annotated[Session, Depends(obtener_session)],
) -> RepositorioTareas:
    return RepositorioTareasSQLAlchemy(session)


RepoTareas = Annotated[RepositorioTareas, Depends(obtener_repo)]


class CrearTareaIn(BaseModel):
    titulo: str


class TareaOut(BaseModel):
    id: int
    titulo: str
    completada: bool


@app.post("/tareas", status_code=201, response_model=TareaOut)
def crear_tarea(payload: CrearTareaIn, repo: RepoTareas) -> TareaOut:
    servicio = ServicioTareas(repo)
    try:
        tarea = servicio.crear_tarea(payload.titulo)
    except LimiteTareasPendientes as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return TareaOut(id=tarea.id, titulo=tarea.titulo, completada=tarea.completada)


@app.get("/tareas", response_model=list[TareaOut])
def listar_tareas(repo: RepoTareas) -> list[TareaOut]:
    return [
        TareaOut(id=t.id, titulo=t.titulo, completada=t.completada)
        for t in ServicioTareas(repo).listar_tareas()
    ]
```

> Nota: en producción el `engine` apunta a Postgres; el `test_api.py` jamás lo toca porque `dependency_overrides` reemplaza `obtener_repo` por el doble en memoria. Para correr la app de verdad contra SQLite local basta cambiar la URL a `sqlite:///tareas.db` y llamar `Base.metadata.create_all(engine)` al arrancar.

## Mini-ADR esperado en `bitacora.md`
- **Decisión:** introducir el puerto `RepositorioTareas` para la persistencia, con dos adaptadores (memoria y SQLAlchemy).
- **Contexto:** la regla "máx. 5 pendientes" debe testearse sin levantar una DB; la persistencia es un punto de cambio plausible.
- **Consecuencia:** un adaptador extra y un mapeo `TareaORM`↔`Tarea`. A cambio, tests en milisegundos y libertad de cambiar de backend.
- **Qué NO lleva puerto (light):** la validación del `titulo` (Pydantic en el borde HTTP), el mapeo a `TareaOut`, o cualquier helper puro. Ponerles puerto sería ceremonia sin testabilidad ni cambio real en juego.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Entidad vs modelo ORM.** La referencia mantiene `Tarea` (dataclass) separada de `TareaORM`. Si el alumno usa `TareaORM` como entidad y lo importa en `dominio.py`, el test de pureza falla; si lo importa solo en el adaptador pero lo devuelve al dominio, `test_agregar_devuelve_entidad_de_dominio` lo caza.
2. **`flush()` para el id.** Sin `flush()` (o `commit()`), `fila.id` es `None` tras `add`. La referencia usa `flush()` para no cerrar la transacción del test.
3. **Override con instancia compartida.** `lambda: fake` (misma instancia) vs `lambda: RepositorioTareasMemoria()` (nueva cada vez). Solo la primera hace persistir el estado entre requests; la segunda nunca alcanza el límite.
4. **Traducción de la excepción.** `LimiteTareasPendientes` → 409 en el endpoint. Si la dejan propagar, el test recibe 500.
5. **`Protocol` vs herencia.** Los adaptadores NO heredan de `RepositorioTareas`; cumplen por estructura. Aceptar también una solución con `ABC` + herencia (igualmente válida, más nominal).

## Rango de soluciones aceptables
- `selectinload`/eager no aplica aquí; cualquier implementación correcta del contrato pasa.
- Usar `ABC` + `@abstractmethod` en vez de `Protocol` → ✅ válido (los adaptadores heredarían).
- `commit()` en lugar de `flush()` en el adaptador → ✅ funciona (el test usa la sesión abierta).
- Devolver `TareaORM`/dict al dominio → ❌ rompe el contrato (test lo caza).
- Dejar la regla de negocio en el endpoint → ❌ no cumple O1 (no es testeable sin HTTP).
- ❌ **No aceptable como competente:** dominio que importa infra, o un solo adaptador.
