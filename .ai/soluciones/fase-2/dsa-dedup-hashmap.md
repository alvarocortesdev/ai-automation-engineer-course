---
ejercicio_id: fase-2/dsa-dedup-hashmap
fase: fase-2
sub_unidad: "2.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — De O(n²) a O(n): two-sum con hashmap

## Respuesta canónica

```python
def tiene_dos_que_suman(nums: list[int], objetivo: int) -> bool:
    vistos: set[int] = set()
    for x in nums:
        if (objetivo - x) in vistos:
            return True
        vistos.add(x)
    return False
```

- **Tiempo:** O(n) — un solo recorrido; cada `in` y cada `add` sobre un `set` son O(1) amortizado.
- **Espacio:** O(n) — `vistos` puede llegar a contener los `n` elementos.

## Razonamiento paso a paso

1. **La versión obvia (la que el alumno debe descartar):**
   ```python
   def tiene_dos_que_suman(nums, objetivo):
       for i in range(len(nums)):
           for j in range(i + 1, len(nums)):
               if nums[i] + nums[j] == objetivo:
                   return True
       return False
   ```
   Bucle anidado → **O(n²)** tiempo, O(1) espacio. Correcta, pero lenta.

2. **La idea clave:** en vez de comparar cada par, recorro una vez y por cada `x` pregunto si ya vi su
   **complemento** `objetivo - x`. Si lo vi, hay un par. La pregunta "¿ya lo vi?" es O(1) con un `set`
   (tabla hash), no O(n) como sería con `x in lista`.

3. **El orden importa — preguntar antes de agregar:** se consulta `if (objetivo - x) in vistos` **antes**
   de hacer `vistos.add(x)`. Así un elemento nunca se empareja consigo mismo. Traza de `[1]`, objetivo `2`:
   `x=1`, complemento `1` no está en `vistos` (vacío) → se agrega `1` → fin del bucle → `False`. Correcto:
   un solo `1` no basta. Traza de `[3, 3]`, objetivo `6`: `x=3`, complemento `3` no está → agrega `3`;
   `x=3` (segunda posición), complemento `3` **sí** está → `True`. Correcto: dos posiciones distintas.

4. **El trade-off (lo que mide `NOTAS.md`):** se pasa de O(n²)/O(1) a O(n)/O(n). Se **gasta memoria** (el
   `set`) para **ganar tiempo**. Es el *space–time trade-off*, el más recurrente en DSA.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Agregar antes de preguntar** → empareja un elemento consigo mismo. `[1]` con objetivo `2` daría
   `True` (incorrecto). Es el bug más común; revisa el orden de las dos líneas.
2. **`(objetivo - x) in vistos` con la lista en vez del set** (`in nums`) → reintroduce O(n) interno y
   vuelve a O(n²). Verifica que `vistos` sea un `set`, no una `list`.
3. **`nums.count(...)` o doble índice "optimizado"** que sigue siendo O(n²) — pasa los tests pero no
   cumple el objetivo de complejidad.
4. **Espacio mal reportado:** decir que la solución con `set` es O(1) de espacio. El `set` crece con `n`.
5. **Caso de ceros:** `[0, 4, 3, 0]` con objetivo `0` debe dar `True` (los dos ceros). El algoritmo lo
   maneja: segundo `0` encuentra el primero en `vistos`.

## Rango de soluciones aceptables

- Usar un `dict` `{valor: True}` en vez de `set` es equivalente (mismo O(1) de lookup); no penalizar.
- Construir todo en un solo `return any(...)` con un generador y un `set` acumulado es válido si mantiene
  la semántica de "preguntar antes de agregar" — pero suele ser más enrevesado; aceptar si es correcto.
- Para `NOTAS.md`, vale cualquier redacción que (a) dé tiempo y espacio de **ambas** versiones y (b) nombre
  el trade-off. No se exige la palabra "amortizado", pero el nivel **excelente** sí la usa y reconoce que
  para `n` muy pequeño el O(n²) podría bastar.
- **Variante de control para detectar dependencia-IA:** pedir que explique qué pasa si `vistos` fuera una
  `list` y usara `in`. Quien entendió responde "vuelve a O(n²)"; quien no, se traba.
