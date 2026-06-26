"""Tests de aceptación del circuit breaker.

Deterministas: un reloj falso que avanzamos a mano, sin esperar de verdad.

Ejecuta:
    uv run pytest        # o: pytest

NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

import pytest

from solucion import CircuitBreaker, CircuitoAbierto


class _RelojFalso:
    """Reloj inyectable: avanza solo cuando tú lo dices."""

    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t

    def avanzar(self, segundos: float) -> None:
        self.t += segundos


class _FalloDependencia(Exception):
    pass


def _ok() -> str:
    return "ok"


def _falla() -> str:
    raise _FalloDependencia("la dependencia se cayó")


def _nuevo(umbral=3, espera=30.0):
    reloj = _RelojFalso()
    return CircuitBreaker(umbral_fallos=umbral, espera_apertura=espera, reloj=reloj), reloj


def test_arranca_cerrado():
    cb, _ = _nuevo()
    assert cb.estado == "closed"
    assert cb.llamar(_ok) == "ok"


def test_umbral_de_fallos_abre_el_circuito():
    cb, _ = _nuevo(umbral=3)
    for _ in range(3):
        with pytest.raises(_FalloDependencia):
            cb.llamar(_falla)
    assert cb.estado == "open"


def test_abierto_rechaza_sin_llamar_a_fn():
    cb, _ = _nuevo(umbral=2)
    for _ in range(2):
        with pytest.raises(_FalloDependencia):
            cb.llamar(_falla)
    assert cb.estado == "open"

    invocada = {"si": False}

    def fn():
        invocada["si"] = True
        return "no debería ejecutarse"

    with pytest.raises(CircuitoAbierto):
        cb.llamar(fn)
    assert invocada["si"] is False        # NO se invocó fn estando abierto


def test_tras_la_ventana_queda_half_open():
    cb, reloj = _nuevo(umbral=2, espera=30.0)
    for _ in range(2):
        with pytest.raises(_FalloDependencia):
            cb.llamar(_falla)
    assert cb.estado == "open"
    reloj.avanzar(30.0)
    assert cb.estado == "half-open"       # ya se permite una prueba


def test_prueba_exitosa_cierra_el_circuito():
    cb, reloj = _nuevo(umbral=2, espera=30.0)
    for _ in range(2):
        with pytest.raises(_FalloDependencia):
            cb.llamar(_falla)
    reloj.avanzar(30.0)
    assert cb.llamar(_ok) == "ok"         # prueba exitosa
    assert cb.estado == "closed"


def test_prueba_fallida_reabre_y_reinicia_temporizador():
    cb, reloj = _nuevo(umbral=2, espera=30.0)
    for _ in range(2):
        with pytest.raises(_FalloDependencia):
            cb.llamar(_falla)
    reloj.avanzar(30.0)
    assert cb.estado == "half-open"
    with pytest.raises(_FalloDependencia):
        cb.llamar(_falla)                 # la prueba falla
    assert cb.estado == "open"            # vuelve a abierto
    # y el temporizador se reinició: una llamada inmediata se rechaza
    with pytest.raises(CircuitoAbierto):
        cb.llamar(_ok)


def test_exito_reinicia_el_contador_de_fallos():
    cb, _ = _nuevo(umbral=3)
    with pytest.raises(_FalloDependencia):
        cb.llamar(_falla)
    with pytest.raises(_FalloDependencia):
        cb.llamar(_falla)                 # 2 fallos consecutivos (umbral 3)
    assert cb.llamar(_ok) == "ok"         # éxito: reinicia el contador
    assert cb.estado == "closed"
    # dos fallos más NO deberían abrir todavía (el contador volvió a 0)
    with pytest.raises(_FalloDependencia):
        cb.llamar(_falla)
    with pytest.raises(_FalloDependencia):
        cb.llamar(_falla)
    assert cb.estado == "closed"


# TODO(estudiante): añade un caso borde tuyo. Por ejemplo, umbral_fallos=1
# (un solo fallo abre) o varias pruebas half-open seguidas.
