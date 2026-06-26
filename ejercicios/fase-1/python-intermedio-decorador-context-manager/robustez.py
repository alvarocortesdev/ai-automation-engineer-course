"""Ejercicio 1.2 — Decorador de reintento y context manager (Primero-Sin-IA).

Completa `reintentar` y `conexion`. NO cambies sus firmas: los tests dependen de ellas.

Corre los tests con:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import functools
from contextlib import contextmanager


def reintentar(veces: int):
    """Decorador PARAMETRIZADO: reintenta la función hasta `veces` veces.

    Comportamiento:
      - Si una llamada a la función tiene éxito, devuelve su resultado.
      - Si lanza una excepción, la reintenta (hasta `veces` intentos en total).
      - Si TODAS fallan, re-lanza la ÚLTIMA excepción.
      - La función decorada debe conservar su __name__ (usa functools.wraps).

    Uso:
        @reintentar(veces=3)
        def llamar_api():
            ...

    Pista de estructura: tres niveles anidados
        reintentar(veces) -> decorador(func) -> envoltura(*args, **kwargs)
    """
    # TODO(estudiante): borra esto y escribe los tres niveles a mano, sin IA.
    raise NotImplementedError("Implementa reintentar como decorador parametrizado")


@contextmanager
def conexion(registro: list):
    """Context manager: registra apertura y cierre de un recurso simulado.

    Comportamiento:
      - Al ENTRAR al `with`: agrega "conectado" a `registro` y entrega `registro`
        (es lo que recibe el `as ...`).
      - Al SALIR del `with`: agrega "desconectado" a `registro` SIEMPRE, incluso si
        el bloque lanzó una excepción.
      - Si el bloque lanza una excepción, esta debe PROPAGARSE (no se traga).

    Uso:
        log = []
        with conexion(log) as recurso:
            ...   # recurso es la misma lista `log`
        # aquí log == ["conectado", "desconectado"]

    Pista: lo que va antes del `yield` es el setup; lo del `finally` tras el `yield`
    es el teardown que corre siempre.
    """
    # TODO(estudiante): borra esto y escribe el setup/yield/finally a mano, sin IA.
    raise NotImplementedError("Implementa conexion con @contextmanager (yield + finally)")
    yield  # noqa: marca a Python que esto es un generador; reemplázalo por tu solución


if __name__ == "__main__":
    # Predict–Run: ¿cuántas veces se imprime "intento" ANTES de correrlo?
    intentos = {"n": 0}

    @reintentar(veces=3)
    def inestable():
        intentos["n"] += 1
        print(f"intento {intentos['n']}")
        if intentos["n"] < 2:
            raise RuntimeError("falló")
        return "ok"

    print(inestable())

    log: list = []
    with conexion(log) as recurso:
        recurso.append("trabajando")
    print(log)
