---
ejercicio_id: fase-0/spec-first-divisor-cuenta
fase: fase-0
sub_unidad: "0.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Spec-first: divisor de cuenta

## Mini-spec esperada (forma canónica)

Lo central del ejercicio es que **la spec exista y sea anterior al código**. Una spec competente se ve así:

| Parte | Decisión |
|---|---|
| **Entrada** `total` | `int` o `float`, monto en pesos. Debe ser `>= 0`. |
| **Entrada** `personas` | `int`, número de personas. Debe ser `>= 1`. |
| **Salida** | `float`: `total / personas`, sin redondear. |
| **Borde — total cero** | `total == 0` → `0.0` (cuenta gratis, válida). |
| **Borde — división no exacta** | `100, 3` → `33.333...` (no se redondea). |
| **Borde — total negativo** | `total < 0` → `ValueError`. |
| **Borde — cero personas** | `personas == 0` → `ValueError` (no `ZeroDivisionError`). |
| **Borde — personas negativas** | `personas < 0` → `ValueError`. |
| **Decisión de diseño** | No redondeo: redondear a peso es responsabilidad de quien muestra el número. Alternativa válida si se documenta: redondear con `round(x, 2)`. |

## Código de referencia

```python
def dividir_cuenta(total, personas):
    # 1) VALIDAR antes de dividir: si dividiéramos primero, personas == 0
    #    reventaría con ZeroDivisionError antes de nuestro mensaje claro.
    if personas <= 0:
        raise ValueError("personas debe ser un entero mayor o igual a 1")
    if total < 0:
        raise ValueError("total no puede ser negativo")
    # 2) Reparto en partes iguales, sin redondear (decisión de diseño documentada).
    return total / personas
```

Las 7 aserciones de `test_dividir_cuenta.py` pasan con este cuerpo (verificado).

## Por qué cada decisión

1. **Validar antes de dividir.** El orden no es cosmético: `100 / 0` lanza `ZeroDivisionError`
   *antes* de llegar a cualquier `raise` que pongas después. Validar primero te deja controlar el
   mensaje y el tipo de error. Es el punto que más separa una entrega `competente` de una `en-progreso`.
2. **`personas <= 0` en una sola guarda.** Cubre cero y negativos juntos. Un alumno que escribe dos
   `if` separados (uno `== 0`, otro `< 0`) también es correcto; agrupar es más limpio, no obligatorio.
3. **`total == 0` es válido, no error.** Una cuenta de 0 repartida da 0.0 por persona. Marcar el cero
   como inválido es un error de diseño (confunde "cero" con "negativo").
4. **Sin redondeo.** Mantiene el cálculo puro y testeable con `pytest.approx`. Redondear es una
   decisión legítima **si se documenta en la spec**; lo que no es aceptable es redondear sin haberlo
   pensado y luego sorprenderse de que un test falle.

## Rango de soluciones aceptables

- Mensajes de `ValueError` con cualquier redacción clara cuentan como `competente`.
- Redondear el resultado **es aceptable** sólo si la spec lo declara como decisión de diseño *y* los
  tests propios del alumno reflejan ese contrato. Si redondea pero deja los tests de base intactos, los
  romperá: eso es señal de que codeó sin spec.
- Validar con `if not isinstance(personas, int)` adicional es un extra de nivel `excelente`, no exigido.
- Aceptar la spec en prosa (no tabla) si cubre entradas, salida y los bordes con la misma cobertura.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Spec ausente o escrita después.** Si no hay `spec.md`, o se nota que describe el código ya hecho
   (mismas palabras, ningún borde que el código no maneje), falla el objetivo O1 aunque el código pase.
2. **Dividir antes de validar.** El síntoma típico: `dividir_cuenta(100, 0)` lanza `ZeroDivisionError`
   en vez de `ValueError`. Su test `test_cero_personas_lanza_value_error` igual pasa (porque
   `ZeroDivisionError` es subclase de `ArithmeticError`, no de `ValueError`) → en realidad **falla**.
   Verificar que sea `ValueError`.
3. **Tratar `total == 0` como inválido.** Rompe `test_total_cero_es_valido`.
4. **Test propio trivial** (otro caso ya cubierto) en vez de un borde nuevo de su spec.
