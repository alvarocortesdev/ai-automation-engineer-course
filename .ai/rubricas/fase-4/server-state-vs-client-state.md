---
ejercicio_id: fase-4/server-state-vs-client-state
fase: fase-4
sub_unidad: "4.7"
version: 1
---

# Rúbrica — Diagnostica y diseña la capa de datos (server vs client)

> Ejercicio de **razonamiento/diseño**, sin tests. La entrega es `diseno-datos.md`. El corrector
> evalúa la **claridad conceptual** (clasificación correcta, problemas bien emparejados, diseño
> defendible), no la elegancia de un código que aquí no existe.

## Objetivos evaluados
- **O1** — Clasificar cada pieza de estado como server o client, con justificación.
- **O2** — Nombrar los cinco déficits del `fetch`-en-`useEffect` y emparejarlos con el mecanismo de TanStack Query.
- **O3** — Diseñar la capa (queryKey, query/mutaciones, invalidación) y justificar optimistic vs invalidateQueries.

## Criterios y niveles

### C1 — Clasificación server vs client (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Clasifica mal lo esencial (p. ej. `tareas` como client state, o el `titulo` del input como server). |
| **en-progreso** | Acierta `tareas` pero confunde alguna pieza de UI, o justifica con "porque sí". |
| **competente** | `tareas`/`error`/`cargando` = **server**; `titulo`/`prioridad`/`errorTitulo`/`filaExpandida`/`modalAbierto` = **client**; cada una con justificación de una línea basada en "quién es el dueño del dato". |
| **excelente** | Nota que `cargando`/`error` **no deberían ser estado propio** sino derivarse de la query (`isPending`/`isError`), y que `errorTitulo` es validación de formulario (client) que delega en zod. |

### C2 — Los cinco problemas mapeados (comprensión) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Menos de 3 problemas, o "soluciones" vagas ("usar la librería"). |
| **en-progreso** | Nombra 3–4 problemas pero el mapeo a mecanismos es difuso o repite el mismo mecanismo para todo. |
| **competente** | Los 5: (1) sin caché/dedup → **queryKey/caché compartida**; (2) race condition → **cancelQueries / identidad por key**; (3) sin retry/refetch → **retry + refetchOnWindowFocus**; (4) no se puede invalidar → **invalidateQueries**; (5) boilerplate repetido → **useQuery encapsula data/isPending/isError**. Cada uno con su síntoma observable. |
| **excelente** | Conecta cada síntoma de `componente-buggy.md` con su problema (pestaña con datos viejos → staleness/refetch; "Error para siempre" → sin retry; otra pantalla no se entera → falta invalidación; lista del usuario anterior → race por key). |

### C3 — Diseño de la capa + decisión de optimistic (diseño) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No define queryKeys, o mezcla lecturas y escrituras sin criterio. |
| **en-progreso** | Define `useQuery` y mutaciones pero el flujo de invalidación es vago o incorrecto (p. ej. invalida una key que no existe). |
| **competente** | `queryKey: ["tareas", usuarioId]` (incluye el usuario); `useQuery` para leer; `useMutation` para crear/toggle/borrar; tras crear, **invalida `["tareas", usuarioId]`** en `onSuccess`/`onSettled` y explica que por eso "la otra pantalla se entera" (comparte la key). Decide optimistic para el toggle con trade-off nombrado. |
| **excelente** | Justifica meter `usuarioId` en la key (evita la race al cambiar de usuario), distingue invalidación `active` vs todas, y argumenta optimistic solo donde el lag se nota (toggle) dejando `invalidateQueries` simple para crear. |

### C4 — Seguridad (nota de cliente vs servidor) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona seguridad, o dice que validar en el cliente "ya protege". |
| **competente** | Una línea correcta: el cliente es manipulable (DevTools, curl directo); la validación de cliente es UX, el servidor **debe** re-validar (defensa en profundidad, OWASP de la Fase 3). |
| **excelente** | Conecta con el contrato compartido: el mismo esquema zod del formulario espeja el modelo pydantic del backend, y ambos validan. |

## Errores típicos a marcar
- Clasificar `cargando`/`error` como algo que "hay que guardar en `useState`" en vez de derivarlo de la query.
- Confundir "marcar la lista vieja" (invalidar) con "borrar la caché" o con "recargar la página".
- Proponer `setQueryData` a mano tras crear (en vez de invalidar) sin notar que el servidor calcula `id`/`creadaEn`.
- Olvidar `usuarioId` en la queryKey → no explica la race "lista del usuario anterior".
- Decir que optimistic es "siempre mejor" sin nombrar el costo (más código, hay que manejar rollback).
- (transversal) afirmar que validar en cliente exime al backend.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Documento exhaustivo y pulido pero la clasificación tiene un error conceptual de base (señal de copiar una plantilla sin pensar el caso concreto).
- Usa jerga avanzada (structural sharing, refetchType) sin poder explicar el caso simple de este componente.
- **Verificación sugerida:** pídele que, sin notas, clasifique una pieza nueva (p. ej. "el scroll position de la lista", "el resultado de un buscador que pega a `/api/buscar`") y justifique. Si entiende el criterio "quién es el dueño", acierta al instante.

## Feedback sugerido (graduado)
> Es un ejercicio de razonamiento: guía con preguntas, no con la tabla resuelta.
- **Pista (nivel 1):** "Para cada pieza, una sola pregunta: ¿el dueño de este dato es el servidor o tu UI? Eso decide la cubeta."
- **Pregunta socrática (nivel 2):** "El síntoma 'otra pantalla no se entera cuando creas una tarea': ¿qué tendrían que compartir las dos pantallas para enterarse a la vez? ¿Y qué acción marca ese dato compartido como 'vuelve a pedirlo'?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Empareja uno a uno: cada bullet de la sección 4.2 de la lección es UN problema; cada sección 4.3–4.6 es UNA solución. Empieza por 'la otra pantalla no se entera' = falta invalidación. No te doy la tabla completa."

## Conexión con el proyecto / capstone
- Este diseño en papel es el plano de la capa de datos del [Capstone F4](/fase-4-frontend/proyecto/): decidir qué es query (lista de mensajes), qué es mutación (enviar), qué se queda en `useState` (texto del input) es exactamente esta clasificación aplicada al chat.
