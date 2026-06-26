"""Ejercicio 2.11 — Extraer un pedido estructurado desde texto libre usando un LLM inyectado.

Este módulo es el SYSTEM UNDER TEST (SUT). Está CORRECTO. NO lo modifiques.
Tu trabajo es escribir la suite en `test_solucion.py`.

La llamada al LLM es la FRONTERA: no determinista, red, costo. Aquí se inyecta
como un callable `generar(prompt: str) -> str`, para poder testear sin red, sin
tokens y sin no-determinismo.

Tu suite verifica el CÓDIGO (construcción del prompt, parseo, validación, manejo
de error). NUNCA la calidad del modelo: que el modelo "extraiga bien" es un eval
(Fase 6), no un unit test.
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
    """Arma el prompt determinista que se enviará al modelo."""
    return f"{INSTRUCCION}\n\nMensaje del cliente: {mensaje}"


def extraer_pedido(mensaje: str, generar) -> Pedido:
    """Extrae un Pedido desde `mensaje` usando el callable `generar`.

    `generar(prompt) -> str` es la frontera (en producción, un LLM). El resto es
    lógica pura y determinista: validar entrada, construir prompt, parsear y
    validar la respuesta.
    """
    if not mensaje.strip():
        # Entrada inválida: ni siquiera vale la pena llamar al modelo.
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

    cantidad = datos["cantidad"]
    # bool es subclase de int en Python: True/False NO son cantidades válidas.
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        raise ExtraccionInvalida(f"cantidad inválida: {cantidad!r}")

    return Pedido(producto=str(datos["producto"]), cantidad=cantidad)


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que pasa ANTES de ejecutarlo?
    fake = lambda prompt: '{"producto": "café", "cantidad": 2}'  # noqa: E731
    print(extraer_pedido("quiero 2 cafés", fake))
