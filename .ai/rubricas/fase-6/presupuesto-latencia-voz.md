---
ejercicio_id: fase-6/presupuesto-latencia-voz
fase: fase-6
sub_unidad: "6.12"
version: 1
---

# Rúbrica — El cerebro de un voice agent: latencia percibida + barge-in

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector evalúa el
> **proceso** (¿predijo a mano antes de codear?) y la **comprensión** (¿entiende por qué el
> streaming saca al total de la cuenta?), no solo si los tests pasan. Lee la solución de
> referencia **al final**, cuando ya formaste tu propio juicio.

## Objetivos evaluados

- **O1** — `latencia_percibida`: sumar solo las etapas del time-to-first-audio.
- **O2** — `decidir_barge_in`: la tabla de verdad de los cuatro estados.
- **O3** — `evaluar_turno`: combinar latencia y barge-in reusando las funciones base.

## Criterios y niveles

### C1 — Corrección de `latencia_percibida` · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Suma **todo** el dict (incluye `llm_total`/`tts_total`), o revienta con una clave ausente, o no maneja claves desconocidas. |
| **en-progreso** | Suma las etapas correctas pero falla un borde (clave ausente, dict vacío, o no ignora `_total`). |
| **competente** | Suma solo `ETAPAS_PERCIBIDAS` presentes; ignora `llm_total`, `tts_total` y claves desconocidas; etapa ausente = 0; dict vacío = 0. |
| **excelente** | Implementación legible (recorre el conjunto y usa `.get(clave, 0)`); no acopla a un orden ni a la existencia de claves. |

### C2 — Corrección de `decidir_barge_in` (tabla de verdad) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Colapsa dos casos en uno, o solo distingue "interrumpir/no", perdiendo "escuchar"/"esperar". |
| **en-progreso** | Tres de los cuatro casos correctos; confunde "escuchar" (turno normal del usuario) con "interrumpir". |
| **competente** | Los cuatro estados distintos y correctos; "interrumpir" **solo** cuando ambos booleanos son verdaderos. |
| **excelente** | Lógica clara y sin ramas redundantes; nombres de estado consistentes con el dominio (barge-in real). |

### C3 — `evaluar_turno` compone, no reimplementa · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Recalcula la latencia o la decisión a mano dentro de `evaluar_turno` en vez de llamar a las otras dos. |
| **en-progreso** | Reusa una de las dos pero duplica la otra, o el `cumple` usa `<` en vez de `<=`. |
| **competente** | Llama a `latencia_percibida` y `decidir_barge_in`; `cumple` usa `<=` contra el target; arma el dict con las tres claves. |
| **excelente** | Cero duplicación; el `target_ms` por defecto y parametrizable bien usado (S2S sub-250 vs turn-based realista). |

### C4 — Proceso Primero-Sin-IA + comprensión (streaming, costo) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`/`verificacion.md`, o se escribieron después de correr los tests. |
| **en-progreso** | Predice pero sin razón; o la reflexión dice "el streaming ayuda" sin explicar por qué saca al total de la cuenta. |
| **competente** | `prediccion.md` antes de ejecutar con las 3 razones; `verificacion.md` explica que `llm_total`/`tts_total` ocurren **mientras el agente ya habla** y que cancelar en vuelo ahorra USD/min. |
| **excelente** | Conecta con S2S vs turn-based (un salto vs etapas sumadas) y con la observabilidad (medir por etapa para saber dónde recortar); nombra el riesgo de indirect prompt injection por voz (LLM01). |

## Errores típicos a marcar

- **Sumar `llm_total` y `tts_total`** en `latencia_percibida`: el error conceptual #1; el total de generación no cuenta para el primer audio (lo atrapa `test_latencia_suma_solo_las_etapas_percibidas`).
- **Reventar con clave ausente** (`KeyError`) en vez de tratarla como 0 (lo atrapa `test_latencia_etapa_ausente_cuenta_como_cero`).
- **No ignorar claves desconocidas** (sumar `ruido_misterioso`): lo atrapa `test_latencia_ignora_claves_desconocidas`.
- **`decidir_barge_in` que solo distingue interrumpir/no**: pierde "escuchar" y "esperar".
- **`cumple` con `<`** en vez de `<=`: el caso justo en el target cae mal (lo atrapa `test_evaluar_en_el_target_cumple`).
- **`evaluar_turno` que reimplementa** la suma o la tabla en vez de reusar: duplicación que se desincroniza.
- (transversal) Tratar el audio transcrito como confiable, sin mencionar que es input no confiable (LLM01).

## Señales de dependencia-IA

> Describir sin acusar; proponer una verificación.

- Implementación correcta pero `prediccion.md` ausente o idéntica al output real (predijo "después").
- `verificacion.md` repite "el streaming ayuda" como eslogan pero no puede decir **cuáles** etapas no cuentan ni **por qué**.
- **Verificación sugerida:** pedir que invente un stack donde la latencia percibida cumpla el sub-250 pero el total de generación sea enorme, y que explique por qué la conversación se sentiría rápida igual.

## Feedback sugerido (graduado)

> Nunca pegar el código de la solución.

- **Pista (nivel 1):** "¿Tu `latencia_percibida` suma `llm_total`? ¿El usuario espera a que el LLM termine TODA la respuesta antes de oír la primera sílaba?"
- **Pregunta socrática (nivel 2):** "Si el agente está hablando y el usuario también, ¿es lo mismo que si solo habla el usuario? ¿Cuántos casos distintos hay realmente en ese cruce?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Separa los tres pasos: (1) `latencia_percibida` recorre un conjunto fijo de etapas y suma `.get(clave, 0)` —ignora el resto—; (2) `decidir_barge_in` es un cruce de dos booleanos con cuatro salidas; (3) `evaluar_turno` llama a las dos y compone el dict, con `cumple = latencia <= target`."

## Conexión con el proyecto / capstone

- Este cálculo es lo que documentas en un **ADR** si le pones voz al capstone RAG (Fase 6): la decisión S2S vs turn-based, el presupuesto de latencia y el manejo de barge-in. El "decidir antes de actuar" es el mismo patrón del agente de la Fase 7.
