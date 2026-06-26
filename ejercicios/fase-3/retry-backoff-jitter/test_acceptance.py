"""Tests de aceptación del reintento con backoff + jitter.

Deterministas y rápidos: NO duermen de verdad. Inyectamos `dormir` (que solo
registra cuánto se habría dormido) y `aleatorio` (con un valor fijo) para poder
afirmar la secuencia exacta de esperas.

Ejecuta:
    uv run pytest        # o: pytest

NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

import pytest

from solucion import ErrorPermanente, ErrorTransitorio, reintentar


class _SpyDormir:
    """Registra las esperas en vez de dormir de verdad."""

    def __init__(self) -> None:
        self.esperas: list[float] = []

    def __call__(self, segundos: float) -> None:
        self.esperas.append(segundos)


def _fn_que_falla(n_fallos: int, exc: type[Exception]):
    """Devuelve una fn que falla las primeras `n_fallos` veces y luego retorna 'ok'."""
    estado = {"llamadas": 0}

    def fn() -> str:
        estado["llamadas"] += 1
        if estado["llamadas"] <= n_fallos:
            raise exc("fallo simulado")
        return "ok"

    fn.estado = estado  # type: ignore[attr-defined]
    return fn


def test_exito_al_primer_intento_no_duerme():
    dormir = _SpyDormir()
    fn = _fn_que_falla(0, ErrorTransitorio)
    assert reintentar(fn, dormir=dormir, aleatorio=lambda: 1.0) == "ok"
    assert fn.estado["llamadas"] == 1
    assert dormir.esperas == []


def test_falla_dos_veces_y_luego_acierta():
    dormir = _SpyDormir()
    fn = _fn_que_falla(2, ErrorTransitorio)
    assert reintentar(fn, dormir=dormir, aleatorio=lambda: 1.0) == "ok"
    assert fn.estado["llamadas"] == 3        # 2 fallos + 1 acierto
    assert len(dormir.esperas) == 2          # durmió antes de cada reintento


def test_error_permanente_se_propaga_sin_reintentar():
    dormir = _SpyDormir()
    fn = _fn_que_falla(99, ErrorPermanente)
    with pytest.raises(ErrorPermanente):
        reintentar(fn, dormir=dormir, aleatorio=lambda: 1.0)
    assert fn.estado["llamadas"] == 1        # NO reintenta lo permanente
    assert dormir.esperas == []


def test_agota_intentos_y_relanza_transitorio():
    dormir = _SpyDormir()
    fn = _fn_que_falla(99, ErrorTransitorio)
    with pytest.raises(ErrorTransitorio):
        reintentar(fn, max_intentos=4, dormir=dormir, aleatorio=lambda: 1.0)
    assert fn.estado["llamadas"] == 4        # 4 intentos totales
    assert len(dormir.esperas) == 3          # durmió entre cada par


def test_backoff_exponencial_respeta_el_tope():
    # aleatorio()=1.0 -> full jitter devuelve el delay completo (max(tope, base*2^n)).
    dormir = _SpyDormir()
    fn = _fn_que_falla(99, ErrorTransitorio)
    with pytest.raises(ErrorTransitorio):
        reintentar(
            fn, max_intentos=5, base=2.0, tope=3.0,
            dormir=dormir, aleatorio=lambda: 1.0,
        )
    # delays: n=0 -> 2; n=1 -> 4 (cap 3); n=2 -> 8 (cap 3); n=3 -> 16 (cap 3)
    assert dormir.esperas == [2.0, 3.0, 3.0, 3.0]


def test_jitter_acota_la_espera_por_debajo_del_delay():
    # aleatorio()=0.0 -> la espera siempre es 0 (full jitter en su mínimo).
    dormir = _SpyDormir()
    fn = _fn_que_falla(99, ErrorTransitorio)
    with pytest.raises(ErrorTransitorio):
        reintentar(fn, max_intentos=3, dormir=dormir, aleatorio=lambda: 0.0)
    assert dormir.esperas == [0.0, 0.0]


# TODO(estudiante): añade un caso borde tuyo. Por ejemplo, max_intentos=1
# (no debería reintentar nunca) o varias excepciones en `transitorias`.
