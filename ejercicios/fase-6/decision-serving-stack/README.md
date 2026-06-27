# Ejercicio 6.10 — Decisión: stack de serving para tres escenarios

> **Modalidad: diseño / razonamiento (sin código).** No hay tests ni función que
> implementar. Entregas un documento donde **decides y justificas** cómo correr un LLM
> para tres escenarios reales. Es exactamente lo que defiendes en una entrevista de AI
> Engineer y lo que escribes como ADR en el capstone.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.10` Open-source, local y serving
**Ruta:** crítica · **Timebox:** 35 min · **Modalidad:** a-mano (diseño)

## 🎯 Objetivo

Para tres escenarios distintos, elegir y **justificar**: (a) **local vs API**, (b) si es
local, el **motor** (Ollama/MLX single-user vs vLLM/TGI de producción), (c) la
**cuantización** (GGUF vs AWQ, según dónde corre), (d) la **restricción dominante** que
manda la decisión, y (e) **una consideración de privacidad/seguridad**. No hay una única
respuesta correcta: se evalúa la **calidad del trade-off**.

## 📋 Contexto

En el Capstone F6 escribirás un ADR ("Architecture Decision Record") justificando por qué
tu RAG corre contra una API y bajo qué condiciones migrarías a local. Si no puedes derivar
esa decisión de la restricción dominante —ni nombrar por qué Ollama no sirve a 500
usuarios— el revisor o el entrevistador te desarma. Este ejercicio entrena ese músculo.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba), apoyándote solo en la lección.
2. Para cada escenario, identifica **primero** la restricción que manda y deja que ella
   guíe el resto de las decisiones.
3. Solo al final, usa IA para *atacar* tus trade-offs, no para escribirlos.

## 🛠️ Instrucciones

Crea un archivo `decisiones.md` en esta carpeta. Resuelve los **tres** escenarios usando,
para cada uno, esta plantilla exacta:

```markdown
## Escenario N

- **Restricción dominante:** <costo | privacidad | latencia | concurrencia | operación> — por qué manda aquí.
- **Local o API:** <local | API> — derivado de la restricción, no "el mejor".
- **Motor (si es local):** <Ollama | MLX | vLLM | TGI | N/A si es API> — single-user vs serving de producción, por qué.
- **Cuantización:** <GGUF | AWQ | N/A> — justificada por DÓNDE corre (CPU/Mac vs GPU) y qué se pierde.
- **Mecanismo clave (si es serving de producción):** menciona KV cache y/o continuous batching y para qué sirven aquí.
- **Privacidad/seguridad:** una consideración concreta (datos que no pueden salir, logs/PII, acceso al servidor) + mitigación.
```

### Escenario 1 — Asistente de código en la laptop de un dev

Un desarrollador quiere un copiloto de código **en su propio MacBook** (Apple Silicon).
Su código es propietario y **no debe salir a la nube**. Lo usa **solo él**, de forma
intermitente, mientras programa. No tiene GPU NVIDIA ni quiere montar infraestructura.

### Escenario 2 — Chatbot interno para 500 empleados, on-prem por regulación

Un banco quiere un asistente que responda preguntas sobre sus políticas internas a **500
empleados, muchos a la vez** durante el horario laboral. Por regulación, **los datos no
pueden salir de la infraestructura del banco**. Tienen un equipo de plataforma y GPUs en
su datacenter. La latencia debe ser razonable bajo carga alta.

### Escenario 3 — Feature de IA en una startup que recién valida

Una startup quiere agregar un resumen automático a su app. Tiene **unos 100 usuarios**,
tráfico **bajo y muy variable** (picos impredecibles), presupuesto chico y **ningún
ingeniero de ML ops**. La prioridad es **salir esta semana** y no quemar plata en
infraestructura ociosa.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los tres escenarios resueltos con la plantilla completa.
- [ ] Cada decisión local/API se deriva de la **restricción dominante**, no de "el mejor".
- [ ] Al menos un escenario usa **vLLM o TGI** y nombra **KV cache** y/o **continuous
      batching** explicando por qué Ollama/MLX no servirían ahí.
- [ ] La cuantización se justifica por **dónde corre** (GGUF en Mac/CPU, AWQ en GPU de prod)
      y menciona qué se pierde al cuantizar.
- [ ] Cada escenario nombra **una** consideración de privacidad/seguridad con su mitigación.
- [ ] Puedes **defender oralmente** cada decisión sin leer tus notas.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/decision-serving-stack/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad. (Hay varias respuestas defendibles; el corrector evalúa tu
**justificación**, no que coincidas palabra por palabra.)
