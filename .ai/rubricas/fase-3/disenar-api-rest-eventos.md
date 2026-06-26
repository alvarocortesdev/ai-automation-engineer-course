---
ejercicio_id: fase-3/disenar-api-rest-eventos
fase: fase-3
sub_unidad: "3.7"
version: 1
---

# Rúbrica — Diseña la API de un sistema de eventos

> Rúbrica **analítica** atada a los `objetivos`. Ejercicio **a-mano**: no hay test. Se evalúa el
> diseño en `diseno-api.md` y el fragmento `openapi.yaml`. Varias decisiones tienen **más de una
> respuesta defendible** (versionado, status del "evento pasado", offset vs cursor); lo que se mide
> es el **criterio y la justificación**, no una respuesta única. Lo que sí tiene lectura correcta:
> recursos como sustantivos, acciones no-CRUD modeladas como recursos, y el conflicto de estado.

## Objetivos evaluados
- **O1** — Diseñar recursos y endpoints REST con status codes correctos.
- **O2** — Modelar acciones no-CRUD (inscribirse/cancelar) sin verbos en la URL.
- **O3** — Justificar trade-offs: conflicto de estado, paginación, versionado (mini-ADR).
- **O4** — Especificar errores `problem+json` y un fragmento OpenAPI válido.

## Criterios y niveles

### C1 — Recursos y endpoints (sustantivos + verbos correctos) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | URLs con verbos (`/crearEvento`, `/eventos/buscar`); el CRUD no mapea a `GET/POST/PUT/PATCH/DELETE`. |
| **en-progreso** | La mayoría son sustantivos, pero mezcla algún verbo o usa status genéricos (todo `200`). |
| **competente** | Recursos = sustantivos; CRUD bien mapeado; `201` en creación, `204` en `DELETE`, listar con `GET`. |
| **excelente** | Además marca correctamente la **idempotencia** de cada verbo y usa `Location` en el `201`. |

### C2 — Acciones no-CRUD modeladas como recursos · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Inscribir" / "cancelar" quedaron como `/eventos/{id}/inscribir` u otro verbo en la ruta. |
| **en-progreso** | Modela una de las dos como recurso pero la otra sigue como verbo. |
| **competente** | "Inscribirse" → `POST /inscripciones`; "cancelar" → `DELETE /inscripciones/{id}` (o `PATCH` de estado). |
| **excelente** | Justifica por qué la inscripción es un recurso de primera clase (tiene estado, fecha, se consulta por sí misma) y no un sub-verbo del evento. |

### C3 — Status codes de error y conflicto de estado · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Evento lleno" o "evento pasado" como `400` o `200`; no distingue 401 de 403, ni 400 de 404. |
| **en-progreso** | Acierta los básicos (404/400) pero trata el conflicto de estado como un 400 genérico. |
| **competente** | Evento lleno → `409 Conflict`; 401 (sin auth) ≠ 403 (sin permiso); 404 (no existe) ≠ 400 (mal formado). |
| **excelente** | Distingue `409` vs `422` para el "evento pasado" y **defiende** su elección; menciona que el mensaje de error de auth no debe filtrar si el recurso existe (seguridad). |

### C4 — Trade-offs justificados: paginación y versionado (mini-ADR) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Elige paginación/versionado sin justificar, o no los aborda. |
| **en-progreso** | Elige ambos pero la justificación es una frase genérica ("es mejor"). |
| **competente** | Justifica cursor (o offset) con un argumento de rendimiento/estabilidad atado a "miles de eventos"; ADR de versionado con contexto-decisión-consecuencia. |
| **excelente** | Conecta el cursor con índices (lo de 3.3), y el ADR reconoce explícitamente lo que se **pierde** con la opción elegida (no solo lo que se gana). |

### C5 — Modelo de errores + OpenAPI · mapea: O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay cuerpo `problem+json`, o el `openapi.yaml` no es YAML válido / no describe los endpoints pedidos. |
| **en-progreso** | `problem+json` incompleto (le faltan campos o el `Content-Type`); OpenAPI describe solo un endpoint. |
| **competente** | `problem+json` con sus 5 campos y `application/problem+json`; OpenAPI con `POST /inscripciones` (incl. 409) y `GET /eventos` (incl. params). |
| **excelente** | Reutiliza un `$ref` al schema `Problem`, declara el `Location` del 201 y deja el contrato listo para generar mocks. |

## Errores típicos a marcar
- **Verbo en la URL** (`/inscribir`, `/buscar`, `/crearEvento`): el error #1; la URL nombra cosas, el método HTTP la acción.
- **Todo `200`**: error con `200` rompe métricas y obliga al cliente a parsear el cuerpo para saber si falló.
- **Confundir 401 con 403**: 401 = no sé quién eres (sin/mal token); 403 = sé quién eres pero no puedes.
- **"Evento lleno" como 400**: la petición está bien formada; el choque es con el **estado** → `409`.
- **Paginación offset "porque es lo que conozco"** para una lista que crece: páginas profundas lentas y resultados inestables.
- (transversal seguridad) `detail` o `500` que filtra si un email/recurso existe, o que devuelve stack trace.
- (transversal spec-driven) versionado elegido pero no documentado en un ADR.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diseño impecable pero incapaz de explicar **por qué** "evento lleno" es 409 y no 400.
- Status codes exóticos bien escritos (`423 Locked`, `428`) sin poder defender cuándo aplican (vocabulario de IA sin criterio).
- ADR de versionado pulido pero genérico, que no menciona la consecuencia concreta de la opción.
- **Verificación sugerida:** pídele que, sin notas, clasifique GET/POST/PUT/PATCH/DELETE en safe/idempotente y que justifique un solo status code dudoso de su propio diseño.

## Feedback sugerido (graduado)
> Nunca dar el diseño completo antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Recorre tus URLs y subraya cualquier verbo. ¿`/inscribir` nombra una cosa o una acción? ¿Qué *cosa* se crea al inscribirse?"
- **Pregunta socrática (nivel 2):** "La petición para inscribirse a un evento lleno está perfectamente bien formada y el evento existe. Entonces no es 400 ni 404. ¿Con qué choca? ¿Qué familia de status code describe 'choque con el estado actual del recurso'?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Modela `inscripción` como recurso: `POST /inscripciones` crea, `DELETE /inscripciones/{id}` cancela. El evento lleno es `409 Conflict`. Para listar miles de eventos con scroll, el cursor (keyset) se apoya en un índice y no se desordena con inserciones; escribe esa razón en tu justificación, no solo la elección."

## Conexión con el proyecto / capstone
- Este diseño es el plano directo del **Capstone F3 (API de producción)**: los recursos, los status codes y el modelo de errores que definas aquí se implementan tal cual en FastAPI, y la decisión de versionado va a un ADR del repo.
