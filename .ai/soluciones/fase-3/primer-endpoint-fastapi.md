---
ejercicio_id: fase-3/primer-endpoint-fastapi
fase: fase-3
sub_unidad: "3.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Tu primera API FastAPI: tareas con CRUD parcial

## Implementación canónica (`app.py`)

```python
from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="API de tareas")

_TAREAS: dict[int, dict] = {}
_siguiente_id = 1


class TareaPublica(BaseModel):
    id: int
    titulo: str
    descripcion: str | None = None
    completada: bool


class TareaCrear(BaseModel):
    titulo: str = Field(min_length=1)          # obligatorio y no vacío
    descripcion: str | None = None


@app.post("/tareas", response_model=TareaPublica, status_code=status.HTTP_201_CREATED)
async def crear_tarea(datos: TareaCrear) -> dict:
    global _siguiente_id
    tarea = {
        "id": _siguiente_id,
        "titulo": datos.titulo,
        "descripcion": datos.descripcion,
        "completada": False,
    }
    _TAREAS[_siguiente_id] = tarea
    _siguiente_id += 1
    return tarea


@app.get("/tareas/{tarea_id}", response_model=TareaPublica)
async def obtener_tarea(tarea_id: int) -> dict:
    tarea = _TAREAS.get(tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@app.get("/tareas", response_model=list[TareaPublica])
async def listar_tareas(
    completada: bool | None = None,
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[dict]:
    tareas = list(_TAREAS.values())
    if completada is not None:
        tareas = [t for t in tareas if t["completada"] == completada]
    return tareas[:limite]
```

Verificado contra `test_app.py`: **7 passed**.

## Por qué cada decisión

- **`titulo: str = Field(min_length=1)`** — sin `min_length`, `{"titulo": ""}` pasaría y `test_titulo_vacio` quedaría en rojo. Marcarlo requerido (sin default) hace que `{}` dé 422 (`test_titulo_ausente`). La validación vive en el modelo, no en ifs.
- **`status_code=status.HTTP_201_CREATED`** — crear un recurso es 201, no 200 (contrato REST de `3.7`).
- **`response_model=TareaPublica`** — fija qué campos salen. Aquí el dict ya calza, pero el hábito correcto (y lo que el test de `set(body)` verifica) es declarar la salida explícita: nada fuera del modelo viaja al cliente.
- **`raise HTTPException(404, ...)`** — un `return {"error": ...}` daría 200; el cliente no podría distinguir éxito de fallo.
- **`global _siguiente_id`** — sin él, asignar dentro de la función crea una local y revienta con `UnboundLocalError`.

## Variantes aceptables
- Endpoints `def` normales en vez de `async def`: **aceptable** aquí (no hay I/O real); el `async` es la práctica del puente a IA, pero no cambia el resultado en memoria.
- Filtrar y recortar en una sola comprensión, o usar `itertools.islice`: válido mientras respete `limite`.
- `TareaCrear` con `descripcion: str | None = None` o `Optional[str] = None`: equivalentes.

## No aceptable como competente
- ❌ Validar `titulo` con `if not datos.titulo: raise ...` en vez de en el modelo.
- ❌ Manejar el "no existe" devolviendo 200 con un cuerpo de error.
- ❌ Devolver 200 al crear (sin `status_code=201`).
- ⚠️ Omitir `response_model`: el test de campos puede pasar igual con el dict, pero márcalo: pierde la barrera anti-fuga (pregúntale qué pasaría con un campo `secreto` en el dict).

## Puntos resbalosos (donde el corrector debe mirar)
1. **`completada=false` como query.** FastAPI parsea `"false"`/`"true"` a bool. Si el alumno compara contra strings, el filtro falla.
2. **Estado compartido entre tests.** El dict persiste durante la sesión de tests; la solución no asume base vacía, filtra por id. Si el alumno hace asserts de conteo global, es frágil (pero el test dado no lo exige).
3. **`bitacora.md`** debe responder: quién valida (pydantic, en el borde), qué hace `response_model` (filtra + valida salida + documenta), por qué 201.
