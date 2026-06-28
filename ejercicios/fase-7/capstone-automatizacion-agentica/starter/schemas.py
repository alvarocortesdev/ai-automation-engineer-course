"""Esquema de la propuesta del LLM — el "cerebro" llena esto.

El LLM nunca ejecuta una acción: produce una PROPUESTA estructurada que el plano
de control (control_plane.py) valida y decide. Este modelo se valida con pydantic
a la salida del modelo (salida estructurada de la API, ver la lección §4.2).

Nota: control_plane.decidir() NO depende de pydantic — opera sobre cualquier
objeto con los atributos `accion_propuesta` y `confianza`. Así puedes testear el
plano de control sin instalar pydantic ni llamar a ningún modelo.
"""

from __future__ import annotations

try:
    from pydantic import BaseModel, Field
except ImportError:  # pydantic es necesario solo para la extracción real, no para los tests del plano de control
    BaseModel = object  # type: ignore

    def Field(*_args, **_kwargs):  # type: ignore
        return None


class PropuestaTicket(BaseModel):  # type: ignore[misc]
    """Salida estructurada que el LLM debe llenar al clasificar/extraer un ticket."""

    categoria: str = Field(description="reembolso | consulta | queja | spam")
    monto_clp: int | None = Field(default=None, description="monto del reembolso en CLP, o null")
    accion_propuesta: str = Field(description="emitir_reembolso | responder | escalar | descartar")
    confianza: float = Field(ge=0.0, le=1.0, description="confianza auto-reportada del modelo (NO calibrada)")
