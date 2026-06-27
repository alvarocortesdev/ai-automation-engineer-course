# Ejercicio 6.12 — Elegir la arquitectura y diseñar un voice agent

> **Modalidad: a mano (diseño / razonamiento).** No hay código que ejecutar ni tests. El
> entregable es un documento de diseño donde **eliges** S2S vs turn-based para cada caso y
> **justificas** por la restricción dominante, y luego diseñas un voice agent completo. Es
> el tipo de decisión que defiendes en una entrevista de system design.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.12` Voice/multimodal realtime
**Ruta:** opcional/profundización · **Timebox:** 40 min

## 🎯 Objetivos

- **O1** — Elegir la arquitectura de voz (S2S / turn-based / híbrido) para un escenario,
  justificando por la **restricción dominante**.
- **O2** — Defender la elección nombrando **qué se pierde** (sobre todo: qué pierde el S2S al
  no tener texto intermedio).
- **O3** — Diseñar un voice agent end-to-end: presupuesto de latencia, barge-in, economía
  USD/min, observabilidad y un control de seguridad.

## 📏 Primero-Sin-IA

Resuélvelo **a mano**, razonando tú primero. Solo después consulta documentación oficial; y
solo al final usa IA para *revisar*, no para *generar*. Escribe todo en `diseno.md`.

## 🛠️ Tu tarea

### Parte A — Elegir S2S vs turn-based (4 escenarios)

Para cada escenario indica **(1)** qué arquitectura eliges (S2S / turn-based / híbrido) y
**(2)** cuál es la **restricción dominante** que decide (la cosa que, si la haces mal, hunde
el caso). Una o dos líneas por escenario.

1. **Soporte telefónico de alto volumen**, charla abierta, donde **sonar natural** y la
   latencia baja son lo que retiene al cliente.
2. Asistente de voz que debe **consultar una base de conocimiento (RAG)** y **citar la
   fuente exacta** de cada dato, en un dominio **regulado** (salud o finanzas).
3. **Prototipo** para validar una idea con 10 usuarios en una semana, presupuesto mínimo.
4. Asistente de voz **on-device** para datos sensibles que **no pueden salir** del
   dispositivo/empresa.

### Parte B — Diseñar el voice agent del escenario 1

Diseña el flujo end-to-end (puedes usar un diagrama Mermaid). Cubre:

- **Arquitectura:** S2S, turn-based o híbrido. Justifica por la restricción dominante y
  nombra **qué pierdes** con tu elección.
- **Presupuesto de latencia:** lista las **etapas que cuentan** para el time-to-first-audio,
  da un número objetivo, y di **dónde** recortarías si no cumples.
- **Barge-in:** describe las acciones (cortar audio, **cancelar el trabajo en vuelo**, vaciar
  buffers, escuchar) y por qué cancelar en vuelo también es una decisión de **costo**.
- **Economía USD/min:** cómo se compone el costo de tu arquitectura y **cuándo** el agente
  conviene sobre un humano (incluye el efecto de la **tasa de escalamiento a humano**).
- **Observabilidad:** **dos** métricas que registrarías (p. ej. latencia percibida p95, tasa
  de barge-in, tasa de escalamiento a humano).
- **Seguridad:** **un** riesgo concreto (p. ej. indirect prompt injection por voz — LLM01; o
  consentimiento/PII del audio) con una **mitigación accionable**.

## 📦 Qué entregar

- `diseno.md` — Partes A y B completas, con justificaciones por restricción dominante.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los 4 escenarios traen una **restricción dominante** explícita, no un "me gusta más".
- [ ] El escenario 2 elige **turn-based** (o híbrido) por el texto auditable/citas, no S2S puro.
- [ ] El escenario 4 va **on-device/local** por privacidad y lo justificas.
- [ ] El presupuesto de latencia suma **solo** las etapas del primer audio (no el total de generación).
- [ ] El barge-in incluye **cancelar el trabajo en vuelo** y lo liga al costo.
- [ ] La economía nombra el efecto de la **tasa de escalamiento** en el ahorro.
- [ ] **Dos** métricas de observabilidad accionables + **un** riesgo de seguridad con mitigación.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/diseno-voice-agent/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector evaluará la **calidad de tus justificaciones** (¿hay una restricción dominante
real?, ¿nombras lo que pierdes?), no que coincidas con una respuesta única — varios diseños
son válidos si están bien defendidos. La **solución de referencia** vive en
`.ai/soluciones/fase-6/diseno-voice-agent.md` — no la mires antes de intentarlo de verdad.
