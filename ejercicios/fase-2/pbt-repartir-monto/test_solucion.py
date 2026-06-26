"""Tests del ejercicio 2.8 — repartir_monto.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Esta suite trae:
  1. Tests de EJEMPLO (abajo): definen el contrato con casos concretos y legibles.
     Implementa `repartir_monto` en solucion.py hasta dejarlos en VERDE.
  2. Un hueco para tus PROPERTY-BASED TESTS con Hypothesis (la parte central del
     ejercicio). Instala Hypothesis: `uv add --dev hypothesis` o `pip install hypothesis`.

La filosofia: los ejemplos comunican la intencion; las propiedades cazan los bordes.
"""

import pytest

from solucion import repartir_monto


# ---------------------------------------------------------------------------
# 1) Tests de EJEMPLO (provistos). No los borres: documentan el contrato.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "total, partes, esperado",
    [
        (100, 4, [25, 25, 25, 25]),   # reparto exacto
        (101, 4, [26, 25, 25, 25]),   # el resto (1) va a la primera parte
        (10, 3, [4, 3, 3]),           # el resto (1) -> primera; piso 3
        (0, 3, [0, 0, 0]),            # total cero
        (10, 1, [10]),                # una sola parte
        (7, 7, [1, 1, 1, 1, 1, 1, 1]),# cada parte recibe 1
    ],
)
def test_ejemplos_de_reparto(total, partes, esperado):
    assert repartir_monto(total, partes) == esperado


def test_partes_invalidas_lanzan_valueerror():
    with pytest.raises(ValueError):
        repartir_monto(100, 0)


# ---------------------------------------------------------------------------
# 2) TUS PROPERTY-BASED TESTS (Hypothesis).  <-- la parte central del ejercicio.
#
# Descomenta el import y escribe al menos TRES propiedades. Guia:
#
#   from hypothesis import given, strategies as st
#
#   montos = st.integers(min_value=0, max_value=10**9)
#   cuantas = st.integers(min_value=1, max_value=1000)
#
#   @given(montos, cuantas)
#   def test_la_suma_se_conserva(total, partes):
#       # P1 — conservacion: el reparto no pierde ni inventa plata.
#       assert ...  # <- tu invariante, NO una copia del algoritmo
#
#   # P2 — equidad:  max(resultado) - min(resultado) <= 1
#   # P3 — cantidad: len(resultado) == partes
#
# Recuerda: una propiedad afirma una RELACION que vale siempre, no un valor fijo.
# Evita la tautologia (reimplementar la funcion dentro del assert).
# ---------------------------------------------------------------------------

# TODO(estudiante): escribe aqui tus property-based tests.
