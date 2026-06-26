"""Tests del builder de errores problem+json (RFC 9457).

Verifican la FORMA del problema y la elección de status codes.
Corre:  uv run pytest   (o)   pytest
Cuando pasen todos en verde, añade al menos un caso de prueba tuyo abajo.
"""

import pytest

from problem_details import (
    PROBLEM_CONTENT_TYPE,
    build_problem_detail,
    choose_status,
)


def test_content_type_es_el_estandar():
    assert PROBLEM_CONTENT_TYPE == "application/problem+json"


def test_minimo_tiene_status_title_y_type_por_defecto():
    p = build_problem_detail(404, "Recurso no encontrado")
    assert p["status"] == 404
    assert p["title"] == "Recurso no encontrado"
    # type ausente => about:blank (default del estándar)
    assert p["type"] == "about:blank"


def test_campos_opcionales_ausentes_si_no_se_pasan():
    p = build_problem_detail(404, "No encontrado")
    assert "detail" not in p
    assert "instance" not in p


def test_campos_opcionales_presentes_si_se_pasan():
    p = build_problem_detail(
        409,
        "El libro no está disponible",
        type_="https://api.x/errors/libro-no-disponible",
        detail="El libro 42 ya tiene un préstamo activo.",
        instance="/prestamos",
    )
    assert p["type"] == "https://api.x/errors/libro-no-disponible"
    assert p["detail"].startswith("El libro 42")
    assert p["instance"] == "/prestamos"


def test_ningun_valor_none_se_cuela():
    # Pasar detail=None NO debe meter una clave "detail": None
    p = build_problem_detail(400, "Petición inválida", detail=None)
    assert "detail" not in p
    assert all(v is not None for v in p.values())


def test_extension_members_se_incluyen():
    p = build_problem_detail(
        422,
        "Validación fallida",
        campos_invalidos=["titulo", "anio"],
    )
    assert p["campos_invalidos"] == ["titulo", "anio"]
    assert p["status"] == 422


@pytest.mark.parametrize(
    "situation,code",
    [
        ("ok", 200),
        ("created", 201),
        ("no_content", 204),
        ("malformed_body", 400),
        ("missing_auth", 401),
        ("forbidden", 403),
        ("not_found", 404),
        ("state_conflict", 409),
        ("validation_failed", 422),
        ("server_error", 500),
    ],
)
def test_choose_status_mapea_cada_situacion(situation, code):
    assert choose_status(situation) == code


def test_choose_status_situacion_desconocida_levanta_valueerror():
    with pytest.raises(ValueError):
        choose_status("teleport")


# --- Tu caso de prueba (añade al menos uno) -------------------------------
# Ejemplo de idea: ¿qué pasa si pasas una extensión que choca de nombre con
# un campo estándar? ¿O un problem con type_ explícito y sin detail?
