"""Tests del gate de validación.

Verifican la POLÍTICA (permiso -> forma -> semántica), no detalles de implementación.
Todo es determinista: no se llama a ninguna API.
"""

from gate import decidir


# --- Capa 1: permiso (allowlist) --------------------------------------------
def test_tool_fuera_de_allowlist_se_rechaza():
    d = decidir("borrar_todo", {})
    assert d.accion == "RECHAZAR"


def test_tool_no_permitida_no_se_ejecuta_aunque_traiga_args_validos():
    # Argumentos con forma perfecta, pero la tool no está permitida -> RECHAZAR.
    d = decidir("transferir", {"monto_clp": 100})
    assert d.accion == "RECHAZAR"


# --- Capa 2: forma (pydantic) -----------------------------------------------
def test_buscar_pedido_valido_ejecuta():
    d = decidir("buscar_pedido", {"pedido_id": 8842})
    assert d.accion == "EJECUTAR"


def test_pedido_id_negativo_se_rechaza():
    d = decidir("buscar_pedido", {"pedido_id": -1})
    assert d.accion == "RECHAZAR"


def test_pedido_id_no_numerico_se_rechaza():
    d = decidir("buscar_pedido", {"pedido_id": "abc"})
    assert d.accion == "RECHAZAR"


def test_argumento_requerido_ausente_se_rechaza():
    d = decidir("buscar_pedido", {})
    assert d.accion == "RECHAZAR"


def test_reembolsar_sin_monto_se_rechaza():
    d = decidir("reembolsar", {"pedido_id": 1})
    assert d.accion == "RECHAZAR"


def test_reembolsar_monto_no_positivo_se_rechaza():
    d = decidir("reembolsar", {"pedido_id": 1, "monto_clp": -5})
    assert d.accion == "RECHAZAR"


# --- Capa 3: semántica / negocio --------------------------------------------
def test_reembolso_dentro_del_techo_ejecuta():
    d = decidir("reembolsar", {"pedido_id": 1, "monto_clp": 29990})
    assert d.accion == "EJECUTAR"


def test_reembolso_sobre_el_techo_pide_confirmacion():
    d = decidir("reembolsar", {"pedido_id": 1, "monto_clp": 950000})
    assert d.accion == "CONFIRMAR"


def test_reembolso_justo_en_el_techo_ejecuta():
    # 200_000 NO está "sobre" el techo -> EJECUTAR (frontera inclusiva).
    d = decidir("reembolsar", {"pedido_id": 1, "monto_clp": 200000})
    assert d.accion == "EJECUTAR"
