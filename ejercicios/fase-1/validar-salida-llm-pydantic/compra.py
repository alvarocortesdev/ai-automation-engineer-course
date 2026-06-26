"""Ejercicio 1.4 — Validar la salida de un LLM con pydantic (Primero-Sin-IA).

Un LLM extrajo una compra desde el texto de un correo y devolvió un JSON. NO confíes
en él: puede mandar el monto como string, dejar campos en blanco, devolver una lista
de items vacía, una fecha que no es fecha, o ALUCINAR campos que no pediste.

Tu trabajo: diseñar el modelo `Compra` (pydantic v2) que valide ese JSON en la FRONTERA
—lo acepta limpio y tipado, o lo rechaza con ValidationError— e implementar `parsear_compra`.

Contrato del modelo (esto es tu spec; los tests lo fijan):
    comercio:   str  no vacío ni de solo espacios   (ej. "Lider")
    monto:      int  > 0, en pesos chilenos          (ej. 12990; acepta "12990" y lo coacciona)
    categoria:  str  no vacío ni de solo espacios     (ej. "supermercado")
    fecha:      date ISO (YYYY-MM-DD)                  (ej. "2026-06-20")
    items:      list[str] con AL MENOS un elemento     (ej. ["leche", "pan"])
    + campos NO declarados (alucinados por el LLM) => la validación debe FALLAR.

Pistas de diseño (no la solución):
  - Constraints con Field: gt, min_length.
  - "   " (solo espacios) pasa min_length: necesitas un @field_validator con strip.
  - Cerrar la puerta a campos extra: model_config = ConfigDict(extra="forbid").
  - parsear + validar en UN paso: Compra.model_validate_json(...).

Instala una vez:  uv add pydantic   (o: pip install pydantic)
Corre los tests:  uv run pytest
"""

from pydantic import BaseModel


class Compra(BaseModel):
    # TODO(estudiante): define los campos, sus constraints y los validadores que
    # haga falta, según el contrato del docstring de arriba. Borra este `pass`.
    pass


def parsear_compra(raw_json: str) -> "Compra":
    """Valida la salida (JSON crudo) de un LLM contra el modelo Compra.

    Debe parsear el string JSON Y validar a la vez (un solo método de pydantic v2).
    Si el JSON no cumple el contrato, deja que se propague el ValidationError.
    """
    # TODO(estudiante): implementa con pydantic v2 (no uses json.loads por separado).
    raise NotImplementedError("Implementa parsear_compra con pydantic v2")
