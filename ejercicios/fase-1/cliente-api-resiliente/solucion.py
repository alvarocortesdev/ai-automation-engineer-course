"""Starter del ejercicio — Primero-Sin-IA.

Implementa `nombre_de_usuario` a mano, sin IA. NO cambies su firma: los tests de
`test_solucion.py` dependen de ella. Las excepciones de dominio ya están definidas.

La clave del ejercicio: `fetch` está INYECTADO. Tu función no sabe (ni le importa)
de dónde viene la respuesta — solo decide qué hacer con ella. Eso la hace testeable
sin tocar la red. Lee la sección 4.8 de la lección si te trabas.
"""

from __future__ import annotations

from typing import Any, Callable, Protocol


class Respuesta(Protocol):
    """Lo MÍNIMO que tu función necesita de una respuesta HTTP.

    Tanto una respuesta real de httpx como la respuesta falsa de los tests
    cumplen este contrato: tienen `.status_code` y un método `.json()`.
    """

    status_code: int

    def json(self) -> Any: ...


# `fetch` recibe un user_id y devuelve algo que cumple el Protocol Respuesta.
Fetch = Callable[[int], Respuesta]


class ServicioInalcanzable(Exception):
    """No hubo respuesta: error de red (timeout, conexión rechazada, sin internet)."""


class UsuarioNoEncontrado(Exception):
    """El servidor respondió 404: el usuario no existe."""


class ServicioCaido(Exception):
    """El servidor respondió 5xx: falló del lado del servidor."""


class RespuestaInesperada(Exception):
    """El servidor respondió con un status que no sabemos manejar."""


def nombre_de_usuario(user_id: int, fetch: Fetch) -> str:
    """Devuelve el nombre del usuario, manejando cada modo de fallo.

    Ver el contrato completo en el README.md de este ejercicio.
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Demostración con un `fetch` falso (sin red). Predice qué imprime antes de correr.
    class _RespFalsa:
        def __init__(self, status_code: int, payload: Any) -> None:
            self.status_code = status_code
            self._payload = payload

        def json(self) -> Any:
            return self._payload

    def fetch_demo(user_id: int) -> _RespFalsa:
        return _RespFalsa(200, {"name": "Ada Lovelace"})

    print(nombre_de_usuario(1, fetch_demo))
