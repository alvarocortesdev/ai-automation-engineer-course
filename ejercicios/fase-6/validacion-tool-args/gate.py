"""Gate de validación de argumentos de una tool call.

El modelo PIDE una llamada (nombre + argumentos); este módulo decide qué hacer con
ella ANTES de ejecutarla. Implementa `decidir` aplicando, en orden:
    1. permiso  (allowlist de tools)
    2. forma    (validación pydantic de los argumentos)
    3. semántica (reglas de negocio: techo de monto -> HITL)

No depende de ninguna API: recibe lo que ya extrajiste del bloque `tool_use`.
"""

from __future__ import annotations

from dataclasses import dataclass

# --- Constantes del dominio (NO las cambies) --------------------------------
TECHO_REEMBOLSO_CLP = 200_000
ALLOWLIST = {"buscar_pedido", "reembolsar"}


@dataclass
class Decision:
    """La salida del gate. `accion` es uno de: EJECUTAR | RECHAZAR | CONFIRMAR."""

    accion: str
    motivo: str


# --- TODO: define aquí tus modelos pydantic por tool ------------------------
# Pista: un modelo para buscar_pedido (pedido_id: int positivo) y otro para
# reembolsar (pedido_id: int positivo, monto_clp: int positivo). Usa
# field_validator para exigir que sean positivos.


def decidir(nombre: str, argumentos: dict) -> Decision:
    """Decide qué hacer con la tool call que pidió el modelo.

    Capa 1 (permiso): si `nombre` no está en ALLOWLIST -> RECHAZAR, sin mirar args.
    Capa 2 (forma):   valida `argumentos` con el modelo pydantic de esa tool;
                      si no validan -> RECHAZAR.
    Capa 3 (negocio): un reembolso con monto_clp > TECHO_REEMBOLSO_CLP -> CONFIRMAR;
                      en otro caso (y buscar_pedido válido) -> EJECUTAR.
    """
    raise NotImplementedError("Implementa el gate de tres capas")
