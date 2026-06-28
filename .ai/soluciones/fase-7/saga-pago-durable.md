---
ejercicio_id: fase-7/saga-pago-durable
fase: fase-7
sub_unidad: "7.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Mini-proyecto: saga de checkout durable

## `workflow.py` (método `run` completo)

```python
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from actividades import (
        Orden,
        cobrar_pago,
        confirmar_envio,
        liberar_inventario,
        reservar_inventario,
    )

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
        # 1) Reservar (lo compensaremos si algo posterior falla).
        reserva_id = await workflow.execute_activity(
            reservar_inventario,
            orden,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=REINTENTOS,
        )

        # 2) Ventana de cancelación: timer DURABLE (sobrevive crashes/deploys).
        await workflow.sleep(timedelta(minutes=30))

        # 3) Cobrar dentro de la saga.
        try:
            cargo_id = await workflow.execute_activity(
                cobrar_pago,
                orden,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=REINTENTOS,
            )
        except Exception:
            # COMPENSACIÓN antes de propagar: el mundo queda consistente.
            await workflow.execute_activity(
                liberar_inventario,
                reserva_id,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=REINTENTOS,
            )
            raise

        # 4) Confirmar envío (dos argumentos -> args=[...]).
        envio_id = await workflow.execute_activity(
            confirmar_envio,
            args=[orden, reserva_id],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=REINTENTOS,
        )

        return {
            "estado": "confirmado",
            "reserva_id": reserva_id,
            "cargo_id": cargo_id,
            "envio_id": envio_id,
        }
```

## Por qué cada decisión

- **Cero I/O en el workflow.** `reservar/cobrar/confirmar/liberar` son activities; el `run` solo
  decide el orden, espera y compensa. Por eso es replayable y determinista.
- **`workflow.sleep(30 min)`** no bloquea ningún proceso: es un timer durable. En los tests, el
  time-skipping lo salta al instante.
- **`RetryPolicy`** en cada activity → un timeout transitorio se reintenta (hasta 5 veces). El error
  `TarjetaRechazada` es `non_retryable=True` en `actividades.py`, así que **no** se reintenta y la
  saga compensa de inmediato.
- **Saga:** la compensación (`liberar_inventario`) va **dentro** del `except` y **antes** del `raise`.
  Re-lanzar hace fallar el workflow, pero con el inventario ya liberado: estado consistente, no roto.
- **`args=[orden, reserva_id]`**: `execute_activity` toma un único arg posicional o la lista `args`
  para múltiples; mezclarlos es el error de firma típico.

## Idempotencia (por qué importa aunque el test no lo fuerce)

Temporal entrega las activities **at-least-once**: pueden ejecutarse más de una vez ante reintentos.
Por eso las activities aceptan un identificador estable (`orden.id`) y no duplican efectos. El
`workflow_id` estable (`checkout-<orden>`) da idempotencia a nivel de workflow: un disparo duplicado
con el mismo id es rechazado por Temporal.

## Ejemplo de test propio aceptable (idempotencia de workflow)

```python
def test_workflow_id_duplicado_no_reprocesa():
    orden = Orden(id="C-3", monto=500, tarjeta="ok")
    llamadas, acts = _mocks(rechazar_pago=False)

    async def correr():
        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with Worker(
                env.client, task_queue="tq-dup",
                workflows=[ProcesoCheckoutWorkflow], activities=acts,
            ):
                wid = "checkout-C-3"
                await env.client.execute_workflow(
                    ProcesoCheckoutWorkflow.run, orden, id=wid, task_queue="tq-dup"
                )
                # Segundo disparo con el MISMO id: Temporal lo rechaza/retorna el existente,
                # no vuelve a ejecutar los pasos.
                with pytest.raises(Exception):
                    await env.client.start_workflow(
                        ProcesoCheckoutWorkflow.run, orden, id=wid, task_queue="tq-dup"
                    )

    asyncio.run(correr())
    # Los pasos corrieron UNA sola vez.
    assert llamadas.count("reservar") == 1
```

> Nota: por el `WorkflowIDReusePolicy` por defecto, reusar un id de un workflow ya completado puede
> permitir una nueva corrida; el caso férreo es **mientras está corriendo** (rechazo por id en uso).
> Cualquier test del alumno que demuestre "no se reprocesa dos veces" o "un fallo transitorio se
> reintenta" es aceptable; lo que importa es que **asere comportamiento real**, no `assert True`.

## Rango de soluciones aceptables

- El orden de los kwargs y los valores de la `RetryPolicy` pueden variar; lo esencial es: activities
  para todo I/O, `workflow.sleep`, RetryPolicy presente, y la saga compensando antes del `raise`.
- Devolver un objeto/dataclass en vez de un `dict` es válido si el happy-path test sigue verde (el
  test lee `resultado["estado"]`, así que un dict —o un objeto con acceso por clave— es lo esperado).
- Es válido extraer la compensación a un helper, siempre que se ejecute dentro del `except` y antes
  de propagar.
