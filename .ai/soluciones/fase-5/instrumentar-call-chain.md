---
ejercicio_id: fase-5/instrumentar-call-chain
fase: fase-5
sub_unidad: "5.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Hay grados de libertad en la
> forma (qué atributos extra, orden de los logs); penaliza el **fondo** (spans mal anidados,
> correlation_id ausente, atributos del LLM con tipo equivocado, secreto logueado), no las variantes.

# Solución de referencia — Instrumenta el call-chain

## `servicio.py` instrumentado (una versión correcta)

```python
from __future__ import annotations

import structlog
from opentelemetry import trace

tracer = trace.get_tracer("api-despensa")
log = structlog.get_logger()


def responder(pregunta: str, correlation_id: str) -> dict:
    with tracer.start_as_current_span("responder") as span:
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
        span.set_attribute("correlation_id", correlation_id)
        span.set_attribute("pregunta.longitud", len(pregunta))
        log.info("inicio_consulta")
        contexto = buscar_contexto(pregunta)
        respuesta = generar_respuesta(pregunta, contexto)
        log.info("fin_consulta", chars_respuesta=len(respuesta))
        structlog.contextvars.clear_contextvars()
        return {"respuesta": respuesta}


def buscar_contexto(pregunta: str) -> str:
    with tracer.start_as_current_span("buscar_contexto") as span:
        filas = 3
        span.set_attribute("db.system", "postgresql")
        span.set_attribute("db.filas_devueltas", filas)
        return f"contexto con {filas} filas relevantes"


def generar_respuesta(pregunta: str, contexto: str) -> str:
    with tracer.start_as_current_span("generar_respuesta") as span:
        tokens_in, tokens_out = 1200, 340
        costo = round(tokens_in * 3e-6 + tokens_out * 1.5e-5, 6)
        span.set_attribute("gen_ai.request.model", "claude-sonnet-4-5")
        span.set_attribute("gen_ai.usage.input_tokens", tokens_in)
        span.set_attribute("gen_ai.usage.output_tokens", tokens_out)
        span.set_attribute("gen_ai.usage.cost_usd", costo)
        return "respuesta generada por el LLM"
```

(El bloque `__main__` y `telemetria.py` ya venían dados; no son parte del trabajo del alumno.)

## El razonamiento que el alumno debe poder defender

- **¿Por qué los hijos se anidan solos?** `start_as_current_span` no solo crea el span: lo pone como **span actual** del contexto. Cuando `responder` (su span ya es el actual) llama a `buscar_contexto` y esta abre el suyo, OTel lo cuelga automáticamente como hijo del span actual. No se pasa el padre a mano. Si el alumno no puede explicar esto, copió el patrón sin entenderlo.
- **¿Qué responde la traza que un log no responde?** La traza muestra **estructura y latencia**: el árbol de operaciones y dónde se fue el tiempo (`generar_respuesta` se llevó el 90%). Un log da el **detalle de un evento puntual**. En un incidente: la traza te lleva al span lento, el log te dice por qué.
- **¿Por qué el correlation_id va en `contextvars` y no como parámetro?** En un sistema concurrente, decenas de peticiones intercalan sus logs. El `correlation_id` atado al contexto aparece en **cada** log de esa petición sin tener que pasarlo a cada función (sería ruido y se olvidaría). Permite filtrar "todos los eventos de ESTA petición".
- **¿Por qué importan `gen_ai.usage.*`?** Esos atributos son el puente a la Fase 6: agrupando trazas por modelo y sumando `cost_usd` se diagnostica una factura disparada; cada traza es además un caso del dataset de evals. La observabilidad de hoy es la materia prima de los evals de mañana.

## Notas para el corrector

- **Variantes válidas:** atributos extra (`db.system`, `gen_ai.request.model`, longitudes); más o menos logs; nombres de evento de log distintos; usar `clear_contextvars` o no (es higiene, no obligatorio para el test). Lo que el test exige es lo del README.
- **`gen_ai.usage.cost_usd` debe ser float.** El test rechaza un int aquí (un costo es un número con decimales). Si el alumno lo puso como int, nómbralo: revela que no pensó en el dato, solo en pasar el assert.
- **Penaliza el fondo, no la forma:**
  - spans **no anidados** (los tres como raíces, o creados con `start_span` sin activarlos como current) → el árbol no se forma; es el error conceptual central.
  - `correlation_id` faltante o no propagado a los logs.
  - **secreto o PII logueado** (header de auth, pregunta cruda volcada entera "por si acaso") → es violación de OWASP A09, no un detalle estético.
  - log con f-string en vez de campos (`log.info(f"...")`) → vuelve el log no consultable.
- **Señal de dependencia-IA:** instrumentación impecable pero no sabe explicar por qué los hijos se anidan, o usa términos (sampling, tail-based, baggage) que el código no implementa y no puede defender. Pídele: "¿qué pasaría con el árbol si usaras `start_span` en vez de `start_as_current_span`?" — si no sabe, lo generó sin comprender.
- **Comprobación objetiva:** `uv run pytest` en verde (5 tests). El test solo mira spans + valor devuelto; el logging-con-correlation_id y la ausencia de secretos se verifican **leyendo el código** y pidiendo la explicación.
