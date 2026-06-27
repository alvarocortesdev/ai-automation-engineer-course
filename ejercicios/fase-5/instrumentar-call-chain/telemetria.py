"""Configuración de telemetría YA RESUELTA — no necesitas tocar este archivo.

Lo usa la demo de `servicio.py` (el bloque __main__) para que VEAS tus logs y spans
en consola. El test NO usa este módulo: monta su propio exporter en memoria.

  - configurar_logs():   structlog en JSON, con merge_contextvars (inyecta el correlation_id).
  - configurar_trazas(): TracerProvider que imprime los spans a la consola al cerrarse.

En producción cambiarías ConsoleSpanExporter por OTLPSpanExporter(endpoint=...) hacia
un colector (Grafana / Datadog / Azure Monitor): tu instrumentación NO cambia, solo el destino.
"""

from __future__ import annotations

import logging

import structlog
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configurar_logs() -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  # trae el correlation_id atado en la petición
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),  # en dev podrías usar ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )


def configurar_trazas() -> None:
    recurso = Resource.create({"service.name": "api-despensa"})
    provider = TracerProvider(resource=recurso)
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
