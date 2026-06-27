---
ejercicio_id: fase-6/similitud-coseno-a-mano
fase: fase-6
sub_unidad: "6.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Similitud coseno desde cero

## Respuesta canónica

```python
import math


def producto_punto(a, b):
    if len(a) != len(b):
        raise ValueError(f"Vectores de distinto largo: {len(a)} vs {len(b)}")
    return sum(x * y for x, y in zip(a, b))


def magnitud(a):
    return math.sqrt(sum(x * x for x in a))


def similitud_coseno(a, b):
    mag_a = magnitud(a)
    mag_b = magnitud(b)
    if mag_a == 0 or mag_b == 0:
        raise ValueError("El vector cero no tiene dirección: coseno indefinido")
    return producto_punto(a, b) / (mag_a * mag_b)


def rankear(consulta, documentos):
    puntajes = [
        (i, similitud_coseno(consulta, doc)) for i, doc in enumerate(documentos)
    ]
    return sorted(puntajes, key=lambda t: t[1], reverse=True)
```

## Razonamiento paso a paso

1. **`producto_punto`** valida el largo **primero** (si difieren, `zip` truncaría en silencio y daría un
   resultado mal sin avisar), luego `sum(x*y for x, y in zip(a, b))`.
2. **`magnitud`** = raíz de la suma de cuadrados. `x * x` evita el costo simbólico de `x ** 2` y es
   igual de claro.
3. **`similitud_coseno`** calcula las dos magnitudes **antes** de dividir y corta con `ValueError` si
   alguna es 0. El vector cero no tiene dirección, así que el coseno no está definido; devolver 0.0
   sería mentir (0 significa "perpendicular", no "indefinido").
4. **`rankear`** usa `enumerate` para conservar el índice original, arma tuplas `(indice, similitud)` y
   ordena por el segundo elemento en orden descendente (`reverse=True`). Reusa `similitud_coseno`.

## Verificación numérica (caso de la lección)

- `similitud_coseno([7,1],[9,1])` = `64 / (√50 · √82)` = `64 / 64.03` ≈ **0.9995**.
- `similitud_coseno([7,1],[8,0])` = `56 / (√50 · 8)` = `56 / 56.57` ≈ **0.990**.
- `similitud_coseno([7,1],[1,9])` = `16 / (√50 · √82)` = `16 / 64.03` ≈ **0.250**.
- `rankear([7,1], [[1,9],[9,1],[8,0]])` → `[(1, 0.9995), (2, 0.990), (0, 0.250)]`.

## Puntos resbalosos (donde el corrector debe mirar)

1. **División por cero sin proteger** (error #1): el vector cero debe lanzar `ValueError`, no
   `ZeroDivisionError` ni un 0.0 silencioso.
2. **No validar largos**: `zip` trunca al más corto y produce un coseno "válido" pero incorrecto.
3. **Dividir por `|a| + |b|`** en vez de `|a| · |b|`: error de fórmula frecuente.
4. **`rankear` que pierde el índice** o que ordena ascendente.
5. **Reimplementar producto punto y magnitud dentro de `similitud_coseno`** en vez de reusarlos:
   funciona, pero es menos limpio (no descalifica; es la diferencia competente vs excelente).

## Rango de soluciones aceptables

- Usar `math.hypot(*a)` para la magnitud es **excelente** (es exactamente la norma euclidiana y evita
  overflow); válido si el alumno sabe qué hace.
- Ordenar con `key=lambda t: -t[1]` en vez de `reverse=True` es equivalente.
- Devolver una lista de objetos/diccionarios en `rankear` en vez de tuplas **no** pasa los tests tal
  como están escritos; si el alumno cambió la firma, marcarlo (el contrato pide tuplas) pero reconocer
  si la lógica de ordenamiento es correcta.
- `numpy` (`np.dot`, `np.linalg.norm`) da el resultado correcto pero **contradice el enunciado**
  ("Python puro, a mano"): no cuenta como haber hecho el ejercicio; pedir la versión a mano.
