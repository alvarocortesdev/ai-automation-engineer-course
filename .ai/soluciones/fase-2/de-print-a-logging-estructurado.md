---
ejercicio_id: fase-2/de-print-a-logging-estructurado
fase: fase-2
sub_unidad: "2.12"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — De print-spam a logging estructurado (niveles + contexto)

> El reto no es "que compile": es **clasificar bien cada mensaje por nivel**, **mover el
> contexto a `extra=`** y **centralizar la configuración**. La lógica de negocio no se
> toca. La comprensión vive en `por-que.md`.

## `solucion.py` canónico

```python
"""Mini-pipeline de pedidos — instrumentado con logging estructurado."""

import json
import logging
import sys

logger = logging.getLogger(__name__)   # se OBTIENE en el módulo; se configura afuera


def procesar_pedidos(pedidos, correlation_id):
    procesados = []
    for pedido in pedidos:
        pedido_id = pedido.get("id")
        ctx = {"pedido_id": pedido_id, "correlation_id": correlation_id}
        logger.debug("procesando pedido", extra=ctx)            # detalle interno
        cantidad = pedido.get("cantidad", 0)
        precio = pedido.get("precio", 0)
        if cantidad <= 0 or precio <= 0:
            logger.warning("pedido inválido, se omite", extra=ctx)   # anomalía recuperable
            continue
        total = cantidad * precio
        logger.debug("total calculado", extra={**ctx, "total": total})
        procesados.append({"id": pedido_id, "total": total})
        logger.info("pedido procesado", extra={**ctx, "total": total})  # ciclo de vida
    return procesados


class JsonFormatter(logging.Formatter):
    """Formateador JSON mínimo: lee el contexto de `extra=` con getattr."""

    def format(self, record):
        datos = {
            "nivel": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "pedido_id": getattr(record, "pedido_id", None),
            "correlation_id": getattr(record, "correlation_id", "-"),
        }
        return json.dumps(datos, ensure_ascii=False)


def configurar_logging(nivel=logging.INFO):
    """Configura el logging UNA sola vez: handler a stdout + nivel dado."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=nivel, handlers=[handler])


if __name__ == "__main__":
    configurar_logging(logging.INFO)   # con INFO, el debug DESAPARECE sin tocar el código
    pedidos = [
        {"id": 1, "cantidad": 2, "precio": 5000},
        {"id": 2, "cantidad": 0, "precio": 9990},   # inválido: se omite
        {"id": 3, "cantidad": 1, "precio": 7000},
    ]
    resultado = procesar_pedidos(pedidos, correlation_id="req-demo")
    logger.info("pipeline terminado",
                extra={"pedido_id": None, "correlation_id": "req-demo",
                       "total": sum(p["total"] for p in resultado)})
```

> Nota sobre el `__main__`: lo único intocable es que **no quede ningún `print` de
> instrumentación** dentro de `procesar_pedidos` (que es lo que `capsys` vigila al
> importar el módulo). El bloque `main` no lo ejecutan los tests (importan la función),
> así que un `print(resultado)` ahí no rompería nada — pero la versión idiomática loguea.

## Por qué cada nivel
| Mensaje original (`print`) | Nivel | Razón |
|---|---|---|
| "DEBUG procesando pedido" | `debug` | detalle interno; ruido en prod, se filtra con nivel `INFO`. |
| "OJO pedido invalido, lo omito" | `warning` | anomalía **recuperable** (la ejecución sigue); no es `error` (no falla) ni `info` (no es rutina). |
| "total calculado" | `debug` | detalle de cálculo; solo útil al diagnosticar. |
| "pedido procesado ok" | `info` | evento de ciclo de vida; lo que quieres ver en prod en nivel normal. |

## Verificación contra los tests (todos verdes)
- `test_logica_intacta` → `[{"id": 1, "total": 10000}, {"id": 3, "total": 7000}]`: la lógica (`cantidad*precio`, validación, retorno) no cambió.
- `test_no_quedan_prints` (capsys) → `stdout` vacío al llamar `procesar_pedidos`: cero `print` dentro de la función.
- `test_pedido_valido_emite_info_con_contexto` (caplog) → hay un record `INFO` con `pedido_id` y `correlation_id` en `extra=`.
- `test_pedido_invalido_emite_warning` (caplog) → el inválido produce `WARNING` con `pedido_id`, y la lista sale vacía.
- `test_detalle_interno_va_en_debug` (caplog) → hay records `DEBUG` (procesando/total).

> `caplog` captura porque el logger **propaga** (default). Si el alumno puso
> `logger.propagate = False`, los tests quedan rojos: es un error a marcar, no a "tolerar".

## `por-que.md` de referencia (3 razones, lo esperado)
1. **Niveles filtrables (off-switch):** `print` siempre se imprime; `logger.debug(...)` se silencia subiendo el nivel a `INFO` en config, **sin editar ni redeployar**. En prod ves `INFO+`; al diagnosticar, bajas a `DEBUG`.
2. **Contexto estructurado:** `extra={"pedido_id": ..., "correlation_id": ...}` deja cada línea filtrable por campo (seguir **un** pedido por todo el sistema). `print` mezcla todo en texto plano: no se indexa, no se filtra.
3. **Routing central:** decides **una vez** a dónde van los logs (stdout, archivo, colector) y en qué formato (JSON). `print` siempre va a `stdout` y se pierde en un servidor. Bonus: un `print` en una **librería importada** contamina la salida de quien la usa — es un bug de cortesía.

> Conexión con Fase 5 (lo que sube de nota): el `correlation_id` es el mismo hilo que en
> observabilidad conecta logs ↔ **trazas** (OpenTelemetry); en Fase 6 deja seguir la traza
> del call-chain de un agente paso a paso (tokens/latencia/costo).

## Puntos resbalosos (donde el corrector debe mirar)
1. **Todo en `info`.** El reparto de niveles es el corazón del ejercicio; si "procesando"/"total" quedan en `info`, perdió el sentido de filtrar el ruido. C1 en-progreso como mucho.
2. **Contexto interpolado en el mensaje** (`f"pedido {id}"`) en vez de `extra=`: no es estructurado; `getattr(record, "pedido_id", ...)` daría `None`. C2 incompleto.
3. **`configurar_logging` dentro de `procesar_pedidos`** o con `basicConfig` llamado en cada iteración: la config va una sola vez en el `main`.
4. **`logger.propagate = False`** → `caplog` no ve nada (tests rojos). Default correcto: propaga.
5. **Tocar la lógica** (cambiar `cantidad*precio`, el retorno o la validación): fuera de alcance; `test_logica_intacta` lo caza.
6. **El inválido como `error`** o lanzando excepción: es recuperable → `warning`.

## Rango de soluciones aceptables
- **Sin `JsonFormatter` propio**, solo `getLogger` + `extra=` + `StreamHandler` con formato por defecto: **competente** (el JSON es el "excelente", no el piso).
- **`python-json-logger` o `structlog`** en vez del formateador a mano: **excelente** (es lo idiomático en prod).
- **`extra={**ctx}`** o construir el dict en cada log: ambos válidos mientras lleven `pedido_id` y `correlation_id`.
- **`dictConfig`** en vez de `basicConfig`: válido y más realista para apps grandes.
- Lo que **no** es aceptable: dejar cualquier `print` dentro de `procesar_pedidos`; meter el contexto en el texto; `propagate=False`; un solo nivel para todo; cambiar la lógica o el valor de retorno.
