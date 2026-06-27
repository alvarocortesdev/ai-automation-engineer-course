# Ejercicio 5.10 — Instrumenta el call-chain: trazas + correlation ID

> **Modalidad: código (Primero-Sin-IA, timebox 40–45 min).** Tomas un servicio que **no está instrumentado** y le añades observabilidad: trazas (OpenTelemetry) + structured logging con un correlation ID. No cambias la lógica: la envuelves. Un test captura los spans en memoria y verifica la estructura, así que no necesitas red, colector ni cuenta en ningún proveedor.

## Objetivos

- **O1** — Instrumentar una cadena de llamadas con **spans anidados** que reflejen la estructura de la petición (`responder` → `buscar_contexto` + `generar_respuesta`).
- **O2** — Propagar un **`correlation_id`** por la petición (`contextvars`) y emitir **structured logging JSON** que lo lleve en cada evento.
- **O3** — Adjuntar al span del LLM los **atributos de tokens y costo** que en la Fase 6 conectan la traza con el costo y los evals.

## El punto de partida

`servicio.py` tiene tres funciones que forman un call-chain y **ya devuelven el resultado correcto**, pero no emiten nada de telemetría. `telemetria.py` ya trae la configuración de logs (JSON con `merge_contextvars`) y de trazas (a consola) lista para usar en la demo. Tu trabajo es **solo instrumentar `servicio.py`**.

## Tu tarea (en este orden — sin IA)

1. **Spans.** Envuelve cada función en su span con `tracer.start_as_current_span(...)`. Los nombres **exactos** son: `responder` (el padre), `buscar_contexto` y `generar_respuesta` (los hijos). El anidamiento debe salir **automático**: no pases el padre a mano.
2. **Correlation ID.** En `responder`, ata el `correlation_id` recibido al contexto con `structlog.contextvars.bind_contextvars(correlation_id=...)`, y ponlo también como atributo del span raíz: `span.set_attribute("correlation_id", correlation_id)`.
3. **Atributos del LLM.** En `generar_respuesta`, pon como atributos del span: `gen_ai.usage.input_tokens` y `gen_ai.usage.output_tokens` (enteros) y `gen_ai.usage.cost_usd` (float). Los valores ya están calculados en la función.
4. **Structured logging.** Emite al menos un `log.info(...)` de inicio y uno de fin en `responder`. Gracias a `merge_contextvars`, el `correlation_id` aparecerá solo en cada log.

> ⚠️ **Seguridad:** no loguees secretos ni la pregunta cruda si pudiera traer datos personales. El `event` de un log es un nombre estable y consultable (`"inicio_consulta"`), no una frase.

## Cómo probar

```bash
uv sync                      # instala opentelemetry-* y structlog
uv run pytest                # el test captura tus spans en memoria y los verifica
uv run python servicio.py    # VE tus logs JSON y tus spans impresos en consola
```

El test (`test_observabilidad.py`) es tu **spec**: ábrelo y léelo. Te dice exactamente qué nombres de span y qué claves de atributo espera. Cada assert que falla trae un mensaje con la pista.

## Qué entregar

- `servicio.py` instrumentado (las tres funciones con spans, atributos y logs), con la lógica original intacta.

**Hecho significa:**

- [ ] `uv run pytest` en verde: 3 spans, los dos hijos anidados bajo `responder`, `correlation_id` en el span raíz, y los atributos `gen_ai.*` en el span del LLM con el tipo correcto.
- [ ] `uv run python servicio.py` imprime **JSON estructurado** y cada log lleva el mismo `correlation_id`.
- [ ] `responder(...)` sigue devolviendo el `dict` con la clave `respuesta` (instrumentar es envolver, no reescribir).
- [ ] Puedes explicar **sin notas** por qué los hijos se anidan solos y qué responde la traza que un log no responde.

## Pedir corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-5/instrumentar-call-chain/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **comprensión** (por qué se anida, qué pregunta responde cada pilar, por qué los atributos del LLM importan para la Fase 6), no solo si el test pasa.
