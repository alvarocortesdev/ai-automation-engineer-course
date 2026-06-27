"""Tests para reintentar_con_backoff.

Estrategia: `dormir` y `aleatorio` se inyectan, así verificamos la POLÍTICA
(cuántas esperas, de qué tamaño, qué se reintenta) de forma determinista y sin red
ni tiempo real. `SIN_JITTER` devuelve 0 para que las esperas sean exactas.
"""

import pytest

from backoff import ErrorReintentable, reintentar_con_backoff


def _grabador():
    """Devuelve (dormir, esperas): `dormir` registra cada espera en la lista `esperas`."""
    esperas: list[float] = []

    def dormir(segundos: float) -> None:
        esperas.append(segundos)

    return dormir, esperas


SIN_JITTER = lambda base: 0.0  # jitter determinista = 0 -> esperas exactas


def test_exito_al_primer_intento_no_duerme():
    dormir, esperas = _grabador()
    llamadas = {"n": 0}

    def op():
        llamadas["n"] += 1
        return "ok"

    assert reintentar_con_backoff(op, dormir=dormir, aleatorio=SIN_JITTER) == "ok"
    assert llamadas["n"] == 1
    assert esperas == []


def test_exito_al_tercer_intento():
    dormir, esperas = _grabador()
    llamadas = {"n": 0}

    def op():
        llamadas["n"] += 1
        if llamadas["n"] < 3:
            raise ErrorReintentable("429")
        return "ok"

    assert reintentar_con_backoff(op, base=1.0, dormir=dormir, aleatorio=SIN_JITTER) == "ok"
    assert llamadas["n"] == 3
    # falló en i=0 (espera 1) y en i=1 (espera 2); al 3er intento (i=2) tuvo éxito
    assert esperas == [1.0, 2.0]


def test_backoff_exponencial_respeta_tope():
    dormir, esperas = _grabador()

    def op():
        raise ErrorReintentable("siempre falla")

    with pytest.raises(ErrorReintentable):
        reintentar_con_backoff(
            op, max_intentos=6, base=1.0, tope=8.0, dormir=dormir, aleatorio=SIN_JITTER
        )
    # i = 0..4 duermen (el 6º intento, i=5, no duerme): base*2**i = 1,2,4,8,16
    # con tope 8 -> 1,2,4,8,8
    assert esperas == [1.0, 2.0, 4.0, 8.0, 8.0]


def test_retry_after_gana_sobre_el_backoff():
    dormir, esperas = _grabador()
    llamadas = {"n": 0}

    def op():
        llamadas["n"] += 1
        if llamadas["n"] == 1:
            raise ErrorReintentable("429", retry_after=7.5)
        return "ok"

    # jitter enorme: NO debe aplicarse cuando hay Retry-After
    reintentar_con_backoff(op, base=1.0, dormir=dormir, aleatorio=lambda b: 999.0)
    assert esperas == [7.5]


def test_error_no_reintentable_se_propaga_de_inmediato():
    dormir, esperas = _grabador()

    def op():
        raise ValueError("request inválido (400)")

    with pytest.raises(ValueError):
        reintentar_con_backoff(op, dormir=dormir, aleatorio=SIN_JITTER)
    assert esperas == []  # no durmió: no reintentó


def test_agota_intentos_relanza_ultima():
    dormir, esperas = _grabador()
    llamadas = {"n": 0}

    def op():
        llamadas["n"] += 1
        raise ErrorReintentable(f"fallo {llamadas['n']}")

    with pytest.raises(ErrorReintentable):
        reintentar_con_backoff(op, max_intentos=3, dormir=dormir, aleatorio=SIN_JITTER)
    assert llamadas["n"] == 3   # 3 intentos
    assert len(esperas) == 2    # 2 esperas (entre los 3 intentos)


def test_jitter_se_suma_al_backoff_calculado():
    dormir, esperas = _grabador()
    llamadas = {"n": 0}

    def op():
        llamadas["n"] += 1
        if llamadas["n"] < 2:
            raise ErrorReintentable("429")
        return "ok"

    # jitter fijo = 0.5 * base
    reintentar_con_backoff(op, base=2.0, dormir=dormir, aleatorio=lambda b: 0.5 * b)
    # i=0: base_i = min(60, 2*1) = 2 ; espera = 2 + 0.5*2 = 3
    assert esperas == [3.0]
