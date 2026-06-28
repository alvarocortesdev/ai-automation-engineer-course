"""Tests del token bucket — definen el CONTRATO del ejercicio.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Fíjate que NINGÚN test usa time.sleep ni un reloj real: el tiempo se inyecta como
`ahora`. Eso es lo que hace que estos tests sean deterministas y rápidos.
"""

from rate_limiter import TokenBucket


def test_bucket_arranca_lleno_y_se_agota():
    b = TokenBucket(capacity=5, refill_rate=1.0, ahora=0.0)
    # 5 tokens disponibles en t=0 -> 5 permitidos
    assert [b.allow(0.0) for _ in range(5)] == [True] * 5
    # el 6º se rechaza: el bucket está vacío
    assert b.allow(0.0) is False


def test_recarga_por_tiempo_transcurrido():
    b = TokenBucket(capacity=5, refill_rate=1.0, ahora=0.0)
    for _ in range(5):
        b.allow(0.0)  # agota el bucket
    assert b.allow(0.0) is False
    # a t=2.0, con 1 token/s, se repusieron 2 tokens
    assert b.allow(2.0) is True
    assert b.allow(2.0) is True
    assert b.allow(2.0) is False


def test_tokens_no_superan_la_capacidad():
    b = TokenBucket(capacity=5, refill_rate=1.0, ahora=0.0)
    for _ in range(5):
        b.allow(0.0)  # vacío
    # pasa muchísimo tiempo: NO se acumulan 100 tokens; el tope es la capacidad (5)
    assert [b.allow(100.0) for _ in range(5)] == [True] * 5
    assert b.allow(100.0) is False


def test_parametro_cost():
    b = TokenBucket(capacity=10, refill_rate=1.0, ahora=0.0)
    assert b.allow(0.0, cost=4) is True   # quedan 6
    assert b.allow(0.0, cost=7) is False  # 6 < 7: no alcanza y NO consume
    assert b.allow(0.0, cost=6) is True   # 6 >= 6: ok, quedan 0
    assert b.allow(0.0, cost=1) is False  # vacío


def test_recarga_fraccionaria():
    b = TokenBucket(capacity=10, refill_rate=2.0, ahora=0.0)
    for _ in range(10):
        b.allow(0.0)  # vacío
    assert b.allow(0.0) is False
    # a t=0.5, con 2 tokens/s, se repuso 1.0 token
    assert b.allow(0.5) is True
    assert b.allow(0.5) is False


def test_reloj_no_retrocede():
    b = TokenBucket(capacity=5, refill_rate=1.0, ahora=10.0)
    for _ in range(5):
        b.allow(10.0)  # vacío en t=10
    # un `ahora` anterior no debe recargar (ni reventar)
    assert b.allow(5.0) is False


# TODO(estudiante): añade al menos un caso borde tuyo. Ideas:
#   - un cost mayor que la capacidad nunca se concede, ni con el bucket lleno.
#   - allow repetido en el MISMO instante no recarga (la recarga necesita tiempo > 0).
# def test_mi_caso_borde():
#     ...
