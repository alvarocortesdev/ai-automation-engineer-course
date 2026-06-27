---
ejercicio_id: fase-6/costo-llamada-llm
fase: fase-6
sub_unidad: "6.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**: el alumno debe corregir su trabajo, no recibir este código. Úsala para
> detectar el error y graduar las pistas.

# Solución de referencia — Calculadora de costo y elección de modelo

## Respuesta canónica (implementación)

```python
from __future__ import annotations


def calcular_costo(tokens_entrada, tokens_salida, modelo, precios):
    if modelo not in precios:
        raise ValueError(f"modelo desconocido: {modelo!r}")
    p = precios[modelo]
    return (tokens_entrada / 1e6) * p["in"] + (tokens_salida / 1e6) * p["out"]


def modelo_mas_barato(tokens_entrada, tokens_salida, precios):
    if not precios:
        raise ValueError("la tabla de precios está vacía")
    return min(
        precios,
        key=lambda m: calcular_costo(tokens_entrada, tokens_salida, m, precios),
    )
```

## Razonamiento paso a paso

1. **La fórmula es lineal y por lado.** Cada lado (entrada, salida) se paga a su propio
   precio: `tokens / 1e6 * precio_de_ese_lado`. El total es la suma. El `1e6` es porque
   el pricing viene **por millón** de tokens.
2. **Fallar fuerte ante lo desconocido.** Un modelo que no está en la tabla no tiene
   precio: devolver `0` factura mal en silencio. Lanzar (`KeyError` natural por
   `precios[modelo]`, o `ValueError` explícito) es lo correcto. La solución de
   referencia lo hace explícito para dar un mensaje útil.
3. **`modelo_mas_barato` reusa `calcular_costo`.** No reimplementa la fórmula: evalúa el
   costo de cada modelo con la misma carga y se queda con el mínimo. `min(iterable,
   key=...)` itera las **claves** del dict (los nombres de modelo) y compara por costo.
4. **El más barato depende de la carga.** No es un modelo fijo: con mucha salida gana el
   barato-para-escribir; con mucha entrada gana el barato-para-leer. Por eso `key`
   recibe los tokens.

### Traza del caso del README (10 000 in / 2 000 out)
- opus: 10000/1e6·5 + 2000/1e6·25 = 0.05 + 0.05 = **0.10**
- sonnet: 0.03 + 0.03 = **0.06**
- haiku: 0.01 + 0.01 = **0.02** → **el más barato es haiku** (5x menos que opus).

## Puntos resbalosos (donde el corrector debe mirar)

1. **`/ 1000` en vez de `/ 1e6`**: costo 1000x inflado. El test de Opus (0.10) lo atrapa.
2. **Usar un solo precio para ambos lados** (o promediar `in` y `out`): pasa por
   casualidad cuando in == out, pero `test_salida_pesa_mas_que_entrada` lo revienta.
3. **No lanzar ante modelo desconocido**: si la implementación usa `.get(modelo, {})` y
   luego `{}.get("in", 0)`, devuelve 0 en silencio — `test_modelo_desconocido_falla` lo
   atrapa.
4. **`modelo_mas_barato` que compara `precios[m]["out"]`** (el precio fijo) en vez del
   costo real para la carga: falla `test_mas_barato_depende_de_la_proporcion_in_out`.
5. **No manejar la tabla vacía**: `min([])` lanza `ValueError` por su cuenta, pero un
   mensaje propio es más claro; cualquiera de los dos pasa el test.

## Rango de soluciones aceptables

- Redondear el resultado (`round(..., 6)`) es aceptable; los tests usan `pytest.approx`.
- `modelo_mas_barato` con un bucle explícito que lleve el mínimo (en vez de `min(...,
  key=...)`) es igual de válido si produce el mismo resultado y reusa `calcular_costo`.
- Lanzar `KeyError` (dejando que `precios[modelo]` falle solo) en vez de `ValueError`
  explícito es válido: el test acepta ambas (`pytest.raises((KeyError, ValueError))`).
- **Profundización opcional (excelente, no requerida):** una variante que también
  devuelva el **ahorro** vs. el modelo más caro, o que acepte un umbral de calidad
  mínima por modelo (anticipo de model routing con evals, 6.9). No penalizar a quien
  hace solo lo pedido.
