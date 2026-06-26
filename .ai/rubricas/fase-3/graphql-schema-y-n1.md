---
ejercicio_id: fase-3/graphql-schema-y-n1
fase: fase-3
sub_unidad: "3.11"
version: 1
---

# Rúbrica — Diseña el schema y caza el N+1

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio de **diseño a mano** (no se ejecuta nada): se evalúa el schema, la query y el razonamiento del N+1 en `NOTAS.md`. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica.

## Objetivos evaluados
- **O1** — Modelar un schema de GraphQL (types, relaciones con nullability, `type Query`) a partir de un escenario REST.
- **O2** — Escribir una query que pida exactamente los campos de una pantalla (anti-over-fetching).
- **O3** — Diagnosticar el N+1 en resolvers (número `1+N`) y explicar la cura DataLoader (batching `IN` + contrato de orden).

## Criterios y niveles

### C1 — Corrección del schema · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta algún `type` (User/Post/Comment) o no hay relaciones; o `type Query` no cubre ambas pantallas. Confunde el campo de relación con la FK escalar. |
| **en-progreso** | Los types existen pero la nullability es incoherente (todo `!` o nada), o una relación 1:N no se modela como lista, o el `Query` solo cubre una pantalla. |
| **competente** | Tres types con campos tipados; `User.posts: [Post!]!`, `Post.author: User!` y `Post.comments: [Comment!]!`, `Comment.author: User!`; `Query` con `user(id)` y una entrada de feed (lista de posts). Nullability defendible. |
| **excelente** | Además **no expone `authorId` como campo** (usa `author: User!` y deja la FK al resolver), justifica la nullability (`user(id): User` sin `!` porque puede no existir) y comenta el porqué de cada decisión. |

### C2 — La query no hace over-fetching · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Pide campos de más (email, bio, body) o no es una query válida / no anida `posts { title }`. |
| **en-progreso** | Query válida pero con un campo de más, o pide `posts` completo en vez de solo `title`. |
| **competente** | `user(id) { name posts { title } }` exacto: ni un campo de sobra. Demuestra que entendió la promesa de GraphQL. |
| **excelente** | Además explica, en `NOTAS.md`, por qué la misma API serviría otra pantalla (admin) con **otra** query distinta sin tocar el servidor. |

### C3 — Diagnóstico del N+1 y la cura · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No da número, o da uno arbitrario; no menciona DataLoader ni el batching. |
| **en-progreso** | Da el número aproximado pero sin el formato `1 + N`, o menciona DataLoader sin explicar el `IN (...)` ni el contrato de orden. |
| **competente** | Traza **1 + 30 = 31**; explica que DataLoader junta los `authorId` y hace **una** query `WHERE id IN (...)` (baja a ~2); menciona el contrato "mismo orden / misma longitud que las keys". |
| **excelente** | Además conecta explícitamente con el N+1 de ORMs ([`3.5`]) ("es el mismo bug") y explica por qué en GraphQL es **más fácil de provocar** (el cliente elige la profundidad de la query). |

### C4 — Trade-off nombrado (hilo transversal) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra ningún costo de GraphQL; lo trata como upgrade gratis. |
| **en-progreso** | Nombra un costo genérico ("es más complejo") sin aterrizarlo. |
| **competente** | Nombra un costo real y concreto: caching HTTP perdido (todo `POST /graphql`), autorización por campo, u observabilidad por ruta. |
| **excelente** | Conecta el costo con seguridad (queries no acotadas = DoS / Unbounded Consumption) o con observabilidad (necesita trazas por campo), anticipando [`3.13`]. |

## Errores típicos a marcar
- **Exponer `authorId: ID!` como campo del `type Post`** en vez de la relación `author: User!` (mezcla el modelo de tabla con el grafo de GraphQL).
- **Poner toda la nullability igual** (todo `!` o nada): señal de copiar sin entender qué significa el `!`.
- **Modelar una relación 1:N como un solo objeto** (`posts: Post` en vez de `[Post!]!`).
- **Query con over-fetching** (pedir `email`/`body` "por si acaso"): contradice el punto entero de GraphQL.
- **N+1 mal contado** (decir "30 queries" en vez de 31, olvidando la query de la lista) o creer que GraphQL "no tiene N+1".
- **DataLoader sin el contrato de orden**: si `load_fn` devuelve en otro orden, cada usuario recibe los posts de otro (bug de correctitud, no de rendimiento).
- (transversales) vender GraphQL como gratis; no nombrar un solo trade-off defendible.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Schema perfecto y "de manual" pero `NOTAS.md` no puede explicar **por qué** el `!` va donde va, o por qué `author` no es `authorId`.
- El N+1 explicado con la frase exacta de un blog pero sin poder dar el número con otro N (p. ej. "¿y con 7 posts?").
- **Verificación sugerida:** pedir que recalcule el N+1 con **5** posts en vez de 30 (debe responder `1 + 5 = 6`) y que diga qué pasa si `load_fn` devuelve los autores en orden alfabético en vez del orden de las keys (debe ver el cruce de datos). Quien razonó lo construye; quien copió se traba.

## Feedback sugerido (graduado)
> Ordenadas de menos a más directas. **Nunca incluir el schema/solución completos.**
- **Pista (nivel 1):** "Mira tu `type Post`: ¿`author` es un escalar (`ID`) o un objeto (`User`)? ¿Y cuántas veces se ejecuta el resolver de `author` cuando listas muchos posts?"
- **Pregunta socrática (nivel 2):** "Si tienes 30 posts y cada uno resuelve su `author` por separado, ¿cuántas queries son en total contando la del listado? ¿Qué tendría que hacer una sola query para traer los 30 autores de una vez?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El N+1 es 1 (lista) + N (relación por fila). La cura es DataLoader: agrupa las N keys y hace un `WHERE id IN (...)`, devolviendo los resultados **en el mismo orden** que las keys. Reescribe `NOTAS.md` con el número `1 + 30` y esa explicación."

## Conexión con el proyecto / capstone
- El **[Capstone F3 — API de producción](/fase-3-backend/proyecto/)** es REST, pero el N+1 que aquí diagnosticas en resolvers es **el mismo** que ataca el capstone (relación cargada por fila). Saber nombrarlo y curarlo en ambos estilos (DataLoader / `selectinload`) es el instinto que el Definition of Done premia, y la decisión REST-vs-GraphQL es un ADR candidato del proyecto.
