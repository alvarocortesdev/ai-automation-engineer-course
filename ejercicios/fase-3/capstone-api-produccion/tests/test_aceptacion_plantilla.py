"""Plantilla de tests de aceptación (contrato) para el capstone.

NO es una solución: es un molde con los PATRONES que tu API debe cumplir. Cada test está marcado con
`@pytest.mark.skip` y trae TODOs para que lo adaptes a TUS rutas y modelos. Quita el skip cuando lo
cablees a tu app. Mídete con `mutmut`, no con coverage%.

Asume un fixture `client` (un fastapi.testclient.TestClient apuntando a tu app) y un fixture
`auth_headers` que devuelve {"Authorization": f"Bearer {token}"} de un usuario recién registrado.
Defínelos en tu propio `conftest.py`.
"""
import pytest

pytestmark = pytest.mark.skip(reason="plantilla: cablea a tu app y quita este skip")


def test_body_invalido_da_422(client):
    """Un campo obligatorio faltante se rechaza en el borde, antes de tu lógica."""
    # TODO: usa tu endpoint de creación y omite un campo requerido.
    resp = client.post("/recurso", json={})  # TODO: tu ruta + body incompleto
    assert resp.status_code == 422


def test_endpoint_protegido_sin_token_da_401(client):
    """Sin credenciales válidas, el endpoint protegido no se ejecuta."""
    resp = client.get("/recurso/1")  # TODO: tu ruta protegida, sin Authorization
    assert resp.status_code == 401


def test_recurso_inexistente_da_404_rfc9457(client, auth_headers):
    """404 con la forma estándar de error (RFC 9457)."""
    resp = client.get("/recurso/999999", headers=auth_headers)  # TODO: id inexistente
    assert resp.status_code == 404
    assert resp.headers["content-type"].startswith("application/problem+json")
    cuerpo = resp.json()
    assert {"type", "title", "status", "detail"} <= cuerpo.keys()


def test_idor_recurso_de_otro_no_se_filtra(client):
    """Broken Access Control cerrado: el recurso de OTRO usuario 'no existe' para mí (404, no 200)."""
    # TODO: crea un recurso con el usuario A; intenta leerlo con el token del usuario B.
    # token_a = registrar_y_login(client, "a@x.com")
    # creado = client.post("/recurso", json={...}, headers=bearer(token_a)).json()
    # token_b = registrar_y_login(client, "b@x.com")
    # resp = client.get(f"/recurso/{creado['id']}", headers=bearer(token_b))
    # assert resp.status_code == 404   # NO 200: el ajeno no existe para B
    raise NotImplementedError("adapta este test a tu dominio")


def test_idempotencia_reintento_no_repite_efecto(client, auth_headers):
    """Mismo Idempotency-Key dos veces = efecto una sola vez, misma respuesta."""
    key = "11111111-1111-1111-1111-111111111111"
    headers = {**auth_headers, "Idempotency-Key": key}
    primera = client.post("/recurso/procesar", json={}, headers=headers)  # TODO: tu endpoint sensible
    segunda = client.post("/recurso/procesar", json={}, headers=headers)
    assert primera.status_code in (200, 202)
    # La segunda reconoce la clave y devuelve el mismo resultado, sin volver a ejecutar el efecto.
    assert segunda.json() == primera.json()
    # TODO: además, verifica con tu repo/contador que el efecto (encolado/cobro) ocurrió UNA vez.


@pytest.mark.parametrize(
    "url_interna",
    [
        "http://169.254.169.254/latest/meta-data/",  # metadata del cloud
        "http://127.0.0.1:5432/",                      # loopback
        "http://10.0.0.5/",                            # rango privado
    ],
)
def test_import_bloquea_ssrf(client, auth_headers, url_interna):
    """La guardia SSRF rechaza destinos internos antes de hacer la petición saliente."""
    resp = client.post("/recurso/importar", json={"url": url_interna}, headers=auth_headers)
    assert resp.status_code == 400


def test_rate_limit_da_429(client):
    """Superar el límite de /auth/token responde 429."""
    # TODO: ajusta el número de intentos a tu RATE_LIMIT_AUTH.
    ultimas = [client.post("/auth/token", data={"username": "x", "password": "y"}) for _ in range(20)]
    assert any(r.status_code == 429 for r in ultimas)
