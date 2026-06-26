"""TUS tests — este archivo es el entregable del ejercicio.

Testea `agenda.py` (provisto y correcto, NO lo modifiques). Aplica lo de la
sección 4.6 de la lección 1.6: tmp_path, fixtures propias, parametrize y raises.

Corre:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Cubre, como mínimo:
  - round-trip con tmp_path (guardar + cargar -> mismos datos),
  - archivo inexistente -> [],
  - archivo corrupto -> AgendaCorrupta (pytest.raises),
  - proximos() con @pytest.mark.parametrize (varios `hoy`),
  - una @pytest.fixture propia con eventos de ejemplo, reutilizada,
  - al menos UN caso borde tuyo.
"""

import pytest

from agenda import (
    AgendaCorrupta,
    cargar_eventos,
    guardar_eventos,
    proximos,
)


# --- Semilla: el round-trip con tmp_path. Imítala para el resto. ---
def test_guardar_y_cargar_es_round_trip(tmp_path):
    # Arrange: un dir temporal desechable que pytest borra solo.
    ruta = tmp_path / "agenda.json"
    eventos = [{"fecha": "2026-07-01", "titulo": "café con Ada"}]
    # Act
    guardar_eventos(ruta, eventos)
    # Assert
    assert cargar_eventos(ruta) == eventos


# TODO(estudiante): test de archivo inexistente -> cargar_eventos devuelve [].

# TODO(estudiante): test de archivo corrupto -> pytest.raises(AgendaCorrupta).
#   Pista: ruta.write_text("esto no es json {", encoding="utf-8")

# TODO(estudiante): @pytest.fixture llamada `eventos_demo` que devuelva una lista
#   de eventos, y úsala en al menos dos tests de proximos().

# TODO(estudiante): test parametrizado de proximos() con varios `hoy` y su esperado.
