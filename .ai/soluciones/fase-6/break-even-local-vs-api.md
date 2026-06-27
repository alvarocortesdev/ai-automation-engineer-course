---
ejercicio_id: fase-6/break-even-local-vs-api
fase: fase-6
sub_unidad: "6.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**: el alumno debe corregir su trabajo, no recibir este código. Úsala para
> detectar el error y graduar las pistas.

# Solución de referencia — Calculadora del punto de equilibrio local vs API

## Respuesta canónica (implementación)

```python
from __future__ import annotations


def costo_api_por_request(tokens_in, tokens_out, precio_in, precio_out):
    return (tokens_in / 1e6) * precio_in + (tokens_out / 1e6) * precio_out


def costo_api_mensual(requests_mes, tokens_in, tokens_out, precio_in, precio_out):
    return requests_mes * costo_api_por_request(tokens_in, tokens_out, precio_in, precio_out)


def punto_equilibrio_requests(costo_local_mensual, tokens_in, tokens_out, precio_in, precio_out):
    por_request = costo_api_por_request(tokens_in, tokens_out, precio_in, precio_out)
    if por_request == 0:
        raise ValueError("costo por request = 0: una API gratis no tiene punto de equilibrio")
    return costo_local_mensual / por_request
```

## Razonamiento paso a paso

1. **Costo por request: la fórmula por lado.** Cada lado (entrada, salida) se paga a su
   propio precio: `tokens / 1e6 * precio_de_ese_lado`. El `1e6` es porque el pricing viene
   **por millón** de tokens. Es la misma fórmula de 6.3, aquí por request.
2. **Mensual = lineal.** El costo de la API sube linealmente con el uso:
   `requests_mes * costo_por_request`. Reusar `costo_api_por_request` evita duplicar la
   fórmula (DRY) y mantiene una sola fuente de verdad.
3. **El equilibrio es una división.** Local es **costo fijo**: `costo_local_mensual` no
   depende de cuántos requests haces. La API lo iguala cuando
   `requests * costo_por_request == costo_local_mensual`, o sea
   `requests = costo_local_mensual / costo_por_request`. Por debajo gana la API; por
   encima, local.
4. **Fallar fuerte ante lo imposible.** Si el costo por request es 0 (API gratis), no hay
   número de requests que iguale un costo local positivo: la división por cero no tiene
   sentido de negocio → `ValueError` explícito en vez de `ZeroDivisionError` o `inf`
   silencioso.

### Traza del caso del README
- Costo por request: `1000/1e6*0.20 + 1000/1e6*0.80 = 0.0002 + 0.0008 = 0.001` USD.
- Costo local mensual: `1.00 * 730 = 730` USD.
- Equilibrio: `730 / 0.001 = 730_000` requests/mes (~24.000/día).
- A **20.000 requests/mes**: API `= 20_000 * 0.001 = 20` USD vs local `730` USD →
  **gana la API por 36×**. Lección: a volumen bajo, local no compite por costo.

## Puntos resbalosos (donde el corrector debe mirar)

1. **`/ 1000` en vez de `/ 1e6`**: costo 1000× inflado; `test_costo_por_request` lo atrapa.
2. **Un solo precio para ambos lados** (o promediar in/out): pasa de casualidad cuando
   in == out, pero `test_salida_pesa_mas_que_entrada` lo revienta.
3. **Reimplementar la fórmula en `punto_equilibrio_requests`** en vez de reusar
   `costo_api_por_request`: no falla los tests, pero es una señal de que no vio la
   composición; márcalo como deuda de diseño (DRY), no como error de corrección.
4. **No manejar el costo por request 0**: devolver `inf` o dejar reventar
   `ZeroDivisionError` en vez de `ValueError` con mensaje → `test_api_gratis_no_tiene_equilibrio`.
5. **Confundir "por encima del equilibrio" con "API más cara"** en la reflexión: por
   encima del equilibrio la API es **más cara** que local (gana local), no al revés.

## Rango de soluciones aceptables

- `1_000_000` literal en vez de `1e6` es igual de válido.
- Redondear el resultado del equilibrio (`round(...)`) es aceptable; los tests usan
  `pytest.approx` y `round` en el lado del test.
- **Profundización opcional (excelente, no requerida):** una cuarta función
  `quien_gana(requests_mes, costo_local_mensual, ...)` que devuelva `"api"` o `"local"`
  comparando contra el equilibrio; o incorporar que la API también puede tener su propio
  costo de latencia/ops. No penalizar a quien hace solo lo pedido.
- En `verificacion.md`, cualquier razón no-costo válida cuenta: **privacidad/cumplimiento**
  (datos que no pueden salir), **latencia** (sin round-trip de red), **disponibilidad/
  control** (no depender de un proveedor externo).
