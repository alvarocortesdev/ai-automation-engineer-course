---
ejercicio_id: fase-3/fase-3-index
fase: fase-3
sub_unidad: "3.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Este ejercicio
> no tiene "respuesta correcta": lo que sigue es un **exemplar** y una lista de
> qué observar. Úsalo como vara de medir honestidad/realismo/alineación, nunca
> como plantilla a copiar (ver `.ai/soluciones/README.md` y
> `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnóstico, plan y mapa al capstone de Fase 3

## Respuesta canónica
**No existe una respuesta única.** Una entrega `competente` es cualquier
conjunto de tres archivos que sea **honesto, concreto y alineado con el
capstone**. La calidad se mide por el proceso (autoevaluación, planificación,
mapeo), no por contenido específico.

## Qué constituye una entrega correcta (por archivo)

### `diagnostico.md` — exemplar (alumno cero real)
Tabla con las **16** sub-unidades. En un cero real (que ya pasó F0–F2), lo
esperable es mayoría de `nuevo` con algún `lo reconozco` en lo más cercano a lo
ya visto (p. ej. SQL básico si lo tocó en algún lado). La señal de calidad es la
**razón por fila** y aplicar la prueba "¿podría resolverlo sin notas ahora?".

| Sub-unidad | Nivel | Por qué (ejemplo) |
|---|---|---|
| 3.1 SQL y modelado | lo reconozco | Vi tablas y SELECT, pero nunca normalicé ni diseñé claves. |
| 3.2 Queries avanzadas | nuevo | Nunca escribí un CTE ni una window function. |
| 3.3 PostgreSQL a fondo | nuevo | No sé qué es un isolation level ni leer un EXPLAIN. |
| 3.4 Migraciones | nuevo | Nunca versioné un esquema. |
| 3.5 ORMs y N+1 | nuevo | No sé qué es el problema N+1. |
| 3.6 Prisma (opcional) | nuevo | — |
| 3.7 Diseño de APIs REST | lo reconozco | He consumido APIs, no diseñado una. |
| 3.8 FastAPI | nuevo | Nunca levanté un servidor. |
| 3.9 Ports & adapters | nuevo | No conozco la arquitectura hexagonal. |
| 3.10 NestJS (opcional) | nuevo | — |
| 3.11 GraphQL (opcional) | nuevo | — |
| 3.12 Auth y OAuth2 | nuevo | No sé la diferencia entre sesión y token. |
| 3.13 OWASP Top 10 | nuevo | He oído de injection, nada más. |
| 3.14 Idempotencia | nuevo | Nunca diseñé para reintentos. |
| 3.15 Redis (opcional) | nuevo | — |
| 3.16 Colas async (opcional) | nuevo | — |

> Para un perfil **oxidado-con-experiencia** (p. ej. tocó RAG/backend en prod),
> lo esperable es más `lo reconozco` y algún `lo sé hacer sin notas` —pero solo
> si lo puede defender. La trampa a detectar es marcar "lo sé hacer" sin
> evidencia (sobreconfianza), sobre todo en 3.3 (isolation/locking) y 3.14
> (idempotencia), que casi nadie domina aunque "haya hecho backend".

### `plan-fase-3.md` — exemplar
Un plan creíble, p. ej.:
- **Mar/Jue 20:00–21:00** (2 bloques × 60 min) + **Dom 10:00–12:00** (sesión larga).
- **Ritual de repaso:** cada sesión arranca con 5–10 min reescribiendo de memoria
  lo del bloque anterior; los domingos, repaso de la semana.
- Más tiempo asignado a lo marcado `nuevo` (casi todo, en un cero real).
- **Decisión sobre las 5 opcionales**, con razón. Ejemplo defendible para perfil
  que apunta a IA/Automatización:
  - 3.6 Prisma → **saltar** (foco Python; FastAPI + SQLAlchemy bastan).
  - 3.10 NestJS → **saltar** (mismo motivo; no apunto a fullstack TS empresarial).
  - 3.11 GraphQL → **saltar ahora**, anotar para si un rol lo pide.
  - 3.15 Redis → **hacer** (el caching y el *semantic caching* me sirven en F6).
  - 3.16 Colas async → **hacer** (enlaza con DLQ/outbox de F7, mi pilar de automatización).

La señal de calidad: **día/hora concretos**, **ritual de repaso explícito** y una
**decisión razonada por cada opcional** (no "quizás", no ignorarlas). Un plan que
salta las 5 también es válido y `excelente` si la razón es coherente con el rol.

### `mapa-capstone.md` — exemplar
Tabla que conecta los 7 puntos del DoD con las sub-unidades. Mapeo de referencia:

| # DoD | Punto | Sub-unidad(es) que lo enseñan |
|---|---|---|
| 1 | Spec + ADRs | 3.7 (contrato/OpenAPI) + 3.9 (decisiones de arquitectura); spec-driven viene de F0/F2. |
| 2 | Tests verdes + lint en CI (aserciones reales) | Hábito de F2 reaplicado; aserciones sobre endpoints en 3.8. |
| 3 | Seguridad OWASP + secret/dependency scanning | **3.13** (OWASP, gitleaks) + **3.12** (auth/control de acceso). |
| 4 | Observabilidad mínima (logs + correlation IDs) | Se introduce aquí (puente a F5); apoyo en 3.8/3.14. |
| 5 | Resiliencia (idempotency keys, retries, timeouts) | **3.14**. |
| 6 | Demo que corre + README inglés + write-up | Integra todo; datos (3.1–3.5) + API (3.7–3.9). |
| 7 | Conventional Commits | Hábito desde F0; se mantiene. |

Señal de calidad: los 7 puntos conectados, con los "difíciles" bien ubicados
(ADRs→3.9, no a 3.8; resiliencia→3.14, no genérico). `Excelente` si además nota
qué partes del DoD la fase **no** cubre del todo (trazas OTel completas, IA), que
llegan en F5/F6.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Sobreconfianza en el diagnóstico.** "Lo sé hacer" sin evidencia, en especial
   en 3.3 (isolation levels), 3.5 (N+1) y 3.14 (idempotencia). Verificación:
   que justifique una fila en voz alta.
2. **Opcionales sin decidir.** Dejarlas en "quizás" o ignorarlas incumple O2; o
   tratarlas como obligatorias (confundir camino crítico con profundización).
3. **Mapa forzado.** Mapear todo a 3.8 "porque es el backend" en vez de ubicar
   seguridad en 3.12/3.13 y resiliencia en 3.14.
4. **Plan que no responde al diagnóstico.** Marca varias `nuevo` pero reparte el
   tiempo por igual: la autoevaluación no está sirviendo.
5. **Delegar a la IA.** Plan genérico y pulido sin contexto real del alumno.

## Rango de soluciones aceptables
- Cualquier formato (tabla, listas, prosa breve) sirve si los tres entregables
  están y son honestos/concretos/alineados.
- Saltar las 5 opcionales o hacer las 5 son ambas válidas: lo que se evalúa es la
  **razón** ligada al rol objetivo, no la elección.
- Un plan **modesto pero sostenible** es preferible a uno ambicioso e irreal.
- En el mapa, varias asociaciones son defendibles (p. ej. el punto 1 puede ligar
  a 3.7 o a 3.9, o a ambos); no penalizar un camino válido distinto al de arriba
  mientras esté justificado.
- Tanto un perfil cero como uno oxidado pueden ser `excelente`: se mide la
  **calidad del proceso**, no el nivel de partida.
