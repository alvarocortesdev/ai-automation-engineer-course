"""Tests del ejercicio — definen el contrato.

Ejecuta desde la carpeta del ejercicio:
    uv run pytest        # recomendado
    pytest

Necesitan `bash` y `jq`. Si jq no está instalado, el test principal se salta
(skip) con un aviso; instálalo con `brew install jq` o `sudo apt install jq`.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

EJERCICIO = Path(__file__).resolve().parent.parent
SCRIPT = EJERCICIO / "consulta.sh"
JSON = EJERCICIO / "usuarios.json"

# Activos con logins > 5: Ana (42) y Carla (17). Eva (5) queda fuera por el ">"
# estricto; Diego (0) por pocos logins; Beto por inactivo.
ESPERADO = ["Ana", "Carla"]


def correr(*args):
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


@pytest.mark.skipif(shutil.which("jq") is None, reason="jq no está instalado")
def test_activos_con_mas_de_5_logins():
    r = correr(str(JSON))
    assert r.returncode == 0, f"el script falló: {r.stderr}"
    # .split() ignora el salto final y conserva el orden de aparición.
    assert r.stdout.split() == ESPERADO


def test_sin_argumento_falla():
    r = correr()
    assert r.returncode != 0


# TODO(estudiante): añade un test tuyo. Por ejemplo, un JSON donde nadie cumpla
# la condición y la salida deba ser vacía.
