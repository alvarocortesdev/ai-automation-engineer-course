"""Paquete `despensa` — fachada del inventario.

Este archivo `__init__.py` marca la carpeta como un PAQUETE y, al re-exportar,
da una fachada limpia: quien use el paquete escribe `from despensa import
resumen_inventario` sin saber en qué módulo vive.

TODO(estudiante): re-exporta aquí `resumen_inventario` y `formatear_lineas`
desde el módulo `despensa.inventario`, para que el test `test_import_desde_paquete`
pase. (Una sola línea de import.)
"""
# TODO(estudiante): añade el import de re-exportación.
