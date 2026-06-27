---
ejercicio_id: fase-4/mutacion-optimista-tareas
fase: fase-4
sub_unidad: "4.7"
version: 1
---

# Rúbrica — useToggleTarea con optimistic update y rollback

> Rúbrica analítica atada a los `objetivos` del contrato. Los tests (Vitest + Testing Library)
> verifican el **efecto sobre la caché**: en éxito la tarea queda volteada; en fallo la caché
> vuelve al snapshot. Pero **no** ven el código por dentro. El corrector abre `useToggleTarea.ts`
> y revisa el **patrón completo** (cancelar, snapshot, inmutable, invalidar) y si el alumno lo entiende.

## Objetivos evaluados
- **O1** — `useMutation` v5 con `onMutate`/`onError`/`onSettled`.
- **O2** — Optimistic update inmutable con `cancelQueries` + snapshot, y rollback ante error.
- **O3** — Invalidación de la query al terminar (`onSettled`) para reconciliar con el servidor.

> Resultado esperado (el corrector lo sabe; NO se lo entrega): `useQueryClient()` dentro del hook;
> `onMutate` = `await cancelQueries` → `getQueryData` (snapshot) → `setQueryData` con `.map` que voltea
> `hecha` solo del `id` → `return { previas }`; `onError` restaura `contexto.previas`; `onSettled` invalida.

## Criterios y niveles

### C1 — Estructura de la mutación (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No usa `useMutation`, o no llama a `toggleApi` como `mutationFn`; el test de éxito falla. |
| **en-progreso** | `useMutation` con `mutationFn`, pero la actualización de caché está en `onSuccess` (no es optimista) o faltan ganchos. |
| **competente** | `useMutation` con `mutationFn: toggleApi` y los tres ganchos `onMutate`/`onError`/`onSettled` presentes y con responsabilidades correctas. |
| **excelente** | Tipa el contexto de `onMutate` (`{ previas: Tarea[] \| undefined }`) y/o explica por qué la actualización va en `onMutate` y no en `onSuccess`. |

### C2 — Optimistic update inmutable + cancelQueries + snapshot · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No actualiza la caché optimistamente, o la **muta en sitio** (`push`/asignación). |
| **en-progreso** | Actualiza optimistamente pero **falta `cancelQueries`** o **falta el snapshot** (toma uno tarde, o lo toma después de `setQueryData`). |
| **competente** | Orden correcto: `cancelQueries` → snapshot (`getQueryData`) → `setQueryData` con `.map`+spread (inmutable, voltea solo el `id`) → `return { previas }`. El test de éxito pasa. |
| **excelente** | Articula por qué `cancelQueries` evita que un refetch en vuelo pise el update, y por qué el snapshot debe tomarse **antes** de actualizar. |

### C3 — Rollback ante error · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `onError`, o no restaura nada: tras un fallo la tarea queda volteada (el test de rollback falla). |
| **en-progreso** | Intenta restaurar pero no usa el contexto (p. ej. recalcula a mano) o no maneja `contexto` indefinido. |
| **competente** | `onError(_e, _id, contexto)` restaura con `setQueryData(TAREAS_KEY, contexto.previas)` (con guarda `if (contexto?.previas)`); el test de rollback pasa. |
| **excelente** | Explica qué pasaría sin snapshot (la tarea desaparece/queda mal "para siempre" en la UI aunque el servidor no cambió). |

### C4 — Invalidación + calidad de ingeniería (testing) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No invalida, o dejó tests en rojo. |
| **en-progreso** | Invalida pero no agregó el test propio, o lo invalida en el gancho equivocado (p. ej. solo en `onSuccess`, perdiendo la reconciliación tras error). |
| **competente** | `onSettled` invalida `["tareas"]`; todos los tests pasan **y** agregó un test propio. |
| **excelente** | El test propio es significativo (promesa controlada que verifica el cambio **antes** de resolver la API = optimismo real) y revela comprensión, no relleno. |

## Errores típicos a marcar
- Poner el `setQueryData` en `onSuccess` en vez de `onMutate`: **no es optimista** (la UI espera al servidor). Márcalo en C1/C2.
- Olvidar `await queryClient.cancelQueries(...)`: race con refetches en vuelo (C2).
- Tomar el snapshot **después** de `setQueryData`: el rollback restaura el valor ya modificado (no sirve).
- Mutar la caché en sitio (`viejas.push`, `t.hecha = !t.hecha` sobre el objeto original) en vez de `.map` + spread.
- `onError` sin guarda de `contexto` indefinido (revienta si `onMutate` no retornó).
- Invalidar solo en `onSuccess`: tras un error la caché no se reconcilia con el servidor.
- (transversal) tests verdes sin entender: persigue "que pase" en vez de razonar la carrera y el rollback.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Hook impecable con tipos sofisticados pero el alumno no sabe explicar por qué `cancelQueries` es necesario ni qué rompe sin snapshot.
- Usa `onMutateResult`/firmas de 4 argumentos de la última v5 pero no puede explicar qué es el contexto (copió de docs muy nuevas sin entender).
- **Verificación sugerida:** pídele que, en vivo, **borre** `cancelQueries` y prediga qué test/escenario se vuelve frágil; o que explique por qué `onSettled` invalida aunque ya hubo `setQueryData` optimista. Si entiende, responde al instante; si copió, titubea.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el hook completo.
- **Pista (nivel 1):** "¿En qué gancho actualizas la caché? Si esperas a `onSuccess`, ¿es optimista o reactivo? ¿Y dónde guardas el valor por si hay que deshacer?"
- **Pregunta socrática (nivel 2):** "Si una `useQuery(['tareas'])` estaba refetcheando justo cuando el usuario hace clic, ¿qué le pasa a tu `setQueryData` optimista cuando esa respuesta vieja aterriza? ¿Qué línea lo previene?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Ordena `onMutate` así: cancela las queries de la key, toma el snapshot con `getQueryData`, actualiza con `setQueryData` (map + spread, sin mutar), y retorna `{ previas }`. En `onError` restaura ese `previas`. No te doy el cuerpo del `.map`."

## Conexión con el proyecto / capstone
- Este hook es **idéntico** al de "enviar mensaje" del [Capstone F4](/fase-4-frontend/proyecto/): el mensaje del usuario aparece al instante (optimista) y se revierte si el backend falla. Dominar el rollback aquí evita el bug clásico de las apps de chat (mensajes fantasma que quedan tras un fallo de red).
