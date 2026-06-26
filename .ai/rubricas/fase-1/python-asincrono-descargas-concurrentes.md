---
ejercicio_id: fase-1/python-asincrono-descargas-concurrentes
fase: fase-1
sub_unidad: "1.3"
version: 1
---

# Rúbrica — Descargas concurrentes que se miden solas

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con
> `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback.

## Objetivos evaluados

- **O1:** Implementar una corutina que ejecute varias operaciones de I/O concurrentemente, preservando el orden de entrada de los resultados.
- **O2:** Demostrar con una medición de tiempo que la versión concurrente no tarda la suma de las demoras, sino aproximadamente la mayor.
- **O3:** Explicar por qué hacer `await` dentro de un bucle, uno por uno, NO produce concurrencia.

## Criterios y niveles

### C1 — Corrección: concurrencia real + orden · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `obtener_todos` no es `async def`, o no corre; `NotImplementedError` sigue ahí. |
| **en-progreso** | Devuelve los strings correctos pero **en serie** (`await` dentro del `for`): `test_es_concurrente` falla por tiempo. O es concurrente pero **pierde el orden** (usó `as_completed` y appendea por llegada). |
| **competente** | Concurrente y en orden: los 4 tests pasan. Usa `asyncio.gather(*corutinas)` o un `TaskGroup`, y devuelve resultados en orden de entrada. |
| **excelente** | Lo anterior + maneja la lista vacía explícita o naturalmente, y por iniciativa demuestra el hilo **costo/latencia**: comenta o mide la diferencia suma-vs-máximo, o menciona acotar la concurrencia con `Semaphore` para *rate limits*. |

### C2 — Calidad de ingeniería (tests reales, clean code) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó ningún test propio; no corrió la suite. |
| **en-progreso** | Agregó un test trivial que no aporta (duplica uno existente) o que no asegura nada (sin `assert` útil). |
| **competente** | Agregó al menos un caso borde con valor (lista vacía, un solo recurso, demoras iguales) con aserción clara; la corutina interna tiene nombre y responsabilidad claros. |
| **excelente** | Test propio que ataca un riesgo real (p. ej. que el orden se mantiene aunque el primero sea el más lento), nombres expresivos, sin código muerto. |

### C3 — Comprensión demostrada (el write-up/explicación calza) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar por qué su versión es concurrente; "lo hice con gather" sin entender qué cambia. |
| **en-progreso** | Explica que gather "es más rápido" pero no por qué (no menciona que el `await` en serie espera cada una hasta el final). |
| **competente** | Explica que `await x` dentro del `for` bloquea hasta terminar cada tarea antes de lanzar la siguiente, y que la solución es **lanzar todas y esperar después**. |
| **excelente** | Además distingue concurrencia de paralelismo (un solo hilo intercalando esperas) y reconoce que esto solo ayuda porque es I/O-bound. |

## Errores típicos a marcar

- `await` dentro del `for` (secuencial) creyendo que ya es concurrente: el clásico de esta lección.
- Usar `as_completed` y appendear por orden de llegada → pierde el orden de entrada (rompe O1).
- Olvidar el `*` al desempacar en `gather(*corutinas)` (pasa la lista como un solo argumento).
- Llamar a `asyncio.run` **dentro** de `obtener_todos` (el `run` va en el test / `main`, no anidado).
- Meter un `time.sleep` por costumbre en vez de `asyncio.sleep` (bloquearía el loop; aquí además rompe el test de tiempo).
- (transversales) confiar en que "anda en mi máquina" sin correr el test de tiempo; no pensar en acotar la concurrencia (Semaphore) de cara a *rate limits* reales.

## Señales de dependencia-IA

- Solución que usa patrones avanzados (`Semaphore`, `wait`, `wait_for`, callbacks) sin poder explicar el `gather` básico → sofisticación impropia del nivel; pídele que explique qué hace `gather` línea a línea.
- Explicación que dice "async lo hace paralelo" mientras el código es correcto → copió la solución pero no internalizó el modelo (un solo hilo). Verificación: que prediga, sin ejecutar, el tiempo del PREDICT de la sección 6.1.
- Resultado correcto pero sin ningún test propio agregado y sin poder justificar el umbral del test de tiempo.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Tu salida es correcta, pero `test_es_concurrente` falla por tiempo. Mira **dónde** pones el `await`: ¿esperas cada descarga antes de lanzar la siguiente?"
- **Pregunta socrática (nivel 2):** "Si tienes 3 corutinas y quieres que sus esperas se solapen, ¿en qué momento deben estar las 3 ya 'lanzadas'? ¿Antes o después del primer `await`?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Separa **crear** las corutinas de **esperarlas**: arma la lista `[descargar(r) for r in recursos]` y pásala entera a `asyncio.gather(*...)`. No la esperes dentro del bucle. No te doy el cuerpo: ya tienes la pieza que faltaba."

## Conexión con el proyecto / capstone

- Es el reflejo que usará el alumno en el Capstone F1 cuando su mini-API tenga que hablar con I/O externo, y el patrón base de los agentes (Fase 6/7) que llaman a varias herramientas a la vez.
