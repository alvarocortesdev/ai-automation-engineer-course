"""Test ESTRUCTURAL de tu workflow de release (`release.yml`).

Valida la FORMA del YAML (matriz, caché, jobs encadenados, deploy gated). No corre
nada en GitHub. El razonamiento (write-up.md) lo corrige tu IA con la rúbrica.

Requisito: pyyaml  ->  uv add --dev pyyaml   (o: pip install pyyaml)
Correr:    uv run pytest test_workflow.py
"""

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml", reason="Instala pyyaml: uv add --dev pyyaml")

WORKFLOW = Path(__file__).parent / ".github" / "workflows" / "release.yml"


def cargar():
    assert WORKFLOW.exists(), f"No encuentro {WORKFLOW}. Crea .github/workflows/release.yml."
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "El YAML no es un mapeo válido."
    return data


def jobs(data):
    js = data.get("jobs")
    assert isinstance(js, dict), "Falta el bloque 'jobs:'."
    return js


def needs_de(job):
    n = job.get("needs")
    if n is None:
        return []
    return [n] if isinstance(n, str) else list(n)


def steps_de(job):
    return job.get("steps") or []


def test_existen_los_tres_jobs():
    js = jobs(cargar())
    for nombre in ("test", "build", "deploy"):
        assert nombre in js, f"Falta el job '{nombre}'."


def test_matriz_de_tres_versiones_y_cache():
    job = jobs(cargar())["test"]
    matrix = (job.get("strategy") or {}).get("matrix") or {}
    versiones = matrix.get("python-version") or []
    versiones = [str(v) for v in versiones]
    for v in ("3.11", "3.12", "3.13"):
        assert v in versiones, f"La matriz del job 'test' debe incluir Python {v}."
    # caché: o bien setup-uv con enable-cache, o bien un step actions/cache
    texto = yaml.safe_dump(job)
    assert "enable-cache" in texto or "actions/cache" in texto, (
        "El job 'test' debe cachear dependencias (enable-cache: true en setup-uv, "
        "o un step actions/cache)."
    )


def test_build_depende_de_test_y_sube_artefacto():
    job = jobs(cargar())["build"]
    assert "test" in needs_de(job), "El job 'build' debe declarar 'needs: test'."
    usa_upload = any(
        (s.get("uses") or "").startswith("actions/upload-artifact") for s in steps_de(job)
    )
    assert usa_upload, "El job 'build' debe subir un artefacto (actions/upload-artifact)."


def test_deploy_gated_por_rama_y_con_environment():
    job = jobs(cargar())["deploy"]
    assert "build" in needs_de(job), "El job 'deploy' debe declarar 'needs: build'."
    condicion = str(job.get("if") or "")
    assert "main" in condicion, (
        "El job 'deploy' debe limitarse con un 'if:' que referencie la rama main "
        "(p. ej. github.ref == 'refs/heads/main')."
    )
    assert job.get("environment") in ("production", {"name": "production"}) or (
        isinstance(job.get("environment"), dict)
        and job["environment"].get("name") == "production"
    ), "El job 'deploy' debe usar 'environment: production'."


def test_secret_referenciado_no_en_texto_plano():
    job = jobs(cargar())["deploy"]
    referencia_ok = False
    for s in steps_de(job):
        env = s.get("env") or {}
        for clave, valor in env.items():
            valor = str(valor)
            if "TOKEN" in clave.upper():
                assert "${{" in valor and "secrets." in valor, (
                    "El valor de '" + clave + "' parece un secreto en texto plano. "
                    "Usa una referencia a secrets.NOMBRE entre ${{ }}, nunca el valor literal."
                )
                if "DEPLOY_TOKEN" in valor:
                    referencia_ok = True
    assert referencia_ok, (
        "El deploy debe inyectar el secret como una referencia a secrets.DEPLOY_TOKEN."
    )
