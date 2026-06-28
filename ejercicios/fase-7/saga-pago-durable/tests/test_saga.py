"""
test_saga.py — suite provista. NO la edites para "hacerla pasar"; haz que tu
workflow.py la satisfaga. Sí puedes AÑADIR tests propios al final (ver README).

Usa el time-skipping environment de Temporal: corre en segundos, sin Docker y
sin esperar los 30 minutos reales del workflow.sleep.

  La PRIMERA corrida descarga el binario del test-server de Temporal (necesita
  internet una vez). Después corre offline.

Patrón de testing: registramos activities MOCK con el mismo `name` que las
reales. El workflow las despacha por nombre, así que corren los mocks; estos
anotan en una lista para poder asertar el ORDEN de los pasos y la compensación.
"""
import asyncio
import uuid

from temporalio import activity
from temporalio.client import WorkflowFailureError
from temporalio.exceptions import ApplicationError
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from actividades import Orden
from workflow import ProcesoCheckoutWorkflow


def _mocks(rechazar_pago: bool):
    """Crea mocks que registran las llamadas; devuelve (lista_llamadas, [activities])."""
    llamadas: list[str] = []

    @activity.defn(name="reservar_inventario")
    async def reservar(orden: Orden) -> str:
        llamadas.append("reservar")
        return f"reserva-{orden.id}"

    @activity.defn(name="cobrar_pago")
    async def cobrar(orden: Orden) -> str:
        llamadas.append("cobrar-intento")
        if rechazar_pago:
            raise ApplicationError(
                "Tarjeta rechazada", type="TarjetaRechazada", non_retryable=True
            )
        llamadas.append("cobrar-ok")
        return f"cargo-{orden.id}"

    @activity.defn(name="confirmar_envio")
    async def confirmar(orden: Orden, reserva_id: str) -> str:
        llamadas.append("confirmar")
        return f"envio-{orden.id}"

    @activity.defn(name="liberar_inventario")
    async def liberar(reserva_id: str) -> None:
        llamadas.append(f"liberar:{reserva_id}")

    return llamadas, [reservar, cobrar, confirmar, liberar]


async def _correr(orden: Orden, rechazar_pago: bool):
    llamadas, acts = _mocks(rechazar_pago)
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue="test-checkout",
            workflows=[ProcesoCheckoutWorkflow],
            activities=acts,
        ):
            try:
                resultado = await env.client.execute_workflow(
                    ProcesoCheckoutWorkflow.run,
                    orden,
                    id=f"test-{uuid.uuid4()}",
                    task_queue="test-checkout",
                )
                return resultado, llamadas, None
            except WorkflowFailureError as err:
                return None, llamadas, err


def test_happy_path_orden_de_pasos():
    orden = Orden(id="A-1", monto=1000, tarjeta="ok")
    resultado, llamadas, error = asyncio.run(_correr(orden, rechazar_pago=False))

    assert error is None, "el happy path no debería fallar"
    assert resultado["estado"] == "confirmado"
    # Orden correcto: reservar -> cobrar -> confirmar, SIN compensación.
    assert llamadas == ["reservar", "cobrar-intento", "cobrar-ok", "confirmar"]
    assert not any(c.startswith("liberar") for c in llamadas)


def test_tarjeta_rechazada_compensa_y_falla():
    orden = Orden(id="B-2", monto=1000, tarjeta="rechazada")
    resultado, llamadas, error = asyncio.run(_correr(orden, rechazar_pago=True))

    assert error is not None, "una tarjeta rechazada debe hacer fallar el workflow"
    # Se reservó, se intentó cobrar, y se COMPENSÓ liberando esa reserva...
    assert "reservar" in llamadas
    assert "liberar:reserva-B-2" in llamadas
    # ...y NUNCA se confirmó el envío (no se cobró, así que no hay nada que enviar).
    assert "confirmar" not in llamadas


# TODO (tuyo): añade al menos un test propio. Ideas:
#   - Un workflow con el MISMO id no se procesa dos veces (idempotencia de workflow).
#   - Un fallo TRANSITORIO (no non_retryable) se reintenta según la RetryPolicy.
