# Fase 7 (entrada) — Diagnóstico de Fase 7 + decisión de capstone estrella

> **Modalidad: a mano (sin IA).** Este es el ejercicio de *placement* de la fase.
> No se corrige "bien o mal": se corrige por **honestidad, concreción y un
> trade-off defendible**. Su objetivo es que entres a una fase densa —que mezcla
> integración confiable, data engineering y agentes— sabiendo dónde estás parado,
> con un plan que de verdad vayas a cumplir, y con tu proyecto estrella decidido.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering ★ · **Lección:** `7.0` Portada de la fase
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivos

- **O1** — Autoevaluar tus **prerrequisitos** reales (idempotencia/resiliencia de
  `3.14`, APIs+OAuth2 de F3, agentes+evals+seguridad LLM de F6) y tu punto de
  partida por sub-unidad (7.1–7.7), distinguiendo *"lo sé hacer sin notas"* de
  *"lo reconozco"*.
- **O2** — Diseñar un plan de Fase 7 con bloques semanales concretos, un ritual de
  *active recall* / *spaced repetition*, y una decisión explícita de qué
  **diferir** (7.4 y 7.6 son profundización).
- **O3** — Decidir tu **estrella de portafolio** (capstone agéntico de F7 vs RAG
  de F6) con un **trade-off defendible**, reconociendo qué puntos del Definition
  of Done (eval gate de agente, HITL + techo de costo, DLQ/replay durable) te
  costarán más.

## 📋 Contexto

La Fase 7 es tu otro pilar y una de las más densas del curso: 10 sub-unidades que
cruzan tres mundos (confiabilidad de integración, data engineering, automatización
agéntica). Sin un diagnóstico honesto, la sobreconfianza ("ya armo flujos en n8n,
me lo sé") o el desánimo te sabotean. Sin un plan realista, el método
Primero-Sin-IA se queda en buenas intenciones. Y sin decidir desde el principio
cuál es tu **proyecto estrella**, terminas con el mismo RAG-sobre-tus-docs que el
80% de los portafolios en vez del agéntico end-to-end que te diferencia. Este
ejercicio cierra los tres huecos y se conecta directo con el capstone: la
disciplina y la decisión que declaras aquí son las que vas a ejecutar toda la fase.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox 40 min). No le pidas a una IA que te diga "qué
   nivel tienes" ni que elija tu capstone: eso lo decides tú.
2. Si quieres referencias, consulta la **portada de la fase** y la documentación
   oficial enlazada ahí, no un chat.
3. **Solo al final**, usa IA para que te *corrija* (revise honestidad, realismo y
   si tu decisión trae un trade-off), no para que te lo *escriba*.
4. Mañana, **relee tu plan y tu decisión** y ajústalos si ya se revelaron poco
   realistas.

## 🛠️ Instrucciones

Deja **tres archivos markdown en esta carpeta** (`ejercicios/fase-7/fase-7-index/`):

1. **`diagnostico.md`** — dos tablas:

   **Prerrequisitos:**

   | Prerrequisito | Estado (`listo` · `a medias` · `me falta`) | Por qué / a qué fase vuelvo |
   |---|---|---|
   | Idempotencia y resiliencia (`3.14`) | … | … |
   | APIs + OAuth2 (Fase 3) | … | … |
   | Agentes + evals + seguridad LLM (Fase 6) | … | … |

   **Las 10 sub-unidades:**

   | Sub-unidad | Nivel (`nuevo` · `lo reconozco` · `lo sé hacer sin notas`) | Por qué (1 línea) |
   |---|---|---|
   | 7.1 n8n como arquitectura | … | … |
   | 7.2 Integración + confiabilidad | … | … |
   | 7.3 Durable execution / Temporal | … | … |
   | 7.4 De RPA a código *(opcional)* | … | … |
   | 7.5a ELT + modelado | … | … |
   | 7.5b dbt de verdad | … | … |
   | 7.5c Un orquestador | … | … |
   | 7.5d Data contracts + quality | … | … |
   | 7.6 CDC + streaming *(opcional)* | … | … |
   | 7.7 Agentes de automatización con IA | … | … |

   La prueba para marcar **"lo sé hacer sin notas"**: ¿podrías, ahora mismo,
   resolver un ejercicio de ese tema sin notas y sin IA dentro del timebox? Si
   dudas, no lo es. Ojo con la trampa: *usar* n8n o un ETL no es lo mismo que
   *diseñar* un flujo idempotente con DLQ ni *modelar* un star schema.

2. **`plan-fase-7.md`** — tu plan de estudio:
   - bloques semanales **concretos** (día y hora; ej. "Lun/Mié/Vie 20:00–20:45"),
   - duración por sesión y tu **ritual de repaso** (cuándo reescribes de memoria),
   - **qué difieres:** di explícitamente si dejas 7.4 (RPA) y/o 7.6 (CDC) para
     después, y por qué; asigna más tiempo a lo que marcaste `nuevo`,
     especialmente el bloque de Data Engineering (7.5a–d) si nunca tocaste dbt.

3. **`decision-capstone.md`** — tu **estrella de portafolio**:
   - El curso recomienda el agéntico de F7 por encima del RAG de F6. ¿Lo adoptas
     o eliges distinto? Elige uno como estrella.
   - **Un trade-off defendible**: saturación del mercado, tu nicho, complejidad,
     tiempo disponible. No basta "me gusta más" ni "porque el curso lo dice".
   - **Tres puntos del Definition of Done** que prevés que te costarán más
     (p. ej. eval gate de **agente** con regresión, HITL + techo de costo,
     DLQ/replay durable) y por qué.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La tabla de **prerrequisitos** está completa, y si algo falta, dice a qué fase/sub-unidad volver.
- [ ] La tabla de **las 10 sub-unidades** (7.1–7.7, incluidas 7.4/7.6) tiene nivel y razón por fila.
- [ ] El diagnóstico es **defendible**: no está todo en "lo sé hacer".
- [ ] El plan tiene **bloques reales en tu semana** (día/hora), no "estudiaré más".
- [ ] El plan incluye un **ritual de repaso** explícito y dice **qué difieres** (7.4/7.6).
- [ ] `decision-capstone.md` elige una estrella **y** trae un **trade-off**, no solo una preferencia.
- [ ] Nombra **tres** puntos del DoD que te costarán más.
- [ ] Puedes **explicar tu plan y tu decisión sin notas**.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No optimices por "parecer avanzado": optimiza por honestidad. Si nunca montaste un
pipeline con dbt o evaluaste un **agente** (no un RAG), esas filas son `nuevo` —y
es justo donde más valor vas a extraer, así que dales tiempo. Para el plan, busca
lo **sostenible**: tres bloques de 45 min que cumples valen más que dos horas
diarias que abandonas el jueves. Para la decisión de capstone, el curso recomienda
el agéntico, pero la nota que vale es **por qué**, no copiar la recomendación. La
diferencia entre `competente` y `excelente` es si **nombras qué pierdes** al no
elegir la otra opción —eso es el trade-off— no cuál elijas.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu intento (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-7/fase-7-index.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

El corrector revisa **honestidad, realismo y la calidad del trade-off**, no si
"acertaste": no hay una respuesta única. La **solución de referencia**
(`.ai/soluciones/fase-7/fase-7-index.md`) es un *exemplar* para el corrector — no
la mires antes de intentarlo.
