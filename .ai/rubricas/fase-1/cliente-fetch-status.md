---
ejercicio_id: fase-1/cliente-fetch-status
fase: fase-1
sub_unidad: "1.7"
version: 1
---

# Rúbrica — Cliente fetch que rutea status codes (sin red)

> Rúbrica **analítica** atada a los `objetivos`. El corazón del ejercicio NO es "llamar fetch" (no se
> llama el real), sino entender la **trampa de JS** —`fetch` no rechaza por 404/500— y modelar los modos
> de fallo separando red de status. Evaluar la comprensión del seam y del doble `await` tanto como la
> corrección de las guardas. Es el gemelo JavaScript de `cliente-api-resiliente` (1.5).

## Objetivos evaluados
- **O1** — Distinguir status codes (200/404/5xx/otro) y mapearlos a errores de dominio.
- **O2** — Separar el error de red (la promesa rechaza) del status de error (resuelve con status malo).
- **O3** — Usar el doble `await` (la respuesta y luego `.json()`).
- **O4** — Validar el input antes de gastar una petición; testear inyectando `fetchFn`.

## Criterios y niveles

### C1 — Ruteo de status y la trampa de fetch · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Asume que `fetch` rechaza por error: hace `await resp.json()` sin mirar el status, o usa un `try/catch` para "atrapar" el 404. |
| **en-progreso** | Revisa el status pero colapsa casos: usa `>= 400` para todo (pierde 4xx vs 5xx), o no maneja el catch-all. |
| **competente** | Las cuatro ramas correctas y en orden: 200→nombre, 404→`UsuarioNoEncontrado`, `>=500`→`ServicioCaido`, resto→`RespuestaInesperada`. Revisa el status **a mano**. |
| **excelente** | Explica por qué `fetch` resuelve ante un 500 (a diferencia de `httpx.raise_for_status`) y por qué 4xx vs 5xx merecen reacción distinta. |

### C2 — Error de red vs status, y alcance del try · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No envuelve `fetchFn`; el rechazo de red escapa crudo. O envuelve toda la función en un `try` que disfraza otros errores. |
| **en-progreso** | Atrapa el rechazo pero con `catch (e) {}` que también tragaría los `throw` de dominio (los re-lanza como `ServicioInalcanzable`). |
| **competente** | `try/catch` ceñido a `await fetchFn(userId)`; re-lanza `ServicioInalcanzable`. Los `throw` de status viven fuera de ese `try`. |
| **excelente** | Distingue conceptualmente "rechazo = no hubo respuesta" de "status malo = sí hubo respuesta"; usa `cause`/`from` para conservar el error original. |

### C3 — Validación, doble await y diseño testeable · mapea: O3, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No valida `userId`, o valida después de llamar `fetchFn` (test `noDebeCorrer` falla). Olvida el segundo `await` y devuelve una promesa. |
| **en-progreso** | Valida `userId` pero el test propio depende de un fetch real, o no aprovecha el seam inyectado. |
| **competente** | Valida **antes** del primer `await`; usa el doble `await`; el test propio pasa un `fetchFn` falso sin tocar la red. |
| **excelente** | Sabe explicar que inyectar `fetchFn` es inyección de dependencias y que el mismo patrón mockea un LLM (2.11); su stub es mínimo y claro. |

## Errores típicos a marcar
- **Asumir que `fetch` rechaza por 404/500**: el bug conceptual central. `fetch` solo rechaza por red; el status se revisa a mano (`resp.ok`/`resp.status`).
- **Olvidar el segundo `await`** (`resp.json()`): devuelve una promesa en vez del objeto; `datos.name` queda `undefined`.
- **`try` demasiado ancho**: envolver toda la función convierte un `TypeError` de tu lógica o un `throw` de dominio en `ServicioInalcanzable` silenciosamente.
- **`catch` genérico sin re-throw selectivo**: traga los errores de dominio.
- **Usar `>= 400` para todo**: pierde la distinción 4xx (no reintentar) vs 5xx (reintentable).
- **Validar `userId` después de `fetchFn`**: gasta una petición; el test `noDebeCorrer` lo detecta.
- **Orden de guardas equivocado**: catch-all antes de las ramas específicas → ramas muertas.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Uso del `fetch` global real, `AbortController`, `axios` o reintentos con backoff (no pedidos, propios de F3): pegó un cliente genérico sin leer el contrato del `fetchFn` inyectado.
- Maneja excepciones que no aplican (p. ej. atrapa un `TypeError` de "Failed to fetch" del navegador) cuando el ejercicio usa un `fetchFn` falso que rechaza con un `Error` simple.
- No puede explicar por qué el test no necesita internet, ni por qué `fetch` no rechaza ante un 500.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué error lanza su función si `fetchFn` resuelve con status `418`, y que escriba el `fetchFn` falso para ese caso.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Hay dos familias de fallo muy distintas: una donde la promesa de `fetchFn` **rechaza** (la red falló, no hubo respuesta) y otra donde **resuelve** con un status malo (404/500). En JS, `fetch` **no** rechaza por un 500. ¿Tu código las trata distinto?"
- **Pregunta socrática (nivel 2):** "¿En qué momento puede rechazar `fetchFn` — antes o después de tener un `status`? ¿Por qué entonces el `catch` de red y el `if (resp.status)` viven en lugares distintos? ¿Y por qué validar `userId` antes de todo?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Estructura: (1) valida `userId` y lanza `EntradaInvalida` — antes de cualquier `await`; (2) `try { resp = await fetchFn(userId) } catch { throw new ServicioInalcanzable() }`; (3) ramifica por `resp.status` con 200 primero (y ahí el segundo `await` de `resp.json()`). Revisa 4.6 y reintenta antes de mirar la referencia."

## Conexión con el proyecto / capstone
- El seam inyectado, el doble `await` y el ruteo de status son la base del cliente HTTP del lado JS del **Capstone F1**, la mecánica de la UI de streaming de F4, y exactamente el mismo patrón que `cliente-api-resiliente` (1.5, Python): un LLM o una API se mockean igual, sin red.
