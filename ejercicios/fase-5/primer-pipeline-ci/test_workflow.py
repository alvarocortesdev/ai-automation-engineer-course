"""Test ESTRUCTURAL de tu workflow de CI.

No corre tu pipeline en GitHub (no hace falta): parsea el YAML que escribiste en
`.github/workflows/ci.yml` y verifica que tenga la forma correcta. Es tu "spec"
del workflow — léelo: cada assert te dice exactamente qué se espera y por qué.

Requisito: pyyaml. Si no lo tienes:
    uv add --dev pyyaml      # o:  pip install pyyaml
Correr:
    uv run pytest test_workflow.py    # o:  pytest test_workflow.py
"""

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml", reason="Instala pyyaml: uv add --dev pyyaml")

WORKFLOW = Path(__file__).parent / ".github" / "workflows" / "ci.yml"


def cargar():
    assert WORKFLOW.exists(), (
        f"No encuentro {WORKFLOW}. Crea el archivo .github/workflows/ci.yml "
        "dentro de la carpeta del ejercicio."
    )
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "El YAML no es un mapeo válido en el nivel superior."
    return data


def bloque_on(data):
    # Gotcha de YAML 1.1: la clave 'on' se parsea como el booleano True.
    # Por eso aceptamos ambas representaciones.
    if True in data:
        return data[True]
    return data.get("on")


def steps_del_job_test(data):
    jobs = data.get("jobs")
    assert isinstance(jobs, dict), "Falta el bloque 'jobs:' (un mapeo de jobs)."
    assert "test" in jobs, "Debe existir un job llamado 'test'."
    job = jobs["test"]
    assert job.get("runs-on") == "ubuntu-latest", (
        "El job 'test' debe correr en 'ubuntu-latest'."
    )
    steps = job.get("steps")
    assert isinstance(steps, list) and steps, "El job 'test' necesita una lista de steps."
    return steps


def test_triggers_push_y_pull_request():
    data = cargar()
    on = bloque_on(data)
    assert on is not None, "Falta el bloque 'on:' que define los triggers."
    assert "pull_request" in on, (
        "Debe dispararse en 'pull_request' (el check que condiciona el merge)."
    )
    assert "push" in on, "Debe dispararse también en 'push' a main."
    push = on["push"]
    assert isinstance(push, dict) and "main" in (push.get("branches") or []), (
        "El trigger 'push' debe limitarse a la rama main (branches: [main])."
    )


def test_permisos_minimos():
    data = cargar()
    perms = data.get("permissions")
    assert isinstance(perms, dict) and perms.get("contents") == "read", (
        "Declara 'permissions: { contents: read }' (mínimo privilegio)."
    )


def test_orden_de_steps():
    data = cargar()
    steps = steps_del_job_test(data)

    def idx(predicado, descripcion):
        for i, s in enumerate(steps):
            uses = (s.get("uses") or "")
            run = (s.get("run") or "")
            if predicado(uses, run):
                return i
        raise AssertionError(f"No encontré el step: {descripcion}")

    i_checkout = idx(lambda u, r: u.startswith("actions/checkout"), "checkout del repo")
    i_setup = idx(lambda u, r: u.startswith("astral-sh/setup-uv"), "setup-uv")
    i_sync = idx(lambda u, r: "uv sync" in r and "--frozen" in r,
                 "uv sync --frozen (instalar desde el lockfile)")
    i_lint = idx(lambda u, r: "ruff" in r, "lint con ruff")
    i_test = idx(lambda u, r: "pytest" in r, "tests con pytest")

    assert i_checkout == 0, "El 'checkout' debe ser el PRIMER step (el runner arranca vacío)."
    assert i_checkout < i_setup < i_sync, "Orden: checkout -> setup-uv -> uv sync --frozen."
    assert i_sync < i_lint, "Instala las deps ANTES de lintear."
    assert i_lint < i_test, "Lint antes de test (feedback más rápido y barato)."


def test_actions_pineadas_a_version():
    data = cargar()
    steps = steps_del_job_test(data)
    for s in steps:
        uses = s.get("uses")
        if not uses:
            continue
        assert "@" in uses, f"La action '{uses}' no está pineada (falta @version)."
        ref = uses.split("@", 1)[1]
        prohibido = {"main", "master", "latest", "develop"}
        assert ref not in prohibido, (
            f"'{uses}' está pineada a una rama móvil ('{ref}'). Usa un tag de "
            "versión (@v7, @v8...) o un commit SHA. Nunca @main en una action ajena."
        )
