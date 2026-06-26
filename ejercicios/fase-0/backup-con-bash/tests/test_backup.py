"""Tests del ejercicio — definen el contrato.

Ejecuta desde la carpeta del ejercicio:
    uv run pytest        # recomendado
    pytest

Necesitan `bash`, `tar` y `date` (presentes por defecto en macOS y Linux).
"""

import os
import subprocess
import tarfile
from pathlib import Path

EJERCICIO = Path(__file__).resolve().parent.parent
SCRIPT = EJERCICIO / "backup.sh"


def correr(args, env=None):
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_crea_targz_con_el_contenido(tmp_path):
    origen = tmp_path / "datos"
    origen.mkdir()
    (origen / "a.txt").write_text("hola")
    (origen / "b.txt").write_text("mundo")

    destino = tmp_path / "respaldos"
    destino.mkdir()

    env = {**os.environ, "BACKUP_DIR": str(destino)}
    r = correr([str(origen)], env=env)

    assert r.returncode == 0, f"el script falló: {r.stderr}"

    ruta = Path(r.stdout.strip())
    assert ruta.exists(), f"no se creó el archivo: {r.stdout!r}"
    assert ruta.name.endswith(".tar.gz"), f"nombre inesperado: {ruta.name}"
    assert ruta.parent == destino, "debe respetar BACKUP_DIR"

    with tarfile.open(ruta) as tf:
        nombres = tf.getnames()
    assert any(n.endswith("a.txt") for n in nombres), nombres
    assert any(n.endswith("b.txt") for n in nombres), nombres


def test_sin_argumento_falla():
    r = correr([])
    assert r.returncode != 0
    texto = (r.stderr + r.stdout).lower()
    assert "uso" in texto or "usage" in texto


def test_directorio_inexistente_falla(tmp_path):
    r = correr([str(tmp_path / "no-existe")])
    assert r.returncode != 0


# TODO(estudiante): añade un test tuyo. Por ejemplo, verifica que sin BACKUP_DIR
# el archivo aparece en la carpeta actual.
