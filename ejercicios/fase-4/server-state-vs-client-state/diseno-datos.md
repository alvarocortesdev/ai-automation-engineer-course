# Mi diseño de la capa de datos — `PanelTareas`

> Completa los huecos. Es un documento de diseño: prosa y tablas, **no** código de
> implementación (a lo sumo, nombres de queryKey y firmas de una línea). Hazlo tú,
> sin IA, en el timebox.

## 1. Clasificación: server state vs client state

| Pieza de estado | server / client | Justificación (1 línea) |
|---|---|---|
| `tareas` (+ `cargando`, `error`) | _completar_ | _completar_ |
| `titulo` del formulario | _completar_ | _completar_ |
| `prioridad` del formulario | _completar_ | _completar_ |
| `errorTitulo` (validación) | _completar_ | _completar_ |
| `filaExpandida` | _completar_ | _completar_ |
| `modalAbierto` | _completar_ | _completar_ |

## 2. Los cinco problemas del `fetch`-en-`useEffect` y su solución

| # | Problema del enfoque actual | Síntoma que provoca | Mecanismo de TanStack Query que lo resuelve |
|---|---|---|---|
| 1 | _completar_ | _completar_ | _completar_ |
| 2 | _completar_ | _completar_ | _completar_ |
| 3 | _completar_ | _completar_ | _completar_ |
| 4 | _completar_ | _completar_ | _completar_ |
| 5 | _completar_ | _completar_ | _completar_ |

## 3. Diseño de la capa de datos

- **queryKey(s) que usaría:** _completar_
- **`useQuery`:** _qué lee, con qué key y queryFn (firma de una línea)_
- **`useMutation`(es):** _crear, toggle, borrar — una línea cada una_
- **Flujo de invalidación tras crear una tarea:** _qué key invalido, en qué gancho, y por qué eso resuelve el síntoma de "otra pantalla no se entera"_

## 4. Decisión: "marcar tarea como hecha"

- **Elijo:** optimistic update / solo `invalidateQueries` (marca una)
- **Por qué + trade-off:** _completar_

## 5. Nota de seguridad

- _Una línea: por qué validar con zod en el cliente no exime al backend de validar._
