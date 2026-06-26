---
ejercicio_id: fase-3/problem-details-rfc9457
fase: fase-3
sub_unidad: "3.7"
version: 1
---

# Rúbrica — Construye errores problem+json (RFC 9457)

> Rúbrica **analítica** atada a los `objetivos`. Ejercicio **de código** con `pytest`: el test es la
> primera verificación, pero el corrector mira **más allá del verde** (que entienda por qué, no que
> el test pase por casualidad). Hay una lectura correcta de la forma del problema y de cada status
> code; el "excelente" se gana con los hilos transversales (test propio significativo, seguridad).

## Objetivos evaluados
- **O1** — Construir un problem+json válido (campos, default `about:blank`, sin `None`).
- **O2** — Soportar extension members sin romper la forma.
- **O3** — Elegir el status code correcto por situación y distinguir 400/401/403/404/409/422.

## Criterios y niveles

### C1 — Corrección del builder (forma problem+json) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Los tests no pasan; faltan campos, o mete `"detail": null`, o `type` ausente no cae en `about:blank`. |
| **en-progreso** | Pasa los casos felices pero falla en algún borde (extension members o el caso `detail=None`). |
| **competente** | Todos los tests verdes: `status`+`title` siempre, `type` default correcto, opcionales solo si vienen, extensiones incluidas. |
| **excelente** | Implementación limpia (no repite el filtro de `None` ad-hoc) y un test propio que prueba algo **no trivial** (p. ej. extensión que choca de nombre, o que `instance` se omite solo). |

### C2 — Corrección de `choose_status` · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Mapea mal varias situaciones (p. ej. `state_conflict` → 400) o no levanta error ante desconocida. |
| **en-progreso** | Acierta la mayoría pero confunde un par (401↔403, o 409↔422). |
| **competente** | Las 10 situaciones correctas y `ValueError` ante una desconocida. |
| **excelente** | Puede **explicar** cada elección dudosa: 401 (sin/mal credencial) vs 403 (sin permiso), 409 (conflicto de estado) vs 422 (validación de negocio), 400 (mal formado) vs 404 (no existe). |

### C3 — Calidad de ingeniería y testing (hilo transversal) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No añadió test propio, o el test propio no afirma nada real (`assert True`). |
| **en-progreso** | Test propio presente pero redundante con uno existente. |
| **competente** | Test propio que cubre un caso no cubierto, con aserción concreta. |
| **excelente** | El test propio nombra un riesgo real (colisión de extensión, omisión de opcionales) y el código maneja errores con claridad. |

## Errores típicos a marcar
- **Meter `"detail": null`** en el dict: el ejercicio entero gira en torno a no incluir claves vacías; un `if x is not None` antes de asignar lo resuelve.
- **`type` ausente como clave faltante** en vez de `"about:blank"`: relee qué dice RFC 9457 cuando el miembro `type` no está.
- **Confundir 401 con 403** en `choose_status`: el error clásico de status codes.
- **`state_conflict` → 400**: un evento/recurso en mal estado no es una petición mal formada; es `409`.
- **No levantar `ValueError`** ante situación desconocida (devolver `None` o `200` por defecto silencia bugs).
- (transversal seguridad) si el alumno comenta o pone un `detail` con datos sensibles de ejemplo, recordarle que `detail` no debe filtrar PII ni confirmar existencia de cuentas.
- (transversal testing) "el test pasa" no es la meta: que cada aserción **signifique** algo.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Builder perfecto pero incapaz de explicar por qué no se incluye `"detail": null` (señal de copy-paste sin entender).
- `choose_status` con un `match`/diccionario impecable pero sin poder defender 409 vs 422.
- Test propio "sofisticado" (mocks, fixtures) impropio del nivel y sin relación con el riesgo real.
- **Verificación sugerida:** pídele que, sin ejecutar, prediga el dict exacto que devuelve `build_problem_detail(403, "Sin permiso")` (debe incluir `type: about:blank`, `title`, `status`, y **nada** más), y que explique por qué un error con `200` rompe las métricas (conexión con observabilidad).

## Feedback sugerido (graduado)
> Nunca pegar la implementación completa antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu dict mete `detail` aunque sea `None`. ¿Cómo agregas una clave **solo** cuando hay valor? Piensa en construir el dict base y luego añadir condicionalmente."
- **Pregunta socrática (nivel 2):** "Si el cliente manda un JSON perfectamente válido pero pide inscribirse a un evento lleno, ¿la petición está *mal formada*? ¿Qué familia de código describe 'el recurso no está en un estado que permita esto'? ¿Y en qué se diferencia de una validación de campo (422)?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Para el builder: `p = {'type': type_ or 'about:blank', 'title': title, 'status': status}`, luego `if detail is not None: p['detail'] = detail` (igual con instance), y al final `p.update(extensions)`. Para `choose_status`, un dict situación→código con `.get` y `raise ValueError` si sale `None`. La gracia es que ahora puedes explicar cada código."

## Conexión con el proyecto / capstone
- Este builder es el **manejador de errores global** del Capstone F3 reducido a su esencia: tu API debe responder `problem+json` consistente y nunca filtrar stack traces en un `500`, lo que el Definition of Done verifica como criterio de seguridad y consistencia.
