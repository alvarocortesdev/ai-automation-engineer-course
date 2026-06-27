"""Ejercicio 6.2 — Token budget.

Completa `armar_contexto`. La idea es decidir qué cabe en la ventana de contexto
cuando el historial crece, sin depender de ninguna API: el contador de tokens se
inyecta como el parámetro `contar`.

Política a implementar:
  1. El `system` es obligatorio y va primero (nunca se descarta).
  2. Si el `system` solo ya excede el presupuesto -> ValueError.
  3. Se conservan los turnos MÁS RECIENTES que quepan en lo que sobra.
  4. Un turno entra entero o no entra (nunca se parte).
  5. La salida mantiene el orden cronológico (más viejo primero).
"""

from __future__ import annotations

from typing import Callable


def armar_contexto(
    system: str,
    historial: list[dict],
    presupuesto_tokens: int,
    contar: Callable[[str], int],
) -> dict:
    """Arma {"system": ..., "messages": [...]} que cabe en el presupuesto.

    Pasos sugeridos (piénsalos antes de escribir):
      1. Cuenta el costo del `system`. Si excede el presupuesto, lanza ValueError.
      2. Recorre el historial del MÁS RECIENTE al más viejo, sumando turnos que
         quepan en lo que resta del presupuesto. Corta cuando uno ya no cabe.
      3. Restaura el orden cronológico antes de devolver.
    """
    # TODO: implementa la función.
    raise NotImplementedError("Completa armar_contexto")


def palabras(texto: str) -> int:
    """Contador de tokens de juguete: cuenta palabras. Útil para experimentar.

    En producción usarías el conteo real del proveedor (p. ej. la API de token
    counting de Anthropic), no este. Aquí basta para ver la lógica.
    """
    return len(texto.split())


if __name__ == "__main__":
    # Pequeño explorador manual. Ejecuta:  python presupuesto.py
    system = " ".join(["sys"] * 5)
    historial = [
        {"role": "user", "content": " ".join(["t0"] * 10)},
        {"role": "assistant", "content": " ".join(["t1"] * 10)},
        {"role": "user", "content": " ".join(["t2"] * 10)},
        {"role": "assistant", "content": " ".join(["t3"] * 10)},
        {"role": "user", "content": " ".join(["t4"] * 10)},
    ]
    try:
        ctx = armar_contexto(system, historial, 35, palabras)
        print("incluidos:", [m["content"].split()[0] for m in ctx["messages"]])
    except NotImplementedError:
        print("aún sin implementar")
