# Ejercicio 3.6 — Decide: Prisma o SQLAlchemy para tres proyectos

> **Modalidad: razonamiento/diseño (a mano, sin IA).** No se ejecuta código. Lo que se evalúa es tu **criterio de ingeniería**: que elijas una herramienta por razones concretas (lenguaje del equipo, control de SQL, ecosistema, integración con IA) y no por moda, y que reconozcas el **costo** de tu elección. Es exactamente la decisión que defiendes en un ADR y en una entrevista de arquitectura.

## Objetivo

- **O1** — Decidir entre Prisma y SQLAlchemy para distintos contextos, justificando con criterios concretos y nombrando el trade-off (ninguna elección es gratis).

## Los tres escenarios

> Para cada uno, elige **un** ORM y defiende la decisión. No hay una respuesta universalmente correcta; hay decisiones **defendibles** y decisiones que delatan que repites eslóganes.

1. **Startup fullstack.** Equipo de 3 personas, todas cómodas en TypeScript. Construyen una app web con **Next.js** (frontend + API en el mismo proyecto), Postgres, y quieren iterar rápido sobre el modelo de datos. El producto es un SaaS de gestión de tareas, sin IA por ahora.

2. **Servicio de IA en producción.** Un equipo Python sirve un sistema **RAG** (FastAPI + un modelo de embeddings + Postgres con `pgvector`). Necesitan integrar la capa de datos con librerías del ecosistema Python (pipelines de datos, validación con pydantic) y, a veces, escribir SQL fino para queries vectoriales.

3. **Migración de un monolito legacy.** Una empresa tiene un backend grande en **Node.js** con queries SQL crudas dispersas por todo el código, sin tipos, propenso a errores. Quieren introducir un ORM para ganar seguridad de tipos y centralizar el modelo de datos, sin reescribir el lenguaje.

## Tu tarea (en este orden — Primero-Sin-IA, timebox 30–35 min)

1. **A mano primero**, para cada escenario decide Prisma o SQLAlchemy.
2. **Justifica** con criterios concretos: ¿en qué lenguaje está el equipo? (el ORM no debería forzar cambiar de lenguaje). ¿Necesitan control fino del SQL o velocidad de desarrollo? ¿El ecosistema (Next.js / IA en Python) empuja hacia un lado?
3. **Nombra un costo o riesgo** de tu elección en cada caso (algo que pierdes o que te puede morder).
4. **Di qué dato adicional** te haría cambiar de opinión en cada escenario.
5. Escribe todo en `DECISION.md` (hay una plantilla en este directorio).

> Hazlo a mano. El valor está en *defender* la decisión, no en acertar una respuesta "oficial".

## Qué entregar

- `DECISION.md` — tu análisis de los tres escenarios (plantilla incluida).

## Criterios de "hecho"

- [ ] Las tres decisiones están justificadas con criterios concretos, no con "Prisma es más moderno" ni "Python es mejor".
- [ ] Reconoces al menos un escenario donde la elección **no** es obvia y explicas la tensión.
- [ ] Cada elección nombra un **costo real** (no vendes ninguna como perfecta).
- [ ] Para cada escenario dices qué dato te haría cambiar de opinión.
- [ ] Puedes defender, sin notas, por qué el escenario 2 (IA en Python) suele inclinarse a SQLAlchemy **por ecosistema**, aunque Prisma sea más cómodo de usar.

## Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El criterio que más pesa casi siempre es **el lenguaje del equipo**: un ORM no debería obligarte a cambiar de lenguaje. Escenario 1 (equipo TS + Next.js) → Prisma encaja por ecosistema. Escenario 2 (equipo Python + IA + pgvector) → SQLAlchemy encaja por ecosistema y por el control de SQL que las queries vectoriales suelen pedir. Escenario 3 (Node legacy) → Prisma, porque ya están en Node y el cliente type-safe ataca justo su dolor (SQL crudo sin tipos). El costo a nombrar: Prisma te da menos control fino del SQL generado; SQLAlchemy tiene una curva más empinada y menos "magia" de tipos. Revisa las secciones 5 y 4 de la lección. Pista, no solución.

</details>

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-3/prisma-ts-decidir-orm/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará la **calidad de tu razonamiento** (criterios concretos, trade-offs nombrados), no si coincides con una respuesta única.
