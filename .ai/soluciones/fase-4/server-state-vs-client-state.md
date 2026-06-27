---
ejercicio_id: fase-4/server-state-vs-client-state
fase: fase-4
sub_unidad: "4.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnostica y diseña la capa de datos

## 1. Clasificación esperada

| Pieza | server / client | Justificación |
|---|---|---|
| `tareas` | **server** | Vienen de la DB vía `GET /api/tareas`; pueden quedar viejas; las comparte otra pantalla. |
| `cargando` | **server (derivado)** | No debería ser estado propio: es `isPending` de la query. |
| `error` | **server (derivado)** | Tampoco propio: es `isError`/`error` de la query. |
| `titulo` | **client** | Texto que el usuario escribe; vive en la UI hasta el submit. |
| `prioridad` | **client** | Selección del formulario, local a la UI. |
| `errorTitulo` | **client** | Validación de formulario (la delega zod); no es del servidor. |
| `filaExpandida` | **client** | Estado puro de presentación. |
| `modalAbierto` | **client** | Estado puro de UI. |

> Punto fino (excelente): `cargando` y `error` **no** deberían existir como `useState` separados; al usar `useQuery` se obtienen como `isPending`/`isError`. Ese es justo el "fin del boilerplate".

## 2. Los cinco problemas y su mecanismo

| # | Problema | Síntoma en `componente-buggy.md` | Mecanismo de TanStack Query |
|---|---|---|---|
| 1 | Sin caché ni deduplicación | Otra pantalla repite el request; volver a la vista recarga desde cero | **queryKey + caché compartida**: misma key = un request, un resultado compartido |
| 2 | Race condition al cambiar deps | "A veces aparece la lista del usuario anterior" | **Identidad por queryKey** (`["tareas", usuarioId]`) + `cancelQueries`: solo la query vigente actualiza |
| 3 | Sin reintentos ni refetch | "Si la red parpadea queda en Error para siempre"; datos viejos al volver a la pestaña | **retry** + `refetchOnWindowFocus`/`refetchOnReconnect` + `staleTime` |
| 4 | No se puede invalidar | "Otra pantalla no se entera cuando se crea una tarea" | **invalidateQueries(key)**: marca la lista vieja y refetchea en todas las pantallas que comparten la key |
| 5 | Boilerplate repetido en cada pantalla | Tres `useState` + efecto copiados por todos lados | **useQuery** encapsula `data`/`isPending`/`isError` en una línea |

## 3. Diseño de la capa esperado

- **queryKey:** `["tareas", usuarioId]` — incluir `usuarioId` es lo que evita la race del síntoma "lista del usuario anterior" (cada usuario tiene su entrada de caché).
- **`useQuery`:** lee la lista: `useQuery({ queryKey: ["tareas", usuarioId], queryFn: () => obtenerTareas(usuarioId) })`. De ahí salen `data`, `isPending`, `isError` (adiós a `cargando`/`error` a mano).
- **`useMutation` (tres):**
  - crear: `POST /api/tareas`;
  - toggle: `PATCH /api/tareas/{id}/toggle`;
  - borrar: `DELETE /api/tareas/{id}`.
- **Flujo de invalidación tras crear:** en `onSuccess`/`onSettled` de la mutación de crear, `invalidateQueries({ queryKey: ["tareas", usuarioId] })`. Como **toda** pantalla que muestra esa lista usa la misma key, todas refetchean y se enteran a la vez. Esto resuelve el síntoma de la "otra pantalla". Importa porque el servidor asigna `id` y `creadaEn`: invalidar trae la versión real en vez de adivinar con `setQueryData`.

## 4. Decisión de optimistic
- **Toggle:** **optimistic update** (el síntoma "se siente con lag" lo pide). Trade-off: se siente instantáneo, pero cuesta más código (cancel + snapshot + rollback + invalidate); hay que manejar el fallo. Es el ejercicio A.
- **Crear:** basta `invalidateQueries` (más simple y siempre correcto; el pequeño retraso al crear es tolerable, y el servidor calcula campos que no conviene adivinar).
- Regla: optimistic donde el lag se nota y el cálculo del nuevo estado es trivial; `invalidateQueries` donde el servidor decide campos o el retraso no molesta.

## 5. Nota de seguridad
- Validar con zod en el cliente es **UX** (feedback inmediato). El cliente es manipulable (DevTools, curl directo al endpoint), así que el backend **debe** re-validar siempre (lo hace con pydantic, `422` si falla). Defensa en profundidad: el mismo contrato en dos capas, OWASP de la Fase 3 aplicado al frontend.

## Cómo calificar
- **Competente** exige: clasificación correcta de lo esencial (`tareas`=server, formulario/UI=client), los 5 problemas mapeados a su mecanismo, queryKey con `usuarioId`, flujo de invalidación correcto y trade-off de optimistic nombrado, y la nota de seguridad.
- Acepta sinónimos: "datos obsoletos" ≈ "staleness"; "marcar vieja la lista" ≈ "invalidar"; "carrera" ≈ "race condition".
- **No** aceptes: `tareas` como client state; "validar en cliente ya protege"; `setQueryData` manual tras crear sin notar que el servidor asigna `id`/`creadaEn`; queryKey sin `usuarioId` cuando además no explica la race del usuario anterior.
- El error conceptual más grave (corregir primero): tratar `cargando`/`error` como estado a mantener a mano en vez de derivarlo de la query — es la señal de que no internalizó qué resuelve la herramienta.
