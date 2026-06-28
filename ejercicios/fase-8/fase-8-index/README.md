# Fase 8 (entrada) — Diagnóstico de Fase 8 + contrato de método de diseño

> **Modalidad: a mano (sin IA).** Este es el ejercicio de *placement* de la fase.
> No se corrige "bien o mal": se corrige por **honestidad, concreción y un
> trade-off defendible**. Su objetivo es que entres a una fase que se evalúa por
> cómo **piensas** (no por cuánto código produces) sabiendo dónde estás parado, con
> un plan que de verdad vayas a cumplir, y con tu método de diseño —ADRs +
> diagramas— ya comprometido.

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.0` Portada de la fase
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivos

- **O1** — Autoevaluar tus **prerrequisitos** reales (arquitectura *light* / ports &
  adapters de `3.9`, bases de datos de F3, sistemas de IA de F6, automatización e
  integración de F7) y tu punto de partida por sub-unidad (8.1–8.5), distinguiendo
  *"lo sé explicar/diseñar sin notas"* de *"lo reconozco"*.
- **O2** — Diseñar un plan de Fase 8 con bloques semanales concretos, un ritual de
  *active recall* / *spaced repetition*, y una decisión explícita de qué **diferir**
  (8.3 y 8.4 son profundización).
- **O3** — Comprometerte con el **método de la fase** (cada decisión = un ADR; cada
  arquitectura = un diagrama) y articular el **triángulo latencia/costo/calidad** con
  un ejemplo propio, pre-clasificando los 3 sistemas del ejercicio de cierre por
  dificultad con una **restricción dominante** cada uno.

## 📋 Contexto

La Fase 8 es distinta a las anteriores: casi no escribes código, **piensas,
diagramas y decides con argumentos**. Esa es la habilidad que se examina frente a
una pizarra en las entrevistas de los roles mejor pagados. Sin un diagnóstico
honesto, la sobreconfianza ("ya he dibujado arquitecturas") o el desánimo te
sabotean. Sin un plan realista, el método Primero-Sin-IA se queda en buenas
intenciones. Y sin comprometerte desde el principio con **ADRs + diagramas**,
terminas dibujando cajas y flechas decorativas en vez de defender decisiones. Este
ejercicio cierra los tres huecos y se conecta directo con el ejercicio de cierre
(diseña 3 sistemas en papel): la disciplina y el método que declaras aquí son los
que vas a ejecutar toda la fase.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox 40 min). No le pidas a una IA que te diga "qué nivel
   tienes" ni que escriba tu plan o tu contrato de método: eso lo decides tú.
2. Si quieres referencias, consulta la **portada de la fase** y la documentación
   oficial enlazada ahí (System Design Primer, DDD Reference, adr.github.io), no un
   chat.
3. **Solo al final**, usa IA para que te *corrija* (revise honestidad, realismo y si
   tu contrato articula el triángulo de trade-offs), no para que te lo *escriba*.
4. Mañana, **relee tu plan y tu contrato** y ajústalos si ya se revelaron poco
   realistas.

## 🛠️ Instrucciones

Deja **tres archivos markdown en esta carpeta** (`ejercicios/fase-8/fase-8-index/`):

1. **`diagnostico.md`** — dos tablas:

   **Prerrequisitos:**

   | Prerrequisito | Estado (`listo` · `a medias` · `me falta`) | Por qué / a qué fase vuelvo |
   |---|---|---|
   | Arquitectura *light* / ports & adapters (`3.9`) | … | … |
   | Bases de datos a fondo (Fase 3) | … | … |
   | Sistemas de IA: RAG, agentes, evals (Fase 6) | … | … |
   | Automatización e integración (Fase 7) | … | … |

   **Las 5 sub-unidades:**

   | Sub-unidad | Nivel (`nuevo` · `lo reconozco` · `lo sé explicar/diseñar sin notas`) | Por qué (1 línea) |
   |---|---|---|
   | 8.1 Fundamentos de system design | … | … |
   | 8.2 Arquitectura de apps + DDD táctico | … | … |
   | 8.3 Monolito vs microservicios *(opcional)* | … | … |
   | 8.4 Comunicación entre servicios *(opcional)* | … | … |
   | 8.5 Arquitectura de sistemas de IA a escala | … | … |

   La prueba para marcar **"lo sé explicar/diseñar sin notas"**: imagina la
   entrevista —40 minutos, una pizarra, "diséñame esto"—. ¿Lo dirigirías sin notas y
   defenderías un trade-off? Si dudas, no lo es. Ojo con la trampa: haber *dibujado*
   arquitecturas no es lo mismo que haber *defendido una decisión con números*.

2. **`plan-fase-8.md`** — tu plan de estudio:
   - bloques semanales **concretos** (día y hora; ej. "Mar/Jue 20:00–20:50"),
   - duración por sesión y tu **ritual de repaso** (cuándo reescribes de memoria un
     diagrama o un ADR),
   - **qué difieres:** di explícitamente si dejas 8.3 (monolito vs micro) y/o 8.4
     (comunicación) para después, y por qué; protege tiempo para 8.5 (tu
     especialización) y para el ejercicio de cierre, que es largo (3 diseños).

3. **`contrato-metodo.md`** — tu compromiso con el método de la fase:
   - Te comprometes a que **cada decisión de diseño sea un ADR** y **cada
     arquitectura tenga un diagrama Mermaid**. Explica en 2–3 frases por qué un
     diagrama sin ADR es "decoración".
   - De los **3 sistemas** del ejercicio de cierre (RAG multi-tenant, automatización
     de tickets con IA, pipeline de datos para IA), nombra **cuál crees que te
     costará más** y **cuál menos**, y para cada uno **una restricción dominante** que
     anticipas (p. ej. aislamiento entre tenants, latencia del agente, frescura del
     dato).
   - Nombra el **triángulo latencia/costo/calidad** y da un **ejemplo propio** de una
     decisión donde subir una arista baja otra.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La tabla de **prerrequisitos** está completa, y si algo falta, dice a qué fase/sub-unidad volver.
- [ ] La tabla de **las 5 sub-unidades** (8.1–8.5, incluidas 8.3/8.4) tiene nivel y razón por fila.
- [ ] El diagnóstico es **defendible**: no está todo en "lo sé diseñar".
- [ ] El plan tiene **bloques reales en tu semana** (día/hora), no "estudiaré más".
- [ ] El plan incluye un **ritual de repaso** explícito y dice **qué difieres** (8.3/8.4).
- [ ] `contrato-metodo.md` adopta **ADRs + diagramas** con una razón (no solo "sí, los usaré").
- [ ] Pre-clasifica los **3 sistemas** por dificultad y nombra una **restricción dominante** para cada uno.
- [ ] Articula el **triángulo latencia/costo/calidad** con un **ejemplo propio**.
- [ ] Puedes **explicar tu plan y tu contrato sin notas**.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No optimices por "parecer arquitecto": optimiza por honestidad. Si nunca diseñaste
un sistema completo en una pizarra ni escribiste un ADR, varias filas son `nuevo` o
`lo reconozco` —y está perfecto, es justo el músculo que esta fase construye. Para
el nivel "lo sé diseñar sin notas", la prueba es la entrevista de 40 min: ¿la
dirigirías? Para el contrato de método, la clave del triángulo
latencia/costo/calidad es que **no puedes maximizar las tres a la vez**: un modelo
más grande sube calidad pero también costo y latencia; un caché las baja pero
arriesga servir algo obsoleto. Tu ejemplo propio vale más que repetir la teoría. Y
al pre-clasificar los 3 sistemas, lo que se evalúa no es si "aciertas" cuál es más
difícil, sino que nombres una **restricción dominante** plausible para cada uno.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu intento (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-8/fase-8-index.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

El corrector revisa **honestidad, realismo y la calidad del contrato de método**, no
si "acertaste": no hay una respuesta única. La **solución de referencia**
(`.ai/soluciones/fase-8/fase-8-index.md`) es un *exemplar* para el corrector — no la
mires antes de intentarlo.
