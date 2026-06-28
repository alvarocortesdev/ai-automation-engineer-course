"""
actividades.py — el trabajo REAL con el mundo (provisto, no lo tienes que cambiar).

Cada activity:
  - hace side effects (aquí simulados con logs; en la vida real: HTTP/DB),
  - es IDEMPOTENTE (acepta un identificador y no duplica si Temporal la reintenta),
  - puede fallar. Temporal la reintenta según la RetryPolicy del workflow.

`cobrar_pago` lanza un error de NEGOCIO no-reintentable cuando la tarjeta es
"rechazada": reintentar una tarjeta rechazada no sirve de nada.
"""
from dataclasses import dataclass

from temporalio import activity
from temporalio.exceptions import ApplicationError


@dataclass
class Orden:
    id: str
    monto: int
    tarjeta: str  # "ok" o "rechazada" (simula la respuesta del emisor)


@activity.defn
async def reservar_inventario(orden: Orden) -> str:
    activity.logger.info("Reservando inventario para %s", orden.id)
    return f"reserva-{orden.id}"


@activity.defn
async def liberar_inventario(reserva_id: str) -> None:
    # COMPENSACIÓN de reservar_inventario. Idempotente: liberar dos veces no rompe.
    activity.logger.info("Liberando %s", reserva_id)


@activity.defn
async def cobrar_pago(orden: Orden) -> str:
    if orden.tarjeta == "rechazada":
        raise ApplicationError(
            "Tarjeta rechazada por el emisor",
            type="TarjetaRechazada",
            non_retryable=True,  # reintentar no ayuda: es un error de negocio
        )
    activity.logger.info("Cobrando %s a la orden %s", orden.monto, orden.id)
    return f"cargo-{orden.id}"


@activity.defn
async def confirmar_envio(orden: Orden, reserva_id: str) -> str:
    activity.logger.info("Confirmando envío de %s (%s)", orden.id, reserva_id)
    return f"envio-{orden.id}"
