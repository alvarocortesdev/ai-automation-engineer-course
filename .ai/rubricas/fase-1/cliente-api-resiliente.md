---
ejercicio_id: fase-1/cliente-api-resiliente
fase: fase-1
sub_unidad: "1.5"
version: 1
---

# Rúbrica — Cliente de API resiliente y testeable

> Rúbrica **analítica** atada a los `objetivos`. El corazón del ejercicio NO es "llamar una API"
> (no se llama ninguna), sino **modelar los modos de fallo** y entender por qué inyectar `fetch`
> hace el código testeable. Evaluar la comprensión del seam tanto como la corrección de las guardas.

## Objetivos evaluados
- **O1** — Distinguir status codes (200/404/5xx/otro) y mapearlos a errores de dominio.
- **O2** — Convertir errores de red (timeout, conexión) en una excepción de dominio.
- **O3** — Hacer testeable el código inyectando la dependencia de red (`fetch`).
- **O4** — Validar el input antes de gastar una petición.

## Criterios y niveles

### C1 — Corrección del ruteo de status · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No distingue status; asume siempre 200; o llama `.json()` sin mirar el código. |
| **en-progreso** | Maneja 200 y 404 pero colapsa 5xx con "cualquier otro", o usa `>= 400` para todo (pierde la distinción 4xx/5xx). |
| **competente** | Las cuatro ramas correctas: 200→nombre, 404→`UsuarioNoEncontrado`, `>=500`→`ServicioCaido`, resto→`RespuestaInesperada`, en orden válido. |
| **excelente** | Además explica por qué 4xx vs 5xx merecen reacción distinta (4xx no se reintenta, 5xx sí) y por qué el caso feliz va primero. |

### C2 — Manejo de errores de red · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No envuelve la llamada; un `TimeoutError`/`ConnectionError` escapa crudo. |
| **en-progreso** | Atrapa el error de red pero con un `except Exception` genérico (atraparía también bugs de su propia lógica). |
| **competente** | `try/except (TimeoutError, ConnectionError)` específico que re-lanza `ServicioInalcanzable`. |
| **excelente** | Distingue conceptualmente "error de red = no hubo respuesta" de "status de error = sí hubo respuesta"; el `try` envuelve **solo** `fetch(...)`, no toda la función. |

### C3 — Diseño testeable y validación · mapea: O3, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No valida `user_id`; o valida después de llamar `fetch` (desperdicia la petición). |
| **en-progreso** | Valida `user_id` pero el test propio depende de un `fetch` real o no aprovecha el seam. |
| **competente** | Valida **antes** del `try`; el test propio usa un `fetch` falso (stub) sin tocar la red. |
| **excelente** | Sabe explicar que inyectar `fetch` es inyección de dependencias y que el mismo patrón sirve para mockear un LLM (2.11); su stub es mínimo y claro. |

## Errores típicos a marcar
- **Asumir que un 404 lanza excepción solo**: `httpx`/`requests` no lo hacen; revisar `status_code` es responsabilidad del código.
- **`except Exception` genérico** alrededor de todo: atrapa también `KeyError`/`ValueError` de la propia lógica y los disfraza de error de red.
- **Orden de guardas equivocado**: poner el catch-all (`RespuestaInesperada`) antes del `if 404` lo vuelve inalcanzable.
- **Usar `>= 400` para todo**: pierde la distinción 4xx (no reintentar) vs 5xx (reintentable), que es el punto.
- **Validar `user_id` después de `fetch`**: gasta una petición de red en input que ya se sabía inválido.
- **Test que toca la red real**: lento, frágil, con rate limits; contradice el objetivo del seam.
- (transversal seguridad) acceder a `resp.json()["name"]` sin contemplar que el payload podría no tener `name` — semilla de "no confíes en el payload externo" (conecta con pydantic, 1.4).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Manejo de excepciones de `httpx` reales (`httpx.HTTPStatusError`, `httpx.TimeoutException`) cuando el ejercicio usa `fetch` inyectado y errores **builtin** (`TimeoutError`/`ConnectionError`): señal de haber pegado un cliente httpx genérico sin leer el contrato.
- Reintentos con backoff o `tenacity` (no pedidos, propios de F3): sofisticación impropia del nivel.
- No puede explicar por qué el test no necesita internet.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué excepción lanza su función si `fetch` devuelve status `418`, y por qué; y que escriba el `fetch` falso para ese caso.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Hay dos familias de fallo muy distintas: una donde **sí** llegó una respuesta (con status malo) y otra donde **no llegó nada** (la red falló). Tu código las está tratando igual. Sepáralas."
- **Pregunta socrática (nivel 2):** "¿En qué momento exacto puede fallar la red — antes o después de tener un `status_code`? ¿Por qué entonces el `except` de red y el `if status_code` viven en lugares distintos del flujo? ¿Y por qué validar `user_id` antes de todo?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Estructura: (1) valida `user_id` y lanza `ValueError` si es inválido — antes del `try`; (2) `try: resp = fetch(user_id)` / `except (TimeoutError, ConnectionError): raise ServicioInalcanzable`; (3) ramifica por `resp.status_code` con 200 primero. Revisa secciones 4.6–4.8 y reintenta antes de mirar la referencia."

## Conexión con el proyecto / capstone
- El seam de inyección y el ruteo de status son la base del cliente HTTP del **Capstone F1**, y exactamente la mecánica de `1.10` (primer llamado a un LLM) y de `2.11` (testear código que llama LLMs): un LLM es una API, y se mockea igual.
