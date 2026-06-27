"""Test de observabilidad: captura los spans EN MEMORIA y verifica su estructura.

No usa red, ni un colector, ni ningún proveedor cloud: un InMemorySpanExporter recoge
los spans que emite tu `servicio.py`. Este test es tu SPEC — los nombres de span y las
claves de atributo que verifica son exactamente lo que el README te pide instrumentar.

Requisitos: opentelemetry-sdk, structlog, pytest  ->  uv sync
Correr:     uv run pytest
"""

import pytest

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

import servicio


@pytest.fixture(scope="module")
def exportador():
    """Monta un TracerProvider con un exporter en memoria (se setea una vez por sesión)."""
    provider = TracerProvider()
    exp = InMemorySpanExporter()
    provider.add_span_processor(SimpleSpanProcessor(exp))
    trace.set_tracer_provider(provider)
    return exp


@pytest.fixture
def spans(exportador):
    """Ejecuta una petición instrumentada y devuelve {nombre_span: span}."""
    exportador.clear()
    servicio.responder("¿queda leche?", "test-cid-123")
    return {s.name: s for s in exportador.get_finished_spans()}


def test_se_crean_los_tres_spans(spans):
    for nombre in ("responder", "buscar_contexto", "generar_respuesta"):
        assert nombre in spans, (
            f"Falta el span '{nombre}'. Envuelve esa función en "
            f'tracer.start_as_current_span("{nombre}"). Spans encontrados: {sorted(spans)}'
        )


def test_hijos_anidados_bajo_responder(spans):
    raiz = spans["responder"]
    assert raiz.parent is None, (
        "El span 'responder' debe ser la raíz (sin padre). Si tiene padre, lo estás "
        "creando dentro de otro span por error."
    )
    raiz_id = raiz.context.span_id
    for hijo in ("buscar_contexto", "generar_respuesta"):
        s = spans[hijo]
        assert s.parent is not None and s.parent.span_id == raiz_id, (
            f"'{hijo}' debe ser HIJO de 'responder'. El anidamiento es AUTOMÁTICO: abre su "
            "span mientras 'responder' es el span actual; no pases el padre a mano."
        )


def test_correlation_id_en_span_raiz(spans):
    raiz = spans["responder"]
    assert raiz.attributes.get("correlation_id") == "test-cid-123", (
        "El span 'responder' debe llevar el atributo 'correlation_id' con el valor recibido. "
        'Usa span.set_attribute("correlation_id", correlation_id).'
    )


def test_atributos_gen_ai_en_el_span_del_llm(spans):
    attrs = spans["generar_respuesta"].attributes
    in_tok = attrs.get("gen_ai.usage.input_tokens")
    out_tok = attrs.get("gen_ai.usage.output_tokens")
    costo = attrs.get("gen_ai.usage.cost_usd")
    assert isinstance(in_tok, int) and in_tok > 0, (
        "Falta el atributo entero 'gen_ai.usage.input_tokens' en el span 'generar_respuesta'."
    )
    assert isinstance(out_tok, int) and out_tok > 0, (
        "Falta el atributo entero 'gen_ai.usage.output_tokens' en el span 'generar_respuesta'."
    )
    assert isinstance(costo, float) and costo > 0, (
        "Falta el atributo float 'gen_ai.usage.cost_usd' en el span del LLM. "
        "Es el que en la Fase 6 conecta la traza con el costo por paso."
    )


def test_la_instrumentacion_no_cambia_el_comportamiento(spans):
    salida = servicio.responder("¿queda pan?", "otra-cid-456")
    assert isinstance(salida, dict) and "respuesta" in salida, (
        "responder(...) debe seguir devolviendo un dict con la clave 'respuesta'. "
        "Instrumentar es ENVOLVER, no reescribir la lógica."
    )
