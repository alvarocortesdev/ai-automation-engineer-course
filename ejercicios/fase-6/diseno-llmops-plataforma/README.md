# Ejercicio 6.16 — Diseño: la capa LLMOps de la plataforma RAG

> **Modalidad: diseño / razonamiento (sin código).** No hay tests ni función que implementar.
> Entregas un documento donde **decides y justificas** cómo operar un RAG de producción en
> costo, latencia y confiabilidad. Es exactamente el ADR que escribes en el capstone y lo que
> defiendes en una entrevista de AI Engineer.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.16` Costo/latencia + LLMOps
**Ruta:** crítica · **Timebox:** 40 min · **Modalidad:** a-mano (diseño)

## 🎯 Objetivo

Diseñar la capa de **costo/latencia + LLMOps** de la **Plataforma RAG de producción** (el capstone
de la fase): las dos capas de caching, el ruteo de modelos, el corte batch vs. interactivo, el
budget como gate, la capa LLMOps (fallbacks, versionado, despliegue seguro, monitoreo) y un riesgo
de seguridad del caching. No hay una única respuesta correcta: se evalúa la **calidad del trade-off**.

## 📋 Contexto

Tienes un RAG con ingest → vector DB → retrieval + reranking → generación streaming, ~30.000
consultas/mes, y un eval harness de [6.9](/fase-6-ai-engineering/6-9-eval-driven-development/). El
cliente pregunta "¿cuánto cuesta y cuánto tarda?". Si no puedes responder con un número y un diseño
que lo sostenga, no tienes un sistema de producción: tienes una demo.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba), apoyándote solo en la lección.
2. Para cada decisión, identifica **primero** la restricción que manda (costo, latencia,
   confiabilidad, seguridad) y deja que ella guíe el diseño.
3. Solo al final, usa IA para *atacar* tus trade-offs, no para escribirlos.

## 🛠️ Instrucciones

Crea un archivo `diseno.md` en esta carpeta. Resuelve las **seis** secciones:

### 1. Caching (dos capas)

- **Prompt caching del provider:** ¿qué va en el **prefijo estable** (cacheado a 0.1×) y qué va al
  **final** (volátil)? Da un ejemplo concreto del system prompt / contexto del RAG.
- **Semantic cache:** ¿dónde lo pones? ¿cómo eliges el **umbral** de similitud y cómo lo
  **calibras con el eval**? Nombra **un** escenario donde el caching **no** sirva.

### 2. Ruteo de modelos

- Define los **escalones** (qué tipo de consulta a qué modelo: Haiku / Sonnet / Opus) y de dónde
  sale la **señal de dificultad**.
- Di cómo evitas que el router **degrade la calidad** (cómo lo evalúas).

### 3. Batching

- Identifica qué parte del pipeline va por **Message Batches** (asíncrono, 50% off) y cuál **no
  puede** (interactivo). Justifica el corte por latencia.

### 4. Budget de costo/latencia (gate)

- Define el **techo** concreto (USD/consulta y latencia p95, con números) que actúa como **gate**:
  un cambio que lo supera se **bloquea**. Conéctalo con el gate de regresión de 6.9.

### 5. LLMOps

- **Fallbacks:** describe la cadena (qué modelo de respaldo, qué errores la disparan).
- **Versionado:** cómo versionas prompt y modelo (ADR + Conventional Commits).
- **Despliegue seguro:** canary + rollback (qué % primero, qué métricas vigilas).
- **Monitoreo:** qué atas en cada traza de Langfuse (USD, ms, score, prompt, modelo) y cómo
  realimenta el dataset de eval.

### 6. Seguridad (hilo transversal)

- Nombra **un** riesgo de seguridad que el caching introduce (pista: ¿qué pasa si un semantic cache
  sirve la respuesta de un usuario a otro, o cachea datos sensibles?) y su **mitigación** concreta.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las dos capas de caching distinguidas, con prefijo estable vs. volátil explícito y un ejemplo.
- [ ] El umbral del semantic cache se calibra con el eval, no es inventado; hay un caso donde no sirve.
- [ ] Escalones de ruteo justificados + cómo evalúas el router.
- [ ] Corte interactivo vs. batch justificado por latencia.
- [ ] Budget de costo/latencia como **gate** con números, atado al eval de 6.9.
- [ ] LLMOps cubre fallback, versionado, despliegue seguro y monitoreo.
- [ ] Un riesgo de seguridad del caching con su mitigación.
- [ ] Puedes **defender oralmente** cada decisión sin leer tus notas.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/diseno-llmops-plataforma/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de intentarlo de
verdad. (Hay varias respuestas defendibles; el corrector evalúa tu **justificación**, no que
coincidas palabra por palabra.)
