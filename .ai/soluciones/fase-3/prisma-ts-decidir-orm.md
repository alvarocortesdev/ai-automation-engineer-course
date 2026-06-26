---
ejercicio_id: fase-3/prisma-ts-decidir-orm
fase: fase-3
sub_unidad: "3.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Este ejercicio **no tiene respuesta única**: lo que sigue son las decisiones más defendibles y los criterios para juzgar otras.

# Solución de referencia — Decide: Prisma o SQLAlchemy para tres proyectos

## Principio rector para corregir

No corrijas *qué* ORM eligió, corrige *cómo* lo justificó. El criterio que más pesa, casi siempre, es **el lenguaje y ecosistema del equipo**: un ORM no debería forzar un cambio de lenguaje. Una elección "contraria a la esperada" bien argumentada con trade-offs vale más que la "esperada" justificada con un eslogan.

## Decisiones defendibles por escenario

### Escenario 1 — Startup fullstack (equipo TS, Next.js, sin IA)
- **Elección esperada: Prisma.**
- **Criterios:** el equipo ya está 100% en TypeScript; Next.js + Prisma es una combinación de primera clase (cliente type-safe compartido entre API y front, iteración rápida del modelo con `migrate dev`). Meter SQLAlchemy obligaría a un servicio Python aparte sin beneficio.
- **Costo a nombrar:** Prisma da menos control fino del SQL generado; si más adelante necesitan queries muy optimizadas, recurrirán a `$queryRaw`.
- **Dato que cambia la decisión:** que el SaaS vaya a tener cargas analíticas pesadas con SQL muy fino desde el día 1.

### Escenario 2 — Servicio de IA en Python (RAG, FastAPI, pgvector)
- **Elección esperada: SQLAlchemy.**
- **Criterios:** el equipo es Python y la app es IA; SQLAlchemy vive en ese ecosistema (integra con pydantic, pipelines de datos, el resto del stack de IA) y da el control de SQL que las queries vectoriales (`pgvector`) suelen requerir. Prisma sería un cuerpo extraño en un stack Python.
- **Costo a nombrar:** SQLAlchemy tiene curva más empinada y no regala el cliente type-safe perfecto de Prisma; hay que ser más disciplinado con los tipos.
- **Dato que cambia la decisión:** que el equipo fuera en realidad TS sirviendo el modelo, o que existiera soporte de primera para el operador de `pgvector` que necesitan sin SQL crudo.
- **Tensión (nivel excelente):** reconocer que Prisma es *más cómodo* de usar y que la decisión no es por superioridad técnica, sino por ecosistema/lenguaje.

### Escenario 3 — Migración de monolito legacy (Node.js, SQL crudo sin tipos)
- **Elección esperada: Prisma.**
- **Criterios:** ya están en Node (no hay que cambiar de lenguaje), y el dolor concreto es SQL crudo disperso y sin tipos — justo lo que ataca el cliente type-safe y el schema centralizado de Prisma. La migración es incremental (Prisma convive con SQL existente).
- **Costo a nombrar:** introducir Prisma implica modelar el schema sobre una base que ya existe (`prisma db pull`/introspección) y disciplina para no seguir escribiendo SQL crudo en paralelo; hay esfuerzo de adopción.
- **Dato que cambia la decisión:** que el monolito en realidad estuviera planeando migrar a Python, o que el SQL crudo fuera tan específico que el ORM no lo cubra.

## Qué hace que una entrega sea "competente" vs "excelente"

- **Competente:** las tres decisiones se apoyan en el lenguaje/ecosistema del equipo y nombran un costo real por escenario.
- **Excelente:** además expone la tensión del escenario ambiguo (no finge que todo es obvio), y los costos/datos-que-cambian-la-decisión son específicos del caso (no genéricos como "tiene curva de aprendizaje").

## Errores a marcar (resumen)
- Decidir por moda/popularidad o por chovinismo de lenguaje.
- Vender una opción como perfecta (sin costo).
- Recomendar cambiar de lenguaje solo por el ORM.
- No reconocer ninguna ambigüedad en los tres.

## Variante de control anti-IA
Pedir el **contrafactual** del escenario 2: "¿qué tendría que ser verdad para que Prisma fuera la mejor opción en un servicio de IA?". Respuesta razonada esperada: que el equipo sirviera el modelo desde Node/TS, o que la comodidad type-safe pesara más que el ecosistema Python para ese caso concreto. Quien copió una comparativa genérica no puede construir el contrafactual.
