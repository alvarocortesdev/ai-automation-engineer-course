"""Verificación de firma de webhook (HMAC + anti-replay) — Primero-Sin-IA.

Implementa `verificar_webhook` a mano, sin IA. NO cambies la firma de la función
ni los strings que devuelve: los tests de `test_verificador.py` dependen de ellos.

Idea: un webhook entra por una URL pública. Antes de creerle, hay que verificar
(1) que viene de quien dice (autenticidad), (2) que nadie lo manipuló en el camino
(integridad) y (3) que no es la reproducción de un mensaje viejo capturado
(anti-replay). El HMAC con un secreto compartido resuelve (1) y (2); firmar el
timestamp y rechazar lo viejo resuelve (3).

──────────────────────────────────────────────────────────────────────────────
CONTRATO

    verificar_webhook(payload, header_firma, secreto, ahora, tolerancia_seg=300)

Parámetros:
    payload: bytes        -> el body CRUDO tal como llegó (NO un dict, NO un str
                             re-serializado: el HMAC depende de cada byte).
    header_firma: str     -> cabecera con formato  "t=<timestamp>,v1=<hmac_hex>"
                             p. ej.  "t=1718900000,v1=5257a86920ab..."
    secreto: str          -> el secreto compartido con el emisor (whsec_...).
    ahora: int            -> timestamp UNIX actual, en segundos (se inyecta para
                             poder testear; en producción sería int(time.time())).
    tolerancia_seg: int   -> ventana de frescura; por defecto 300 (5 minutos).

Devuelve EXACTAMENTE uno de estos strings:
    "VALIDO"          -> firma correcta y dentro de la ventana de tiempo.
    "FIRMA_INVALIDA"  -> el HMAC recomputado no coincide (payload alterado o
                         secreto equivocado).
    "EXPIRADO"        -> la firma es válida pero el timestamp es más viejo que la
                         tolerancia (posible replay).
    "MALFORMADO"      -> la cabecera no se puede parsear (faltan 't' o 'v1', o 't'
                         no es un entero).

Reglas (donde está el aprendizaje):
    - La firma se calcula sobre  f"{t}.".encode() + payload  (el timestamp y el
      body, separados por un punto). Firmar SOLO el payload no permite anti-replay.
    - Compara las firmas con hmac.compare_digest (tiempo constante), NUNCA con '=='
      (la comparación corta filtra información por timing -> timing attack).
    - Verifica la firma ANTES que la frescura: solo confías en 't' si la firma es
      auténtica. Si no, un atacante podría inventar cualquier 't'.
    - Orden sugerido de chequeos: MALFORMADO -> FIRMA_INVALIDA -> EXPIRADO -> VALIDO.
"""

import hashlib
import hmac


def verificar_webhook(
    payload: bytes,
    header_firma: str,
    secreto: str,
    ahora: int,
    tolerancia_seg: int = 300,
) -> str:
    """Verifica un webhook firmado. Ver el contrato completo arriba."""
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    import time

    secreto = "whsec_demo"
    payload = b'{"id":"evt_1","monto":1000}'
    t = int(time.time())
    base = f"{t}.".encode() + payload
    firma = hmac.new(secreto.encode(), base, hashlib.sha256).hexdigest()
    header = f"t={t},v1={firma}"
    print(verificar_webhook(payload, header, secreto, t))  # esperado: "VALIDO"
