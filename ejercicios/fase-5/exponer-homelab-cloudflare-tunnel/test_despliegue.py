"""Lint de seguridad del `docker-compose.yml` (no ejecuta nada contra Cloudflare).

Verifica que tu Compose tome las decisiones correctas de la lección 5.9, sección 4.4:
expone el backend solo en la red interna, no publica puertos al host (el túnel es saliente),
y toma el token del túnel desde el entorno sin hardcodearlo. Corre con `pytest`. Solo stdlib.
"""

import re
from pathlib import Path

HERE = Path(__file__).parent
COMPOSE = HERE / "docker-compose.yml"


def _text() -> str:
    assert COMPOSE.exists(), "Falta docker-compose.yml en esta carpeta."
    return COMPOSE.read_text(encoding="utf-8")


def _strip_comments(t: str) -> str:
    """Quita los comentarios (#...) para no confundir TODO/pistas con configuración real."""
    out = []
    for line in t.splitlines():
        # conserva la parte antes del primer '#' (los valores de este ejercicio no usan '#')
        out.append(line.split("#", 1)[0])
    return "\n".join(out)


def test_define_servicios_api_y_cloudflared() -> None:
    t = _strip_comments(_text())
    assert re.search(r"^\s{2}api:\s*$", t, re.MULTILINE), "Define el servicio `api`."
    assert re.search(r"^\s{2}cloudflared:\s*$", t, re.MULTILINE), "Define el servicio `cloudflared`."


def test_usa_imagen_oficial_de_cloudflared() -> None:
    t = _strip_comments(_text())
    assert "cloudflare/cloudflared" in t, (
        "El conector debe usar la imagen oficial `cloudflare/cloudflared`."
    )


def test_cloudflared_corre_tunnel_run() -> None:
    t = _strip_comments(_text())
    assert "tunnel" in t and "run" in t and "--token" in t, (
        "El conector debe correr `tunnel ... run --token ...`."
    )


def test_token_desde_entorno_no_hardcodeado() -> None:
    t = _strip_comments(_text())
    # El token debe venir de la variable de entorno, p. ej. --token ${CF_TUNNEL_TOKEN}
    assert re.search(r"--token\s+\"?\$\{?CF_TUNNEL_TOKEN\}?\"?", t), (
        "El token debe inyectarse desde el entorno: `--token ${CF_TUNNEL_TOKEN}`, no un literal."
    )
    # No debe haber un token literal largo (base64/JWT) tras --token.
    assert not re.search(r"--token\s+\"?[A-Za-z0-9_\-\.]{30,}", t), (
        "Hay un token hardcodeado tras `--token`. Un secreto en el repo está comprometido: usa ${CF_TUNNEL_TOKEN}."
    )


def test_backend_solo_interno_con_expose() -> None:
    t = _strip_comments(_text())
    assert "expose" in t, (
        "El backend debe ser visible SOLO en la red interna: declara `expose` (no `ports`)."
    )


def test_ningun_puerto_publicado_al_host() -> None:
    t = _strip_comments(_text())
    # En el diseño por túnel (conexión saliente) NINGÚN servicio publica puertos al host.
    assert not re.search(r"^\s*ports:\s*$", t, re.MULTILINE), (
        "No publiques puertos al host: el túnel es SALIENTE. Quita cualquier `ports:` "
        "(el backend va con `expose`; cloudflared no necesita puertos de entrada)."
    )


def test_restart_policy_en_ambos_servicios() -> None:
    t = _strip_comments(_text())
    assert t.count("unless-stopped") >= 2, (
        "Ambos servicios deben tener `restart: unless-stopped` para sobrevivir a reinicios."
    )


def test_env_example_documenta_el_token() -> None:
    ej = HERE / ".env.example"
    assert ej.exists(), "Debe existir un `.env.example` que documente las variables."
    assert "CF_TUNNEL_TOKEN" in ej.read_text(encoding="utf-8"), (
        "`.env.example` debe documentar la clave `CF_TUNNEL_TOKEN` (sin valor)."
    )


def test_gitignore_excluye_el_env() -> None:
    gi = HERE / ".gitignore"
    assert gi.exists(), "Debe existir un `.gitignore`."
    lineas = {l.strip() for l in gi.read_text(encoding="utf-8").splitlines()}
    assert ".env" in lineas, "`.gitignore` debe excluir `.env` (el secreto nunca se commitea)."
