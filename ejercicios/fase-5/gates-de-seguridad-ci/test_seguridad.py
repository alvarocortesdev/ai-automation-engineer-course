"""Test ESTRUCTURAL de tu pipeline endurecido.

Valida la FORMA de `.github/workflows/ci.yml` y `.github/dependabot.yml`:
permisos mínimos, actions pineadas a SHA, gate de SCA, gate de secret-scanning, y un
dependabot.yml válido. No corre nada en GitHub ni descarga CVEs: solo parsea YAML.

NOTA: no verifica que el SHA sea el real de esa versión (no tiene red). Solo exige que
sea un hash de 40 hex y NO un tag (@v4) ni una rama (@main): eso es lo que te inmuniza
del tag hijacking.

Requisito: pyyaml  ->  uv add --dev pyyaml   (o: pip install pyyaml)
Correr:    uv run pytest test_seguridad.py
"""

import re
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml", reason="Instala pyyaml: uv add --dev pyyaml")

RAIZ = Path(__file__).parent
WORKFLOW = RAIZ / ".github" / "workflows" / "ci.yml"
DEPENDABOT = RAIZ / ".github" / "dependabot.yml"

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def cargar(path):
    assert path.exists(), f"No encuentro {path.relative_to(RAIZ)}. Créalo."
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{path.name} no es un mapeo YAML válido."
    return data


def jobs(data):
    js = data.get("jobs")
    assert isinstance(js, dict), "Falta el bloque 'jobs:' en ci.yml."
    return js


def steps_de(job):
    return job.get("steps") or []


def todos_los_uses(data):
    """Devuelve [(nombre_job, ref_uses)] de cada step con 'uses:'."""
    out = []
    for nombre, job in jobs(data).items():
        for s in steps_de(job):
            u = s.get("uses")
            if u:
                out.append((nombre, u))
    return out


# --- 1. Mínimo privilegio -----------------------------------------------------

def test_permisos_minimos_a_nivel_global():
    data = cargar(WORKFLOW)
    perms = data.get("permissions")
    assert isinstance(perms, dict), (
        "Falta un bloque 'permissions:' a nivel global. Declara al menos 'contents: read'."
    )
    assert perms.get("contents") == "read", (
        "El permiso global debe ser mínimo: 'contents: read'. "
        "Sube permisos puntuales solo en el job que los necesite (p. ej. security-events: write)."
    )


# --- 2. Pin a SHA (no tags, no ramas) -----------------------------------------

def test_todas_las_actions_pineadas_a_sha():
    data = cargar(WORKFLOW)
    usos = todos_los_uses(data)
    assert usos, "No hay ninguna action ('uses:') en el workflow."
    malas = []
    for nombre_job, u in usos:
        ref = u.rsplit("@", 1)[-1] if "@" in u else ""
        if not SHA_RE.match(ref):
            malas.append(f"  job '{nombre_job}': {u}")
    assert not malas, (
        "Estas actions NO están pineadas a un commit SHA (40 hex). Un tag (@v4) o una rama "
        "(@main) son MUTABLES: el ataque de Trivy (marzo 2026) movió tags a malware.\n"
        + "\n".join(malas)
    )


# --- 3. Gate de SCA (dependency scanning) -------------------------------------

def test_existe_gate_de_sca():
    data = cargar(WORKFLOW)
    tiene_pip_audit = False
    tiene_dep_review = False
    for _, job in jobs(data).items():
        for s in steps_de(job):
            run = str(s.get("run") or "")
            if "pip-audit" in run:
                tiene_pip_audit = True
            if str(s.get("uses") or "").startswith("actions/dependency-review-action"):
                tiene_dep_review = True
    assert tiene_pip_audit or tiene_dep_review, (
        "Falta el gate de SCA. Añade un step con `uvx pip-audit` (escanea el árbol "
        "instalado) o el actions/dependency-review-action (revisa los cambios del PR)."
    )


# --- 4. Gate de secret-scanning -----------------------------------------------

def test_existe_gate_de_secret_scanning_con_historial_completo():
    data = cargar(WORKFLOW)
    job_gitleaks = None
    for _, job in jobs(data).items():
        if any(str(s.get("uses") or "").startswith("gitleaks/gitleaks-action") for s in steps_de(job)):
            job_gitleaks = job
            break
    assert job_gitleaks is not None, (
        "Falta el gate de secret-scanning. Añade un job con gitleaks/gitleaks-action."
    )
    # gitleaks necesita el historial completo: el checkout de ese job debe usar fetch-depth: 0
    fetch_depth_ok = False
    for s in steps_de(job_gitleaks):
        if str(s.get("uses") or "").startswith("actions/checkout"):
            with_ = s.get("with") or {}
            if str(with_.get("fetch-depth")) == "0":
                fetch_depth_ok = True
    assert fetch_depth_ok, (
        "El job de gitleaks debe hacer checkout con 'fetch-depth: 0' para escanear TODO el "
        "historial; sin eso solo ve el último commit."
    )


# --- 5. Dependabot ------------------------------------------------------------

def test_dependabot_version_2_con_ecosistemas_y_groups():
    data = cargar(DEPENDABOT)
    assert data.get("version") == 2, "dependabot.yml debe declarar 'version: 2'."
    updates = data.get("updates")
    assert isinstance(updates, list) and updates, "Falta la lista 'updates:' en dependabot.yml."
    ecosistemas = {str(u.get("package-ecosystem")) for u in updates}
    for eco in ("github-actions", "pip"):
        assert eco in ecosistemas, (
            f"dependabot.yml debe cubrir el ecosistema '{eco}'. "
            "Mantener actualizado github-actions es lo que sube tus pins de SHA sin que te quedes "
            "con CVEs sin parchar."
        )
    tiene_groups = any(isinstance(u.get("groups"), dict) and u.get("groups") for u in updates)
    assert tiene_groups, (
        "Al menos una entrada de 'updates' debe usar 'groups' para agrupar las actualizaciones "
        "en un PR revisable (sin esto, Dependabot abre un PR por dependencia = fatiga de PRs)."
    )
