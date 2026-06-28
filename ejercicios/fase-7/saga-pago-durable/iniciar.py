"""
iniciar.py — OPCIONAL: dispara un checkout contra el Temporal real (ver worker.py).
Cambia tarjeta="rechazada" para ver la saga compensar en la Web UI.
"""
import asyncio

from temporalio.client import Client

from actividades import Orden
from workflow import ProcesoCheckoutWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    resultado = await client.execute_workflow(
        ProcesoCheckoutWorkflow.run,
        Orden(id="A-1001", monto=29990, tarjeta="ok"),
        id="checkout-A-1001",  # id estable = idempotencia a nivel de workflow
        task_queue="checkout-tq",
    )
    print(resultado)


if __name__ == "__main__":
    asyncio.run(main())
