"""Caché semántico + router multi-modelo con cadena de fallback (esqueleto 8.5).

Completa los TODO. Regla de oro de testabilidad: NADA aquí llama a un LLM real ni a
la red. La función de embedding (`embed_fn`) y la de llamada al modelo (`call_fn`) se
INYECTAN, así los tests son deterministas (mismo input -> mismo output, sin sleep, sin
flakiness). Eso es exactamente lo que hace este código revisable y barato de testear.
"""

from __future__ import annotations

import math
from typing import Callable

UMBRAL_DEFECTO = 0.95


# --- Errores que simulan el comportamiento del proveedor del LLM -------------------

class ModeloSaturado(Exception):
    """Reintentable: el proveedor devolvió 429 (rate limit) o 5xx (caída/sobrecarga).

    Ante esto, la cadena de fallback debe PROBAR EL SIGUIENTE modelo.
    """


class RequestInvalido(Exception):
    """NO reintentable: el proveedor devolvió 400 (el request está mal armado).

    Ante esto, la cadena de fallback NO debe enmascarar el bug: el error se propaga.
    """


# --- Helper provisto: no es el objetivo de aprendizaje, ya está hecho --------------

def coseno(a: list[float], b: list[float]) -> float:
    """Similitud coseno entre dos vectores. Devuelve 0.0 si alguno es el vector cero."""
    punto = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return punto / (na * nb)


# --- Caché semántico ---------------------------------------------------------------

class SemanticCache:
    """Guarda respuestas indexadas por el embedding de la pregunta, AISLADAS por tenant.

    Un `get` devuelve una respuesta cacheada solo si existe, EN EL MISMO TENANT, una
    pregunta previa cuya similitud coseno con la nueva sea >= umbral. Si no, None.
    """

    def __init__(self, embed_fn: Callable[[str], list[float]], umbral: float = UMBRAL_DEFECTO) -> None:
        self.embed_fn = embed_fn
        self.umbral = umbral
        # TODO: inicializa el almacén de entradas. Sugerencia: una lista de tuplas
        #       (tenant_id, embedding, respuesta) basta para este ejercicio.
        ...

    def put(self, pregunta: str, tenant_id: str, respuesta: str) -> None:
        """Guarda (embedding de la pregunta, respuesta) para ese tenant."""
        # TODO: calcula el embedding de `pregunta` con self.embed_fn y guárdalo
        #       junto al tenant_id y la respuesta.
        raise NotImplementedError

    def get(self, pregunta: str, tenant_id: str) -> str | None:
        """Devuelve la respuesta cacheada si hay un vecino del MISMO tenant con
        similitud >= umbral; si no, None.
        """
        # TODO:
        #   1. embedding de `pregunta`
        #   2. entre las entradas del MISMO tenant_id, encuentra la de mayor similitud
        #   3. si esa similitud >= self.umbral, devuelve su respuesta; si no, None
        #   (si no hay entradas de ese tenant, es un miss -> None)
        raise NotImplementedError


# --- Router multi-modelo -----------------------------------------------------------

def elegir_modelo(tipo_tarea: str) -> str:
    """Rutea la tarea al modelo adecuado: la fácil al barato, la difícil al caro."""
    # TODO:
    #   - "clasificacion" | "saludo" | "extraccion_simple" -> "claude-haiku-4-5"
    #   - "sintesis_larga"                                  -> "claude-opus-4-8"
    #   - cualquier otra                                    -> "claude-sonnet-4-6"
    raise NotImplementedError


# --- Cadena de fallback ------------------------------------------------------------

def responder_con_fallback(
    call_fn: Callable[[str, list], str],
    cadena: list[str],
    messages: list,
) -> str:
    """Recorre la cadena de modelos llamando a call_fn(modelo, messages).

    - Si call_fn lanza ModeloSaturado (429/5xx): prueba el SIGUIENTE modelo.
    - Si call_fn lanza RequestInvalido (400): NO lo enmascares -> que se propague.
    - Si todos los modelos de la cadena se saturan: lanza RuntimeError.
    Procesa la cadena en orden y sin duplicados.
    """
    # TODO: implementa el recorrido con su manejo de errores.
    raise NotImplementedError
