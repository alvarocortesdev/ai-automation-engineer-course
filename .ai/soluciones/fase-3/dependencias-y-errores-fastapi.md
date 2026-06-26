---
ejercicio_id: fase-3/dependencias-y-errores-fastapi
fase: fase-3
sub_unidad: "3.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Dependencias, errores globales y background tasks

## Implementación canónica (`app.py`)

```python
from __future__ import annotations

from typing import Annotated

from fastapi import (
    BackgroundTasks, Depends, FastAPI, Header, HTTPException, Query, status,
)
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel

app = FastAPI(title="API de notas")

API_KEY = "secreto-demo"
_NOTAS: dict[int, dict] = {}
_siguiente_id = 1
_AUDITORIA: list[str] = []


class NotaCrear(BaseModel):
    titulo: str
    cuerpo: str


class NotaPublica(BaseModel):
    id: int
    titulo: str
    cuerpo: str


class RecursoNoEncontrado(Exception):
    def __init__(self, recurso: str, id_: int) -> None:
        self.recurso = recurso
        self.id = id_


def registrar_auditoria(mensaje: str) -> None:
    _AUDITORIA.append(mensaje)


def obtener_api_key(x_api_key: Annotated[str | None, Header()] = None) -> str:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="api-key inválida")
    return x_api_key


def parametros_paginacion(
    saltar: Annotated[int, Query(ge=0)] = 0,
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict[str, int]:
    return {"saltar": saltar, "limite": limite}


ApiKeyDep = Annotated[str, Depends(obtener_api_key)]
PaginacionDep = Annotated[dict[str, int], Depends(parametros_paginacion)]


@app.exception_handler(RecursoNoEncontrado)
async def manejar_no_encontrado(request: Request, exc: RecursoNoEncontrado):
    return JSONResponse(
        status_code=404,
        content={"error": "no_encontrado", "recurso": exc.recurso, "id": exc.id},
    )


@app.get("/notas", response_model=list[NotaPublica])
async def listar_notas(api_key: ApiKeyDep, paginacion: PaginacionDep) -> list[dict]:
    notas = [_NOTAS[k] for k in sorted(_NOTAS)]
    inicio = paginacion["saltar"]
    return notas[inicio : inicio + paginacion["limite"]]


@app.get("/notas/{nota_id}", response_model=NotaPublica)
async def obtener_nota(nota_id: int, api_key: ApiKeyDep) -> dict:
    nota = _NOTAS.get(nota_id)
    if nota is None:
        raise RecursoNoEncontrado("nota", nota_id)
    return nota


@app.post("/notas", response_model=NotaPublica, status_code=status.HTTP_201_CREATED)
async def crear_nota(datos: NotaCrear, api_key: ApiKeyDep, tareas: BackgroundTasks) -> dict:
    global _siguiente_id
    nota = {"id": _siguiente_id, "titulo": datos.titulo, "cuerpo": datos.cuerpo}
    _NOTAS[_siguiente_id] = nota
    tareas.add_task(registrar_auditoria, f"nota creada: {_siguiente_id}")
    _siguiente_id += 1
    return nota
```

Verificado contra `test_app.py`: **6 passed**.

## Por qué cada decisión

- **`obtener_api_key` como dependencia** — el header `x-api-key` llega como `x_api_key` (FastAPI convierte `-`→`_`). Inyectarla (no leerla con `request.headers.get`) permite sustituirla en tests con `app.dependency_overrides[obtener_api_key] = ...`. El `!=` con `raise HTTPException(401)` cubre tanto "falta" (None) como "incorrecta".
- **401, no 403** — el ejercicio prueba *autenticación* (no hay credencial válida) = 401. 403 sería "autenticado pero sin permiso".
- **Excepción de dominio + handler global** — `obtener_nota` lanza `RecursoNoEncontrado` (no sabe de HTTP); el handler la traduce a 404 con la forma JSON exacta. Esto desacopla el dominio del transporte (semilla de `3.9`). **Sin el handler registrado, el `raise` da 500**, no 404 — el test `test_obtener_inexistente_usa_handler_custom` lo caza.
- **`tareas.add_task(registrar_auditoria, f"...")`** — se pasa la función **por referencia** con sus args; FastAPI la corre tras enviar la respuesta. `TestClient` ejecuta la tarea dentro del request, por eso `len(_AUDITORIA)` crece (+1) en el test.
- **Alias `ApiKeyDep`/`PaginacionDep`** — `Annotated[..., Depends(...)]` reutilizable: el mismo tipo en varios endpoints.

## Variantes aceptables
- `if x_api_key is None or x_api_key != API_KEY` (explícito): equivalente al `!=` (None nunca iguala la clave).
- Devolver la sesión/paginación como objeto pydantic en vez de dict: válido si los endpoints lo consumen bien.
- Aplicar la auth con `dependencies=[Depends(obtener_api_key)]` en un `APIRouter` o en el decorador en vez de como parámetro: **válido y más limpio**, mientras el 401 salga.
- Endpoints `def` en vez de `async def`: aceptable (no hay I/O real).

## No aceptable como competente
- ❌ Lanzar `HTTPException(404)` en `obtener_nota` en vez de `RecursoNoEncontrado` + handler: traiciona O2 aunque el test de status pase. (El test compara el **cuerpo** `{"error":...}`, así que un `HTTPException` con `{"detail":...}` **falla** el test — buena red de seguridad.)
- ❌ Leer el header con `request.headers.get(...)` dentro de cada endpoint: no es dependencia, no testeable.
- ❌ `tareas.add_task(registrar_auditoria(...))` (llamada inline): ejecuta antes de responder y rompe el patrón.
- ❌ No registrar el handler (da 500).

## Puntos resbalosos (donde el corrector debe mirar)
1. **El cuerpo JSON exacto.** El test compara `== {"error": "no_encontrado", "recurso": "nota", "id": 999999}`. Cualquier otra forma (incluido `{"detail": ...}`) falla. Verifica que el handler arme ese dict.
2. **Orden de validación.** Con clave válida + query inválido sale 422; sin clave + query válido sale 401. La solución no depende del orden porque el test nunca mezcla ambos fallos.
3. **`bitacora.md`** debe explicar: por qué dominio lanza excepción propia (desacople), por qué auth como dependencia (testeable), y el límite de las background tasks (mismo proceso, sin reintentos → cola real para trabajo crítico, `3.16`).
