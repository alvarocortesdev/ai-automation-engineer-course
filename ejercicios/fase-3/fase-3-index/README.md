# Ejercicio 3.0 — Diagnóstico, plan y mapa al capstone de Fase 3

> **Modalidad: a mano (sin IA).** Este es el ejercicio de entrada de la Fase 3.
> No mide si "sabes backend": mide si entras con un **plan honesto** y si ves la
> fase como una **construcción hacia el capstone**, no como 16 temas sueltos. Se
> corrige por honestidad y concreción, no por "respuesta correcta".

## Objetivos

- **O1** — Autoevaluar con honestidad tu nivel de partida en las 16 sub-unidades.
- **O2** — Diseñar un plan realista que **decida explícitamente** sobre las 5
  sub-unidades opcionales (3.6, 3.10, 3.11, 3.15, 3.16) según tu rol objetivo.
- **O3** — Mapear cada punto del **Definition of Done del Capstone F3** a las
  sub-unidades que lo enseñan (*constructive alignment*).

## Contexto

La Fase 3 te lleva de no haber escrito una query SQL a tener una **API REST de
producción** (el capstone `3.P`). Antes de empezar conviene saber **de dónde
partes** y **hacia dónde construyes**. Las 16 sub-unidades:

| Camino crítico | Opcional / profundización |
|---|---|
| 3.1 SQL y modelado · 3.2 Queries avanzadas · 3.3 PostgreSQL a fondo · 3.4 Migraciones · 3.5 ORMs y N+1 · 3.7 Diseño de APIs REST · 3.8 FastAPI · 3.9 Ports & adapters · 3.12 Auth y OAuth2 · 3.13 OWASP Top 10 · 3.14 Idempotencia y resiliencia | 3.6 Prisma (TS) · 3.10 NestJS · 3.11 GraphQL · 3.15 Redis · 3.16 Colas async |

Los 7 puntos del **Definition of Done del Capstone F3** (de la portada de la fase):

1. Spec inicial (contrato de la API) + ADRs de las decisiones clave.
2. Tests verdes + lint en CI; calidad por aserciones reales (no % de cobertura).
3. Seguridad OWASP web + secret-scanning + dependency scanning en el pipeline.
4. Observabilidad mínima: structured logs + correlation IDs por request.
5. Resiliencia: idempotency keys + retries con backoff + timeouts.
6. Demo que CORRE + README en inglés + write-up de trade-offs.
7. Conventional Commits en todo el historial.

## Tu tarea (Primero-Sin-IA, timebox 35 min)

Crea tres archivos markdown **en esta carpeta**:

1. **`diagnostico.md`** — tabla con las 16 sub-unidades y tu nivel **honesto**
   por cada una: `nuevo` · `lo reconozco` · `lo sé hacer sin notas`. La prueba
   de "lo sé hacer" es concreta: ¿podrías, **ahora, sin notas y sin IA**,
   escribir un JOIN de tres tablas / levantar un endpoint / explicar qué
   *isolation level* evita un *lost update*? Si dudas, no es "lo sé hacer".

2. **`plan-fase-3.md`** — tu plan de estudio:
   - **Bloques semanales concretos** (día + hora + duración), no buenas
     intenciones.
   - Tu **ritual de repaso** (cuándo reescribes de memoria lo del día anterior).
   - Una **decisión explícita sobre cada una de las 5 opcionales**: ¿la haces o
     la saltas? **Justificada por tu rol objetivo** (ej.: "salto Prisma y NestJS
     porque apunto a IA/Python; hago Redis porque el *semantic caching* me sirve
     en F6").

3. **`mapa-capstone.md`** — tabla que conecte **cada uno de los 7 puntos del
   Definition of Done** con **qué sub-unidad(es) te lo enseñan**. Una fila por
   punto del DoD.

## Qué entregar

- `diagnostico.md`, `plan-fase-3.md`, `mapa-capstone.md` en esta carpeta.

## Hecho significa

- [ ] El diagnóstico cubre las **16** sub-unidades con un nivel **defendible**
      (no todo en "lo sé hacer": eso es sobreconfianza, no diagnóstico).
- [ ] El plan tiene **bloques reales** en tu semana y un ritual de repaso.
- [ ] El plan **decide explícitamente** sobre las 5 opcionales, **con una razón**
      ligada a tu objetivo (no "quizás", no las ignora).
- [ ] El mapa conecta los **7** puntos del DoD con **al menos una** sub-unidad
      cada uno, sin inventar conexiones forzadas.

## Pedir corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-3/fase-3-index/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará la **honestidad** de tu autoevaluación, la **realidad** de
tu plan y la **coherencia** de tu mapa, no si "acertaste". No hay respuesta única.
