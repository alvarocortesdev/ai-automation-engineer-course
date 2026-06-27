---
ejercicio_id: fase-6/diseno-voice-agent
fase: fase-6
sub_unidad: "6.12"
version: 1
---

# Rúbrica — Elegir la arquitectura y diseñar un voice agent

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio de **diseño**: no hay
> una respuesta única. El corrector evalúa la **calidad de la justificación** (¿hay una
> restricción dominante real?, ¿nombra qué pierde?), no que coincida con la solución de
> referencia. Lee la solución **al final**, cuando ya formaste tu juicio.

## Objetivos evaluados

- **O1** — Elegir S2S / turn-based / híbrido por la restricción dominante.
- **O2** — Defender la elección nombrando qué se pierde (en especial, el texto del S2S).
- **O3** — Diseñar el voice agent: latencia + barge-in + economía + observabilidad + seguridad.

## Criterios y niveles

### C1 — Elección de arquitectura por restricción dominante (Parte A) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige sin justificar, o pone S2S en todo "porque es más moderno". |
| **en-progreso** | Arquitecturas razonables pero la "restricción dominante" es genérica ("es mejor"). |
| **competente** | Los 4 casos con una restricción dominante concreta: 1=naturalidad/latencia (S2S), 2=auditabilidad/citas (turn-based), 3=time-to-market/costo (S2S gestionado o lo más simple), 4=privacidad (local/on-device). |
| **excelente** | Distingue matices: reconoce que el 3 puede ir S2S gestionado por velocidad de prototipo, y que el 2 puede ser **híbrido** (S2S conversacional + tool-call a RAG) sin sobre-ingenierizar. |

### C2 — IDP del trade-off: qué pierde el S2S (Parte B) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Elige arquitectura sin nombrar qué pierde, o cree que el S2S "no tiene desventajas". |
| **en-progreso** | Nombra una pérdida vaga ("menos control") sin aterrizarla. |
| **competente** | Nombra concretamente lo que pierde el S2S: el **texto intermedio** → menos observabilidad/evals, control indirecto de tools/RAG, guardrails más difíciles, dependencia de proveedor. |
| **excelente** | Liga la pérdida a una consecuencia de negocio (no poder citar fuentes, no poder auditar en un dominio regulado) y propone cómo mitigarla si igual va S2S. |

### C3 — Latencia + barge-in (Parte B) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay presupuesto de latencia, o suma el total de generación; no hay barge-in o es solo "detectar voz". |
| **en-progreso** | Lista etapas pero incluye el total; o el barge-in no menciona cancelar el trabajo en vuelo. |
| **competente** | Presupuesto que suma **solo** las etapas del primer audio con un objetivo; barge-in con cortar audio + **cancelar en vuelo** + vaciar buffers + escuchar, ligando la cancelación al costo. |
| **excelente** | Identifica dónde recortar (VAD endpoint, LLM TTFT) y por qué el sub-250 es la vara del S2S; conecta barge-in roto con la tasa de escalamiento. |

### C4 — Economía, observabilidad y seguridad (Parte B) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay economía, ni métricas, ni seguridad; o métricas no accionables ("número de llamadas"). |
| **en-progreso** | Una de las tres floja: economía sin la tasa de escalamiento, una sola métrica, o seguridad sin mitigación. |
| **competente** | Economía USD/min compuesta por arquitectura + el efecto de la **tasa de escalamiento** en el ahorro; dos métricas accionables (latencia p95, tasa de barge-in, tasa de escalamiento); un riesgo con mitigación (LLM01 por voz, o PII/consentimiento). |
| **excelente** | Liga el barge-in (cancelar en vuelo) al costo; conecta la PII/consentimiento del audio con governance/EU AI Act (6.15); métricas con umbral de alerta. |

## Errores típicos a marcar

- **Elegir S2S para el escenario 2** sin notar que pierde el texto auditable/citable (el corazón del caso regulado).
- **No mandar el escenario 4 a local/on-device** pese a "los datos no pueden salir" (privacidad, no costo).
- **Sumar el total de generación** en el presupuesto de latencia (mismo error del ejercicio de código).
- **Barge-in = "detectar voz"**: omite cortar el audio y, sobre todo, **cancelar el trabajo en vuelo** (que también es costo).
- **Economía sin la tasa de escalamiento**: "el agente cuesta menos por minuto" ignora que si escala a humano, pagas las dos cosas.
- **Métricas no accionables** ("cantidad de conversaciones") en vez de señales de salud (latencia p95, barge-in, escalamiento).
- (transversal) Tratar el audio transcrito como confiable → ignora indirect prompt injection por voz (LLM01).

## Señales de dependencia-IA

> Describir sin acusar; proponer una verificación.

- Diseño impecable que, ante una repregunta, no puede defender **por qué** el S2S pierde observabilidad o **qué** etapas cuentan para el primer audio.
- Lista de riesgos OWASP "de catálogo" que no aplican al canal de voz (copiados sin filtrar).
- **Verificación sugerida:** pedir que invente un quinto escenario y lo razone, o que explique en voz alta por qué el escenario 2 no va S2S puro pese a que el S2S sea más rápido.

## Feedback sugerido (graduado)

> Nunca entregar el diseño completo de la solución de referencia.

- **Pista (nivel 1):** "Para el escenario 2: ¿qué te da el texto en el medio que el S2S no? Esa diferencia decide el caso."
- **Pregunta socrática (nivel 2):** "Si el agente cuesta menos por minuto que un humano pero escala a humano el 60% de las veces, ¿de verdad ahorraste? ¿Qué métrica te lo diría?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Para cada caso, pregúntate qué pasa si fallas en una sola dimensión: en el 1 es sonar robot (latencia → S2S), en el 2 es no poder auditar/citar (texto → turn-based), en el 3 es no llegar a tiempo (lo más simple), en el 4 es que el dato salga (local). El presupuesto de latencia suma solo lo que cuenta para el primer audio; el barge-in corta + **cancela en vuelo** + vacía + escucha."

## Conexión con el proyecto / capstone

- Esta decisión (S2S vs turn-based, presupuesto de latencia, barge-in) es un **ADR** si le pones voz al capstone RAG (Fase 6) o al agente de la Fase 7. El barge-in con cancelación en vuelo y el techo de USD/min son entregables del Definition of Done de un agente que actúa.
