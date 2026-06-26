# Diseño de la API — Plataforma de eventos

> Completa cada sección. Borra los `<...>` y los comentarios de ayuda al rellenar.
> Esto es diseño en papel: no programas nada, decides y justificas.

## 1. Recursos

> Los sustantivos del dominio convertidos en recursos. Para cada uno, la colección y el elemento.

| Recurso | Colección | Elemento |
|---|---|---|
| <Eventos> | `/eventos` | `/eventos/{id}` |
| < ... > | | |
| < ... > | | |

## 2. Tabla de endpoints

> CRUD de cada recurso + las acciones que NO son CRUD. "Idempotente": sí / no / depende.

| Operación | Verbo + URL | Status éxito | Idempotente |
|---|---|---|---|
| Listar eventos próximos | `GET /eventos` | `200` | sí (safe) |
| < Crear evento > | | | |
| < Inscribirse a un evento > | | | |
| < Cancelar una inscripción > | | | |
| < Ver inscritos de un evento > | | | |
| < Ver eventos de un asistente > | | | |
| < ... > | | | |

## 3. Casos de error

| Situación | Status code | Por qué |
|---|---|---|
| El evento no existe | < 404 > | < ... > |
| Cuerpo de la petición mal formado / falta un campo | | |
| El evento ya alcanzó su cupo | | |
| El evento ya pasó (fecha pasada) | | |
| Petición sin token de autenticación | | |
| Usuario autenticado pero sin permiso | | |

## 4. Modelo de errores (problem+json, RFC 9457)

> Ejemplo del cuerpo de error para "evento lleno". Incluye el Content-Type.

```http
HTTP/1.1 <código> <razón>
Content-Type: <media type>

{
  "type": "<uri del tipo de error>",
  "title": "<resumen humano corto>",
  "status": <código>,
  "detail": "<explicación de esta ocurrencia>",
  "instance": "<uri de la ocurrencia>"
}
```

## 5. Listado y paginación de `GET /eventos`

- **Filtros:** `?categoria=...` , `< ... >`
- **Orden:** `< ... >`
- **Paginación elegida:** < offset | cursor >
- **Justificación (2–3 líneas):**
  > < por qué esta y no la otra, dado que "puede haber miles de eventos" >

## 6. Versionado — mini-ADR

- **Decisión:** versionado en < URL | header >.
- **Contexto:** < por qué hace falta versionar; qué se rompería sin esto >
- **Consecuencia:** < qué ganas y qué aceptas perder con esta opción >
