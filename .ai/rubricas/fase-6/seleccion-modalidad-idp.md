---
ejercicio_id: fase-6/seleccion-modalidad-idp
fase: fase-6
sub_unidad: "6.11"
version: 1
---

# Rúbrica — Elegir la modalidad y diseñar el pipeline de IDP

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio de **diseño**: no
> hay una respuesta única. El corrector evalúa la **calidad de la justificación** (¿hay
> una restricción dominante real?, ¿nombra qué pierde?), no que coincida con la solución
> de referencia. Lee la solución **al final**, cuando ya formaste tu juicio.

## Objetivos evaluados

- **O1** — Elegir adaptador + modo (API/local) por la restricción dominante.
- **O2** — Defender IDP especializado vs LLM de vision nombrando qué se pierde.
- **O3** — Diseñar el pipeline de IDP con gate + HITL + validación + seguridad + observabilidad.

## Criterios y niveles

### C1 — Elección de modalidad por restricción dominante (Parte A) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige adaptadores sin justificar, o se equivoca de adaptador (p. ej. vision para transcribir audio). |
| **en-progreso** | Adaptadores correctos pero la "restricción dominante" es genérica ("es mejor") o falta el modo API/local. |
| **competente** | Los 4 adaptadores correctos, con modo API/local y una restricción dominante concreta por caso (latencia, costo/volumen, accesibilidad, privacidad). |
| **excelente** | Distingue matices: STT realtime vs batch (1 vs 3), reconoce que el caso 2 pide confidence (IDP) y el 4 pide local por compliance, no por costo. |

### C2 — IDP especializado vs LLM de vision (Parte B) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No elige, o elige sin razón, o cree que el LLM de vision "hace todo mejor". |
| **en-progreso** | Elige IDP pero no nombra qué pierde, o lo justifica solo por "es más preciso". |
| **competente** | Elige IDP por el **confidence por campo** (habilita el gate) y el determinismo; nombra qué pierde (flexibilidad / razonamiento sobre contenido / cero-entrenamiento del LLM). |
| **excelente** | Propone un **híbrido** justificado (IDP extrae campos duros + LLM razona sobre el texto) sin sobre-ingenierizar. |

### C3 — Diseño del gate + HITL + validación cruzada (Parte B) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay gate ni HITL, o "el humano revisa todo" (sin valor), o no hay validación cruzada. |
| **en-progreso** | Gate con umbral pero sin distinguir auto/HITL, o validación cruzada vaga ("revisar más confidence"). |
| **competente** | Umbral concreto, auto sobre el umbral y HITL abajo, el monto marcado como crítico; validación cruzada = regla de negocio real (suma de líneas vs total). |
| **excelente** | Umbrales por campo (el monto exige más), explica por qué la validación atrapa lo que el confidence deja pasar, conecta con el DoD del capstone (validar antes de actuar). |

### C4 — Seguridad/privacidad y observabilidad (Parte B) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona seguridad ni métricas, o las menciona sin mitigación/sin accionabilidad. |
| **en-progreso** | Un solo riesgo o una sola métrica, o las mitigaciones son genéricas ("ser cuidadoso"). |
| **competente** | Dos riesgos distintos con mitigación concreta (p. ej. indirect prompt injection LLM01 → no pasar el texto crudo del doc a un agente que actúa sin sanitizar; PII → redacción/cifrado/local); dos métricas accionables (tasa de HITL, distribución de confidence, tasa de fallo de validación). |
| **excelente** | Conecta PII con governance/EU AI Act (6.15) y la tasa de HITL con un umbral de alerta o con el ajuste del threshold; menciona audit logging. |

## Errores típicos a marcar

- **Elegir LLM de vision para el escenario 2** sin notar que pierde el confidence por campo (el corazón del gate HITL).
- **No mandar el escenario 4 a local** pese a "los datos no pueden salir de la empresa" (compliance, no costo).
- **"El humano revisa todas las facturas"**: anula el ROI; el HITL es para lo dudoso, no para todo.
- **Validación cruzada confundida con el gate de confianza**: "revisar los de baja confianza" NO es una regla de negocio; la regla es la coherencia (suma vs total).
- **Riesgos de seguridad sin mitigación** o mitigaciones de relleno ("tener cuidado", "usar HTTPS" para todo).
- **Olvidar la observabilidad** o dar métricas no accionables ("número de facturas") en vez de señales de salud (tasa de HITL, confidence, fallo de validación).
- (transversal) No tratar el texto extraído como input no confiable → ignora LLM01/LLM05.

## Señales de dependencia-IA

> Describir sin acusar; proponer una verificación.

- Diseño impecablemente redactado pero que no puede defender, en una repregunta, **por qué** el confidence no basta o **qué** pierde al elegir IDP.
- Lista de riesgos OWASP "de catálogo" que no aplican al caso concreto (copiados sin filtrar).
- **Verificación sugerida:** pedir que invente un quinto escenario propio y lo razone, o que explique en voz alta por qué el escenario 4 va local y el 2 puede ir a API.

## Feedback sugerido (graduado)

> Nunca entregar el diseño completo de la solución de referencia.

- **Pista (nivel 1):** "¿Qué te da un IDP especializado que un LLM de vision no? Esa diferencia decide el escenario 2."
- **Pregunta socrática (nivel 2):** "Si un humano tuviera que revisar las 8.000 facturas, ¿dónde quedó el ahorro? ¿Qué tendría que pasar para que solo revise un puñado?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Para cada caso, pregúntate qué pasa si fallas en una sola dimensión: en el 1 es la latencia, en el 2 el dinero (necesitas confidence + validación), en el 3 la accesibilidad/voz, en el 4 que el dato salga de la empresa (local). Esa dimensión es la restricción dominante. Para el pipeline: gate por umbral → HITL para lo dudoso → validación de negocio (suma vs total) encima del confidence."

## Conexión con el proyecto / capstone

- Esta decisión (IDP vs vision, dónde el umbral, qué validación) es un **ADR** del capstone agéntico (Fase 7), cuyo input casi siempre entra por IDP. El gate + validación cruzada es el "validar la salida antes de ejecutar" del Definition of Done.
