"""Plano de control determinista — el "código que dispone".

El LLM propone; este código decide si la propuesta se ejecuta. Es PURO: sin red,
sin LLM, sin estado global. Por eso se puede testear exhaustivamente (ver
test_control_plane.py) y por eso es la pieza más examinable del capstone.

EL ORDEN DE LOS CHEQUEOS ES EL DISEÑO DE SEGURIDAD: la primera barrera que aplica
decide la ruta. No combines barreras en un solo `if ... and ...` — separa cada una
para que el `motivo` identifique exactamente qué frenó.

Orden exacto (mismo que la lección 7.7):
  1. Idempotencia   -> un duplicado nunca re-ejecuta nada (gana sobre todo).
  2. Guardrail I/O  -> jamás actuar sobre salida no validada (OWASP LLM05).
  3. Techo de costo -> circuit-breaker de gasto (Unbounded Consumption).
  4. Acción sensible-> least-privilege + HITL OBLIGATORIO, aunque confianza sea 0.99 (OWASP LLM06).
  5. Confianza      -> SOLO para acciones no sensibles, y al final.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Ruta(str, Enum):
    AUTO = "AUTO"            # ejecutar automáticamente
    HITL = "HITL"            # requiere aprobación humana
    RECHAZO = "RECHAZO"      # no ejecutar
    DUPLICADO = "DUPLICADO"  # ya procesado (idempotencia)


# Least-privilege: lista EXPLÍCITA de acciones irreversibles/sensibles que exigen HITL.
# Agregar una acción aquí es una decisión de seguridad, no un detalle.
ACCIONES_SENSIBLES = {"emitir_reembolso"}


@dataclass(frozen=True)
class Decision:
    ruta: Ruta
    motivo: str


def decidir(
    propuesta,
    *,
    schema_valido: bool,
    ya_procesado: bool,
    costo_acumulado_usd: float,
    techo_costo_usd: float,
    umbral_confianza: float = 0.85,
) -> Decision:
    """Decide la ruta de una propuesta del LLM.

    Args:
        propuesta: objeto con `.accion_propuesta` (str) y `.confianza` (float en [0,1]).
        schema_valido: True si la salida del LLM validó contra el schema.
        ya_procesado: True si este input ya fue procesado (idempotency key).
        costo_acumulado_usd: gasto acumulado del run.
        techo_costo_usd: tope de gasto; al alcanzarlo, no se ejecuta más.
        umbral_confianza: piso de confianza para auto-ejecutar acciones NO sensibles.
                          Frontera: confianza == umbral PASA (es >= umbral).

    Returns:
        Decision(ruta, motivo). El `motivo` debe identificar qué barrera decidió.
    """
    # TODO: implementa los 5 chequeos EN ORDEN, con `return` temprano en cada uno.
    #       Recuerda: la primera barrera que aplica gana. Un duplicado con schema
    #       inválido y acción sensible debe devolver DUPLICADO, no RECHAZO ni HITL.
    raise NotImplementedError("Implementa decidir() siguiendo el orden de los chequeos del docstring.")
