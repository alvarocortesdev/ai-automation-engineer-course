---
ejercicio_id: fase-2/de-print-a-logging-estructurado
fase: fase-2
sub_unidad: "2.12"
version: 1
---

# Rúbrica — De print-spam a logging estructurado (niveles + contexto)

> Rúbrica **analítica** atada a los `objetivos`. Lo que se evalúa NO es "que compile":
> es que el alumno entienda **por qué** `logging` reemplaza a `print` en producción —
> niveles filtrables, contexto estructurado, routing central, off-switch— y lo demuestre
> en código + en `por-que.md`. La lógica de negocio no se toca (la vigila
> `test_logica_intacta`); todo el mérito está en la **instrumentación**.

## Objetivos evaluados
- **O1** — Reemplazar `print()` de depuración por `logging` con el **nivel** correcto (`debug`/`info`/`warning`) que se pueda filtrar sin tocar el código.
- **O2** — Emitir logs **estructurados** con contexto (`pedido_id`, `correlation_id`) vía `extra=`, configurando el logging **una sola vez** con salida a `stdout`.
- **O3** — Justificar por qué `print()` es un antipatrón de observabilidad en producción y qué resuelve el logging estructurado (puente a la observabilidad de la Fase 5).

## Criterios y niveles

### C1 — Niveles correctos y cero `print` · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Quedan `print` en `solucion.py` (`test_no_quedan_prints` rojo), o reemplazó todo por `logger.info` sin distinguir niveles. |
| **en-progreso** | Sin `print`, pero el reparto de niveles está mal: detalle interno en `info`, o el pedido inválido en `debug`/`info` en vez de `warning`. |
| **competente** | Cero `print`; `debug` para el detalle (procesando/total), `info` para el ciclo de vida (pedido procesado), `warning` para el pedido inválido omitido. Tests de niveles verdes. |
| **excelente** | Además reserva `error`/`exception` para fallos reales y argumenta por qué el inválido es `warning` (recuperable) y no `error` (la ejecución continúa). |

### C2 — Contexto estructurado + configuración central · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `extra=`; el contexto va interpolado en el mensaje (`f"pedido {id}"`) o no está. `configurar_logging` sigue con `NotImplementedError`. |
| **en-progreso** | Usa `extra=` pero inconsistente (falta `correlation_id` en algunos logs), o configura el logging **dentro** de `procesar_pedidos` en vez de en una función aparte. |
| **competente** | Cada log lleva `extra={"pedido_id": ..., "correlation_id": ...}`; `logger = getLogger(__name__)` a nivel de módulo; `configurar_logging` con `StreamHandler(sys.stdout)` + `basicConfig(level=...)`, llamable desde `__main__`. |
| **excelente** | Formateador JSON propio (lee `extra` con `getattr(record, ..., default)`) o `python-json-logger`/`structlog`; demuestra el off-switch (`INFO` apaga el `debug` sin tocar la lógica). |

### C3 — Comprensión demostrada (`por-que.md`) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `por-que.md`, o argumenta "queda más prolijo / más profesional" sin sustancia. |
| **en-progreso** | Da 1–2 razones válidas pero genéricas; no conecta con producción ni con la observabilidad de la Fase 5. |
| **competente** | 3 razones concretas que cubran **niveles + contexto + routing + off-switch**; explica por qué `print` no sobrevive a un servidor (se pierde, sin nivel, sin filtro). |
| **excelente** | Conecta `correlation_id` con **trazas/OpenTelemetry** (Fase 5) y con depurar la traza de un **agente** (Fase 6); menciona por qué un `print` en una librería importada es un bug de cortesía. |

## Errores típicos a marcar
- **`logger.info` para todo**: pierde el sentido de los niveles (no se puede filtrar el ruido en prod). El detalle interno es `debug`, no `info`.
- **Contexto interpolado en el mensaje** (`f"pedido {id} total {total}"`) en vez de `extra=`: no es estructurado, no se puede filtrar por campo ni indexar por máquina.
- **Configurar el logging dentro de `procesar_pedidos`**: se reconfigura en cada llamada; la config va una sola vez en el `main`.
- **`logger.propagate = False`**: rompe `caplog` y, en general, impide que los handlers raíz vean el log. El default (propagar) es el correcto aquí.
- **Tocar la lógica de negocio** (`cantidad*precio`, validación, retorno): fuera de alcance; `test_logica_intacta` lo caza.
- **El pedido inválido como `error`** (o peor, lanzando excepción): es una anomalía **recuperable** que se omite → `warning`.
- (transversal observabilidad) logs sin `correlation_id` → imposible seguir un pedido a través del sistema; el campo que conecta con trazas en F5.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `solucion.py` impecable con un `JsonFormatter` sofisticado pero `por-que.md` vacío o de una línea: el código vino de fuera, la comprensión no.
- `por-que.md` con jerga ("structured logging", "log aggregation") pero sin poder explicar qué hace `extra=` ni por qué `getLogger(__name__)` y no `getLogger("app")`.
- Niveles repartidos "perfecto" pero el alumno no sabe defender por qué el inválido es `warning` y no `error`.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué ve `caplog` y qué ve `capsys` si dejara **un** `print` y convirtiera el resto a `logger`; y qué pasa con los `logger.debug` si configura nivel `INFO`. Si no lo razona, no interiorizó la diferencia.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Qué nivel le corresponde a 'procesando pedido' frente a 'pedido inválido, lo omito'? Uno es ruido de rutina, el otro es algo que quizá quieras *alertar*. Empieza por clasificar cada `print` por su nivel."
- **Pregunta socrática (nivel 2):** "Si en producción solo quieres ver `INFO` hacia arriba, ¿cómo apagas el detalle sin editar y redeployar el código? ¿Podrías hacer eso con `print`? Esa imposibilidad es media respuesta del `por-que.md`."
- **Dirección concreta (nivel 3, sólo tras intento real):** "Obtén el logger con `getLogger(__name__)` a nivel de módulo (no lo configures ahí). Pon el contexto en `extra={...}`, no en el texto del mensaje. Centraliza la config en `configurar_logging` con `StreamHandler(sys.stdout)`. Verifica el off-switch corriendo con `INFO` y viendo desaparecer el `debug`. Repasa la sección 4.6 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Instrumentar con logging estructurado (no `print`) es un entregable directo del **Capstone F2** y el ensayo de la **observabilidad** de la Fase 5 (logs/métricas/trazas + correlation IDs). El `correlation_id` que pones aquí es el mismo hilo que en F6 te deja seguir la traza de un agente paso a paso.
