"""Gate de calidad shift-left: valida un lote de datos contra un data contract.

Completa `validar_lote` (y el helper `_tipo_ok`) para que detecte las violaciones
descritas en el README. NO uses Great Expectations: implementa el motor a mano.

El modelo mental (de la lección 7.5b/7.5d): un test de datos es un predicado que
cuenta las filas que violan una regla. Si cuenta 0 filas, la regla pasa.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# El DATA CONTRACT: el acuerdo productor <-> consumidor, versionado, en código.
# (Esto ya está completo: NO lo cambies. Es tu "spec" de entrada.)
# ---------------------------------------------------------------------------
CONTRATO_EVENTOS_PAGO: dict = {
    "nombre": "eventos_pago",
    "version": 1,
    "propietario": "equipo-pagos",
    "campos": {
        "evento_id":  {"tipo": "string",   "requerido": True, "unico": True},
        "usuario_id": {"tipo": "string",   "requerido": True},
        "monto":      {"tipo": "number",   "requerido": True, "min": 0},
        "estado":     {"tipo": "string",   "requerido": True,
                       "valores": ["creado", "pagado", "anulado"]},
        "ts":         {"tipo": "datetime", "requerido": True},  # ISO 8601
    },
    "garantias": {
        "frescura_horas": 24,   # el evento más nuevo no puede tener > 24 h
        "volumen_min": 1,       # bandas esperadas del tamaño del lote
        "volumen_max": 10000,
    },
}


# ---------------------------------------------------------------------------
# Modelo del reporte (ya está completo).
# ---------------------------------------------------------------------------
@dataclass
class Violacion:
    """Una regla del contrato que un lote rompió.

    regla:  identificador corto, p. ej. "duplicado", "nulo", "tipo", "campo_extra".
    campo:  el campo afectado (None para reglas de lote como volumen).
    detalle: explicación legible.
    filas:  índices (0-based) de las filas que violan la regla.
    """
    regla: str
    campo: str | None
    detalle: str
    filas: list[int] = field(default_factory=list)


@dataclass
class Reporte:
    contrato: str
    filas_totales: int
    violaciones: list[Violacion] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """El GATE: el lote pasa si y solo si no hay ninguna violación."""
        return len(self.violaciones) == 0

    def resumen(self) -> dict:
        """Resumen tipo métrica (la base de un evento de observabilidad)."""
        filas_malas: set[int] = set()
        for v in self.violaciones:
            filas_malas.update(v.filas)
        return {
            "contrato": self.contrato,
            "filas_totales": self.filas_totales,
            "filas_rechazadas": len(filas_malas),
            "reglas_violadas": [v.regla for v in self.violaciones],
            "ok": self.ok,
        }


# ---------------------------------------------------------------------------
# TODO: implementa estas dos funciones.
# ---------------------------------------------------------------------------
def _tipo_ok(valor, tipo: str) -> bool:
    """Devuelve True si `valor` calza con `tipo` del contrato.

    tipos: "string" -> str ; "number" -> int/float (NO bool) ;
           "datetime" -> str parseable como ISO 8601.
    """
    # TODO: implementa la verificación de tipo.
    raise NotImplementedError


def validar_lote(filas: list[dict], contrato: dict, ahora: datetime | None = None) -> Reporte:
    """Valida `filas` contra `contrato` y devuelve un Reporte con TODAS las violaciones.

    No cortes en la primera violación: acumula todas (un reporte parcial es inútil
    para el productor). Recorre el CONTRATO (no el dato): para cada campo declarado,
    verifica su regla sobre todas las filas; eso te da `campo` y `filas` naturalmente.

    Reglas obligatorias a detectar:
      - campo_faltante     : fila a la que le falta un campo `requerido`.
      - campo_extra        : fila con un campo NO declarado en el contrato (schema drift).
      - tipo               : valor presente cuyo tipo no calza (usa `_tipo_ok`).
      - nulo               : campo `requerido` presente pero con valor None.
      - duplicado          : campo `unico: true` con valores repetidos en el lote.
      - valor_no_aceptado  : campo con `valores` que trae algo fuera de la lista.
      - fuera_de_rango     : campo numérico con `min`/`max` que se sale.

    Profundización (si vienen en contrato["garantias"]):
      - volumen            : len(filas) fuera de [volumen_min, volumen_max].
      - frescura           : el `ts` más nuevo supera `frescura_horas` respecto de `ahora`.

    Cuidado con el orden: si un campo es None, NO evalúes su tipo/rango (ya es 'nulo';
    evita un TypeError).
    """
    # TODO: construye y devuelve el Reporte.
    raise NotImplementedError
