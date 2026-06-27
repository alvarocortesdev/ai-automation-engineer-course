---
ejercicio_id: fase-5/estimador-de-costos
fase: fase-5
sub_unidad: "5.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una solución de referencia para
> graduar pistas y detectar qué se le escapó, **nunca** para entregarla.

# Solución de referencia — Estimador de costos cloud

## Implementación

```python
def estimar_costo_mensual(arquitectura: dict, precios: dict) -> dict:
    # COMPUTE: suma sobre la lista; cada recurso cobra por horas ENCENDIDO.
    # Un recurso always-on (730 h) pesa mucho más que uno scale-to-zero (pocas h).
    compute = sum(
        r["usd_por_hora"] * r["horas_encendido"]
        for r in arquitectura["compute"]
    )

    # STORAGE: lineal por GB-mes. Casi siempre la línea más barata.
    storage = arquitectura["storage_gb"] * precios["storage_usd_por_gb_mes"]

    # EGRESS: el único con truco. Solo se cobra POR ENCIMA del tramo gratis.
    # max(0, ...) evita cobrar (y evita negativos) cuando se sirve menos que el tramo gratis.
    facturable = max(0.0, arquitectura["egress_gb"] - precios["egress_gratis_gb"])
    egress = facturable * precios["egress_usd_por_gb"]

    # REQUESTS: lineal por millón de invocaciones.
    requests = arquitectura["requests_millones"] * precios["usd_por_millon_requests"]

    total = compute + storage + egress + requests

    return {
        "compute": compute,
        "storage": storage,
        "egress": egress,
        "requests": requests,
        "total": total,
    }
```

## Por qué así (lo que el alumno debe poder defender)

- **`max(0, egress - gratis)`** es el detalle que separa una estimación útil de una que miente. Sin
  el `max`, servir 5 GB daría un egress "negativo" que abarataría falsamente el total; sin descontar
  el tramo gratis, se sobre-estima y se asusta sin razón.
- **El compute domina el caso de ejemplo:** 34.85 de un total de 35.48 viene de compute, y de ese,
  **32.85 es el NAT Gateway always-on** (0.045 × 730). Es la lección concreta: un recurso encendido
  24/7 cuesta aunque no pase tráfico. Si el alumno no sabe señalar esto, no entendió el ejercicio.
- **El `total` no es un cálculo aparte:** es la suma del desglose. Calcularlo por separado invita a
  que diverja.
- **No redondear:** los tests usan `pytest.approx`. Redondear dentro de la función es innecesario y
  puede romper la tolerancia.

## Caso propio esperado (ejemplo de "excelente")

Un test que demuestre una **decisión de costo**, no solo otros números:

```python
def test_quitar_nat_always_on_baja_el_total():
    precios = PRECIOS
    con_nat = _arq(compute=[
        {"nombre": "api", "usd_por_hora": 0.02, "horas_encendido": 100},
        {"nombre": "nat", "usd_por_hora": 0.045, "horas_encendido": 730},
    ])
    sin_nat = _arq(compute=[{"nombre": "api", "usd_por_hora": 0.02, "horas_encendido": 100}])
    ahorro = (estimar_costo_mensual(con_nat, precios)["total"]
              - estimar_costo_mensual(sin_nat, precios)["total"])
    assert ahorro == pytest.approx(32.85)   # el NAT always-on era casi todo el costo
```

## Notas para el corrector

- El verde de los 10 tests es necesario pero no suficiente: pide que el alumno **señale qué línea
  domina** el total del caso de ejemplo y por qué.
- Si pasa los tests pero cobra el egress completo en su explicación oral (contradice su código), es
  señal de copia: el código y la comprensión no calzan.
- Premiar (excelente) el caso propio que ilustra una decisión (quitar el NAT, escenario viral con
  egress dominante) por encima del que solo repite aritmética.
