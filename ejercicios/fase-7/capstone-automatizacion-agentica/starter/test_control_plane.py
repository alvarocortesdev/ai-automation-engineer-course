"""Tests que GATEAN el plano de control del capstone.

Corre: `uv run pytest`  (o simplemente `pytest`) dentro de starter/.

Estos tests no requieren pydantic, red ni LLM: el plano de control es puro.
Prestan especial atención al ORDEN de los chequeos (la primera barrera gana).
Añade al menos un test propio (mira el TODO al final).
"""

from dataclasses import dataclass

from control_plane import Ruta, decidir


@dataclass
class Propuesta:
    accion_propuesta: str
    confianza: float


def p(accion="responder", confianza=0.99) -> Propuesta:
    """Propuesta base 'feliz' (no sensible, confianza alta) que cada test ajusta."""
    return Propuesta(accion_propuesta=accion, confianza=confianza)


# Estado base "todo en orden": no duplicado, schema válido, costo bajo.
BASE = dict(schema_valido=True, ya_procesado=False, costo_acumulado_usd=0.0, techo_costo_usd=2.0)


# --- rutas básicas -----------------------------------------------------------

def test_auto_ejecutable_feliz():
    d = decidir(p(accion="responder", confianza=0.99), **BASE)
    assert d.ruta is Ruta.AUTO


def test_schema_invalido_rechaza():
    d = decidir(p(), **{**BASE, "schema_valido": False})
    assert d.ruta is Ruta.RECHAZO


def test_techo_de_costo_rechaza():
    d = decidir(p(), **{**BASE, "costo_acumulado_usd": 2.0, "techo_costo_usd": 2.0})
    assert d.ruta is Ruta.RECHAZO


def test_accion_sensible_va_a_hitl_aunque_confianza_alta():
    # OWASP LLM06: una acción irreversible va a HITL aunque el modelo diga 0.99.
    d = decidir(p(accion="emitir_reembolso", confianza=0.99), **BASE)
    assert d.ruta is Ruta.HITL


def test_confianza_bajo_umbral_va_a_hitl():
    d = decidir(p(accion="responder", confianza=0.50), **BASE)
    assert d.ruta is Ruta.HITL


def test_frontera_confianza_igual_al_umbral_pasa():
    # confianza == umbral debe PASAR (es >= umbral), no caer a HITL.
    d = decidir(p(accion="responder", confianza=0.85), **{**BASE, "umbral_confianza": 0.85})
    assert d.ruta is Ruta.AUTO


# --- ORDEN de los chequeos (la primera barrera gana) -------------------------

def test_duplicado_gana_sobre_schema_invalido_y_sensible():
    # Dispara TRES barreras: idempotencia debe ganar -> DUPLICADO.
    d = decidir(
        p(accion="emitir_reembolso", confianza=0.99),
        **{**BASE, "ya_procesado": True, "schema_valido": False},
    )
    assert d.ruta is Ruta.DUPLICADO


def test_schema_gana_sobre_accion_sensible():
    # Schema inválido (no duplicado) -> RECHAZO, antes de mirar si es sensible.
    d = decidir(
        p(accion="emitir_reembolso", confianza=0.99),
        **{**BASE, "schema_valido": False},
    )
    assert d.ruta is Ruta.RECHAZO


def test_costo_gana_sobre_accion_sensible():
    # Techo de costo excedido (no dup, schema válido) -> RECHAZO antes que HITL.
    d = decidir(
        p(accion="emitir_reembolso", confianza=0.99),
        **{**BASE, "costo_acumulado_usd": 5.0, "techo_costo_usd": 2.0},
    )
    assert d.ruta is Ruta.RECHAZO


# --- el motivo debe identificar la barrera -----------------------------------

def test_motivo_distingue_barreras():
    dup = decidir(p(), **{**BASE, "ya_procesado": True})
    sensible = decidir(p(accion="emitir_reembolso"), **BASE)
    assert dup.motivo != sensible.motivo
    assert dup.motivo and sensible.motivo  # no vacíos


# TODO (alumno): agrega un test propio significativo. Sugerencia: un caso donde
# la acción NO es sensible pero la confianza está justo bajo el umbral por 0.01,
# y verifica que va a HITL con el motivo correcto.
