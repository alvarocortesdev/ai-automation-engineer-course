"""
cron_pagos.py — script de payouts disparado por cron, cada noche a las 03:00.

  # crontab
  0 3 * * *  /usr/bin/python3 /opt/jobs/cron_pagos.py

Procesa los pagos pendientes a proveedores: por cada uno reserva fondos, espera
una ventana de revisión antifraude, transfiere, y notifica al proveedor.

NO modifiques este archivo. Tu tarea es ANALIZARLO (ver README.md): por qué se
rompe en producción, qué rompería el replay de Temporal, y cuál es la frontera
workflow/activity. No estás portándolo todavía: lo estás diagnosticando.
"""
import random
import time
from datetime import datetime

import requests

API = "https://internal.example"


def pagos_pendientes() -> list[dict]:
    return requests.get(f"{API}/payouts?estado=pendiente").json()


def procesar_pago(pago: dict) -> None:
    # 1) Reservar fondos en la cuenta interna.
    requests.post(f"{API}/fondos/reservar", json={"monto": pago["monto"]})

    # 2) Ventana antifraude: esperar 6 horas dentro del proceso.
    time.sleep(6 * 60 * 60)

    # 3) Transferir al proveedor, reintentando "a mano" si falla.
    intentos = 0
    while True:
        intentos += 1
        resp = requests.post(f"{API}/transferencias", json=pago)
        if resp.status_code == 200:
            break
        if intentos >= 5:
            raise RuntimeError("transferencia fallida tras 5 intentos")
        time.sleep(random.uniform(1, 5))  # backoff con jitter

    # 4) Notificar al proveedor con un folio y la marca de tiempo del envío.
    folio = f"PO-{random.randint(100000, 999999)}"
    requests.post(
        f"{API}/notificar",
        json={
            "proveedor": pago["proveedor"],
            "folio": folio,
            "enviado_en": datetime.now().isoformat(),
        },
    )


def main() -> None:
    for pago in pagos_pendientes():
        procesar_pago(pago)


if __name__ == "__main__":
    main()
