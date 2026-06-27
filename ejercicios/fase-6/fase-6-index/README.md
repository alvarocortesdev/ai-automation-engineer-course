# Fase 6 (entrada) — Diagnóstico de Fase 6 + decisión de capstone

> **Modalidad: a mano (sin IA).** Este es el ejercicio de *placement* de la fase.
> No se corrige "bien o mal": se corrige por **honestidad, concreción y un
> trade-off defendible**. Su objetivo es que entres a una fase larga y densa
> sabiendo dónde estás parado, con un plan que de verdad vayas a cumplir, y con
> tu proyecto estrella ya decidido.

**Fase:** Fase 6 — AI Engineering ★ · **Lección:** `6.0` Portada de la fase
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivos

- **O1** — Autoevaluar tus **prerrequisitos** reales (Python+pydantic, FastAPI,
  UI con *streaming*, deploy+observabilidad) y tu punto de partida por sub-unidad
  (6.0–6.16), distinguiendo *"lo sé hacer sin notas"* de *"lo reconozco"*.
- **O2** — Diseñar un plan de Fase 6 con bloques semanales concretos, un ritual
  de *active recall* / *spaced repetition*, y una decisión explícita de qué
  **diferir** (6.12/6.13 son profundización).
- **O3** — Decidir tu **estrella de portafolio** (capstone RAG de F6 vs agéntico
  de F7) con un **trade-off defendible**, reconociendo qué partes del Definition
  of Done de IA (eval harness + gate, budget de costo/latencia, seguridad LLM) te
  costarán más.

## 📋 Contexto

La Fase 6 es tu especialización y la más densa del curso: 18 sub-unidades. Sin un
diagnóstico honesto, la sobreconfianza ("ya hice RAG, me lo sé") o el desánimo te
sabotean. Sin un plan realista, el método Primero-Sin-IA se queda en buenas
intenciones. Y sin decidir desde el principio cuál es tu **proyecto estrella**,
terminas con el mismo RAG-sobre-tus-docs que el 80% de los portafolios. Este
ejercicio cierra los tres huecos y se conecta directo con el capstone: la
disciplina y la decisión que declaras aquí son las que vas a ejecutar durante
toda la fase.

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

Deja **tres archivos markdown en esta carpeta** (`ejercicios/fase-6/fase-6-index/`):

1. **`diagnostico.md`** — dos tablas:

   **Prerrequisitos:**

   | Prerrequisito | Estado (`listo` · `a medias` · `me falta`) | Por qué / a qué fase vuelvo |
   |---|---|---|
   | Python + pydantic | … | … |
   | Backend FastAPI | … | … |
   | UI con streaming | … | … |
   | Deploy + observabilidad | … | … |

   **Las 18 sub-unidades:**

   | Sub-unidad | Nivel (`nuevo` · `lo reconozco` · `lo sé hacer sin notas`) | Por qué (1 línea) |
   |---|---|---|
   | 6.0 Matemática mínima | … | … |
   | 6.0b Puente ML/DL | … | … |
   | … (hasta 6.16, incluidas 6.12 y 6.13) | … | … |

   La prueba para marcar **"lo sé hacer sin notas"**: ¿podrías, ahora mismo,
   resolver un ejercicio de ese tema sin notas y sin IA dentro del timebox? Si
   dudas, no lo es.

2. **`plan-fase-6.md`** — tu plan de estudio:
   - bloques semanales **concretos** (día y hora; ej. "Lun/Mié/Vie 20:00–20:45"),
   - duración por sesión y tu **ritual de repaso** (cuándo reescribes de memoria),
   - **qué difieres:** di explícitamente si dejas 6.12 (voz) y/o 6.13
     (fine-tuning) para después, y por qué; asigna más tiempo a lo que marcaste
     `nuevo` en el diagnóstico (especialmente 6.9 si nunca montaste evals).

3. **`decision-capstone.md`** — tu **estrella de portafolio**:
   - ¿RAG (Fase 6) o agéntico (Fase 7)? Elige uno como estrella.
   - **Un trade-off defendible**: saturación del mercado, tu nicho, complejidad,
     tiempo disponible. No basta "me gusta más".
   - **Tres puntos del Definition of Done** que prevés que te costarán más
     (p. ej. eval harness con gate de regresión, budget de costo/latencia,
     OWASP LLM/Agentic) y por qué.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La tabla de **prerrequisitos** está completa, y si algo falta, dice a qué fase volver.
- [ ] La tabla de **las 18 sub-unidades** (6.0–6.16) tiene nivel y razón por fila.
- [ ] El diagnóstico es **defendible**: no está todo en "lo sé hacer".
- [ ] El plan tiene **bloques reales en tu semana** (día/hora), no "estudiaré más".
- [ ] El plan incluye un **ritual de repaso** explícito y dice **qué difieres**.
- [ ] `decision-capstone.md` elige una estrella **y** trae un **trade-off**, no solo una preferencia.
- [ ] Nombra **tres** puntos del DoD de IA que te costarán más.
- [ ] Puedes **explicar tu plan y tu decisión sin notas**.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No optimices por "parecer avanzado": optimiza por honestidad. Si nunca montaste
un eval harness, 6.9 es `nuevo` —y es justo donde más valor vas a extraer, así
que dale tiempo. Para el plan, busca lo **sostenible**, no lo perfecto: tres
bloques de 45 min que cumples valen más que dos horas diarias que abandonas el
jueves. Para la decisión de capstone, recuerda el matiz honesto: el RAG genérico
es el camino saturado; el agéntico con manejo de fallas es el menos copiado. La
diferencia entre una decisión `competente` y una `excelente` es si **nombras el
trade-off**, no cuál elijas.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu intento (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-6/fase-6-index.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

El corrector revisa **honestidad, realismo y la calidad del trade-off**, no si
"acertaste": no hay una respuesta única. La **solución de referencia**
(`.ai/soluciones/fase-6/fase-6-index.md`) es un *exemplar* para el corrector — no
la mires antes de intentarlo.
