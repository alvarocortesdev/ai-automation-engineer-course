---
ejercicio_id: fase-3/retry-backoff-jitter
fase: fase-3
sub_unidad: "3.14"
version: 1
---

# Rúbrica — Reintentos con backoff exponencial + jitter (a mano)

> Rúbrica **analítica** atada a los `objetivos`. Evalúa `solucion.py` + `bitacora.md` con
> `test_acceptance.py` en verde. Los tests son deterministas (inyectan `dormir` y `aleatorio`),
> así que pasar verifica la mecánica; la `bitacora.md` verifica que el alumno entiende **por qué**.

## Objetivos evaluados
- **O1** — Reintentar SOLO transitorias; propagar las permanentes de inmediato.
- **O2** — Backoff exponencial acotado por tope, con full jitter; relanzar la última transitoria al agotar.
- **O3** — Explicar jitter/retry-storm y por qué no se reintentan los permanentes ni los POST no idempotentes.

## Criterios y niveles

### C1 — Corrección del reintento · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_acceptance.py` en rojo: reintenta permanentes, no respeta el tope, o duerme tras el último intento. |
| **en-progreso** | Reintenta lo transitorio pero falla un caso: relanza una excepción genérica en vez de la transitoria, o el conteo de esperas no calza. |
| **competente** | Todos los tests en verde: éxito-1er-intento sin dormir, falla-N-luego-acierta, permanente sin reintentar, agotar-relanza-transitorio, backoff con tope, jitter por debajo del delay. |
| **excelente** | Verde + código limpio: no atrapa lo que no debe (usa `except transitorias`), no duerme de más, y el cálculo de la espera es legible (`aleatorio() * min(tope, base * 2**n)`). |

### C2 — Disciplina de qué se reintenta · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `except Exception` que reintenta TODO (incluidos los permanentes). |
| **en-progreso** | Distingue transitorio de permanente pero con un `if isinstance(...)` manual frágil en vez de usar el parámetro `transitorias`. |
| **competente** | Usa el parámetro `transitorias` en el `except`; los permanentes se propagan sin entrar al bloque de espera. |
| **excelente** | Razona en `bitacora.md` qué errores reales son transitorios (timeout, conexión, 503, 429) vs permanentes (400/401/422) y por qué. |

### C3 — Comprensión demostrada (bitácora) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `bitacora.md` ausente o describe el código sin explicar el porqué. |
| **en-progreso** | Menciona el jitter pero no explica la retry storm, o no liga reintento con idempotencia. |
| **competente** | Explica que el jitter desincroniza a los clientes y evita la tormenta; explica por qué los 4xx no se reintentan. |
| **excelente** | Conecta con la lección: reintentar un POST no idempotente duplica el efecto; menciona retry amplification (reintentos anidados) o el costo/latencia del reintento. |

## Errores típicos a marcar
- **Reintentar lo permanente:** un `except Exception` ciego reintenta un 400; quema recursos y nunca tendrá éxito.
- **Dormir después del último intento:** si no detecta el "último intento" antes de dormir, hace una espera inútil antes de rendirse.
- **Backoff sin tope:** sin `min(tope, ...)`, la espera crece sin límite (esperas de minutos).
- **Backoff sin jitter:** multiplicar sin `aleatorio()` reintroduce la sincronización; el test del jitter (esperas=0 con `aleatorio=0.0`) lo caza.
- **Relanzar excepción genérica:** al agotar intentos, `raise RuntimeError(...)` en vez de relanzar la transitoria original pierde el contexto del fallo real.
- **Off-by-one en el conteo:** confundir "intentos" con "reintentos" (4 intentos = 1 original + 3 reintentos = 3 esperas).
- (transversal observabilidad) no dejar rastro de los reintentos (en producción, un `before_sleep` log); márcalo como mejora, no como falla del ejercicio a mano.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Usa `tenacity` pese a que el enunciado pide hacerlo a mano (no entendió el objetivo pedagógico).
- Código correcto pero `bitacora.md` que no explica qué es la retry storm ni por qué hace falta el jitter.
- Generalizaciones no pedidas (jitter "decorrelated", múltiples estrategias de backoff configurables) impropias del nivel.
- **Verificación sugerida:** pídele que prediga, sin correr, la secuencia de esperas con `base=1, tope=5, aleatorio=lambda: 1.0` y 5 fallos (`[1, 2, 4, 5]`). Si no puede, no internalizó el cálculo.

## Feedback sugerido (graduado)
> Nunca pegar el cuerpo de la función antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Tu `except` atrapa exactamente `transitorias`, o atrapa `Exception` y reintenta también los errores permanentes?"
- **Pregunta socrática (nivel 2):** "Si mil clientes fallan en el mismo milisegundo y todos esperan `base*2^n` EXACTO, ¿a qué hora reintentan? ¿Qué le pasa a la dependencia que intenta levantarse?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Bucle `for intento in range(max_intentos)`: `try: return fn()`; `except transitorias: if intento+1 >= max_intentos: raise; dormir(aleatorio() * min(tope, base * 2**intento))`. Las permanentes no las atrapas. Repasa 4.4."

## Conexión con el proyecto / capstone
- Es el helper que envuelve cada llamada saliente del capstone. Junto con la idempotency key (`disenar-pago-idempotente`) y el circuit breaker (`circuit-breaker-estados`), forma la trilogía de resiliencia que el Definition of Done espera, y la base de la entrega at-least-once de la Fase 7.
