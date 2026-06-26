"""Starter — Verifica un JWT a mano (Primero-Sin-IA).

Tu trabajo es implementar `verificar_jwt`. NO uses PyJWT ni ninguna librería de
terceros: solo la librería estándar (`hmac`, `hashlib`, `base64`, `json`).
Implementar la verificación a mano es la mejor forma de entender qué protege
—y qué NO protege— un JWT.

Lo que YA viene dado (no necesitas tocarlo):
  - `firmar_jwt(claims, secret)`: crea un JWT HS256. Úsalo para entender la
    estructura y para que los tests generen tokens.
  - `_b64url_encode` / `_b64url_decode`: el plomería de base64url (sin padding).
  - Las excepciones (`TokenMalformado`, `AlgoritmoNoPermitido`, `FirmaInvalida`,
    `TokenExpirado`), todas hijas de `JWTError`.

NO cambies las firmas ni los nombres: los tests dependen de ellos.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json


class JWTError(Exception):
    """Base de todos los errores de verificación de un JWT."""


class TokenMalformado(JWTError):
    """El token no tiene la forma header.payload.signature, o no decodifica."""


class AlgoritmoNoPermitido(JWTError):
    """El header declara un `alg` distinto del esperado (p. ej. 'none')."""


class FirmaInvalida(JWTError):
    """La firma no corresponde al contenido + secreto."""


class TokenExpirado(JWTError):
    """El claim `exp` ya pasó."""


def _b64url_encode(data: bytes) -> str:
    """base64url SIN padding, como exige el estándar JWT."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(texto: str) -> bytes:
    """Invierte `_b64url_encode`: re-agrega el padding '=' que se había quitado."""
    relleno = "=" * (-len(texto) % 4)
    return base64.urlsafe_b64decode(texto + relleno)


def firmar_jwt(claims: dict, secret: str) -> str:
    """Crea un JWT HS256 (header.payload.signature). DADO: no necesitas tocarlo.

    Úsalo para ver cómo se construye un token y en los tests para generar
    tokens válidos (y luego manipularlos).
    """
    header = {"alg": "HS256", "typ": "JWT"}
    h = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    p = _b64url_encode(json.dumps(claims, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{h}.{p}".encode("ascii")
    firma = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    s = _b64url_encode(firma)
    return f"{h}.{p}.{s}"


def verificar_jwt(token: str, secret: str, ahora: int) -> dict:
    """Verifica un JWT HS256 y devuelve sus claims si todo está bien.

    Reglas, EN ESTE ORDEN de defensa (el orden importa: no leas `exp` antes de
    confiar en la firma):

      1. El token debe tener exactamente 3 partes separadas por '.' y cada parte
         debe decodificar (base64url + JSON donde aplique). Si no -> TokenMalformado.
      2. El header debe declarar alg == "HS256". Cualquier otro valor, incluido
         "none" -> AlgoritmoNoPermitido. NUNCA dejes que el token elija con qué
         algoritmo se verifica: el algoritmo permitido lo fijas TÚ.
      3. Recalcula la firma sobre "header.payload" con HMAC-SHA256 + `secret`, y
         compárala en TIEMPO CONSTANTE con `hmac.compare_digest` (no con `==`,
         para no filtrar información por timing). Si no calza -> FirmaInvalida.
      4. Si el payload trae `exp` y `ahora >= exp` -> TokenExpirado.
      5. Si todo pasa, devuelve el dict de claims del payload.

    Args:
        token: el JWT entrante (string `header.payload.signature`).
        secret: el secreto compartido para HMAC-SHA256.
        ahora: epoch en segundos, inyectado para que el test sea determinista.

    Returns:
        El dict de claims del payload, si el token es válido y no expiró.
    """
    raise NotImplementedError("Implementa la verificación a mano, sin IA ni PyJWT.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que pasa ANTES de correrlo?
    secreto = "secreto-de-pruebas"
    t = firmar_jwt({"sub": "ana", "exp": 9999999999}, secreto)
    print("token:", t)
    # print("claims:", verificar_jwt(t, secreto, ahora=1000))  # descomenta al implementar
