"""Tests del plano de control — definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

No edites estos tests para "hacerlos pasar" cambiando el contrato: implementa
`plano_control.py` hasta que pasen en verde. Los tests de ORDEN son los que
importan: verifican que la primera barrera que aplica gana.
"""

from plano_control import decidir


def _prop(input_id="T-1", valido=True, confianza=0.95):
    return {"input_id": input_id, "valido": valido, "confianza": confianza}


def _acc(sensible=False, umbral=0.8):
    return {"sensible": sensible, "umbral_confianza": umbral}


def test_auto_caso_feliz():
    out = decidir(_prop(confianza=0.95), _acc(sensible=False, umbral=0.8), 0.10, set())
    assert out["ruta"] == "AUTO"


def test_hitl_por_confianza_baja():
    out = decidir(_prop(confianza=0.5), _acc(sensible=False, umbral=0.8), 0.10, set())
    assert out["ruta"] == "HITL"
    assert out["motivo"] != "accion_sensible"  # es por confianza, no por sensible


def test_accion_sensible_siempre_hitl_aunque_confianza_alta():
    # La confianza de 0.99 NO debe permitir auto-ejecutar una acción sensible (LLM06)
    out = decidir(_prop(confianza=0.99), _acc(sensible=True, umbral=0.8), 0.10, set())
    assert out["ruta"] == "HITL"


def test_rechazo_por_schema_invalido():
    # Guardrail de I/O: jamás actuar sobre salida no validada (LLM05)
    out = decidir(_prop(valido=False, confianza=0.99), _acc(), 0.10, set())
    assert out["ruta"] == "RECHAZO"


def test_rechazo_por_techo_de_costo():
    out = decidir(_prop(), _acc(), costo_acumulado_usd=0.70, ids_procesados=set())
    assert out["ruta"] == "RECHAZO"
    assert out["motivo"] == "techo_costo"


def test_techo_de_costo_configurable():
    # Con un techo más alto, el mismo costo ya no rechaza
    out = decidir(_prop(), _acc(), 0.70, set(), techo_costo_usd=1.00)
    assert out["ruta"] == "AUTO"


def test_duplicado_idempotencia():
    out = decidir(_prop(input_id="T-9"), _acc(), 0.10, {"T-9"})
    assert out["ruta"] == "DUPLICADO"


# ── Tests de ORDEN: la primera barrera que aplica gana ──────────────────────

def test_orden_duplicado_gana_sobre_schema_invalido():
    # Aunque el schema sea inválido, si ya se procesó -> DUPLICADO (idempotencia 1ª)
    out = decidir(_prop(input_id="T-9", valido=False), _acc(), 0.10, {"T-9"})
    assert out["ruta"] == "DUPLICADO"


def test_orden_schema_gana_sobre_costo():
    # Schema inválido Y sobre presupuesto: el guardrail (2) va antes del costo (3)
    out = decidir(_prop(valido=False), _acc(), 0.70, set())
    assert out["ruta"] == "RECHAZO"
    assert out["motivo"] != "techo_costo"


def test_orden_costo_gana_sobre_accion_sensible():
    # Sobre presupuesto Y acción sensible: el circuit-breaker (3) va antes (4)
    out = decidir(_prop(), _acc(sensible=True), 0.70, set())
    assert out["ruta"] == "RECHAZO"
    assert out["motivo"] == "techo_costo"


def test_orden_sensible_gana_sobre_confianza():
    # Acción sensible con confianza altísima -> HITL por sensible, no AUTO
    out = decidir(_prop(confianza=0.999), _acc(sensible=True, umbral=0.8), 0.10, set())
    assert out["ruta"] == "HITL"


def test_confianza_justo_en_el_umbral_es_auto():
    # confianza == umbral NO está por debajo -> AUTO (frontera exacta)
    out = decidir(_prop(confianza=0.80), _acc(sensible=False, umbral=0.80), 0.10, set())
    assert out["ruta"] == "AUTO"


# TODO(estudiante): añade un caso tuyo. Sugerencia: una acción sensible que además
# es duplicada -> debe ganar DUPLICADO (idempotencia 1ª), no HITL.
# def test_duplicado_gana_sobre_sensible():
#     ...
