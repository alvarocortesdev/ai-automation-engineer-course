---
ejercicio_id: fase-1/python-intermedio-decorador-context-manager
fase: fase-1
sub_unidad: "1.2"
version: 1
---

# Rúbrica — Un decorador de reintento y un context manager con limpieza garantizada

> Rúbrica analítica atada a los `objetivos` del contrato. Evalúa el **código** y la **comprensión**.
> Estas dos construcciones son fáciles de copiar de una IA y difíciles de defender; la rúbrica
> apunta a la comprensión, no solo al verde de los tests.

## Objetivos evaluados
- **O1** — Implementar un **decorador parametrizado** (tres niveles) que preserva la identidad con `functools.wraps`.
- **O2** — Implementar un **context manager** que garantiza la limpieza aunque el bloque lance una excepción.
- **O3** — Explicar qué problema de duplicación (decorador) y de limpieza (context manager) resuelve cada uno.

> Resultado esperado: `reintentar(veces)` reintenta y re-lanza la última excepción si todas fallan,
> conservando `__name__`; `conexion(registro)` agrega `"desconectado"` siempre y propaga la
> excepción. (El corrector lo sabe; no se lo entrega al alumno.)

## Criterios y niveles

### C1 — Corrección del decorador · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No es parametrizado (no funciona como `@reintentar(veces=3)`), o no reintenta, o no corre. |
| **en-progreso** | Reintenta pero no re-lanza la última excepción (devuelve `None` al fallar todo), o reintenta un número equivocado de veces (`veces+1`, infinito). |
| **competente** | Tres niveles correctos; reintenta exactamente `veces`; re-lanza la última excepción; los tests del decorador pasan. |
| **excelente** | Usa `functools.wraps` (test de `__name__` en verde) y lo justifica; el bucle es limpio y el manejo de la excepción guardada, claro. |

### C2 — Corrección del context manager · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No usa `try/finally` (o `__exit__`): si el bloque revienta, no agrega `"desconectado"`. |
| **en-progreso** | Cierra en el caso normal pero **se traga** la excepción (no propaga), o agrega `"desconectado"` antes de tiempo. |
| **competente** | `"desconectado"` se agrega siempre (normal y con excepción) y la excepción **se propaga**; los tests pasan. |
| **excelente** | Explica por qué el `finally` tras el `yield` garantiza el teardown, y por qué **no** debe `except` que silencie la excepción. |

### C3 — Comprensión y calidad de tests · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó test propio, o no puede explicar qué hace `@` ni el `yield` del context manager. |
| **en-progreso** | Test propio trivial; explicación vaga ("envuelve la función"). |
| **competente** | Test borde nuevo (p. ej. `veces=1`, tipo exacto de la excepción re-lanzada) y explicación correcta del problema que cada herramienta resuelve. |
| **excelente** | Conecta el decorador `reintentar` con el patrón de llamada a LLM/API (robustez, costo/latencia) y el context manager con recursos reales. |

## Errores típicos a marcar
- **Decorador de dos niveles cuando se pidió parametrizado**: `@reintentar` sin `()` no acepta `veces`. Deben ser **tres** niveles.
- **Olvidar `functools.wraps`**: el test de `__name__` falla; además la función decorada "miente" sobre su identidad.
- **No re-lanzar la última excepción**: tras agotar los intentos, la función devuelve `None` en silencio en vez de fallar ruidoso.
- **`return envoltura()` con paréntesis**: ejecuta la envoltura en vez de devolverla.
- **Context manager que se traga la excepción**: un `except` alrededor del `yield`, o un `__exit__` que devuelve `True`, oculta el error del bloque.
- **Agregar `"desconectado"` fuera del `finally`**: si el bloque revienta, nunca corre.
- (transversal/testing) test propio que solo replica un caso del enunciado.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Decorador perfecto con `functools.wraps` pero el alumno **no sabe explicar** qué pasaría si lo omitiera, ni por qué hay tres niveles.
- Usa `contextlib.ExitStack`, `tenacity` u otras piezas avanzadas que no calzan con el nivel de la lección.
- **Verificación sugerida:** pide que explique, sin ejecutar, en qué momento se ejecuta el cuerpo de `reintentar` (¿al decorar o en cada llamada?) y por qué el `finally` del context manager corre aunque el `with` lance. Si lo escribió, responde al toque.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el código completo.
- **Pista (nivel 1):** "Para que `@reintentar(veces=3)` funcione necesitas un nivel más de funciones del que tiene un decorador simple. Cuenta los niveles."
- **Pregunta socrática (nivel 2):** "Si los tres intentos fallan, ¿qué debería ver quien llamó tu función: un `None` silencioso o la excepción? ¿Y dónde guardas esa excepción mientras reintentas?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Estructura: `reintentar(veces)` devuelve `decorador(func)` que devuelve `envoltura`. Dentro, un `for` con `try: return func(...)` / `except` que guarda la excepción; tras el bucle, `raise` la guardada. Para `conexion`, pon el `registro.append('desconectado')` en un `finally` después del `yield`, sin `except`. No te doy el código."

## Conexión con el proyecto / capstone
- El decorador `reintentar` es el patrón con el que envolverás cada llamada a un LLM en la Fase 6 (robustez + costo/latencia); el context manager es cómo manejarás el recurso de datos de la mini-API del **Capstone F1** sin filtrarlo.
