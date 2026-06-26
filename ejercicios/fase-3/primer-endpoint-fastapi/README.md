# Ejercicio 3.8a — Tu primera API FastAPI: tareas con CRUD parcial

> **Modalidad: código (Python + FastAPI, sin IA).** Montas una mini-API de tareas en memoria con los tres patrones que repetirás en cada backend: crear con validación de body, leer un recurso (o 404), y listar con filtro y paginación. Sin base de datos: todo vive en un dict.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.8` Backend con FastAPI
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

Implementar tres endpoints en `app.py` sobre el contrato dado, de modo que `pytest` quede en verde:

- `POST /tareas` → crea una tarea desde un body pydantic, responde **201** con el modelo público.
- `GET /tareas/{tarea_id}` → devuelve la tarea o **404** con `HTTPException` si no existe.
- `GET /tareas` → lista, con filtro opcional `completada` y un `limite` validado en `[1, 100]`.

## 📋 Contexto

Esta es la forma exacta de casi cualquier endpoint del capstone: validar la entrada con un modelo, controlar la salida con otro, devolver el status code correcto y manejar el "no existe" como 404 (no como 200 disfrazado). Si interiorizas estos tres endpoints, el resto del backend es repetir el patrón.

## ⚙️ Requisitos

```bash
uv add fastapi httpx pytest      # o:  pip install fastapi httpx pytest
```

(`httpx` lo necesita el `TestClient` de FastAPI para correr los tests sin levantar el servidor.)

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Implementa lo que se te ocurra y **mira el test fallar**: ver el 422 y el 404 funcionando es parte del aprendizaje.
2. Solo entonces, consulta la **documentación oficial** (FastAPI: *Request Body*, *Query Parameters*, *Handling Errors*).
3. **Solo al final**, usa IA para *revisar* tu solución y tu bitácora — no para generarlas.
4. Mañana, reescribe de memoria el `POST /tareas` completo.

## 🛠️ Instrucciones

1. Abre `app.py`. El almacenamiento (`_TAREAS`, `_siguiente_id`) y el modelo de salida `TareaPublica` ya están dados. **No los modifiques.**
2. **Define `TareaCrear`** (modelo de entrada): `titulo` obligatorio y **no vacío** (pista: `Field(min_length=1)`), `descripcion` opcional.
3. **Implementa los tres endpoints** (las firmas y decoradores ya están; completa los cuerpos):
   - `crear_tarea`: nace con `completada=False`, usa `_siguiente_id` (recuerda `global`), guarda en `_TAREAS`, devuelve el dict.
   - `obtener_tarea`: busca por id; si no está, `raise HTTPException(status_code=404, detail=...)`.
   - `listar_tareas`: filtra por `completada` solo si viene dado; recorta a `limite`.
4. Corre el test:

   ```bash
   uv run pytest        # o:  pytest
   ```

5. Escribe `bitacora.md`: ¿por qué un `titulo` ausente da **422** y no 500? ¿Qué hace `response_model=TareaPublica` además de documentar? ¿Por qué `crear` devuelve 201 y no 200?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: los 7 tests pasan (201, 422 por titulo ausente y vacío, 404, filtro, límite).
- [ ] `TareaCrear` exige `titulo` no vacío; no validas con `if` dentro del endpoint.
- [ ] Usas `HTTPException(status_code=404, ...)` para el caso "no existe" (no un `return {"error": ...}`).
- [ ] `bitacora.md` responde las tres preguntas del paso 5.
- [ ] Puedes explicar **sin notas** quién detiene un request inválido y en qué momento (antes o después de tu función).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- El body se valida solo: declara `titulo: str = Field(min_length=1)` en `TareaCrear` y FastAPI rechaza con 422 lo que no calce, **antes** de ejecutar tu endpoint.
- El 404 es un `raise HTTPException(status_code=404, detail="Tarea no encontrada")` dentro de `obtener_tarea` cuando `_TAREAS.get(tarea_id)` es `None`.
- En `listar_tareas`, filtra solo si `completada is not None`; luego `list(...)[:limite]`.

Repasa la sección 4.5–4.7 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `app.py` + `bitacora.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/primer-endpoint-fastapi.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/primer-endpoint-fastapi.md` — no la mires antes de intentarlo de verdad.
