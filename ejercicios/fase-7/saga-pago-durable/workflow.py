"""
workflow.py — TU TRABAJO. Completa el método `run` (los TODO).

Reglas que NO puedes romper (si las rompes, el replay o los tests fallan):
  - NADA de I/O, red, random, datetime.now() ni time.sleep DENTRO del workflow.
    Todo eso ya vive en las activities. El workflow solo ORQUESTA.
  - La espera debe ser `workflow.sleep(...)`, no `time.sleep(...)`.
  - Pasa la RetryPolicy a las activities.
  - Implementa la SAGA: si `cobrar_pago` falla, compensa liberando el inventario
    YA reservado, y luego propaga el fallo (que el workflow falle, pero el mundo
    quede CONSISTENTE: nada reservado, nada cobrado).

Cuando los dos tests pasen en verde, terminaste. Corre:  uv run pytest   (o: pytest)
"""
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

# Importamos las activities "pasándolas a través" del sandbox del workflow.
with workflow.unsafe.imports_passed_through():
    from actividades import (
        Orden,
        cobrar_pago,
        confirmar_envio,
        liberar_inventario,
        reservar_inventario,
    )

# Reintentos para errores TRANSITORIOS. El error "TarjetaRechazada" es
# non_retryable, así que NO lo reintenta (falla al primer intento).
REINTENTOS = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=30),
    maximum_attempts=5,
)


@workflow.defn
class ProcesoCheckoutWorkflow:
    @workflow.run
    async def run(self, orden: Orden) -> dict:
        # TODO 1: reservar inventario (activity) -> guarda el reserva_id.
        #   Usa start_to_close_timeout y retry_policy=REINTENTOS.

        # TODO 2: ventana de cancelación de 30 minutos con workflow.sleep
        #   (NO time.sleep). En los tests, el time-skipping la salta al instante.

        # TODO 3: dentro de un try/except, cobrar el pago (activity).
        #   Si falla: COMPENSA llamando a liberar_inventario(reserva_id) y luego
        #   re-lanza el error (raise) para que el workflow falle consistente.

        # TODO 4: confirmar el envío (activity). Recuerda: dos argumentos ->
        #   se pasan con args=[orden, reserva_id].

        # TODO 5: devolver un dict con estado="confirmado" y los ids.
        raise NotImplementedError("Implementa el método run (borra esta línea).")
