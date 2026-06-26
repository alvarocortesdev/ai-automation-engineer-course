"""
Tests del hook commit-msg.

Definen el CONTRATO antes de implementar (TDD): cada test invoca el script
`commit-msg` con un mensaje de ejemplo (escrito en un archivo temporal, igual
que hace Git) y verifica el código de salida.

    pytest            # desde la carpeta del ejercicio
    uv run pytest
"""

import subprocess
from pathlib import Path

import pytest

# El hook está un nivel arriba de tests/.
HOOK = Path(__file__).resolve().parents[1] / "commit-msg"


def run_hook(message: str, tmp_path: Path) -> int:
    """Ejecuta el hook con `message` y devuelve su código de salida."""
    msg_file = tmp_path / "COMMIT_EDITMSG"
    msg_file.write_text(message, encoding="utf-8")
    result = subprocess.run(
        ["bash", str(HOOK), str(msg_file)],
        capture_output=True,
        text=True,
    )
    return result.returncode


VALIDOS = [
    "feat: agrega comando de exportación",
    "fix(parser): corrige off-by-one en el índice",
    "docs: actualiza el README de instalación",
    "refactor!: renombra el módulo de almacenamiento",
    "chore(deps): sube pytest a 8.x",
    "perf(api)!: cachea la respuesta del catálogo",
]

INVALIDOS = [
    "arregla el bug del login",   # sin type
    "Feature: agrega algo",       # type inválido / con mayúscula
    "feat agrega algo",           # faltan los dos puntos
    "feat:",                      # sin descripción
    "actualizado",                # ni type ni ":"
    "",                           # mensaje vacío
]


def test_el_hook_existe():
    assert HOOK.exists(), f"No encuentro el hook en {HOOK}"


@pytest.mark.parametrize("msg", VALIDOS)
def test_mensajes_validos_pasan(msg, tmp_path):
    assert run_hook(msg, tmp_path) == 0, f"debería ACEPTAR: {msg!r}"


@pytest.mark.parametrize("msg", INVALIDOS)
def test_mensajes_invalidos_fallan(msg, tmp_path):
    assert run_hook(msg, tmp_path) != 0, f"debería RECHAZAR: {msg!r}"


def test_merge_autogenerado_no_se_bloquea(tmp_path):
    assert run_hook("Merge branch 'feature' into main", tmp_path) == 0


def test_revert_autogenerado_no_se_bloquea(tmp_path):
    assert run_hook('Revert "feat: algo que salió mal"', tmp_path) == 0


def test_ignora_lineas_de_comentario(tmp_path):
    # Git añade líneas '#' al final del editor; la cabecera real es la primera
    # línea no-comentario.
    mensaje = "# escribe tu mensaje arriba\nfeat: mensaje real\n# rama: main\n"
    assert run_hook(mensaje, tmp_path) == 0


def test_la_ayuda_va_a_stderr_no_a_stdout(tmp_path):
    msg_file = tmp_path / "COMMIT_EDITMSG"
    msg_file.write_text("mensaje invalido", encoding="utf-8")
    result = subprocess.run(
        ["bash", str(HOOK), str(msg_file)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert result.stderr.strip() != "", "el hook debe explicar el error en stderr"


# TODO (tú): añade aquí al menos un caso borde propio.
# Ideas: scope con guion `fix(date-utils): ...`; descripción muy larga;
# un type válido pero sin espacio tras los dos puntos `feat:x`.
