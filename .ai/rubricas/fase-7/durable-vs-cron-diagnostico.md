---
ejercicio_id: fase-7/durable-vs-cron-diagnostico
fase: fase-7
sub_unidad: "7.3"
version: 1
---

# Rúbrica — Diagnóstico: durable execution vs cron frágil

> Rúbrica **analítica** para un ejercicio **a-mano** de razonamiento. Lo que se evalúa es la
> **calidad del diagnóstico**, no la prosa. Un alumno puede listar fallos genéricos copiados de un
> blog; otro puede señalar la línea exacta y la garantía que la cubre. La rúbrica distingue ambos.
> El corrector **no** da el análisis: guía con pistas hasta que el alumno lo reconstruya.

## Objetivos evaluados

- **O1** — Identificar modos de falla del cron y la garantía de durable execution que resuelve cada uno.
- **O2** — Detectar las violaciones de determinismo que romperían el replay, con su alternativa.
- **O3** — Trazar la frontera workflow/activity (side effects en activities; el workflow orquesta).

## Criterios y niveles

### C1 — Modos de falla y su remedio · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Menos de 4 modos, o genéricos ("puede fallar la red") sin ligarlos a un punto del script. |
| **en-progreso** | 4 modos plausibles, pero al menos uno mal atribuido o sin nombrar la garantía que lo resuelve. |
| **competente** | ≥4 modos **distintos** anclados a líneas/pasos concretos, cada uno con la garantía correcta (reanudación por replay, idempotencia de workflow, timer durable, reintentos con memoria). |
| **excelente** | Además distingue el peor estado (cobrado/transferido sin notificar, o reservado sin transferir) y explica por qué es *silencioso* (nadie se entera) — el argumento de observabilidad. |

### C2 — Violaciones de determinismo · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No identifica el problema de replay, o solo dice "usa Temporal" sin señalar líneas. |
| **en-progreso** | Señala 1–2 violaciones (típicamente solo `datetime.now()`) y omite el resto. |
| **competente** | Señala ≥3 de las 4 violaciones (`datetime.now()`, `random.*`, `requests.*` dentro del workflow, `time.sleep`) con su alternativa correcta. |
| **excelente** | Las 4, y articula la causa raíz: *el workflow se re-ejecuta en replay, así que todo lo que cambia entre corridas o toca el mundo debe salir del workflow*. |

### C3 — Frontera workflow / activity · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No separa, o mete I/O en el workflow. |
| **en-progreso** | Separa parcialmente: identifica algunas activities pero deja un side effect en el workflow, o convierte la orquestación en activity. |
| **competente** | Clasifica bien: `reservar_fondos`, `transferir`, `notificar` (y la lectura de pendientes) como activities; el orden, la espera y la compensación como lógica del workflow. |
| **excelente** | Nota que el `while True` de reintentos **desaparece**: lo reemplaza una `RetryPolicy` sobre la activity (no se reimplementa a mano), y que la idempotencia de cada activity es requisito por el at-least-once. |

## Errores típicos a marcar

- Confundir "la red puede fallar" (problema de cualquier sistema) con "el **proceso** muere y pierde
  el estado de en qué paso iba" (lo específico que resuelve la durable execution).
- Decir que `time.sleep(6h)` "es lento" en vez del problema real: **muere con el proceso** y no
  sobrevive un deploy/reinicio → se debe modelar como `workflow.sleep` (timer durable).
- Proponer reimplementar el `while True` de reintentos dentro del workflow en vez de delegarlo a la
  `RetryPolicy` de la activity.
- Olvidar la idempotencia: si Temporal reintenta una activity at-least-once y no es idempotente,
  reserva/transfiere dos veces. (Conecta con 3.14 y 7.2.)
- Meter `requests` en el workflow "porque es solo una línea" — la falta #1.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- Análisis con vocabulario muy por encima del resto (cita "deterministic constraints",
  "event sourcing") pero **sin anclar a las líneas concretas** del `cron_pagos.py` dado.
- Lista de fallos que no menciona ni el `time.sleep` de 6h ni el `random`/`datetime.now()` —como si
  no hubiera leído *este* script en particular.
- **Verificación sugerida:** pedir que señale, en el archivo, el número de línea exacto de cada
  violación de determinismo y que diga qué pasaría si el proceso muere en la línea del `sleep`. Si
  diagnosticó de verdad, lo hace al instante.

## Feedback sugerido (graduado)

> Nunca entregar el análisis completo antes de que el alumno cierre su intento.

- **Pista (nivel 1):** "Recorre el script preguntándote en cada línea: *si el proceso muere aquí, ¿en
  qué estado queda el mundo?*. Empieza por la línea del `time.sleep`."
- **Pregunta socrática (nivel 2):** "¿Qué tienen en común `datetime.now()`, `random.randint()` y
  `requests.post()` que los hace peligrosos *dentro de una función que Temporal va a re-ejecutar*?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Te falta separar orquestación de
  efectos. Haz dos columnas: 'toca el mundo' (va en activity) y 'decide el orden/espera/compensa'
  (queda en el workflow). El `while True` de reintentos no es ninguna de las dos: es algo que
  Temporal ya te da con `RetryPolicy`."

## Conexión con el proyecto / capstone

Este diagnóstico es el paso previo al [mini-proyecto saga](../../../ejercicios/fase-7/saga-pago-durable/)
y, más allá, al capstone agéntico de la fase: antes de hacer durable un agente hay que saber **ver**
por qué un proceso no-durable se rompe. Es exactamente la pregunta de entrevista "¿cómo evitas un
cobro huérfano si tu servicio se cae a la mitad?".
