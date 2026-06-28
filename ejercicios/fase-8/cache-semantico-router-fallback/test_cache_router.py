"""Tests del caché semántico + router + fallback. Deterministas: embeddings y llamadas
al modelo se inyectan, así que no hay red, ni sleep, ni flakiness.

Corre con:  uv run pytest   (o simplemente:  pytest)
"""

import pytest

from cache_router import (
    SemanticCache,
    elegir_modelo,
    responder_con_fallback,
    coseno,
    ModeloSaturado,
    RequestInvalido,
)

# Embeddings fijos. "vacaciones" y "dias libres" son casi paralelos (~0.99 de coseno);
# "gastos" es ortogonal (0.0). Así controlamos hits y misses sin un modelo real.
VECTORES = {
    "como pido vacaciones": [1.0, 0.0, 0.0],
    "como me tomo dias libres": [0.99, 0.14, 0.0],
    "politica de gastos": [0.0, 1.0, 0.0],
}


def embed(texto: str) -> list[float]:
    return VECTORES[texto]


# --- coseno -------------------------------------------------------------------------

def test_coseno_identico_y_ortogonal():
    assert abs(coseno([1.0, 0.0, 0.0], [1.0, 0.0, 0.0]) - 1.0) < 1e-9
    assert coseno([1.0, 0.0, 0.0], [0.0, 1.0, 0.0]) == 0.0
    assert coseno([0.0, 0.0, 0.0], [1.0, 2.0, 3.0]) == 0.0  # vector cero -> 0.0


# --- caché semántico ----------------------------------------------------------------

def test_hit_por_similitud():
    cache = SemanticCache(embed)
    cache.put("como pido vacaciones", "A", "Solicítalas en el portal de RRHH.")
    # Pregunta distinta pero semánticamente equivalente -> hit.
    assert cache.get("como me tomo dias libres", "A") == "Solicítalas en el portal de RRHH."


def test_miss_bajo_umbral():
    cache = SemanticCache(embed)
    cache.put("como pido vacaciones", "A", "Solicítalas en el portal de RRHH.")
    # Pregunta ortogonal (similitud 0.0) -> miss.
    assert cache.get("politica de gastos", "A") is None


def test_aislamiento_por_tenant():
    cache = SemanticCache(embed)
    cache.put("como pido vacaciones", "A", "respuesta del tenant A")
    # MISMA pregunta, OTRO tenant: nunca debe recibir el hit de A (aislamiento).
    assert cache.get("como pido vacaciones", "B") is None


def test_umbral_mas_alto_convierte_hit_en_miss():
    estricta = SemanticCache(embed, umbral=0.999)
    estricta.put("como pido vacaciones", "A", "resp")
    # ~0.99 de similitud ya no alcanza un umbral de 0.999.
    assert estricta.get("como me tomo dias libres", "A") is None


# --- router -------------------------------------------------------------------------

def test_ruteo_barato_caro_y_default():
    assert elegir_modelo("clasificacion") == "claude-haiku-4-5"
    assert elegir_modelo("saludo") == "claude-haiku-4-5"
    assert elegir_modelo("extraccion_simple") == "claude-haiku-4-5"
    assert elegir_modelo("sintesis_larga") == "claude-opus-4-8"
    assert elegir_modelo("cualquier_otra") == "claude-sonnet-4-6"


# --- cadena de fallback -------------------------------------------------------------

def test_fallback_degrada_en_saturacion():
    llamados = []

    def call_fn(modelo, messages):
        llamados.append(modelo)
        if modelo == "claude-opus-4-8":
            raise ModeloSaturado("429 rate limit")
        return f"ok desde {modelo}"

    out = responder_con_fallback(call_fn, ["claude-opus-4-8", "claude-haiku-4-5"], [])
    assert out == "ok desde claude-haiku-4-5"
    assert llamados == ["claude-opus-4-8", "claude-haiku-4-5"]  # probó en orden


def test_fallback_no_enmascara_request_invalido():
    def call_fn(modelo, messages):
        raise RequestInvalido("400 bad request")  # bug del request, no saturación

    # No debe degradar ni convertirlo en RuntimeError: el bug se propaga tal cual.
    with pytest.raises(RequestInvalido):
        responder_con_fallback(call_fn, ["claude-opus-4-8", "claude-haiku-4-5"], [])


def test_fallback_todos_saturados():
    def call_fn(modelo, messages):
        raise ModeloSaturado("529 overloaded")

    with pytest.raises(RuntimeError):
        responder_con_fallback(call_fn, ["claude-opus-4-8", "claude-haiku-4-5"], [])
