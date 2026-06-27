# Contrato de la API (backend FastAPI de la Fase 3)

> El backend ya existe (lo construiste en la Fase 3). Tu diseño de la capa de datos
> del frontend se apoya en estos endpoints. El servidor valida con pydantic y
> responde JSON con los status codes indicados.

## Recurso `Tarea`

```jsonc
{
  "id": "string (uuid)",
  "titulo": "string (1..80)",
  "prioridad": "baja | media | alta",
  "hecha": "boolean",
  "creadaEn": "string (ISO 8601, lo calcula el servidor)"
}
```

## Endpoints

| Método | Ruta | Qué hace | Respuesta |
|---|---|---|---|
| `GET` | `/api/tareas?usuario={id}` | Lista las tareas del usuario | `200` → `Tarea[]` |
| `POST` | `/api/tareas` | Crea una tarea (body: `{ titulo, prioridad }`) | `201` → `Tarea` (con `id` y `creadaEn` asignados por el servidor) |
| `PATCH` | `/api/tareas/{id}/toggle` | Voltea `hecha` | `200` → `Tarea` |
| `DELETE` | `/api/tareas/{id}` | Borra la tarea | `204` |

## Notas del contrato

- El `id` y `creadaEn` los asigna **el servidor**: el cliente no los inventa.
- El servidor **re-valida** todo el body (no confía en el cliente), aplicando las mismas reglas que tu esquema zod del formulario.
- Errores de validación → `422` con detalle por campo; no autorizado → `401`.
