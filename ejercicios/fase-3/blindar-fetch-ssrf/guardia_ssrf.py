"""Guardia anti-SSRF para fetches SALIENTES.

Un agente de IA (o cualquier feature que haga `fetch` a una URL influida por el
usuario) debe validar el DESTINO antes de salir. Si no, un atacante apunta tu
servidor a recursos internos: bases de datos, paneles sin auth, o el endpoint de
metadatos de la nube (http://169.254.169.254/...) que devuelve credenciales.

Tu trabajo: implementar `validar_destino`. La función auxiliar `_es_ip_peligrosa`
ya está dada (mapea los rangos privados/loopback/link-local de `ipaddress`).

Corre los tests:
    uv run pytest        # o:  pytest
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

ESQUEMAS_PERMITIDOS = {"http", "https"}


class DestinoBloqueado(Exception):
    """El destino de un fetch saliente no pasó la validación anti-SSRF."""


def _es_ip_peligrosa(ip: str) -> bool:
    """True si la IP cae en un rango que un fetch saliente NO debe alcanzar.

    (Ya provista — no la modifiques.) Cubre privadas (10/8, 172.16/12, 192.168/16),
    loopback (127/8, ::1), link-local (169.254/16 = metadatos de la nube), reservadas,
    multicast y la no especificada (0.0.0.0).
    """
    dir_ip = ipaddress.ip_address(ip)
    return (
        dir_ip.is_private
        or dir_ip.is_loopback
        or dir_ip.is_link_local
        or dir_ip.is_reserved
        or dir_ip.is_multicast
        or dir_ip.is_unspecified
    )


def validar_destino(url: str, *, resolver=socket.getaddrinfo) -> str:
    """Valida una URL de destino para un fetch SALIENTE (anti-SSRF).

    Devuelve la URL si es segura; lanza `DestinoBloqueado` si no.

    `resolver` se inyecta (default `socket.getaddrinfo`) para poder testear sin red
    real y para revisar TODAS las IPs a las que resuelve el host (defensa contra DNS
    rebinding: si alguna IP es peligrosa, se bloquea).

    TODO — implementa, en este orden:
      1. Parsea la URL (`urlparse`). Si el esquema no está en ESQUEMAS_PERMITIDOS,
         lanza DestinoBloqueado (esto solo ya bloquea file://, ftp://, gopher://...).
      2. Saca el host (`partes.hostname`). Si no hay host, lanza DestinoBloqueado.
      3. Resuelve el host con `resolver(host, partes.port or 80)`. Si lanza
         `socket.gaierror`, traduce a DestinoBloqueado (no resuelve = no confiable).
      4. Por cada entrada resuelta, la IP está en `info[4][0]` (el sockaddr). Si
         `_es_ip_peligrosa(ip)` es True para CUALQUIERA, lanza DestinoBloqueado.
      5. Si todo pasa, devuelve la url.
    """
    raise NotImplementedError("implementa validar_destino")
