# Casos a clasificar

> Estos son 8 artefactos de un codebase real (un backend de e-commerce en Python).
> Para cada uno decidirás en `decisiones.md` si merece **test unitario**, **no test**,
> o **test de integración**, con una frase de justificación. No los ejecutes: razona.

## A — Getter trivial

```python
class Usuario:
    def __init__(self, nombre: str):
        self._nombre = nombre

    @property
    def nombre(self) -> str:
        return self._nombre
```

## B — Wrapper de una librería externa

```python
import requests

def obtener_usuario(user_id: int) -> dict:
    # Solo reenvía a requests; no hay lógica propia.
    return requests.get(f"https://api.ejemplo.com/users/{user_id}").json()
```

## C — Cálculo de IVA con tramos (lógica de negocio)

```python
def calcular_iva(monto: float, tipo: str) -> float:
    # Productos básicos exentos; alcohol con impuesto adicional; resto IVA normal.
    if tipo == "basico":
        return 0.0
    if tipo == "alcohol":
        return monto * 0.19 + monto * 0.205   # IVA + ILA
    return monto * 0.19
```

## D — Línea de logging

```python
logger.info("Orden %s creada para el usuario %s", orden.id, usuario.id)
```

## E — DTO autogenerado

```python
# Generado por el cliente OpenAPI a partir del schema del proveedor.
# NO se edita a mano; se regenera con cada cambio del contrato.
class PagoResponse(BaseModel):
    id: str
    estado: str
    monto: int
    creado_en: datetime
```

## F — Parser de fechas propio

```python
def parse_fecha_chilena(texto: str) -> date:
    # Acepta "DD-MM-AAAA"; lanza ValueError si el formato o la fecha son inválidos.
    dia, mes, anio = texto.split("-")
    return date(int(anio), int(mes), int(dia))
```

## G — Bloque de arranque

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## H — Endpoint orquestador

```python
@app.post("/ordenes")
def crear_orden(payload: CrearOrden):
    # Orquesta tres servicios: reserva stock, cobra, notifica.
    inventario.reservar(payload.items)
    pago = pasarela.cobrar(payload.usuario_id, payload.total)
    notificaciones.enviar(payload.usuario_id, "orden_creada")
    return {"orden_id": pago.referencia}
```
