---
ejercicio_id: fase-3/dependencias-y-errores-fastapi
fase: fase-3
sub_unidad: "3.8"
version: 1
---

# Rúbrica — Dependencias, errores globales y background tasks

> Rúbrica **analítica** atada a los `objetivos`. Evalúa `app.py` + `bitacora.md` con
> `test_app.py` en verde. El test verifica las cuatro piezas (auth, paginación, handler global,
> background task). Pasar el test prueba que funciona; la `bitacora.md` prueba que el alumno
> entiende **por qué** se hace así y no de la forma ingenua.

## Objetivos evaluados
- **O1** — Dependencias reutilizables con `Depends` (Annotated): auth por header y paginación.
- **O2** — Exception handler global que traduce una excepción de dominio a HTTP, sin acoplar el dominio al transporte.
- **O3** — Background task para trabajo posterior a la respuesta, y conciencia de sus límites frente a una cola real.

## Criterios y niveles

### C1 — Corrección de las cuatro piezas · mapea: O1, O2, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta implementar alguna pieza; varios tests en rojo. |
| **en-progreso** | Auth y paginación andan, pero el handler global no está registrado (el 404 sale como 500 o con cuerpo equivocado) o la background task no corre. |
| **competente** | Los 6 tests en **verde**: 401/200 por api-key, 404 con la forma JSON exacta, +1 en auditoría, 422 de paginación. |
| **excelente** | Verde + dependencias expresadas como alias `Annotated[..., Depends(...)]` reutilizables, y el endpoint lanza `RecursoNoEncontrado` (no `HTTPException`) manteniendo el dominio limpio. |

### C2 — Desacople dominio/transporte (handler global) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El endpoint lanza `HTTPException(404)` directo: "pasa" un 404 pero no usa el handler ni la excepción de dominio que pedía el ejercicio. |
| **en-progreso** | Registra el handler pero con cuerpo o status equivocado (usa `{"detail": ...}` o 400). |
| **competente** | `@app.exception_handler(RecursoNoEncontrado)` devuelve `JSONResponse(404, {"error":..., "recurso":..., "id":...})`; el endpoint lanza la excepción de dominio. |
| **excelente** | Explica en la bitácora que el dominio no debe importar `HTTPException` (acopla negocio a HTTP), y que el handler centraliza la forma del error — semilla de ports & adapters (`3.9`). |

### C3 — Dependencias testeables + background tasks · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Lee el header dentro de cada endpoint (no como dependencia); o hace la auditoría inline. |
| **en-progreso** | Usa `Depends` pero no reutiliza el alias; o agenda mal la background task (la **llama** en vez de pasarla por referencia). |
| **competente** | Auth y paginación como dependencias reutilizables; `tareas.add_task(registrar_auditoria, ...)` correcto. |
| **excelente** | Argumenta que inyectar la api-key permite sustituirla en tests (`dependency_overrides`) y que la background task no debe usarse para trabajo crítico/largo (cola real, `3.16`). |

## Errores típicos a marcar
- **No registrar el handler:** `raise RecursoNoEncontrado(...)` sin `@app.exception_handler` produce **500**, no 404. El test lo caza.
- **Lanzar `HTTPException` en el endpoint** en vez de la excepción de dominio: "pasa" un 404 pero traiciona el objetivo O2; márcalo.
- **Llamar la función de la tarea** (`tareas.add_task(registrar_auditoria("x"))`) en lugar de pasarla por referencia (`tareas.add_task(registrar_auditoria, "x")`): la primera ejecuta inline y rompe el patrón.
- **Leer el header a mano** (`request.headers.get("x-api-key")`) dentro de cada endpoint en vez de una dependencia: funciona pero no es testeable ni reutilizable.
- **Confundir 401 con 403:** el ejercicio pide 401 (no autenticado). 403 es "autenticado pero sin permiso" (matiz de `3.12`).
- (transversal seguridad) hardcodear la api-key sin notar que en producción iría en una variable de entorno / secreto (`3.13`).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución que mete `OAuth2PasswordBearer`, middleware de auth o JWT (material de `3.12`) en un ejercicio que pedía una dependencia simple de header: sobre-ingeniería impropia del nivel.
- `bitacora.md` que no explica la diferencia entre lanzar `HTTPException` y un handler global, ni por qué importa el desacople.
- No sabe decir qué pasaría si la background task fuera trabajo lento o si el proceso se cae.
- **Verificación sugerida:** pídele que prediga el status si quita el `@app.exception_handler` y deja el `raise RecursoNoEncontrado` (sale 500); y por qué inyectar la api-key facilita un test que la sustituye.

## Feedback sugerido (graduado)
> Nunca pegar el cuerpo de las dependencias/handler antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Corre el test del 404. ¿Sale 404 o 500? Si es 500, tu excepción de dominio se lanza pero nadie la traduce a HTTP."
- **Pregunta socrática (nivel 2):** "¿Quién convierte tu `RecursoNoEncontrado` en una respuesta HTTP? Si tu endpoint la lanza pero no registraste un handler, ¿qué cree FastAPI que pasó?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Registra `@app.exception_handler(RecursoNoEncontrado)` que devuelva `JSONResponse(status_code=404, content={...})` con la forma pedida. Para la auditoría, pasa la función por referencia: `tareas.add_task(registrar_auditoria, mensaje)`. Repasa 4.8, 4.10 y 4.12."

## Conexión con el proyecto / capstone
- Auth, paginación y manejo de errores del capstone se montan exactamente así: dependencias reutilizables y un handler global. El desacople dominio/transporte es la primera costura hacia ports & adapters (`3.9`); la auth como dependencia es la base de `3.12`.
