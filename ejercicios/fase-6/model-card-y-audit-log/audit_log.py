"""Audit log estructurado para decisiones de IA (gobernanza / accountability).

Tres piezas que implementas:
    redactar(texto)             -> quita PII (emails, secuencias largas de dígitos)
    registrar(evento, prev)     -> arma UN registro: valida, redacta, encadena y hashea
    verificar_cadena(registros) -> True si la cadena es íntegra y a prueba de manipulación

Reglas (el contrato lo fijan los tests):
- Todo es PURO y DETERMINISTA: sin red, sin reloj (el timestamp viene en el evento).
- El registro NUNCA guarda PII en claro: la entrada se guarda redactada en 'input_redacted',
  y el 'input_text' crudo NO debe quedar en el registro.
- record_hash = hash del registro EXCLUYENDO record_hash (incluye prev_hash).
- verificar_cadena debe RECOMPUTAR cada record_hash (no solo mirar los enlaces): así detecta
  que alguien editó un campo viejo.

Docs oficiales:
    https://docs.python.org/3/library/hashlib.html
    https://docs.python.org/3/library/json.html
"""

from __future__ import annotations

GENESIS = "0" * 64
CAMPOS_REQUERIDOS = (
    "request_id",
    "timestamp",
    "actor",
    "modelo",
    "prompt_version",
    "decision",
)


def redactar(texto: str) -> str:
    """Reemplaza emails y secuencias largas de dígitos (RUT, teléfonos, tarjetas: 7+ dígitos
    con o sin puntos/guiones) por '<REDACTADO>'. El resto del texto se conserva intacto.
    Los números cortos (un año como 2026) NO se redactan."""
    raise NotImplementedError("Implementa redactar")


def registrar(evento: dict, prev_hash: str) -> dict:
    """Construye un registro de auditoría a partir de un evento.

    - Lanza ValueError si falta algún campo de CAMPOS_REQUERIDOS.
    - Copia los campos requeridos.
    - Si 'input_text' viene en el evento, guarda su versión REDACTADA en 'input_redacted'
      y NO guarda el texto crudo.
    - Copia 'confidence' y 'human_in_the_loop' si vienen.
    - Añade 'prev_hash' y calcula 'record_hash' (hash del contenido sin record_hash).
    """
    raise NotImplementedError("Implementa registrar")


def verificar_cadena(registros: list[dict]) -> bool:
    """True si la cadena es íntegra: el primer prev_hash es GENESIS, cada record_hash
    recomputado coincide con el guardado, y cada prev_hash apunta al record_hash anterior."""
    raise NotImplementedError("Implementa verificar_cadena")
