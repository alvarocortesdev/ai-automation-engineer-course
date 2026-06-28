# Ejercicio 7.3 — Diagnóstico: durable execution vs cron frágil

> **Modalidad: a mano (razonamiento/diseño, sin IA).** No escribes código de Temporal aquí. Entrenas
> el músculo que separa al que "copia un tutorial de Temporal" del que **entiende por qué existe**:
> mirar un proceso real y diagnosticar dónde se rompe y por qué la durable execution lo arregla.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.3` Durable execution / Temporal
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

Explicar por qué un workflow de larga duración no puede vivir en un cron frágil: identificar sus
modos de falla, las violaciones de determinismo que romperían el replay si se portara tal cual, y la
frontera correcta entre **workflow** (orquestación) y **activity** (side effects).

## 📋 Contexto

`cron_pagos.py` es un script real-ista de payouts a proveedores que un cron dispara cada noche.
Reserva fondos, espera 6 horas de revisión antifraude, transfiere y notifica. Se ve razonable. En
producción es una bomba de tiempo. Diagnosticarlo es el paso previo —y obligatorio— antes de
construir el [mini-proyecto saga](../saga-pago-durable/) de esta misma lección.

## 📏 Primero-Sin-IA

1. Lee `cron_pagos.py` con calma. **A mano**, sin IA, sin buscar en internet, escribe tu análisis.
2. Solo entonces, consulta la **documentación oficial** de Temporal si necesitas confirmar un término.
3. **Solo al final**, usa IA para *revisar* tu análisis —no para generarlo.
4. Mañana, explícale el diagnóstico a alguien (o en voz alta). Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Crea `analisis.md` en esta carpeta con **tres secciones**:

1. **Modos de falla.** Al menos **4** formas distintas en que este script deja el sistema en un
   estado roto o pierde trabajo. Por cada una, nombra qué garantía de la durable execution la
   resuelve (reanudación por replay, idempotencia de workflow, timer durable, reintentos con memoria).
2. **Determinismo.** Marca las líneas que **romperían el replay** si portaras este código tal cual al
   `run` de un workflow de Temporal, y explica por qué cada una. Indica además su alternativa correcta
   (`workflow.now()`, `workflow.random()`/`workflow.uuid4()`, mover a una activity, `workflow.sleep`).
3. **Frontera workflow / activity.** Lista qué operaciones serían **activities** (tocan el mundo) y
   qué quedaría como lógica del **workflow** (orquesta). Justifica la regla que aplicaste.

> No escribas el workflow en Temporal: este ejercicio es de **diagnóstico**. El código viene en el
> siguiente reto.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `analisis.md` tiene las 3 secciones.
- [ ] Sección 1: ≥4 modos de falla **distintos**, cada uno ligado a una garantía concreta.
- [ ] Sección 2: ≥3 violaciones de determinismo correctamente señaladas con su alternativa.
- [ ] Sección 3: frontera coherente con "todo I/O / side effect va en una activity".
- [ ] Puedes **explicar tu análisis sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Pregúntate, por cada línea: *"si el proceso muere JUSTO aquí, ¿en qué estado queda el mundo y cómo me
entero?"*. Esa pregunta destapa la mayoría de los modos de falla. Para el determinismo, recuerda la
lista del recuadro de la lección: reloj de pared, aleatoriedad, red y `time.sleep` son los cuatro
sospechosos habituales. Para la frontera: el `while True` de reintentos, ¿es trabajo con el mundo o
es orquestación que Temporal ya te da con `RetryPolicy`?

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `analisis.md` (esta carpeta),
- la **rúbrica**: `.ai/rubricas/fase-7/durable-vs-cron-diagnostico.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/durable-vs-cron-diagnostico.md` — no la
mires antes de intentarlo de verdad.
