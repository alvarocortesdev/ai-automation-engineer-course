# Contrato HTTP — API de despensa (idéntico en Python y TypeScript)

> Este contrato es **fijo**: las dos versiones deben responder igual. Cuando `curl`
> a una ruta da el mismo status y cuerpo en Python y en TS, demostraste que
> entendiste el problema por encima del lenguaje.

## Modelo de un ítem

```jsonc
{
  "id": 1,           // entero, asignado por el servidor (autoincremental)
  "name": "arroz",   // string NO vacío
  "quantity": 2,     // número > 0 (acepta decimales: 0.5)
  "unit": "kg"        // string NO vacío
}
```

El cuerpo de un `POST` trae **solo** `name`, `quantity` y `unit` (el `id` lo pone
el servidor).

## Rutas

| Método | Ruta | Cuerpo (entra) | Éxito | Errores |
|---|---|---|---|---|
| `GET` | `/health` | — | `200` `{"status":"ok"}` | — |
| `GET` | `/items` | — | `200` `[ {item}, ... ]` (array, puede ir vacío) | — |
| `POST` | `/items` | `{name, quantity, unit}` | `201` `{item}` (con `id`) | `400` si el JSON está roto · `422` si no valida |
| `GET` | `/items/{id}` | — | `200` `{item}` | `400` si `{id}` no es entero · `404` si no existe |
| `DELETE` | `/items/{id}` | — | `204` (sin cuerpo) | `400` si `{id}` no es entero · `404` si no existe |

## Reglas de los casos borde

1. **Validación (`422`).** `name: ""`, `quantity: 0`, `quantity: -1`, o un campo
   faltante → `422`. El cuerpo de error es libre, pero **el dato malo no se
   persiste**.
2. **JSON roto (`400`).** Un `POST` cuyo body no es JSON parseable → `400` (es un
   error distinto de "no valida": el JSON ni siquiera se pudo leer).
3. **`id` no numérico (`400`).** `GET /items/abc` → `400`, no `404`.
4. **`id` inexistente (`404`).** `GET /items/999` con la despensa sin ese id → `404`.
5. **Persistencia.** El estado vive en un archivo JSON. Si reinicias el servidor,
   los ítems siguen ahí.
6. **`id` autoincremental.** El próximo `id` es `max(ids actuales) + 1`, empezando
   en `1` con la despensa vacía.

## Puertos sugeridos

- Python: `http://127.0.0.1:8000`
- TypeScript: `http://127.0.0.1:8001`

(Distintos para poder levantar ambos a la vez y compararlos con `curl`.)
