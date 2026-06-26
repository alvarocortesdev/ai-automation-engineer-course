---
ejercicio_id: fase-3/graphql-schema-y-n1
fase: fase-3
sub_unidad: "3.11"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Este ejercicio es de **diseño**: hay variantes válidas; lo que sigue es la referencia ejemplar + el criterio para juzgar otras.

# Solución de referencia — Diseña el schema y caza el N+1

## 1. `schema.graphql` (referencia ejemplar)

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  bio: String
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  body: String!
  author: User!
  comments: [Comment!]!
}

type Comment {
  id: ID!
  text: String!
  author: User!
}

type Query {
  user(id: ID!): User
  feed: [Post!]!
}
```

**Por qué así (lo que el alumno debe poder defender):**
- `User.posts: [Post!]!` y `Post.author: User!` modelan la relación 1:N **en los dos lados** del grafo. La FK conceptual (`authorId`) **no** se expone como campo: vive dentro del resolver. Exponer `authorId: ID!` es el error más común (mezcla el modelo de tabla con el grafo).
- `bio: String` (sin `!`) porque puede faltar; el resto es non-null. Que la nullability sea **defendible**, no uniforme.
- `user(id: ID!): User` **sin `!`** en el retorno: si no existe ese id, devuelve `null`. `feed: [Post!]!` cubre la pantalla de feed.
- Variantes aceptables: `feed(limit: Int = 20): [Post!]!` con paginación; nombres distintos (`recentPosts`, `posts`). Lo que importa es que el `Query` cubra **ambas** pantallas.

## 2. `consulta.graphql` (pantalla de perfil)

```graphql
query PerfilDeUsuario {
  user(id: "1") {
    name
    posts {
      title
    }
  }
}
```

Lo clave: **ni `email`, ni `bio`, ni `body`**. Pedir cualquiera de esos es over-fetching y baja a "en-progreso" el criterio C2. La forma del JSON de respuesta será exactamente `{ data: { user: { name, posts: [{ title }] } } }`.

## 3. `NOTAS.md` — respuestas canónicas

### (a) El N+1 del feed
Con resolvers ingenuos, la query `feed { title author { name } }` con **30 posts**:
- **1** query para `feed` → `SELECT * FROM posts ORDER BY created_at DESC LIMIT 30`.
- **30** queries: una por post para resolver `author` → `SELECT * FROM users WHERE id = ?`.

Total: **1 + 30 = 31** queries. Es el N+1 (1 para la lista + N para la relación por fila).

### (b) La cura DataLoader
DataLoader **acumula** los 30 `authorId` que pidieron los resolvers de `author` en este tick y ejecuta **una sola** query:

```sql
SELECT * FROM users WHERE id IN (id1, id2, ..., id30);
```

Total tras la cura: ~**2** queries (la del feed + la batched de autores), sin importar cuántos posts haya. **Contrato de orden** del `load_fn`: debe devolver los resultados **en el mismo orden y con la misma longitud** que las keys recibidas; si los devuelve en otro orden (p. ej. el que vino de la base), cada post recibiría el autor de otro post — bug de correctitud, no de rendimiento.

### (c) Un costo de GraphQL (cualquiera de estos vale)
- **Caching:** todo es `POST /graphql`, así que el caching por URL del navegador y los CDN dejan de servir (con `GET /users/1` lo tendrías gratis).
- **Autorización por campo:** el cliente arma combinaciones imprevistas, así que hay que autorizar campo por campo en vez de proteger rutas.
- **Observabilidad:** las métricas/logs por ruta dejan de servir (todo cae en `/graphql`); se necesitan trazas a nivel de campo.
- **Seguridad (excelente):** el cliente controla la forma → superficie de DoS por queries no acotadas (Unbounded Consumption); exige límites de profundidad/complejidad e introspección apagada en prod.

## 4. Competente vs excelente
- **Competente:** schema con relaciones y nullability defendible; query sin over-fetching; N+1 = `1 + 30 = 31`; DataLoader con `IN`; un costo nombrado.
- **Excelente:** además no expone `authorId`, conecta explícitamente con el N+1 de ORMs ([`3.5`]) ("mismo bug"), explica por qué en GraphQL es más fácil de provocar (el cliente elige la profundidad), y ata el costo a seguridad/observabilidad.

## 5. Errores a marcar (resumen)
- `authorId: ID!` expuesto en vez de `author: User!`.
- Nullability uniforme (todo `!` o nada).
- Relación 1:N como objeto único (`posts: Post`).
- Query con campos de más.
- N+1 = 30 (olvida la query del listado) o "GraphQL no tiene N+1".
- DataLoader sin el contrato de orden.
- GraphQL vendido como gratis (sin costo nombrado).

## 6. Variante de control anti-IA
Pedir el N+1 con **5** posts (respuesta: `1 + 5 = 6`) y qué pasa si `load_fn` devuelve los autores ordenados alfabéticamente en vez de por las keys (respuesta: cada post recibe el autor equivocado — cruce de datos). Quien razonó lo construye; quien copió una explicación genérica se traba.
