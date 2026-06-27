"""Lint de seguridad de `deploy.sh` (no ejecuta nada contra Azure).

Verifica que tu script de despliegue tome las decisiones correctas de la lección 5.5:
crea los recursos necesarios, expone la app públicamente, usa identidad administrada
(sin secretos) y respeta el mínimo privilegio. Corre con `pytest`. Solo usa stdlib.
"""

import re
from pathlib import Path

SCRIPT = Path(__file__).parent / "deploy.sh"


def _text() -> str:
    assert SCRIPT.exists(), "Falta deploy.sh en esta carpeta."
    return SCRIPT.read_text(encoding="utf-8")


def _norm(t: str) -> str:
    """Une las continuaciones de línea ('\\' al final) para encontrar flags partidos en varias líneas."""
    return re.sub(r"\\\s*\n", " ", t)


def test_crea_grupo_y_entorno() -> None:
    t = _norm(_text())
    assert "az group create" in t, "Crea el grupo de recursos con `az group create`."
    assert "az containerapp env create" in t, "Crea el entorno con `az containerapp env create`."


def test_construye_la_imagen_en_el_registry() -> None:
    t = _norm(_text())
    assert "az acr create" in t, "Crea el registry con `az acr create`."
    assert "az acr build" in t, "Construye la imagen en la nube con `az acr build`."


def test_despliega_la_app() -> None:
    t = _norm(_text())
    assert ("az containerapp create" in t) or ("az containerapp up" in t), (
        "Despliega la app con `az containerapp create` (o `az containerapp up`)."
    )


def test_ingress_publico_y_puerto() -> None:
    t = _norm(_text())
    assert "--ingress external" in t, "La app debe ser alcanzable desde internet: `--ingress external`."
    assert "--target-port" in t, "Declara el puerto que escucha tu app con `--target-port`."


def test_usa_identidad_administrada() -> None:
    t = _norm(_text())
    assert "az identity create" in t, "Crea una identidad administrada con `az identity create`."
    assert ("--registry-identity" in t) or ("--user-assigned" in t), (
        "El pull del registry debe autenticarse con la identidad administrada "
        "(`--registry-identity` / `--user-assigned`)."
    )


def test_no_usa_credenciales_de_admin() -> None:
    t = _norm(_text()).lower()
    assert "--admin-enabled true" not in t, (
        "No habilites el admin user del ACR: usa identidad administrada, no credenciales."
    )
    assert "--registry-password" not in t, "No pases password de registry; el secreto se elimina con la identidad."
    assert "--registry-username" not in t, "No pases usuario de registry; usa identidad administrada."


def test_least_privilege_acrpull_no_contributor() -> None:
    t = _norm(_text())
    assert re.search(r"--role\s+\"?acrpull\"?", t, re.IGNORECASE), (
        "Asigna SOLO el rol `acrpull` (el mínimo necesario para hacer pull de la imagen)."
    )
    assert not re.search(r"--role\s+\"?(Contributor|Owner)\"?", t, re.IGNORECASE), (
        "No asignes Contributor/Owner: viola el mínimo privilegio. El contenedor solo necesita acrpull."
    )
