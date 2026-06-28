"""Capa gold sin doble conteo — Primero-Sin-IA.

Implementa a mano (sin pandas, sin IA) dos transformaciones de la capa GOLD sobre
un star schema que ya está limpio en la capa silver. NO cambies las firmas ni las
claves de los dicts que devuelves: `test_transformaciones.py` depende de ellas.

──────────────────────────────────────────────────────────────────────────────
EL MODELO (silver, ya limpio y validado)

`lineas`: list[dict] — la tabla de HECHOS a grain de LÍNEA.
    Una fila = una línea de producto de una orden.
    {"orden_id": str, "producto_id": str, "cantidad": int, "monto": int}
    (monto en CLP, ya = cantidad * precio_unitario)

`productos`: list[dict] — la DIMENSIÓN producto (grain: un producto).
    {"producto_id": str, "categoria": str}
    Supón integridad referencial: todo producto_id de `lineas` existe aquí.

`ordenes`: list[dict] — datos a grain de ORDEN (un costo de envío por orden).
    {"orden_id": str, "cliente_id": str, "envio": int}
    (envio en CLP; una orden tiene UN envío, no uno por línea)

──────────────────────────────────────────────────────────────────────────────
CONTRATO

1) ingresos_por_categoria(lineas, productos) -> dict[str, int]
       Une el hecho (línea) con la dimensión producto y suma `monto` por categoría.
       Devuelve {categoria: ingreso_total}. Solo aparecen categorías con ventas.
       Agregación limpia a grain de línea: aquí NO hay trampa de doble conteo.

2) valor_total_por_cliente(lineas, ordenes) -> dict[str, int]
       Valor total que aportó cada cliente = (suma de `monto` de sus líneas)
                                            + (suma de `envio` de sus órdenes,
                                               contando cada orden UNA sola vez).
       Devuelve {cliente_id: valor_total}.

       ⚠️ LA TRAMPA (el corazón del ejercicio): el envío vive a grain de ORDEN.
       Si "aplanas" uniendo cada línea con su orden y luego sumas `envio`, una
       orden con 3 líneas suma su envío 3 veces (FAN-OUT / doble conteo). El
       número resultante parece válido pero está inflado.

       La forma correcta: agrega CADA grain por separado y luego combínalos.
       - monto por cliente: recorre `lineas`, mapea orden_id -> cliente_id (vía
         `ordenes`), suma `monto`.
       - envío por cliente: recorre `ordenes` (cada orden una vez), suma `envio`.
       - suma ambos por cliente.
"""


def ingresos_por_categoria(lineas: list[dict], productos: list[dict]) -> dict[str, int]:
    """Ingresos totales (suma de monto) por categoría de producto. Ver contrato arriba."""
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


def valor_total_por_cliente(lineas: list[dict], ordenes: list[dict]) -> dict[str, int]:
    """Valor total por cliente = monto de sus líneas + envío de sus órdenes (cada orden una vez).

    Cuidado con el fan-out: el envío NO se cuenta una vez por línea. Ver contrato arriba.
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")
