---
ejercicio_id: fase-3/capstone-api-produccion
fase: fase-3
sub_unidad: "3.P"
version: 1
---

# Rúbrica — Capstone Fase 3: API de producción

> Rúbrica analítica para el **capstone integrador** de la Fase 3. No hay una única respuesta correcta:
> el alumno elige su propio dominio y diseño. Lo que se evalúa es si la API cumple el estándar de
> **producción** (no si "compila en su máquina"): spec primero, arquitectura limpia, seguridad aplicada,
> confiabilidad, tests que detectan de verdad, y entregables comunicables. Una API que "funciona" pero
> filtra recursos ajenos, no es idempotente o esconde un secreto en el código **no** cumple el objetivo.
>
> Se mide contra el **Definition of Done único** (§B de `CURRICULUM-REVIEW.md`). En la Fase 3 aplican los
> puntos **1** (spec + ADR), **2** (tests/lint en CI, mutation score), **3** (seguridad + SCA/secret-scan),
> **4** (observabilidad: logs + correlation IDs), **8** (demo + README inglés + write-up) y **9**
> (Conventional Commits). Los puntos **5** (eval IA), **6** (agente) y **7** (a11y de UI) se *siembran* aquí
> y se *exigen* en F4 y F6 — no los penalices si faltan.

## Objetivos evaluados
> De `objetivos` en `ejercicio.yml`.

- **O1** — Diseñar y construir una API REST end-to-end: spec primero, ports & adapters, PostgreSQL + SQLAlchemy + migraciones Alembic, OpenAPI vivo, errores RFC 9457.
- **O2** — Aplicar seguridad como hábito: OAuth2/JWT + autorización por dueño/scope; mitigar BAC (IDOR), Injection y SSRF; rate limiting; secretos fuera del repo.
- **O3** — Hacer el sistema confiable y demostrable: idempotencia, observabilidad (logs + correlation IDs), tests medidos por mutation score, README en inglés y write-up de trade-offs.

## Criterios y niveles

### C1 — Diseño spec-first + ADR + arquitectura · mapea: O1 · DoD 1 · hilo: spec-driven
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay `SPEC.md`, o se escribió **después** del código (su commit es posterior al primer endpoint), o no hay ADR. La arquitectura es un solo archivo donde el router llama directo a SQLAlchemy. |
| **en-progreso** | Hay spec pero le faltan errores/casos borde; el ADR no justifica nada real ("usé FastAPI porque sí"); hay carpetas `dominio/adapters` pero el dominio importa `fastapi` o `sqlalchemy` (el hexágono es decorativo). |
| **competente** | `SPEC.md` con recursos, endpoints (verbo/status/errores) y casos de seguridad, commiteada **antes** del primer endpoint; ADR con contexto/decisión/alternativas/consecuencias; el paquete de dominio **no importa** frameworks y define puertos que los adapters implementan. |
| **excelente** | Cada caso borde de la spec es trazable a una rama/validación y a un test; el ADR nombra el costo aceptado y anticipa la extensión RAG de F6 (un adapter más); el dominio se testea con un repo en memoria sin levantar Postgres. |

### C2 — Persistencia y corrección REST · mapea: O1 · DoD 8
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No usa Postgres (o usa `create_all` como esquema en prod, sin migraciones); status codes arbitrarios; el CRUD se rompe con cualquier entrada inesperada. |
| **en-progreso** | Postgres + SQLAlchemy pero migraciones a medias (una inicial y luego `create_all`); status codes mayormente correctos; listados con N+1 evidente. |
| **competente** | Todo cambio de esquema es una migración Alembic aplicable/reversible; status codes correctos (201/202/404/409/422); paginación; queries parametrizadas; sin N+1 obvio en los listados. |
| **excelente** | Migraciones limpias y revisadas (no solo autogeneradas a ciegas); usa transacciones/locking donde el estado compartido lo exige (lo de `3.3`); el contrato OpenAPI en `/docs` es completo y fiel. |

### C3 — Seguridad aplicada · mapea: O2 · DoD 3 · hilo: seguridad
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Contraseñas en texto plano o con `==` sobre el hash; sin authz (cualquier token ve cualquier recurso → IDOR abierto); SQL por f-string (Injection); secreto en el código; sin rate limiting. |
| **en-progreso** | Auth con JWT y hashing correctos, pero la autorización es un `if` frágil o falta en algún endpoint; SSRF mitigado solo con un regex de string; rate limiting parcial; `.env` existe pero el secreto real quedó en algún commit. |
| **competente** | OAuth2 password flow + JWT (hash argon2 con `pwdlib`, firma `PyJWT`); **autorización por dueño en la query** (IDOR cerrado, con test); queries parametrizadas/ORM; guardia SSRF que resuelve DNS y rechaza IPs privadas/loopback/metadata; rate limiting en auth/import; secretos en env vars + `.gitignore`. |
| **excelente** | Las tres mitigaciones (BAC/Injection/SSRF) tienen **test que lo demuestra**; la guardia SSRF cubre redirecciones y DNS rebinding; `gitleaks` y un dependency-scan (`pip-audit`) corren en CI; 404 (no 403) para recurso ajeno, para no filtrar existencia. |

### C4 — Confiabilidad y contrato de error · mapea: O3 · DoD 4 (parcial) · hilo: costo-latencia/resiliencia
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El endpoint sensible no es idempotente (un reintento duplica el efecto); errores como `{"detail": "..."}` sin contrato; sin timeouts en el fetch saliente. |
| **en-progreso** | Intenta idempotencia con un `try/except` o un check sin índice único (hay carrera); errores RFC 9457 solo en algunos paths. |
| **competente** | Idempotencia real: `Idempotency-Key` persistida con **índice único**, el reintento devuelve el resultado guardado sin repetir el efecto; **todos** los errores en formato RFC 9457 (`application/problem+json`); timeout en el cliente HTTP. |
| **excelente** | La idempotencia maneja la concurrencia (índice único + manejo del conflicto, no solo "consultar y luego insertar"); aplica backoff+jitter/circuit breaker donde corresponde (lo de `3.14`); el `type` del error apunta a doc útil. |

### C5 — Calidad de tests y observabilidad · mapea: O3 · DoD 2 y 4 · hilos: testing, observabilidad
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin tests, o tests sin `assert`; "calidad" justificada con un % de coverage; logs con `print`; sin correlation ID; sin CI. |
| **en-progreso** | Hay tests de contrato pero acoplados a implementación (mockean de más) o sin tests de dominio; mide coverage pero no corrió mutation testing; logs estructurados a medias. |
| **competente** | Tests de contrato (401/404-RFC9457/409-idempotencia/422/429) + dominio puro; **mutation score reportado** con mutmut (no solo coverage); lint en CI; logs estructurados (JSON) con correlation ID por request. |
| **excelente** | El mutation score es alto y el alumno discute los mutantes sobrevivientes que decidió no matar (y por qué); los tests de dominio corren sin DB (prueba de buen hexágono); la correlation ID se propaga y se ve en la demo. |

### C6 — Entregables y comunicación · mapea: O3 · DoD 8 y 9 · hilo: inglés
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin README usable o sin demo; historial con `wip`/un commit gigante "toda la API"; sin write-up; README en español (cuando el hilo de inglés ya está activo). |
| **en-progreso** | README incompleto (falta `docker compose up` o un ejemplo copiable) o demo no pegada; algunos commits no son Conventional Commits; write-up superficial. |
| **competente** | README **en inglés** que un desconocido sigue (qué es, levantar con `docker compose up`, demo pegada que corre); historial 100% Conventional Commits; write-up de trade-offs (3–6 líneas). |
| **excelente** | El historial se lee como la historia del proyecto (spec → ADR → migración → features verticales → fix de bordes → docs); el write-up nombra un trade-off **defendible** y qué mediría distinto; la demo es reproducible. |

### C7 — Autonomía y comprensión demostrada · gate Primero-Sin-IA · señal anti-dependencia
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar partes de su propio código; sofisticación (abstracciones, patrones) que no calza con lo que defiende; indicios de arquitectura y mitigaciones pegadas de un chat. |
| **en-progreso** | Explica el qué pero no el porqué; titubea al justificar dónde vive el control de acceso o por qué la idempotencia necesita índice único. |
| **competente** | Explica **cada decisión sin notas**: por qué el dominio no importa frameworks, cómo cierra el IDOR en la query, qué garantiza la idempotency key, los tres controles de la guardia SSRF, por qué el mutation score importa. |
| **excelente** | Reflexiona sobre dónde sintió el impulso de delegar a la IA y cómo lo resolvió; convierte una dificultad (p. ej. SSRF) en una regla reutilizable; anticipa cómo evolucionará la API en F4/F6. |

## Errores típicos a marcar
- **Auth confundida con authz:** valida el JWT pero no filtra por dueño → IDOR abierto. La defensa va en la query (`WHERE owner_id = ...`), no en un `if`.
- **Idempotencia con `try/except`:** un reintento tras timeout es un request nuevo; el `except` ni se entera. Falta la clave persistida con índice único.
- **SSRF "mitigado" con regex:** no resuelve DNS, no bloquea `169.254.169.254`/loopback/privadas, no controla redirecciones. Un regex de "parece URL" no protege.
- **Coverage como meta:** "95% de coverage" sin mutation score. Un test sin `assert` da coverage y no detecta nada.
- **`create_all` en producción:** sin migraciones no hay historia ni rollback ni evolución con datos.
- **Secreto en el código/historial:** `SECRET_KEY` hardcodeado, o un `.env` real commiteado en algún punto del historial (revisar `git log -p`, no solo el HEAD).
- **Hexágono decorativo:** carpetas `dominio/adapters` pero el dominio importa `fastapi`/`sqlalchemy`; los tests de dominio necesitan Postgres.
- **Errores sin contrato:** `{"detail": ...}` para todo; el frontend de F4 no puede programar contra eso. Falta RFC 9457.
- **`async def` con cliente bloqueante** dentro: congela el event loop (anti-patrón de `3.8`).
- (transversales) persigue coverage% en vez de mutation score; falta un trade-off defendible en el write-up; README en español con el hilo de inglés ya activo.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación. Nunca dar la solución.
- Arquitectura "de libro" (hexagonal impecable, genéricos avanzados) que el alumno no puede explicar capa por capa.
- `SPEC.md`/ADR con prosa pulida **desconectada** del código (menciona mitigaciones que el código no tiene, o al revés).
- Historial con **un commit gigante** o mensajes genéricos: señal de que pegó un resultado en vez de construir por pasos.
- Mitigaciones de seguridad presentes pero el alumno no sabe *a qué ataque* responden (no puede nombrar el destino de un SSRF ni por qué 404 y no 403 en el IDOR).
- **Verificación sugerida:** pídele que **en vivo** agregue un endpoint nuevo con su control de acceso y un test que pruebe el IDOR, y que explique en qué línea vive el filtro por dueño. Si lo construyó de verdad, lo hace en minutos; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca entregar arquitectura ni código de la solución de referencia. El alumno eligió su dominio: el feedback se ancla en *su* spec.
- **Pista (nivel 1):** "Toma `GET /<recurso>/{id}` y crea un recurso con el usuario A; intenta leerlo con el token del usuario B. ¿Qué status devuelve hoy tu API? Si es 200, ahí está el IDOR."
- **Pregunta socrática (nivel 2):** "Tu endpoint sensible recibe el mismo `Idempotency-Key` dos veces (el cliente reintentó tras un timeout). Sígueme el camino en tu código: ¿dónde reconoces que esa clave ya se usó?, ¿qué pasa si dos requests con la misma clave llegan a la vez? Si no hay un índice único, hay una carrera."
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón es **filtrar por dueño en la query, no validar después**: la consulta lleva siempre `WHERE owner_id = <usuario actual>`, de modo que el recurso ajeno no existe para esta sesión. Reescribe el repo para que reciba el `owner_id` y vuelve a correr tu test de IDOR antes de seguir."

## Conexión con el proyecto / capstone
- Este **es** el capstone de la Fase 3: cierra el constructive alignment de toda la fase (modelado de `3.1-3.3`, FastAPI de `3.8`, hexagonal de `3.9`, OAuth2 de `3.12`, OWASP de `3.13`, idempotencia de `3.14`). El backend que se mide aquí es la **base reutilizable** que el frontend de la Fase 4 consume (su contrato OpenAPI + RFC 9457) y que la plataforma RAG de la Fase 6 extiende como un adapter más —el pago directo de haber hecho ports & adapters. Los puntos del DoD que se ejercitan aquí (spec+ADR, tests medidos, seguridad, observabilidad, demo, Conventional Commits) reaparecen en *todos* los capstones siguientes.
