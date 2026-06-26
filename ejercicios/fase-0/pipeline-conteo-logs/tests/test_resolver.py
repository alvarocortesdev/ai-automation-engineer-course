"""Tests del ejercicio — definen el contrato.

Ejecuta desde la carpeta del ejercicio:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Los tests invocan tu script con bash, así que necesitan `bash`, `awk`, `sort` y
`uniq` (presentes por defecto en macOS y Linux).
"""

import subprocess
from pathlib import Path

# La carpeta del ejercicio es la PADRE de tests/.
EJERCICIO = Path(__file__).resolve().parent.parent
SCRIPT = EJERCICIO / "resolver.sh"
LOG = EJERCICIO / "acceso.log"

# Conteos del fixture acceso.log:
#   192.168.1.10 -> 5,  10.0.0.5 -> 3,  203.0.113.7 -> 2,  198.51.100.2 -> 1
ESPERADO = [
    "5 192.168.1.10",
    "3 10.0.0.5",
    "2 203.0.113.7",
]


def correr(*args):
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


def test_top_3_ips():
    r = correr(str(LOG))
    assert r.returncode == 0, f"el script falló: {r.stderr}"
    lineas = r.stdout.split("\n")
    lineas = [ln.strip() for ln in lineas if ln.strip()]
    assert lineas == ESPERADO


def test_sin_argumento_falla():
    # Sin log que procesar, el script debe terminar con código != 0
    # (no quedarse colgado ni devolver 0 con salida vacía).
    r = correr()
    assert r.returncode != 0


# TODO(estudiante): añade un test tuyo. Por ejemplo, crea un log mínimo en un
# tmp_path con conteos que tú decidas y verifica el top 3.
