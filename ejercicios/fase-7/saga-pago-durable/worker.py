"""
worker.py — OPCIONAL: corre tu lógica contra un Temporal real.

Para correrlo de verdad (no hace falta para pasar los tests):
  1. Instala la CLI de Temporal y levanta el dev server:
       temporal server start-dev          # expone localhost:7233 + UI en :8233
  2. En otra terminal, arranca el worker:
       uv run python worker.py
  3. En una tercera, dispara un checkout:
       uv run python iniciar.py
  4. Mira el historial paso a paso en la Web UI: http://localhost:8233
"""
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from actividades import (
    cobrar_pago,
    confirmar_envio,
    liberar_inventario,
    reservar_inventario,
)
from workflow import ProcesoCheckoutWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="checkout-tq",
        workflows=[ProcesoCheckoutWorkflow],
        activities=[
            reservar_inventario,
            liberar_inventario,
            cobrar_pago,
            confirmar_envio,
        ],
    )
    print("Worker arriba en task_queue='checkout-tq'. Ctrl-C para salir.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
