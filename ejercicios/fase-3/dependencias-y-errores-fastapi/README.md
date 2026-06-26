# Ejercicio 3.8b — Dependencias, errores globales y background tasks

> **Modalidad: código (Python + FastAPI, sin IA).** Conectas las cuatro piezas que separan una API de juguete de una real: inyección de dependencias (auth + paginación), un exception handler global que mantiene tu dominio desacoplado de HTTP, y una background task. Todo en memoria, sin base de datos.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.8` Backend con FastAPI
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Completar `app.py` (una API de **notas**) para que `pytest` quede en verde, implementando:

1. **`obtener_api_key`** — dependencia que lee el header `x-api-key` y exige la clave correcta (**401** si falta o es incorrecta).
2. **`parametros_paginacion`** — dependencia compartida que devuelve `saltar`/`limite` validados.
3. **Exception handler global** para la excepción de dominio `RecursoNoEncontrado` → **404** con una forma JSON propia.
4. **Background task** — al crear una nota, registra un evento en la auditoría sin hacer esperar al cliente.

## 📋 Contexto

Cada endpoint del capstone necesita lo mismo: una sesión, un usuario autenticado, paginación. Repetir ese código en cada función es frágil e intesteable; `Depends` lo resuelve y, de paso, te deja sustituir esas dependencias en los tests. Y un exception handler global es lo que mantiene tu lógica de negocio sin saber qué es un "404" — la primera costura hacia ports & adapters (`3.9`).

## ⚙️ Requisitos

```bash
uv add fastapi httpx pytest      # o:  pip install fastapi httpx pytest
```

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Corre el test y mira fallar cada pieza por separado.
2. Solo entonces, consulta la **documentación oficial** (FastAPI: *Dependencies*, *Handling Errors* → *Install custom exception handlers*, *Background Tasks*).
3. **Solo al final**, usa IA para *revisar*.
4. Mañana, reescribe de memoria la dependencia de api-key y el registro del handler.

## 🛠️ Instrucciones

1. Abre `app.py`. El estado (`_NOTAS`, `_AUDITORIA`, `API_KEY`), los modelos, la excepción `RecursoNoEncontrado` y la función `registrar_auditoria` ya están dados. **No los modifiques.**
2. Implementa **`obtener_api_key`**: si `x_api_key` no coincide con `API_KEY`, `raise HTTPException(status_code=401, ...)`; si coincide, devuélvela.
3. Implementa **`parametros_paginacion`**: devuelve `{"saltar": saltar, "limite": limite}` (la validación de rango ya viene en las firmas `Query`).
4. **Registra el exception handler** con `@app.exception_handler(RecursoNoEncontrado)`. Debe devolver un `JSONResponse(status_code=404, content={"error": "no_encontrado", "recurso": exc.recurso, "id": exc.id})`.
5. Implementa los **tres endpoints** (firmas dadas): `listar_notas` (ordena + saltar/limite), `obtener_nota` (lanza `RecursoNoEncontrado` si no existe), `crear_nota` (crea + `tareas.add_task(registrar_auditoria, ...)`).
6. Corre el test:

   ```bash
   uv run pytest        # o:  pytest
   ```

7. Escribe `bitacora.md`: ¿por qué el dominio lanza `RecursoNoEncontrado` en vez de `HTTPException`? ¿Por qué inyectar la api-key como dependencia es más testeable que leer el header dentro de cada endpoint? ¿Por qué la auditoría va como background task y no inline?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: 401 sin/con-clave-mala, 200 con clave, 404 con la forma JSON exacta, +1 en auditoría tras POST, 422 de paginación inválida.
- [ ] El handler global produce el cuerpo JSON **exacto** (no el `{"detail": ...}` por defecto).
- [ ] Tu lógica de endpoints lanza `RecursoNoEncontrado` (dominio), no `HTTPException` (transporte).
- [ ] `bitacora.md` responde las tres preguntas del paso 7.
- [ ] Puedes explicar **sin notas** qué pasaría si `crear_nota` hiciera la auditoría inline en vez de como background task, y cuándo eso sería un error grave (pista: trabajo lento o crítico).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- El header `x-api-key` llega al parámetro `x_api_key` (FastAPI convierte `-` en `_`). Compara contra `API_KEY`; si no calza, 401.
- El handler se registra con un decorador a nivel de módulo, **debajo** de la definición de la clase:

  ```python
  @app.exception_handler(RecursoNoEncontrado)
  async def manejar_no_encontrado(request: Request, exc: RecursoNoEncontrado):
      return JSONResponse(status_code=404, content={...})
  ```

- La background task: `tareas.add_task(registrar_auditoria, f"nota creada: {nueva_id}")`. La función NO se llama (`registrar_auditoria(...)`), se **pasa** como referencia con sus argumentos.

Repasa las secciones 4.8, 4.10 y 4.12 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `app.py` + `bitacora.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/dependencias-y-errores-fastapi.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/dependencias-y-errores-fastapi.md` — no la mires antes de intentarlo de verdad.
