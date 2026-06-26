"""Mini-pipeline legado de pedidos — instrumentado con print (antipatrón).

Tu trabajo (ver README): reemplazar TODOS los print() por logging estructurado
con NIVELES (debug/info/warning) y CONTEXTO (extra={"pedido_id", "correlation_id"}),
y completar configurar_logging().

NO cambies la lógica de negocio (validación + cantidad*precio): solo cambias la
INSTRUMENTACIÓN. La firma y el valor de retorno de procesar_pedidos NO cambian.
"""

# TODO 1: crea aquí un logger por módulo  ->  logger = logging.getLogger(__name__)
#         (se OBTIENE en el módulo; se CONFIGURA afuera, en configurar_logging.)


def procesar_pedidos(pedidos, correlation_id):
    procesados = []
    for pedido in pedidos:
        print("DEBUG procesando pedido", pedido.get("id"))         # TODO -> logger.debug
        cantidad = pedido.get("cantidad", 0)
        precio = pedido.get("precio", 0)
        if cantidad <= 0 or precio <= 0:
            print("OJO pedido invalido, lo omito:", pedido.get("id"))  # TODO -> logger.warning
            continue
        total = cantidad * precio
        print("total calculado", total)                            # TODO -> logger.debug
        procesados.append({"id": pedido.get("id"), "total": total})
        print("pedido procesado ok", pedido.get("id"))             # TODO -> logger.info
    return procesados


def configurar_logging(nivel=None):
    """Configura el logging UNA sola vez (handler a stdout + nivel dado).

    Idealmente con un formateador JSON (ver lección 4.6). Llamar desde el
    __main__, NUNCA dentro de procesar_pedidos.
    """
    # TODO 2: implementa la configuración (StreamHandler a sys.stdout, level=nivel).
    raise NotImplementedError("completa configurar_logging() (ver README)")


if __name__ == "__main__":
    pedidos = [
        {"id": 1, "cantidad": 2, "precio": 5000},
        {"id": 2, "cantidad": 0, "precio": 9990},   # inválido: se omite
        {"id": 3, "cantidad": 1, "precio": 7000},
    ]
    # Tras tu refactor: configurar_logging(logging.INFO) y verás el debug DESAPARECER
    # sin tocar el código (el off-switch que print nunca tuvo).
    print(procesar_pedidos(pedidos, correlation_id="req-demo"))
