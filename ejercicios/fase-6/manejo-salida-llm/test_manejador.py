"""Tests del gate de salida (output handling).

Verifican la POLITICA (fuga -> presupuesto -> codificacion), no detalles de
implementacion. Todo determinista: no se llama a ninguna API.
"""

from manejador import MAX_CARACTERES, manejar_salida


# --- Capa 3: codificacion para el sink HTML (LLM05) -------------------------
def test_texto_normal_se_renderiza_escapado():
    d = manejar_salida("Hola, tu pedido va en camino.")
    assert d.accion == "RENDER"
    # Texto sin caracteres especiales: el escape no lo altera.
    assert d.valor_seguro == "Hola, tu pedido va en camino."


def test_html_peligroso_se_escapa_no_se_bloquea():
    d = manejar_salida("<script>alert(1)</script>")
    # Decision clave del ejercicio: se RENDERIZA escapado, NO se bloquea.
    assert d.accion == "RENDER"
    # El < ya no aparece crudo -> el script queda inerte.
    assert "<script>" not in d.valor_seguro
    assert "&lt;script&gt;" in d.valor_seguro


def test_ampersand_se_escapa():
    d = manejar_salida("plan basico & avanzado")
    assert d.accion == "RENDER"
    assert "&amp;" in d.valor_seguro
    assert "<" not in d.valor_seguro


# --- Capa 1: fuga (LLM07 / LLM02) -------------------------------------------
def test_marcador_system_prompt_se_bloquea():
    d = manejar_salida("Claro. [[SYSTEM_PROMPT]] eres un asistente de soporte...")
    assert d.accion == "BLOQUEAR"


def test_secreto_se_bloquea():
    d = manejar_salida("Tu token es sk-live-abc123, guardalo bien.")
    assert d.accion == "BLOQUEAR"


def test_fuga_es_insensible_a_mayusculas():
    d = manejar_salida("clave: SK-LIVE-ZZZ")
    assert d.accion == "BLOQUEAR"


def test_fuga_se_bloquea_aunque_sea_corta():
    # Una fuga manda aunque el texto sea cortisimo y sin HTML.
    d = manejar_salida("sk-live-x")
    assert d.accion == "BLOQUEAR"


# --- Capa 2: presupuesto (LLM10) --------------------------------------------
def test_salida_sobre_el_presupuesto_se_bloquea():
    d = manejar_salida("x" * (MAX_CARACTERES + 1))
    assert d.accion == "BLOQUEAR"


def test_salida_justo_en_el_presupuesto_se_renderiza():
    # MAX_CARACTERES exacto NO esta "sobre" el techo -> RENDER (frontera inclusiva).
    d = manejar_salida("x" * MAX_CARACTERES)
    assert d.accion == "RENDER"


# --- Orden de las capas: la fuga gana al presupuesto ------------------------
def test_fuga_manda_sobre_presupuesto():
    # Texto larguisimo Y con secreto: debe bloquear por FUGA (capa 1 primero).
    texto = "sk-live-secreto " + ("x" * (MAX_CARACTERES + 100))
    d = manejar_salida(texto)
    assert d.accion == "BLOQUEAR"


# --- Edge -------------------------------------------------------------------
def test_texto_vacio_se_renderiza():
    d = manejar_salida("")
    assert d.accion == "RENDER"
    assert d.valor_seguro == ""
