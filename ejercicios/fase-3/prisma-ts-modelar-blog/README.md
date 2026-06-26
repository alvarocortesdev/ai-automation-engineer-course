# Ejercicio 3.6 — Modela un dominio en `schema.prisma` y escribe sus queries

> **Modalidad: mixto (diseño + código, a mano primero, sin IA).** Lo que se evalúa no es que memorices la sintaxis de Prisma, sino que traduzcas un requisito en prosa a un **modelo correcto** (relaciones y FK en el lado bien), entiendas por qué el `schema.prisma` es la fuente de verdad, y escribas lecturas de relación que **no caigan en N+1**. Es lo mismo que ya hiciste en SQL ([`3.1`](/fase-3-backend/3-1-sql-modelado-relacional/)), ahora con la cara de Prisma.

## Objetivos

- **O1** — Modelar un dominio en `schema.prisma`: modelos, relación 1:N y relación N:M, e índices, con las FK en el lado correcto.
- **O2** — Validar el schema (`npx prisma validate`) y explicar por qué `schema.prisma` es la única fuente de verdad y qué es el *drift*.
- **O3** — Escribir queries **type-safe** del cliente Prisma que cubran crear (nested write), leer relaciones con `include`/`select` sin N+1, filtrar+paginar y contar.

## El requisito (tal como te lo daría un cliente)

> "Quiero un mini-blog. Tengo **usuarios** (con email único y un nombre opcional). Un usuario escribe **posts** (con título, contenido opcional, y un flag de publicado). Un usuario puede tener muchos posts; cada post tiene **un** autor. Además quiero **etiquetas** (con nombre único): un post puede llevar varias etiquetas y una etiqueta puede estar en muchos posts. Necesito: listar cada usuario con sus posts, ver los posts publicados más recientes con el nombre de su autor, y contar cuántos posts publicados hay."

## Tu tarea (en este orden — Primero-Sin-IA, timebox 40–45 min)

1. **Modela a mano primero** (papel o borrador): ¿qué modelos hay? ¿qué relación es cada una (1:N, N:M)? ¿en qué lado va la FK? ¿qué índice motiva cada consulta del requisito?
2. **Completa `schema.prisma`**: añade los modelos `User`, `Post` y `Tag` con sus campos, relaciones e índices. El starter ya trae el `generator` y el `datasource`.
3. **Valida** sin necesidad de una base corriendo:

   ```bash
   npx prisma validate
   npx prisma format   # opcional: ordena y alinea el schema
   ```

4. **Escribe las cuatro queries** en `consultas.ts` (firmas dadas en el starter): crear un usuario con un post (nested write), listar usuarios con sus posts (sin N+1), traer los 10 posts publicados más recientes con el nombre del autor, y contar los publicados.
5. **Escribe `NOTAS.md`**: dónde pusiste cada FK y por qué, qué índice responde a qué consulta, por qué `schema.prisma` es la fuente de verdad, y qué pasaría si editaras la base por fuera (*drift*).

> Hazlo a mano primero. El valor está en *pensar el modelo y el flujo de datos*, no en que el editor autocomplete. Solo después valida la sintaxis.

## Qué entregar (deja estos archivos en esta carpeta)

- `schema.prisma` — tu modelo completo (parte del starter incluido).
- `consultas.ts` — tus cuatro queries (firmas en el starter; complétalas).
- `NOTAS.md` — tu justificación: relaciones, FK, índices, fuente de verdad y *drift*.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `npx prisma validate` pasa en verde.
- [ ] La relación 1:N tiene la FK (`authorId`) en `Post` (el lado "muchos"), no en `User`; `User` tiene `posts Post[]` (la vista, no una columna).
- [ ] La N:M (Post ↔ Tag) está declarada con `Tag[]`/`Post[]` sin que escribas la tabla intermedia a mano (Prisma la genera) — salvo que argumentes que necesita atributos propios.
- [ ] Hay un índice sobre la FK por la que filtras, justificado por una consulta concreta.
- [ ] Las queries usan campos que existen (type-safe) y leen relaciones con `include`/`select`, **nunca** con una query dentro de un loop.
- [ ] `NOTAS.md` explica la fuente de verdad y el *drift* con tus palabras.
- [ ] Puedes explicar, sin notas, en qué se parece y en qué difiere esto del mismo modelo en SQLAlchemy.

## Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

La 1:N se declara en los dos lados pero la FK real vive en uno solo: `Post` lleva `authorId Int` y `author User @relation(fields: [authorId], references: [id])`; `User` lleva `posts Post[]`. La N:M es `tags Tag[]` en `Post` y `posts Post[]` en `Tag` — Prisma crea la tabla de unión sola. El índice va sobre `authorId` (filtras posts por autor). Para listar usuarios con posts sin N+1: `prisma.user.findMany({ include: { posts: true } })`. Para posts publicados con autor: `findMany({ where: { published: true }, select: { title: true, author: { select: { name: true } } }, orderBy: { createdAt: "desc" }, take: 10 })`. Para contar: `prisma.post.count({ where: { published: true } })`. Revisa la sección 4 de la lección antes de mirar la solución de referencia.

</details>

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-3/prisma-ts-modelar-blog/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **modelo y tu razonamiento** (relaciones, FK, índices, fuente de verdad, ausencia de N+1), no solo si el schema valida.
