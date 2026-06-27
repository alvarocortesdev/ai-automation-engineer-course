"""Linter estático del compose.yaml — NO necesita Docker instalado.

Lee tu `compose.yaml` (ignorando comentarios) y tu `.env.example`, y verifica las
buenas prácticas de la lección 5.1. Es un PISO, no la meta: que pase el linter no
significa que el stack arranque ni que tu razonamiento sea correcto — eso lo
revisa tu `notas.md` y el corrector.

Ejecuta:
    uv run pytest test_compose.py     # recomendado
    pytest test_compose.py            # si ya tienes pytest

Con el esqueleto sin completar, varios tests fallan (rojo). Es lo esperado.
"""

import re
from pathlib import Path

import pytest

AQUI = Path(__file__).parent
COMPOSE = AQUI / "compose.yaml"
ENV_EXAMPLE = AQUI / ".env.example"


def _codigo() -> str:
    """Texto del compose.yaml SIN comentarios (full-line e inline)."""
    assert COMPOSE.exists(), "Falta el archivo compose.yaml."
    lineas = []
    for linea in COMPOSE.read_text(encoding="utf-8").splitlines():
        if linea.strip().startswith("#"):
            continue
        # quita comentario inline ' # ...' (con espacio antes del #)
        linea = re.sub(r"\s+#.*$", "", linea)
        lineas.append(linea)
    return "\n".join(lineas)


def _image_values(codigo: str) -> list[str]:
    vals = []
    for m in re.finditer(r"^\s*image\s*:\s*(.+)$", codigo, re.MULTILINE):
        vals.append(m.group(1).strip().strip("\"'"))
    return vals


def test_compose_no_esta_vacio():
    cod = _codigo()
    assert "services:" in cod, "El compose.yaml no define 'services:'. Complétalo."


def test_sin_campo_version_obsoleto():
    cod = _codigo()
    assert not re.search(r"^version\s*:", cod, re.MULTILINE), (
        "El campo top-level 'version:' es OBSOLETO en Compose moderno. Quítalo."
    )


def test_api_se_construye_localmente():
    cod = _codigo()
    assert re.search(r"^\s*build\s*:", cod, re.MULTILINE), (
        "El servicio api debe construirse con 'build: .' (tu Dockerfile)."
    )


def test_imagenes_pinneadas_y_sin_latest():
    cod = _codigo()
    imagenes = _image_values(cod)
    tiene_pg = any("postgres" in v for v in imagenes)
    tiene_cache = any(("redis" in v) or ("valkey" in v) for v in imagenes)
    assert tiene_pg, "Falta el servicio Postgres (image: postgres:<version>)."
    assert tiene_cache, "Falta el servicio Redis/Valkey (image: redis:<version>)."
    for v in imagenes:
        assert v, "Hay un 'image:' vacío. Pon la imagen pinneada."
        if "postgres" in v or "redis" in v or "valkey" in v:
            assert ":" in v, f"La imagen '{v}' no tiene tag. Fíjala (p. ej. postgres:17)."
            assert not v.endswith(":latest"), (
                f"'{v}' usa ':latest', que no es reproducible. Fija una versión."
            )


def test_healthchecks_de_db_y_cache():
    cod = _codigo()
    assert "healthcheck:" in cod, "Faltan los healthcheck de db y cache."
    assert "pg_isready" in cod, (
        "El healthcheck de Postgres debe usar 'pg_isready'."
    )
    assert "redis-cli" in cod and "ping" in cod, (
        "El healthcheck de Redis debe usar 'redis-cli ping'."
    )


def test_depends_on_con_service_healthy():
    cod = _codigo()
    assert "depends_on:" in cod, "La api debe declarar depends_on."
    assert "condition: service_healthy" in cod, (
        "depends_on en forma CORTA no basta: solo espera a que el contenedor arranque, "
        "no a que el servicio esté listo. Usa la forma larga con "
        "'condition: service_healthy' para db y cache."
    )


def test_named_volume_para_postgres():
    cod = _codigo()
    assert "/var/lib/postgresql/data" in cod, (
        "Postgres debe montar un volumen en /var/lib/postgresql/data, o pierdes los "
        "datos al recrear el contenedor."
    )
    assert re.search(r"^volumes\s*:", cod, re.MULTILINE), (
        "Declara el named volume a nivel raíz (bloque 'volumes:' sin indentación)."
    )


def test_password_por_variable_de_entorno():
    cod = _codigo()
    assert "${POSTGRES_PASSWORD}" in cod, (
        "La contraseña de Postgres debe entrar por \\${POSTGRES_PASSWORD} (de .env), "
        "no escrita en el archivo."
    )
    # no debe haber un literal: POSTGRES_PASSWORD: algo-que-no-sea-${...}
    for m in re.finditer(r"POSTGRES_PASSWORD\s*:\s*(.+)", cod):
        valor = m.group(1).strip().strip("\"'")
        assert valor.startswith("${"), (
            f"POSTGRES_PASSWORD tiene un valor literal ('{valor}'). Usa \\${{POSTGRES_PASSWORD}}."
        )


def test_servicios_se_alcanzan_por_nombre():
    cod = _codigo()
    assert "db:5432" in cod, (
        "La DATABASE_URL debe apuntar al servicio por nombre: '@db:5432', no a una IP."
    )
    assert "cache:6379" in cod, (
        "La REDIS_URL debe apuntar al servicio por nombre: 'cache:6379', no a una IP."
    )


def test_env_example_documenta_la_variable():
    assert ENV_EXAMPLE.exists(), "Falta .env.example (documenta las variables sin secretos reales)."
    texto = ENV_EXAMPLE.read_text(encoding="utf-8")
    assert "POSTGRES_PASSWORD" in texto, ".env.example debe documentar POSTGRES_PASSWORD."


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
