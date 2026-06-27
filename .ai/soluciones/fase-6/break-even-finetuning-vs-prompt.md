---
ejercicio_id: fase-6/break-even-finetuning-vs-prompt
fase: fase-6
sub_unidad: "6.13"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**: el alumno debe corregir su trabajo, no recibir este código. Úsala para detectar
> el error y graduar las pistas.

# Solución de referencia — Break-even fine-tuning vs prompt

## Respuesta canónica (implementación)

```python
from __future__ import annotations


def costo_por_request(prompt_tokens, output_tokens, precio_in, precio_out):
    return (prompt_tokens / 1e6) * precio_in + (output_tokens / 1e6) * precio_out


def costo_total(costo_fijo, costo_req, n_requests):
    return costo_fijo + n_requests * costo_req


def requests_equilibrio_finetuning(costo_entrenamiento, costo_req_baseline, costo_req_ft):
    ahorro = costo_req_baseline - costo_req_ft
    if ahorro <= 0:
        raise ValueError(
            "el modelo fine-tuneado no es mas barato por request: no hay punto de equilibrio"
        )
    return costo_entrenamiento / ahorro
```

## Razonamiento paso a paso

1. **Costo por request: la fórmula por lado.** Cada lado (entrada, salida) a su propio
   precio: `tokens / 1e6 * precio_de_ese_lado`. El `1e6` es porque el pricing viene por
   millón. Misma fórmula de 6.3/6.10, aquí aplicada al prompt largo (baseline) y al corto
   (fine-tuneado).
2. **`costo_total` parametriza el costo fijo.** Baseline: `costo_fijo = 0`. Fine-tuning:
   `costo_fijo = costo_entrenamiento`. Una sola función para ambos → DRY, una sola fuente de
   verdad de "fijo + variable × n".
3. **El equilibrio se divide por el AHORRO, no por el costo total.** Igualamos:
   `n × c_base = costo_entrenamiento + n × c_ft`. Despejando:
   `n × (c_base − c_ft) = costo_entrenamiento`, o sea
   `n = costo_entrenamiento / (c_base − c_ft)`. El denominador es lo que ahorras **por
   request** al acortar el prompt.
4. **Fallar fuerte ante lo imposible.** Si `c_base − c_ft <= 0` (el fine-tuneado cuesta igual
   o más por request), no hay número de requests que recupere el costo fijo → `ValueError`
   explícito, no `ZeroDivisionError` ni un `inf`/negativo silencioso. Es el corazón del
   ejercicio: el fine-tuning **no** es gratis ni siempre más barato.

### Traza del caso del README
- `c_base = 2000/1e6*0.40 + 200/1e6*1.60 = 0.0008 + 0.00032 = 0.00112` USD.
- `c_ft   = 200/1e6*0.60 + 200/1e6*2.40 = 0.00012 + 0.00048 = 0.0006` USD.
- Ahorro por request: `0.00112 − 0.0006 = 0.00052` USD.
- Equilibrio: `26 / 0.00052 = 50_000` requests.
- A **20.000 requests/mes**: baseline `= 20_000 * 0.00112 = 22.40` USD vs fine-tuning
  `= 26 + 20_000 * 0.0006 = 26 + 12 = 38` USD → **gana el baseline** (todavía no se
  amortizó el entrenamiento; falta para los 50.000 del equilibrio).

## Puntos resbalosos (donde el corrector debe mirar)

1. **`/ 1000` en vez de `/ 1e6`**: costo 1000× inflado; `test_costo_por_request_baseline`
   lo atrapa.
2. **Dividir por el costo total del fine-tuneado** en vez de por el ahorro
   `(c_base − c_ft)`: error conceptual; `test_punto_equilibrio_del_readme` falla.
3. **Olvidar el costo fijo** en `costo_total` del lado fine-tuning (devolver solo
   `n * c_ft`): `test_costo_total_finetuning_incluye_entrenamiento` lo revienta.
4. **No manejar ahorro <= 0**: dejar `ZeroDivisionError` o devolver `inf`/negativo →
   `test_si_el_finetuning_no_es_mas_barato_no_hay_equilibrio` y
   `test_ahorro_cero_tampoco_tiene_equilibrio`.
5. **Confundir el ganador a 20.000 requests** en la predicción: por **debajo** del equilibrio
   gana el baseline; el alumno que dice "gana el fine-tuning" no entendió la amortización.

## Rango de soluciones aceptables

- `1_000_000` literal en vez de `1e6` es igual de válido.
- Redondear el equilibrio (`round(...)`) es aceptable; los tests usan `pytest.approx` y
  `round` del lado del test.
- **Profundización opcional (excelente, no requerida):** una función `quien_gana(n, ...)`
  que devuelva `"baseline"` o `"finetuning"` comparando contra el equilibrio; o incorporar
  que el fine-tuning también tiene costo de **ops/mantenimiento** además del entrenamiento.
  No penalizar a quien hace solo lo pedido.
- En `verificacion.md`, cualquier razón no-costo válida cuenta: **formato/estilo/tono
  consistente**, **prompt más corto = menor latencia**, o **comportamiento estrecho repetido**
  que el prompt no logra con suficiente consistencia.
