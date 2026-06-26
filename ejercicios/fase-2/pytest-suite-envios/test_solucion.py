"""Tu suite de tests va AQUÍ. El SUT (`solucion.py`) ya funciona; no lo toques.

Objetivo: escribir una suite que (a) verifique `costo_envio` con parametrize y
bordes, (b) cubra el error con pytest.raises, (c) use una fixture para el doble
de `tasa_usd`, y (d) teste `cotizar` mockeando SOLO la frontera (`tasa_usd`),
nunca `costo_envio`.

Corre:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Autochequeo (cuando tu suite esté verde): cambia el import de abajo por
`from mutantes.mutante_a import costo_envio, cotizar`, corre pytest y confirma
que tu suite se pone ROJA. Repite con `mutante_b`. Luego REVIERTE el import.
"""

import pytest

from solucion import costo_envio, cotizar


# ─────────────────────────────────────────────────────────────────────────────
# 1) costo_envio con parametrize. Piensa la tabla como una mini-especificación:
#    incluye al menos un BORDE no obvio (peso entero vs. con decimales), una
#    zona remota y un caso de socio.
# ─────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize(
    "peso_kg, zona, es_socio, esperado",
    [
        # TODO: completa al menos 5 filas. Calcula el `esperado` a mano leyendo
        #       el SUT (no lo adivines: ese es el punto del Primero-Sin-IA).
        # (2.0, "metropolitana", False, ____),
    ],
)
def test_costo_envio(peso_kg, zona, es_socio, esperado):
    assert costo_envio(peso_kg, zona, es_socio) == pytest.approx(esperado)


# ─────────────────────────────────────────────────────────────────────────────
# 2) El comportamiento de ERROR también se testea (peso_kg <= 0).
# ─────────────────────────────────────────────────────────────────────────────
def test_peso_invalido_lanza_value_error():
    ...  # TODO: usa `with pytest.raises(ValueError, match="...")`


# ─────────────────────────────────────────────────────────────────────────────
# 3) Fixture para el doble de la frontera `tasa_usd`.
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture
def tasa_usd():
    ...  # TODO: devuelve un doble. ¿Un `lambda: 950` (stub) o un Mock para
    #            poder afirmar que se llamó? Decide según lo que quieras verificar.


# ─────────────────────────────────────────────────────────────────────────────
# 4) cotizar: mockea SOLO la frontera (`tasa_usd`), deja `costo_envio` REAL.
# ─────────────────────────────────────────────────────────────────────────────
def test_cotizar_convierte_a_usd(tasa_usd):
    ...  # TODO: afirma el resultado en USD y, si tu fixture lo permite, que la
    #            tasa se consultó. NO mockees costo_envio.
