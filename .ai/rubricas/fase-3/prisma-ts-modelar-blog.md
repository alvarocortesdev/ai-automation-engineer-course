---
ejercicio_id: fase-3/prisma-ts-modelar-blog
fase: fase-3
sub_unidad: "3.6"
version: 1
---

# Rúbrica — Modela un dominio en `schema.prisma` y escribe sus queries

> Rúbrica **analítica** atada a los `objetivos` del contrato. Se evalúa el **modelo** (relaciones y FK en el lado correcto), la **comprensión** (fuente de verdad, drift, type-safety) y que las **queries no caigan en N+1**, no que el alumno memorice la sintaxis de Prisma. Un schema que valida con la FK en el lado equivocado es peor que uno con una errata de sintaxis pero el modelo bien.

## Objetivos evaluados
- **O1** — Modelar 1:N y N:M con las FK en el lado correcto e índices justificados.
- **O2** — Validar el schema y explicar la fuente de verdad y el drift.
- **O3** — Escribir queries type-safe que leen relaciones con `include`/`select` sin N+1.

## Criterios y niveles

### C1 — Modelo de relaciones (corrección del diseño) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta un modelo (p. ej. no separa `Tag`), o pone la FK de la 1:N en `User` en vez de `Post`, o intenta una N:M con una sola FK. El schema no representa el requisito. |
| **en-progreso** | Los tres modelos existen pero la relación está a medias: declara `posts Post[]` en `User` sin la FK `authorId` en `Post`, o escribe una tabla de unión manual para la N:M sin necesidad (sin atributos propios). |
| **competente** | `User`/`Post`/`Tag` correctos; 1:N con `authorId Int` + `@relation` en `Post` y `posts Post[]` en `User`; N:M con `Tag[]`/`Post[]` (Prisma genera la unión); `@@index([authorId])` presente. `npx prisma validate` pasa. |
| **excelente** | Además: justifica que la N:M implícita basta porque la unión no tiene atributos, pero sabe cuándo la haría explícita (un tercer modelo con su fecha de etiquetado); usa tipos correctos (`String?` para lo opcional, `Boolean @default(false)` para `published`); nota que `email`/`name` único va donde corresponde. |

### C2 — Comprensión: fuente de verdad y drift (NOTAS.md calza con el schema) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `NOTAS.md`, o no menciona qué genera Prisma a partir del schema. |
| **en-progreso** | Dice "el schema es la fuente de verdad" sin explicar *qué* se deriva de él (migraciones + cliente) ni qué es el drift. |
| **competente** | Explica que de `schema.prisma` se generan las migraciones SQL **y** el cliente type-safe, y que editar la base por fuera crea drift (el schema deja de describir la base real). |
| **excelente** | Distingue `migrate dev` (genera+aplica, desarrollo) de `migrate deploy` (solo aplica, producción) y por qué el cambio siempre nace en el schema; conecta drift con reproducibilidad/CI. |

### C3 — Queries type-safe sin N+1 (criterio de ingeniería) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Las queries usan campos inexistentes (no type-safe), o lee usuarios con posts haciendo un `findMany` y luego un loop con una query por usuario (N+1 a mano). |
| **en-progreso** | Las queries existen y son type-safe pero no usan `include`/`select` donde tocaba (trae todo y filtra en JS, o no pagina cuando el requisito lo pide). |
| **competente** | Las cuatro queries correctas y type-safe: nested write para crear, `include`/`select` para leer relaciones sin N+1, `where`+`orderBy`+`take` para los recientes, `count` para el conteo. |
| **excelente** | Usa `select` (no `include`) para traer solo lo necesario en la lista de posts (más liviano); comenta el costo/latencia de traer relaciones de más; menciona que `$queryRawUnsafe` sería el agujero a evitar si tentara escribir SQL crudo. |

## Errores típicos a marcar
- **FK en el lado equivocado**: poner `authorId` o la relación "fuerte" en `User` en vez de `Post`. El error central del modelado 1:N.
- **Tabla de unión manual innecesaria** para la N:M (sin atributos propios): Prisma la genera sola; escribirla a mano delata copiar un patrón de SQL sin entender Prisma.
- **N+1 reintroducido a mano**: `findMany` de usuarios seguido de un loop con `findUnique`/`findMany` de posts por usuario. Es el error que la lección persigue.
- **Campo no-nullable cuando el requisito dice opcional** (o al revés): `name` debe ser `String?`.
- **Indexar de más / no indexar la FK** que se filtra: muestra que no trasladó el criterio de 3.1.
- (transversales) `NOTAS.md` que no nombra ni qué se genera del schema ni el drift; queries que traen columnas de más sin notar el costo; ningún trade-off Prisma↔SQLAlchemy defendible.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Schema impecable y sobre-sofisticado (relaciones explícitas con nombres, `@map`, tipos exóticos) impropio de una primera vez con Prisma, pero `NOTAS.md` no puede explicar por qué la FK va en `Post`.
- Queries que usan features avanzadas (`_count`, `connectOrCreate`) sin que el requisito las pida, junto a una explicación que no calza con el código.
- **Verificación sugerida:** pedir, en voz alta, "si quitaras `include` de la query de usuarios-con-posts y cargaras los posts en un loop, ¿cuántas queries harías con 100 usuarios y cómo se llama eso?". Quien entendió dice "101, N+1"; quien dependió de la IA se traba.

## Feedback sugerido (graduado)
> Nunca dar el schema/queries de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "En una relación 1:N, ¿de qué lado vive la columna de clave foránea en SQL: en el 'uno' o en los 'muchos'? Lleva esa misma respuesta a Prisma."
- **Pregunta socrática (nivel 2):** "Tu query de usuarios-con-posts, ¿hace una sola ida a la base o una por usuario? ¿Cómo lo verificarías? ¿Qué palabra de Prisma le dice 'tráete la relación de una'?"
- **Dirección concreta (nivel 3, solo tras intento real):** "La FK `authorId` va en `Post` con `@relation(fields: [authorId], references: [id])`; en `User` solo `posts Post[]`. Para leer sin N+1: `findMany({ include: { posts: true } })`. Reescribe `NOTAS.md` explicando qué se genera del schema y qué es drift."

## Conexión con el proyecto / capstone
- Modelar relaciones con las FK en el lado correcto y leerlas sin N+1 es el mismo criterio que sostiene el **Capstone F3** (aunque el capstone use SQLAlchemy). Si tomas la ruta Node/NestJS ([`3.10`](/fase-3-backend/3-10-backend-nestjs/)), este schema es literalmente la capa de datos del proyecto.
