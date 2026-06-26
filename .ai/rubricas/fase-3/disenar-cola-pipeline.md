---
ejercicio_id: fase-3/disenar-cola-pipeline
fase: fase-3
sub_unidad: "3.16"
version: 1
---

# Rúbrica — Diseña el pipeline: qué encolar, cómo reintentar, qué va a la DLQ

> Rúbrica **analítica** de un ejercicio de **diseño/razonamiento**. No hay una respuesta única: se evalúa la **calidad del criterio** (por qué síncrono o cola) y la **completitud del diseño** (reintentos, idempotency key, DLQ, observabilidad). Una decisión "contraria a la esperada" bien defendida con criterio y costo nombrado vale más que la "esperada" con un eslogan. El corrector NUNCA entrega el `DISENO.md` de referencia; guía con pistas graduadas.

## Objetivos evaluados
- **O1** — Decidir síncrono vs cola por operación con criterio (lento / frágil / no-crítico para la respuesta) y nombrar el costo de agregar una cola.
- **O2** — Diseñar política de reintentos (max_attempts + backoff + jitter) e idempotency key por trabajo encolado.
- **O3** — Distinguir fallo transitorio (reintentar) de poison message (DLQ) y definir el monitoreo de la DLQ.

## Criterios y niveles

### C1 — Calidad de la decisión síncrono vs cola · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Decide por eslogan ("más escalable", "más simple", "lo que se usa") o mete todo a la cola / nada a la cola sin criterio. No aparece la heurística lento/frágil/no-crítico. |
| **en-progreso** | Justifica con algún criterio real pero parcial: acierta los casos obvios (B a la cola, C síncrono) pero no defiende los finos (webhook D, nocturno E) o no nombra el costo de la cola. |
| **competente** | Las cinco decisiones se apoyan en lento/frágil/no-crítico-para-la-respuesta; A→cola para el email, B→cola, C→síncrono, D→responder rápido + delegar, E→programado (no cola por request). Reconoce al menos una operación que NO debe ir a cola (over-engineering). |
| **excelente** | Además expone la **tensión** del caso fino (D: responder 2xx rápido porque el proveedor reintenta el webhook = at-least-once desde afuera, y el handler del webhook debe ser idempotente por `event_id`) y distingue E (cron programado) de una cola disparada por request. |

### C2 — Diseño de la política: reintentos, idempotencia, DLQ · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No define política, o solo "reintenta unas veces" sin tope, sin backoff, sin idempotency key. Confunde caché con cola o cola con `BackgroundTasks`. |
| **en-progreso** | Define `max_attempts` y backoff, pero olvida el **jitter**, o la idempotency key es vaga ("el id") sin decir qué campos la forman, o no distingue transitorio de poison message. |
| **competente** | Cada operación encolada tiene `max_attempts` + backoff **con jitter**, una **idempotency key concreta** (p. ej. `(campaign_id, contacto_id)` para los envíos), distingue un fallo transitorio (reintentar) de un poison message (DLQ) con ejemplo del dominio, y define cómo monitorear la DLQ (alerta + acción). |
| **excelente** | La idempotency key está justificada (por qué esos campos evitan el doble efecto bajo at-least-once), el plan de DLQ incluye **reproceso** (arreglar dato + reencolar) vs descarte consciente, y dimensiona el backoff según cuánto suele durar una caída transitoria del servicio. |

### C3 — Comunicación y diagrama · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin tabla ni diagrama; el `DISENO.md` es prosa difusa. |
| **en-progreso** | Tabla presente pero incompleta, o diagrama que no muestra el camino a la DLQ. |
| **competente** | Tabla de decisión clara (A–E) + diagrama Mermaid de la campaña con producer → broker → worker(s) → (Hecho o DLQ) + párrafo de cierre con un costo real de la cola. |
| **excelente** | El diagrama refleja **un job por contacto** (no un job gigante de 50k) y el cierre conecta el patrón con la confiabilidad de integración de la Fase 7. |

## Errores típicos a marcar
- **Decidir por moda** ("colas porque escala") o **simplismo** ("síncrono porque es fácil") sin atarlo al criterio lento/frágil/no-crítico.
- **Meter el `GET` de estado (C) a una cola**: over-engineering; una lectura rápida no necesita worker.
- **Procesar el webhook (D) entero dentro del request**: si tardas, el proveedor lo reintenta (doble procesamiento) — hay que responder rápido y delegar; y el handler del webhook debe ser idempotente por `event_id`.
- **Un solo job gigante para los 50.000 emails** en vez de un job por contacto (un fallo arrastra a todos; no hay granularidad de reintento).
- **Reintentos sin tope** (loop infinito con un poison message) o **sin jitter** (thundering herd al reintentar todos a la vez).
- **Olvidar la idempotencia**: configurar reintentos at-least-once sin idempotency key = doble efecto garantizado.
- **DLQ sin observabilidad**: tratarla como basurero en vez de superficie con alerta + reproceso.
- (transversales) confundir `BackgroundTasks`/async-await con una cola persistente; no nombrar ningún costo de la cola (señal de razonamiento inmaduro).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Texto pulido que recita ventajas genéricas de las colas (copiables de cualquier blog) sin aterrizar en las cinco operaciones concretas de "Postal".
- Idempotency keys genéricas ("usa un id único") sin decir qué campos del dominio la forman ni por qué.
- Cinco decisiones "de manual" sin una sola tensión (D o E) ni costo específico — sospechosamente limpias.
- **Verificación sugerida:** pedir el contrafactual del webhook (D): "¿qué pasa si procesas todo dentro del request y tardas 10 s en responder?". Quien razonó dice "el proveedor reasume que falló y reenvía el webhook → doble procesamiento, y por eso el handler debe ser idempotente"; quien copió no conecta el reintento externo con la idempotencia.

## Feedback sugerido (graduado)
> Es diseño: el feedback empuja a defender y completar, no a "la respuesta correcta". **Nunca dar el DISENO de referencia.**
- **Pista (nivel 1):** "Para cada operación, hazte tres preguntas: ¿es lento? ¿es frágil (llama a un tercero)? ¿el usuario necesita el resultado antes de tu respuesta? ¿Cuál de las cinco contesta 'no' a la tercera y aun así la dejaste síncrona?"
- **Pregunta socrática (nivel 2):** "Si un worker envía el email #34.000 de la campaña y muere antes del ack, el broker reentrega ese job. ¿Qué evita que ese contacto reciba el email dos veces? ¿Qué campos forman esa idempotency key y por qué?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu política a la campaña necesita cuatro piezas: max_attempts con tope, backoff con jitter, idempotency key `(campaign_id, contacto_id)`, y una regla de poison message (email inválido → DLQ sin reintentar). Reescribe la operación B incluyendo las cuatro y di cómo te enterarías de que la DLQ creció."

## Conexión con el proyecto / capstone
- Esta decisión es un **ADR** del Capstone F3 (cómo manejar el trabajo lento/frágil de la API). Poder escribir "moví el envío de email a una cola con reintentos backoff+jitter, idempotency key por destinatario y DLQ con alerta, aceptando operar un broker Redis" es el trade-off defendible que pide el Definition of Done. Además, el patrón reintentos + idempotencia + DLQ es la columna de la confiabilidad de integración de la Fase 7.
