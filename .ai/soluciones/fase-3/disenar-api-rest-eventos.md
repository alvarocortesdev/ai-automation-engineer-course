---
ejercicio_id: fase-3/disenar-api-rest-eventos
fase: fase-3
sub_unidad: "3.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es **una** solución defendible, no la única.

# Solución de referencia — Diseña la API de un sistema de eventos

## 1. Recursos

| Recurso | Colección | Elemento |
|---|---|---|
| Eventos | `/eventos` | `/eventos/{id}` |
| Asistentes | `/asistentes` | `/asistentes/{id}` |
| Inscripciones | `/inscripciones` | `/inscripciones/{id}` |

> "Organizador" puede ser un tipo de asistente/usuario o un recurso aparte; ambas son aceptables.
> Lo clave: **inscripción es un recurso de primera clase**, no un sub-verbo de evento.

## 2. Tabla de endpoints

| Operación | Verbo + URL | Status éxito | Idempotente |
|---|---|---|---|
| Listar eventos (próximos) | `GET /eventos` | `200` | sí (safe) |
| Ver un evento | `GET /eventos/{id}` | `200` | sí (safe) |
| Crear evento | `POST /eventos` | `201` + `Location` | no |
| Editar evento (parcial) | `PATCH /eventos/{id}` | `200` | depende |
| Reemplazar evento | `PUT /eventos/{id}` | `200`/`204` | sí |
| Borrar evento | `DELETE /eventos/{id}` | `204` | sí |
| Ver inscritos de un evento | `GET /eventos/{id}/inscripciones` | `200` | sí (safe) |
| Inscribirse | `POST /inscripciones` | `201` + `Location` | no |
| Cancelar inscripción | `DELETE /inscripciones/{id}` | `204` | sí |
| Ver eventos de un asistente | `GET /asistentes/{id}/inscripciones` | `200` | sí (safe) |

> Aceptable también: cancelar con `PATCH /inscripciones/{id}` `{"estado":"cancelada"}` si se quiere
> conservar historial. "Ver inscritos" puede vivir como `/eventos/{id}/inscripciones` (anidado) o como
> `/inscripciones?evento_id={id}` (filtro): ambas son correctas; el anidado expresa mejor la pertenencia.

## 3. Casos de error

| Situación | Status | Por qué |
|---|---|---|
| Evento no existe | `404 Not Found` | La petición es válida pero el recurso no está. |
| Cuerpo mal formado / falta campo | `400 Bad Request` (o `422 Unprocessable Content` si el JSON es válido pero falla la validación de negocio) | Sintaxis/estructura inválida vs validación semántica. |
| Evento lleno (cupo alcanzado) | `409 Conflict` | La petición es válida y el evento existe; choca con el **estado actual** (sin cupo). |
| Evento ya pasó | `409 Conflict` **o** `422 Unprocessable Content` | Defendible cualquiera: `409` lo trata como conflicto de estado temporal; `422` como regla de negocio que la entidad no satisface. Exigir **justificación**, no un código fijo. |
| Sin token de auth | `401 Unauthorized` | No hay credencial (o es inválida): el servidor no sabe quién eres. |
| Autenticado sin permiso | `403 Forbidden` | Sabe quién eres, pero no puedes hacer esto. |

## 4. Modelo de errores (problem+json)

```http
HTTP/1.1 409 Conflict
Content-Type: application/problem+json

{
  "type": "https://api.eventos.cl/errors/evento-lleno",
  "title": "El evento alcanzó su cupo máximo",
  "status": 409,
  "detail": "El evento 12 tiene 200/200 inscritos; no admite más inscripciones.",
  "instance": "/inscripciones"
}
```

> Extensión válida y recomendable: `"cupo_maximo": 200, "inscritos_actuales": 200`. El `Content-Type`
> `application/problem+json` es obligatorio para que el cliente sepa interpretarlo.

## 5. Listado y paginación

- **Filtros:** `?categoria=charla&desde=2026-07-01` (eventos próximos = `fecha >= ahora`, por defecto).
- **Orden:** `?sort=fecha` (ascendente por fecha, lo natural para "próximos").
- **Paginación elegida:** **cursor (keyset)**.
- **Justificación:** con "miles de eventos" y un listado que se navega como feed cronológico, el
  cursor se apoya en el índice de `fecha`/`id` y no recorre-y-descarta filas como el offset en
  páginas profundas; además es **estable** cuando se crean eventos nuevos (el offset mostraría
  duplicados o saltos al correrse las filas). Si en cambio fuera un panel de admin con "ir a la
  página 7", offset sería aceptable. (Conexión con índices de 3.3.)

## 6. Versionado — mini-ADR

- **Decisión:** versionado en la **URL** (`/v1/eventos`).
- **Contexto:** habrá clientes externos (web, móvil) consumiendo la API; cualquier cambio
  incompatible de forma de respuesta los rompería de golpe. Sin versión, no hay forma de evolucionar
  sin coordinar un despliegue simultáneo de todos los clientes.
- **Consecuencia:** ganamos visibilidad y testeo trivial (un `curl` o el navegador muestran la
  versión); aceptamos la "impureza" REST de que la URL del recurso cambie entre versiones. La
  alternativa (header `Accept: ...v1+json`) mantendría URLs estables pero es invisible y más fácil de
  olvidar al probar.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Verbo en la URL.** El error más común: `/inscribir`, `/eventos/{id}/cancelar`. La acción va en el método; la cosa, en la URL.
2. **"Evento lleno" como 400.** La petición está bien formada → no es 400. Es conflicto de estado → 409.
3. **401 vs 403.** Confundirlos es clásico. Sin credencial = 401; con credencial pero sin permiso = 403.
4. **Paginación sin defensa.** Elegir offset/cursor está bien; no justificarlo, no.
5. **problem+json incompleto.** Falta el `Content-Type`, o usa `{"error": "..."}` ad-hoc.
6. **Versionado sin ADR.** La decisión existe pero no está documentada → falla el hilo spec-driven.

## Rango de respuestas aceptables
- Recursos: aceptar variaciones de nombres y de anidamiento (`/eventos/{id}/inscripciones` o filtro), siempre que sean sustantivos.
- "Evento pasado": `409` o `422`, **con** justificación.
- Paginación: cursor (preferido aquí) u offset si argumenta un caso de admin; rechazar "sin paginar".
- Versionado: URL o header, **con** ADR que mencione la consecuencia.
- ❌ **No aceptable como competente:** verbos en la URL, errores como `200`, no distinguir 401/403, o paginación/versionado sin justificar.
