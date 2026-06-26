---
ejercicio_id: fase-3/prisma-ts-modelar-blog
fase: fase-3
sub_unidad: "3.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Modela un dominio en `schema.prisma` y escribe sus queries

## `schema.prisma` canónico

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/client"
}

datasource db {
  provider = "postgresql"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  tags      Tag[]
  createdAt DateTime @default(now())

  @@index([authorId])
}

model Tag {
  id    Int    @id @default(autoincrement())
  name  String @unique
  posts Post[]
}
```

`npx prisma validate` debe pasar en verde.

## `consultas.ts` canónico

```typescript
import { PrismaClient } from "./generated/client";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL });
const prisma = new PrismaClient({ adapter });

// 1) Nested write: usuario + su primer post en una operación.
export async function crearUsuarioConPost(email: string, titulo: string) {
  return prisma.user.create({
    data: {
      email,
      posts: { create: [{ title: titulo }] },
    },
  });
}

// 2) Usuarios con posts, sin N+1.
export async function usuariosConPosts() {
  return prisma.user.findMany({ include: { posts: true } });
}

// 3) 10 posts publicados más recientes con el nombre del autor (select liviano).
export async function postsPublicadosRecientes() {
  return prisma.post.findMany({
    where: { published: true },
    select: {
      id: true,
      title: true,
      author: { select: { name: true } },
    },
    orderBy: { createdAt: "desc" },
    take: 10,
  });
}

// 4) Conteo de publicados.
export async function contarPublicados(): Promise<number> {
  return prisma.post.count({ where: { published: true } });
}
```

## Razonamiento paso a paso

1. **Modelos.** Tres entidades con identidad propia: `User`, `Post`, `Tag`. Un usuario existe sin posts; una etiqueta existe sin posts. Cada una pide su tabla.

2. **Relación 1:N (User → Post).** La FK vive en el lado "muchos" (igual que en SQL): `Post.authorId` con `@relation(fields: [authorId], references: [id])`. En `User`, `posts Post[]` es la **vista** del otro lado, no una columna. Poner la FK en `User` sería el error central.

3. **Relación N:M (Post ↔ Tag).** Se declara con `tags Tag[]` en `Post` y `posts Post[]` en `Tag`. Prisma genera la tabla de unión implícita (`_PostToTag`) — el alumno **no** debe escribirla. Solo se modelaría explícitamente (un tercer modelo) si la unión necesitara atributos propios (p. ej. la fecha en que se etiquetó). Reconocer eso es nivel excelente.

4. **Tipos.** `name String?` y `content String?` (opcionales → nullable, se reflejan como `string | null`). `published Boolean @default(false)`. `email`/`name` de tag `@unique`. `DateTime @default(now())` para timestamps.

5. **Índice.** `@@index([authorId])` porque se filtra/une por autor. La PK ya viene indexada; no se indexa de nuevo. El `email @unique` ya crea su propio índice único.

6. **Queries sin N+1.** La #2 usa `include: { posts: true }` → Prisma hace un número fijo de queries (una por nivel de relación), no una por usuario. La #3 usa `select` anidado para traer solo lo necesario (más liviano que `include`, que traería la fila completa del autor). La #1 es un nested write (crea usuario y post atómicamente). La #4 usa `count` (no traer filas para contarlas en JS).

7. **Fuente de verdad / drift (NOTAS.md).** De `schema.prisma` se generan **las migraciones SQL** (`prisma migrate dev`) **y el cliente type-safe** (`prisma generate`). El cambio nace siempre en el schema; la base es un derivado. Editar la base por fuera (`ALTER TABLE` a mano) crea **drift**: el schema deja de describir la base real y la próxima migración detecta una diferencia inesperada.

## Puntos resbalosos (donde el corrector debe mirar)

1. **FK en `User`** en vez de en `Post`: el error #1 de la 1:N.
2. **Tabla de unión escrita a mano** para la N:M sin atributos: innecesaria; Prisma la genera.
3. **N+1 reintroducido**: query #2 hecha con `findMany` + loop en vez de `include`.
4. **`name`/`content` no-nullable** cuando el requisito los pide opcionales (faltó el `?`).
5. **`include` donde bastaba `select`** en la query #3 (trae de más → costo): aceptable pero el excelente usa `select`.
6. **No indexar `authorId`** o indexar de más "por si acaso".

## Rango de soluciones aceptables

- `cuid()`/`uuid()` como PK en vez de `autoincrement()` es válido si lo justifica (IDs no adivinables); no penalizar.
- Usar `include: { author: true }` en la query #3 en vez de `select` anidado es **competente** (funciona y evita N+1); el `select` es la versión excelente por traer menos.
- Modelar la N:M como relación **explícita** (un modelo `PostTag` con `@relation`) es aceptable e incluso necesario **si** el alumno argumenta que la unión tendrá atributos; si no hay atributos, la implícita es preferible por simplicidad.
- `String @db.Text` para `content` largo es un detalle válido, no exigido.
- `NOTAS.md` vale con cualquier redacción que (a) diga qué se genera del schema (migraciones + cliente), (b) defina drift con un ejemplo, y (c) ate el índice a una consulta. El excelente distingue `migrate dev` de `migrate deploy`.
- **Variante de control anti-IA:** pedir que diga, sin `include`, cuántas queries haría la lista de usuarios-con-posts con 100 usuarios cargando en loop. Respuesta esperada: 101, N+1.
