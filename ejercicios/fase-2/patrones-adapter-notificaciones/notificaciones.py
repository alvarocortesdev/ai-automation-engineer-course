"""Starter — Patrón Adapter. Primero-Sin-IA.

Tu app envía notificaciones SOLO a través del contrato `Notificador`.
Te toca integrar DOS librerías de terceros con interfaces incompatibles
(que NO puedes modificar) escribiendo un Adapter para cada una, sin tocar
el código de negocio (`enviar_alerta`) ni el contrato.

Implementa los adapters a mano, sin IA. NO cambies las firmas de las clases
de terceros ni de `enviar_alerta`: los tests dependen de ellas.
"""

from typing import Protocol


# ── El contrato que TU app entiende. NO lo cambies. ─────────────────────────
class Notificador(Protocol):
    """Lo único que tu dominio sabe llamar."""

    def enviar(self, destino: str, mensaje: str) -> None: ...


# ── Librerías de terceros (vendored). NO se pueden modificar. ───────────────
class GatewaySmsLegacy:
    """SMS de terceros. Interfaz incompatible a propósito.

    Guarda en `self.enviados` lo que se envió, para que los tests verifiquen
    que el Adapter tradujo bien la llamada.
    """

    def __init__(self) -> None:
        self.enviados: list[dict] = []

    def send_text(self, to_number: str, body: str, *, sender: str) -> dict:
        envio = {"to": to_number, "body": body, "from": sender}
        self.enviados.append(envio)
        return {"status": "queued", **envio}


class ClienteEmailV2:
    """Email de terceros. OTRA interfaz incompatible.

    `dispatch` espera un payload con las claves: recipient, subject, html.
    Guarda en `self.bandeja` lo recibido.
    """

    def __init__(self) -> None:
        self.bandeja: list[dict] = []

    def dispatch(self, payload: dict) -> None:
        self.bandeja.append(payload)


# ── Código de negocio: habla SOLO el contrato Notificador. NO lo cambies. ───
def enviar_alerta(notificador: Notificador, destino: str) -> None:
    """Negocio puro: no conoce a ningún proveedor, solo el contrato."""
    notificador.enviar(destino, "Tu pedido fue confirmado")


# ── TODO(estudiante): escribe los adapters aquí abajo. ──────────────────────
class SmsAdapter:
    """TODO 1: haz que GatewaySmsLegacy satisfaga `Notificador`.

    Recibe el gateway y el remitente en __init__; traduce
    enviar(destino, mensaje) -> gateway.send_text(destino, mensaje, sender=...).
    """

    def __init__(self, gateway: GatewaySmsLegacy, remitente: str) -> None:
        raise NotImplementedError("Implementa el Adapter a mano, sin IA.")

    def enviar(self, destino: str, mensaje: str) -> None:
        raise NotImplementedError


# TODO 2 (Open/Closed): agrega aquí la clase EmailAdapter para ClienteEmailV2.
#   Debe cumplir `Notificador` y traducir enviar(destino, mensaje) al payload
#   que `dispatch` espera: {"recipient": ..., "subject": ..., "html": ...}.
#   No toques SmsAdapter ni enviar_alerta al hacerlo.
