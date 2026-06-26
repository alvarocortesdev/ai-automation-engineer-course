"""Mutante A — copia de solucion.py con un BUG introducido. NO la edites.

Diferencia con `solucion.py`: NO valida la `cantidad`. Acepta cantidades ≤ 0,
no enteras o booleanas sin protestar. Tu suite debe ponerse ROJA contra este
mutante; si queda verde, te falta el caso de cantidad inválida.

Define los mismos nombres que `solucion.py` para que el autochequeo sea un cambio
de una sola línea en el import de `test_solucion.py`.
"""

import json
from dataclasses import dataclass

INSTRUCCION = (
    "Extrae el pedido del mensaje del cliente y responde SOLO con un JSON con las "
    'claves exactas "producto" (string) y "cantidad" (entero). Sin texto adicional.'
)


class ExtraccionInvalida(ValueError):
    """El modelo no devolvió algo que podamos usar con confianza."""


@dataclass(frozen=True)
class Pedido:
    producto: str
    cantidad: int


def construir_prompt(mensaje: str) -> str:
    return f"{INSTRUCCION}\n\nMensaje del cliente: {mensaje}"


def extraer_pedido(mensaje: str, generar) -> Pedido:
    if not mensaje.strip():
        raise ExtraccionInvalida("el mensaje está vacío")

    respuesta = generar(construir_prompt(mensaje))

    try:
        datos = json.loads(respuesta)
    except json.JSONDecodeError as exc:
        raise ExtraccionInvalida(
            f"el modelo no devolvió JSON válido: {respuesta!r}"
        ) from exc

    if not isinstance(datos, dict) or set(datos) != {"producto", "cantidad"}:
        raise ExtraccionInvalida(f"claves inesperadas en la respuesta: {datos!r}")

    # BUG: se omite por completo la validación de la cantidad.
    return Pedido(producto=str(datos["producto"]), cantidad=datos["cantidad"])
