---
ejercicio_id: fase-6/ruteo-y-medidor-costo
fase: fase-6
sub_unidad: "6.16"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de medir**: el
> alumno debe corregir su trabajo, no recibir este código. Úsala para detectar el error y graduar
> las pistas.

# Solución de referencia — Medidor de costo en vivo + router de modelos

## Respuesta canónica (implementación)

```python
from __future__ import annotations


def costo_usd(usage, precio_in, precio_out):
    M = 1_000_000
    costo_in = (usage.input_tokens / M) * precio_in * 1.00
    costo_read = (usage.cache_read_input_tokens / M) * precio_in * 0.10
    costo_write = (usage.cache_creation_input_tokens / M) * precio_in * 1.25
    costo_out = (usage.output_tokens / M) * precio_out
    return costo_in + costo_read + costo_write + costo_out


def rutear_modelo(dificultad, escalones):
    if not escalones:
        raise ValueError("escalones vacío")
    for techo, modelo in escalones:          # de menor a mayor capacidad
        if dificultad <= techo:              # el borde exacto entra
            return modelo
    return escalones[-1][1]                   # fuera de rango -> el más capaz


def costo_mensual(trafico, escalones, precios):
    por_modelo = {}
    total = 0.0
    for req in trafico:
        modelo = rutear_modelo(req.dificultad, escalones)   # reusa el router
        p = precios[modelo]
        c = costo_usd(req.usage, p["in"], p["out"])         # reusa el medidor
        por_modelo[modelo] = por_modelo.get(modelo, 0.0) + c
        total += c
    return {"total": total, "por_modelo": por_modelo}
```

## Razonamiento paso a paso

1. **Tres tarifas de input, no una.** Cada categoría de token de entrada se paga distinto:
   fresco a `precio_in`, cache read a `precio_in·0.1`, cache write a `precio_in·1.25`. El error
   #1 es sumar `cache_read` a `input_tokens` y cobrarlo a 1× — eso borra el ahorro del cache del
   número. La solución calcula las cuatro componentes por separado y suma.
2. **El `1e6` es porque el pricing viene por millón.** Dividir por 1000 da un costo 1000× inflado.
3. **El router itera de barato a caro.** Devuelve el **primero** cuyo `techo >= dificultad` (el
   `<=` hace que el borde exacto entre en su escalón). Si ninguno cubre, el último (más capaz).
   `escalones` vacío lanza `ValueError` antes de iterar.
4. **`costo_mensual` reusa las dos funciones.** No reimplementa la fórmula: rutea, busca el precio
   del modelo elegido, llama a `costo_usd`, y acumula en un dict por modelo + un total. El desglose
   por modelo es lo que sirve para decir "el 80% del gasto es Opus, ahí hay que optimizar".

### Traza de los casos del README
- Costo opus (input 2000, cache_read 10000, output 500):
  `(2000/1e6)·5 + (10000/1e6)·5·0.1 + (500/1e6)·25 = 0.010 + 0.005 + 0.0125 = `**`0.0275`**.
  Si los 10000 fueran fresco: `(12000/1e6)·5 + (500/1e6)·25 = 0.060 + 0.0125 = `**`0.0725`** (el
  cache read ahorró ~USD 0.045 en esa request).
- Ruteo con `[(0.3,"haiku"),(0.7,"sonnet"),(1.0,"opus")]`: `0.3`→**haiku** (borde exacto),
  `0.71`→**opus**, `1.4`→**opus** (fuera de rango → último).

## Puntos resbalosos (donde el corrector debe mirar)

1. **`cache_read` a 1×**: `test_cache_read_cuesta_un_decimo` y `test_cache_read_es_mas_barato...` lo atrapan.
2. **`cache_write` sin el 1.25×** (tratado como read o como fresco): `test_cache_write_tiene_premium` lo atrapa.
3. **`<` en vez de `<=` en el router**: `test_ruteo_borde_exacto_entra_en_el_escalon` lo atrapa (0.3 caería en sonnet).
4. **`costo_mensual` que no acumula por modelo del mismo tipo**: `test_costo_mensual_agrega_requests_del_mismo_modelo` lo atrapa.
5. **Reimplementar la fórmula en `costo_mensual`**: pasa los tests pero es duplicación; marcar como C3 en-progreso/competente según legibilidad.

## Rango de soluciones aceptables

- Multiplicar `costo_in` por `1.00` o no es indiferente (es lo mismo); lo importante es que las otras tres tarifas usen 0.1 / 1.25 / precio_out.
- `rutear_modelo` con `min(...)` por costo en vez de escalones por dificultad **no** es lo pedido (eso es el `modelo_mas_barato` de 6.3, que ignora la calidad/dificultad); aquí la decisión es por dificultad. Marcar si confunde ambos.
- `costo_mensual` con `collections.defaultdict(float)` en vez de `dict.get` es igual de válido.
- **Profundización opcional (excelente, no requerida):** una variante que también devuelva la latencia p95 estimada por modelo, o el ahorro vs. "todo a Opus". No penalizar a quien hace solo lo pedido.
