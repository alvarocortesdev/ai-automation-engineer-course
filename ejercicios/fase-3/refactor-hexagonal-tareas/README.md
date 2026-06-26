# Ejercicio 3.9 — Refactor: desacopla un endpoint en dominio + puerto + adaptadores

> **Modalidad: código (Python + FastAPI + SQLAlchemy 2.0, sin IA).** Tomas una API de tareas
> acoplada (HTTP + negocio + DB en una sola función) y la refactorizas a hexagonal *light*: dominio
> puro, un puerto, dos adaptadores intercambiables. SQLite **en memoria** para el adaptador SQLAlchemy:
> no necesitas Postgres ni configurar nada.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.9` Ports & adapters / hexagonal light
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Refactorizar `app_acoplado.py` en cuatro piezas con dependencias que apuntan **hacia** el dominio, de
modo que (1) el dominio no importe infraestructura, (2) el mismo puerto tenga dos adaptadores
intercambiables, y (3) la regla de negocio se pueda testear **sin levantar una base de datos**.

## 📋 Contexto

Cada endpoint del capstone que aplique una regla de negocio sobre datos persistidos corre el riesgo de
quedar acoplado al ORM y al framework HTTP: imposible de testear sin DB, imposible de cambiar de
infraestructura sin reescribir. Desacoplarlo con un puerto es lo que vuelve tu backend testeable en
segundos y lo que un reviewer (o un entrevistador preguntando "¿cómo testeas esto sin la base de
datos?") espera de un semi-senior.

## ⚙️ Requisitos

```bash
uv add fastapi "sqlalchemy>=2.0" httpx pytest      # o:  pip install fastapi "sqlalchemy>=2.0" httpx pytest
```

(`httpx` lo necesita `TestClient` de FastAPI; SQLite viene con Python.)

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Empieza leyendo `app_acoplado.py` y `corre` la versión
   acoplada mentalmente: ¿qué tres trabajos hace ese endpoint? Marcar las costuras es medio ejercicio.
2. Solo entonces, consulta la **documentación oficial** (FastAPI — *Dependencies* y *Testing
   Dependencies with Overrides*; `typing.Protocol`).
3. **Solo al final**, usa IA para *revisar* tu refactor y tu ADR — no para generarlos.
4. Mañana, reescribe de memoria el puerto, el servicio y el test sin DB.

## La regla de negocio (no la cambies al refactorizar)

> Al crear una tarea, si ya existen **5 tareas pendientes** (no completadas), la creación se rechaza.

En la app acoplada esa regla está enredada con SQL y `HTTPException`. Tu trabajo es **moverla al
dominio**, intacta, y dejar que el endpoint solo traduzca el error a HTTP.

## 🛠️ El contrato a implementar (esto es la spec — respétalo, los tests dependen de los nombres)

### `dominio.py` (PURO: prohibido importar `fastapi` o `sqlalchemy`)

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
    """Error de dominio: se intentó crear una tarea con el cupo de pendientes lleno."""

class RepositorioTareas(Protocol):          # el PUERTO de salida
    def agregar(self, tarea: Tarea) -> Tarea: ...   # devuelve la tarea con id asignado
    def obtener(self, id: int) -> Tarea | None: ...
    def listar(self) -> list[Tarea]: ...
    def contar_pendientes(self) -> int: ...

class ServicioTareas:                        # el CASO DE USO
    def __init__(self, repo: RepositorioTareas) -> None: ...
    def crear_tarea(self, titulo: str) -> Tarea: ...   # aplica la regla; lanza LimiteTareasPendientes
    def listar_tareas(self) -> list[Tarea]: ...
```

### `adaptador_memoria.py`

```python
class RepositorioTareasMemoria:   # cumple RepositorioTareas, sin DB (para tests)
    ...
```

### `adaptador_sqlalchemy.py`

```python
class RepositorioTareasSQLAlchemy:   # cumple RepositorioTareas usando modelos.py
    def __init__(self, session: Session) -> None: ...
```

`modelos.py` ya define `TareaORM` (el modelo SQLAlchemy) y `Base`. **No lo toques.** Recuerda: la
entidad de dominio `Tarea` **no es** `TareaORM`; tu adaptador traduce entre ambas.

### `api.py`

```python
app = FastAPI()
def obtener_repo(...) -> RepositorioTareas: ...   # punto único de cableado del adaptador
@app.post("/tareas", status_code=201): ...        # crea; 409 si viola la regla
@app.get("/tareas"): ...                           # lista
```

El endpoint pide el **puerto** (`RepositorioTareas`), no el adaptador concreto. La excepción de dominio
`LimiteTareasPendientes` se traduce a **409** aquí (el dominio no sabe qué es un status code).

## 🧪 Qué verifican los tests

1. `test_dominio_sin_infra.py` — escanea los imports de `dominio.py` y **falla si aparece `fastapi` o
   `sqlalchemy`** (pureza); además ejercita la regla de negocio con un doble en memoria, **sin DB**.
2. `test_contrato_repositorio.py` — corre el **mismo** set de pruebas contra `RepositorioTareasMemoria`
   y `RepositorioTareasSQLAlchemy` (SQLite en memoria) → demuestra que son intercambiables.
3. `test_api.py` — usa `app.dependency_overrides[obtener_repo]` para inyectar el doble y comprueba que
   la 6ª tarea pendiente rebota con **409** por HTTP.

```bash
uv run pytest        # o:  pytest
```

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: pureza + regla de negocio + contrato de ambos adaptadores + endpoint.
- [ ] `dominio.py` **no importa** `fastapi` ni `sqlalchemy` (lo verifica el test, no tu palabra).
- [ ] La entidad `Tarea` del dominio es distinta del modelo `TareaORM`; el adaptador traduce entre ambas.
- [ ] El endpoint pide el **puerto**; el adaptador concreto se elige en un único lugar (`obtener_repo`).
- [ ] `bitacora.md` con un **mini-ADR**: por qué pusiste un puerto en la persistencia y qué NO le pusiste
      puerto (y por qué sería sobre-ingeniería).
- [ ] Puedes explicar **sin notas** en qué dirección apuntan las dependencias y por qué el endpoint pide
      el puerto, no el adaptador.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **Dominio:** `ServicioTareas.crear_tarea` solo usa el puerto: `if self._repo.contar_pendientes() >= MAX_PENDIENTES: raise LimiteTareasPendientes(...)`, luego `self._repo.agregar(Tarea(titulo=titulo))`. Cero SQL, cero HTTP.
- **Adaptador memoria:** una `list[Tarea]` y un contador de ids. `agregar` asigna `tarea.id`, lo guarda y lo devuelve.
- **Adaptador SQLAlchemy:** `agregar` crea un `TareaORM`, `session.add(...)`, `session.flush()` (asigna el id), y devuelve `Tarea(id=fila.id, titulo=fila.titulo, completada=fila.completada)`. `contar_pendientes` = `session.scalar(select(func.count()).select_from(TareaORM).where(TareaORM.completada == False))`.
- **api.py:** `obtener_repo` devuelve el adaptador SQLAlchemy tipado como `RepositorioTareas`; el endpoint hace `servicio = ServicioTareas(repo)` y envuelve `crear_tarea` en `try/except LimiteTareasPendientes -> HTTPException(409)`.

Repasa las secciones 4.3–4.8 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu código (este directorio) + `bitacora.md`,
- la **rúbrica**: `.ai/rubricas/fase-3/refactor-hexagonal-tareas.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/refactor-hexagonal-tareas.md` — no la mires
antes de intentarlo de verdad.
