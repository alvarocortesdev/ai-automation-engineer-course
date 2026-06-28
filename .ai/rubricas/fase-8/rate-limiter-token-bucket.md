---
ejercicio_id: fase-8/rate-limiter-token-bucket
fase: fase-8
sub_unidad: "8.1"
version: 1
---

# Rúbrica — Rate limiter token bucket (testeable y determinista)

> Rúbrica **analítica** para un ejercicio de **código** corto pero con dos aprendizajes profundos: el
> algoritmo token bucket y, sobre todo, el **diseño para testabilidad** (reloj inyectado). El
> corrector verifica que los tests pasen, **pero no se queda ahí**: revisa que el diseño sea
> determinista y que el alumno entienda *por qué*. Nunca entrega el código de la solución.

## Objetivos evaluados

- **O1** — Implementar el token bucket: recargar por tiempo transcurrido sin superar la capacidad, luego consumir si alcanza.
- **O2** — Diseñar con el reloj inyectado (`ahora`) para tests deterministas, sin `sleep` ni flakiness.
- **O3** — Explicar por qué un rate limiter protege capacidad y costo, y por qué el orden recargar→decidir es obligatorio.

## Criterios y niveles

### C1 — Corrección del algoritmo · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo; o "rate limiter" que cuenta requests en una ventana fija (no es token bucket); o no recarga por tiempo. |
| **en-progreso** | Pasa algunos tests pero falla un caso: tokens superan la capacidad (falta el `min`), o consume cuando `cost` no alcanza, o decide antes de recargar. |
| **competente** | Todos los tests en verde: arranca lleno, se agota, recarga por tiempo transcurrido, **topa en la capacidad** (`min`), respeta `cost` sin consumir si no alcanza, y no recarga si el reloj no avanza. |
| **excelente** | Maneja correctamente la recarga fraccionaria y el reloj que retrocede sin un `if` frágil; código limpio (un método `_recargar` separado de `allow`). |

### C2 — Testabilidad / determinismo · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Llama a `time.monotonic()`/`time.time()` dentro de la clase; los tests propios usarían `sleep`. |
| **en-progreso** | Inyecta el reloj pero mezcla algo de estado temporal global, o el test propio no es determinista. |
| **competente** | El tiempo entra **solo** por el parámetro `ahora`; la clase no lee ningún reloj; el test propio agregado es determinista (sin `sleep`). |
| **excelente** | El alumno articula que inyectar el reloj es el mismo principio de determinismo de Temporal (7.3) y de los test doubles (2.8): la dependencia del entorno se pasa como argumento para poder controlarla en el test. |

### C3 — Calidad de ingeniería (tests propios, aserciones reales)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó test propio, o el test no asierta nada útil. |
| **en-progreso** | Agregó un test pero duplica un caso ya cubierto. |
| **competente** | Agregó ≥1 test propio con un caso borde nuevo (p. ej. `cost` mayor que la capacidad nunca se concede; `allow` repetido en el mismo instante no recarga). |
| **excelente** | El test propio captura un caso que un bug plausible rompería (mutación viva): p. ej. quitar el `min` o invertir el orden recargar/decidir haría fallar su test. |

### C4 — Comprensión demostrada · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar para qué sirve un rate limiter más allá de "bloquear hackers". |
| **competente** | Explica que protege capacidad y equidad y **controla costo** (clave en APIs de LLM), y por qué el token bucket permite ráfagas hasta la capacidad pero acota la tasa sostenida. |
| **excelente** | Conecta con la lección: dónde vive el rate limiter en un sistema a escala (gateway/borde, estado compartido en Redis para que funcione con varios servidores stateless) y por qué un bucket por proceso no basta tras un load balancer. |

## Errores típicos a marcar

- Implementar **fixed-window counter** (contar requests por minuto) y llamarlo token bucket: no
  permite ráfagas controladas y sufre el problema del borde de ventana.
- Olvidar el `min(capacity, ...)`: los tokens se acumulan sin tope y el limiter deja de limitar tras
  un rato de inactividad.
- **Decidir antes de recargar:** rechaza requests que sí deberían pasar.
- Consumir tokens **aunque** `cost` no alcance (debe devolver `False` sin tocar el estado).
- Leer el reloj dentro de la clase → tests con `time.sleep` (lentos y flaky). Es el anti-patrón que
  este ejercicio combate.
- (transversal) Perseguir "coverage 100%" en vez de tests que maten mutantes reales (quitar el `min`,
  invertir el orden) — ver 2.9.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- Solución que usa una librería externa de rate limiting (no se pidió) o un decorador "mágico" que el
  alumno no sabe explicar línea a línea.
- Código correcto pero el alumno no sabe por qué el reloj se inyecta, ni qué pasaría con `time.sleep`
  en los tests.
- **Verificación sugerida:** pedir que explique, sin notas, qué línea impide que los tokens superen
  la capacidad y qué pasaría si se invirtiera el orden recargar/decidir. Y que prediga la salida de
  `allow(0.0)` repetido cinco veces con un bucket de capacidad 3.

## Feedback sugerido (graduado)

> Nunca entregar el código de la solución antes de que el alumno cierre su intento.

- **Pista (nivel 1):** "¿Qué dos cosas necesitas recordar entre llamadas a `allow`? Una es cuántos
  tokens quedan; la otra tiene que ver con el tiempo."
- **Pregunta socrática (nivel 2):** "Si pasaron 10 segundos y tu refill_rate es 1 token/s, pero la
  capacidad es 5, ¿cuántos tokens hay ahora? ¿Qué operación impide que sean 10?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu `allow` decide antes de recargar, por
  eso rechaza requests que deberían pasar tras esperar. Mueve la recarga al principio del método y
  recién después compara `tokens >= cost`. Y revisa que un `cost` insuficiente no reste nada."

## Conexión con el proyecto / capstone

- El rate limiting es requisito de los dos sistemas con IA del **capstone de la Fase 8** (proteger el
  costo del LLM ante un cliente en loop) y reaparece como defensa de capacidad y costo en cualquier
  API a escala. El principio del reloj inyectado es el mismo que sostiene los evals y la durable
  execution de fases anteriores.
