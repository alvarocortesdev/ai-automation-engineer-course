# Ejercicio 3.11a — Diseña el schema y caza el N+1

> **Modalidad: a mano (sin ejecutar, sin IA).** No se corre ningún servidor. Diseñas un schema de GraphQL, escribes una query que no haga over-fetching, y trazas el N+1 que aparece en los resolvers (con el número exacto) explicando cómo lo cura DataLoader. Se evalúa tu **modelo mental**, no que la query corra.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.11` GraphQL: nociones
**Ruta:** opcional / profundización · **Timebox:** 40–45 min

## 🎯 Objetivo

Leer un escenario REST que sufre over/under-fetching, **modelar** el schema de GraphQL equivalente (types, relaciones, `Query`), escribir una query que pida **exactamente** lo que una pantalla necesita, y **diagnosticar el N+1** de los resolvers dando el número de queries y explicando la cura (DataLoader).

## 📋 Contexto

El N+1 que cazaste en ORMs (lección `3.5`) reaparece en los resolvers de GraphQL, amplificado porque el cliente elige la forma de la query. Saber trazarlo y nombrar su cura es el puente entre "uso GraphQL" y "sé por qué mi API se cae con 200 usuarios". Y elegir el campo justo en una query es el músculo anti-over-fetching que da valor a GraphQL.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** (graphql.org/learn, strawberry.rocks).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* el schema.
4. Mañana, **reescribe de memoria** el `type User` con su relación `posts` y la cuenta del N+1. Si no puedes, no lo aprendiste todavía.

## 🧩 El escenario

Una app de blog con dos pantallas que hoy se sirven con REST:

- **Pantalla de perfil:** muestra el **nombre** de un usuario y los **títulos** de sus posts. Hoy hace `GET /users/1` (devuelve el usuario completo: nombre, email, bio, settings — over-fetching) y luego `GET /users/1/posts` (segundo round trip, devuelve los posts completos con su cuerpo entero — over + under-fetching).
- **Pantalla de feed:** lista los **posts** más recientes, cada uno con su **título** y el **nombre de su autor**.

Entidades del dominio: un **User** (id, name, email, bio) escribe muchos **Post** (id, title, body), y cada **Post** tiene muchos **Comment** (id, text, y el User que lo escribió).

## 🛠️ Instrucciones

Completa los archivos de esta carpeta (tienen TODOs):

1. **`schema.graphql`** — define los `type User`, `type Post`, `type Comment` con sus campos tipados y su nullability (`!`), las relaciones como listas (`[T!]!`) donde corresponda, y un `type Query` con las entradas que **ambas** pantallas necesitan.
2. **`consulta.graphql`** — una sola query que resuelva la **pantalla de perfil** pidiendo **exactamente** los campos que esa pantalla usa (ni `email`, ni `bio`, ni `body`).
3. **`NOTAS.md`** — responde por escrito:
   - **(a)** Para la pantalla de feed, una query lista posts con `title` y `author { name }`. Sobre resolvers ingenuos (cada `author` se resuelve una vez por post) y con **30 posts**, ¿cuántas queries golpean la base? Da el número y muéstralo como `1 + N`.
   - **(b)** Explica con tus palabras cómo **DataLoader** baja eso a ~2 queries (qué hace el batching, qué `WHERE` genera) y cuál es el **contrato de orden** de `load_fn`.
   - **(c)** Nombra **un** costo real de haber elegido GraphQL en esta app (caching HTTP, autorización por campo, u observabilidad por ruta). No lo vendas como gratis.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `schema.graphql` tiene los tres types con campos tipados, relaciones como `[T!]!` donde aplica, y un `Query` que cubre perfil y feed.
- [ ] `consulta.graphql` pide **solo** los campos de la pantalla de perfil (nombre + títulos), demostrando el anti-over-fetching.
- [ ] La traza del N+1 da el número correcto (**1 + 30 = 31**) en formato `1 + N`.
- [ ] La explicación de DataLoader incluye el batching con `IN (...)` **y** el contrato "mismo orden / misma longitud que las keys".
- [ ] Nombras un costo real de GraphQL.
- [ ] Puedes explicar, sin notas, por qué este N+1 es "el mismo" que el de los ORMs.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- `User` tiene `posts: [Post!]!`; `Post` tiene `author: User!` y `comments: [Comment!]!`; `Comment` tiene `author: User!`.
- La FK conceptual (`authorId`) no se expone como campo si ya tienes `author: User!`: el resolver la usa por dentro.
- La query de perfil: `user(id: "1") { name posts { title } }` — nada de `email`, `bio` ni `body`.
- N+1 del feed con 30 posts: **1** query para los posts + **30** para resolver `author` de cada uno = **31** (`1 + 30`).
- DataLoader: junta los 30 `authorId` y hace **una** query `SELECT * FROM users WHERE id IN (...)`, luego devuelve los autores **en el mismo orden** que los ids pedidos. Total ~2.
- Costo más fácil de defender: el caching — todo es `POST /graphql`, así que los CDN no lo cachean por URL como harían con `GET /users/1`.

Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA tu carpeta (`schema.graphql`, `consulta.graphql`, `NOTAS.md`), la **rúbrica** (`.ai/rubricas/fase-3/graphql-schema-y-n1.md`) y las instrucciones (`.ai/INSTRUCCIONES-CORRECTOR.md`). La **solución de referencia** vive en `.ai/soluciones/fase-3/graphql-schema-y-n1.md` — no la mires antes de intentarlo.
