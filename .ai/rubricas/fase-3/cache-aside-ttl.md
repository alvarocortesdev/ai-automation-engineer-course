---
ejercicio_id: fase-3/cache-aside-ttl
fase: fase-3
sub_unidad: "3.15"
version: 1
---

# Rúbrica — Cache-aside con TTL e invalidación

> Rúbrica analítica para un ejercicio de **código**. Lo que se evalúa no es solo que los tests pasen,
> sino que el alumno **entienda el patrón y el orden de las operaciones**, y que pueda defender por qué
> se borra (no se actualiza) la cache y por qué la DB va primero. Un alumno puede hacer pasar los tests
> copiando la forma sin entender el trade-off; la `bitacora.md` y el check de dominio lo distinguen.

## Objetivos evaluados
- **O1** — Implementar cache-aside: HIT devuelve desde cache sin tocar el repo; MISS consulta el repo y puebla la cache con TTL.
- **O2** — Invalidar al escribir: repo primero, borrar la entrada de cache después.
- **O3** — Explicar el trade-off y el orden (borrar vs actualizar; DB primero).

> Resultado esperado: los 4 tests provistos en verde + 1 test propio de "dos cambios seguidos". El corrector
> conoce la solución de referencia; **no se la da al alumno** salvo al cerrar, y nunca como atajo.

## Criterios y niveles

### C1 — Corrección del cache-aside (lectura) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `obtener` no implementa el patrón (siempre va al repo, o nunca puebla la cache). Tests de HIT/MISS en rojo. |
| **en-progreso** | Funciona el MISS pero el HIT igual consulta el repo (no corta con `return`), o puebla sin TTL / con TTL equivocado. |
| **competente** | HIT devuelve desde cache sin tocar el repo; MISS consulta una vez y puebla con `TTL_SEGUNDOS`. Los 3 tests de lectura en verde. |
| **excelente** | Además usa `is not None` (no `if cacheado:`), serializa con JSON (no pickle), y la `bitacora` explica por qué el `return` del HIT precede al acceso al repo. |

### C2 — Corrección de la invalidación (escritura) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `actualizar` no invalida (la siguiente lectura sirve el valor viejo cacheado). Test de invalidación en rojo. |
| **en-progreso** | Invalida pero en el **orden equivocado** (borra la cache antes de escribir el repo), o intenta "actualizar" la cache con el valor nuevo en vez de borrar. |
| **competente** | Escribe el repo primero y luego `delete` de la entrada. Test de invalidación en verde. |
| **excelente** | Añade el test propio de "dos cambios seguidos" que demuestra que nunca se sirve un valor intermedio rancio. |

### C3 — Calidad de ingeniería y testing · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corre `pytest`; no agrega test propio. |
| **en-progreso** | Tests pasan pero el test propio es trivial (repite uno existente) o no añade ninguno. |
| **competente** | Agrega un test propio significativo (dos cambios seguidos sin stale); código limpio, sin cambiar firmas. |
| **excelente** | El test propio nombra el escenario de race/stale en su nombre o comentario; razona sobre qué NO se está testeando (p. ej. concurrencia real). |

### C4 — Comprensión demostrada (la bitácora calza con el código) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `bitacora.md`, o no explica nada del trade-off. |
| **en-progreso** | Explica el "qué" (puse cache-aside) pero no el "por qué" (orden, borrar vs actualizar). |
| **competente** | Justifica los tres puntos: return del HIT antes del repo, invalidar borrando, DB primero. |
| **excelente** | Conecta con el trade-off latencia/frescura y nombra al menos un riesgo (stale, race, thundering herd) que el TTL mitiga. |

## Errores típicos a marcar
- **HIT que igual va al repo:** olvidar el `return` dentro del `if` del HIT, o no cortar. El test `test_hit_no_consulta_repo` lo caza.
- **Poblar sin TTL** o con un número distinto a `TTL_SEGUNDOS`: cache que crece sin límite / TTL equivocado. `test_miss_...` lo caza vía `cache.ttls`.
- **Invalidar en orden inverso** (borrar cache antes de escribir la DB): si la escritura falla, queda sin cache y con dato viejo.
- **"Actualizar" la cache en vez de borrar** en `actualizar`: write-through implícito, con races; el ejercicio pide cache-aside (borrar).
- **`if cacheado:` en vez de `is not None`:** bug latente con valores falsy (no lo cazan estos tests porque un dict serializa no-vacío, pero es un error de fondo a señalar en la bitácora/código).
- **`pickle` en vez de JSON:** acopla a Python y es inseguro al deserializar.
- (transversales) perseguir que "pasen los tests" sin agregar el propio; bitácora que describe el código en vez de defender las decisiones.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución impecable (incluye manejo de TTL con jitter, locks, pipelines) muy por encima del alcance pedido, pero la `bitacora` no explica por qué el `return` del HIT va primero.
- `bitacora.md` con vocabulario sofisticado (write-behind, read-through) que no aparece ni se usa en el código entregado.
- Test propio idéntico en estructura a los provistos, sin el escenario de "dos cambios seguidos".
- **Verificación sugerida:** pedir que explique, sin notas, qué pasaría si invirtiera el orden en `actualizar` (borrar antes de escribir la DB) y la escritura fallara. Si entendió, describe el "sin cache + dato viejo"; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu HIT recupera el valor, pero ¿estás seguro de que no sigue ejecutando hasta el repo? Mira dónde está tu `return`."
- **Pregunta socrática (nivel 2):** "En `actualizar`, si borraras la cache primero y la escritura a la base de datos fallara, ¿en qué estado queda el sistema? ¿Y por qué borrar es más seguro que escribir el valor nuevo en la cache?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El patrón a corregir es el corte del HIT: el `return json.loads(...)` debe estar **dentro** del `if cacheado is not None`, antes de cualquier acceso al repo. Y en `actualizar`, el orden es repo → `delete`. Reescribe ambos métodos con ese esqueleto y vuelve a correr los tests."

## Conexión con el proyecto / capstone
- Este ejercicio es exactamente el endpoint cacheado **opcional** del [Capstone F3 — API de producción](/fase-3-backend/proyecto/): cache-aside + TTL + invalidación inyectados en FastAPI, con la decisión documentada en un ADR. El mismo patrón reaparece como semantic caching de LLM en la Fase 6.
