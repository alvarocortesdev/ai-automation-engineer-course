---
ejercicio_id: fase-6/idp-confianza-gate
fase: fase-6
sub_unidad: "6.11"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**: el alumno debe corregir su trabajo, no recibir este código. Úsala para
> detectar el error y graduar las pistas.

# Solución de referencia — El gate de confianza + validación de un IDP

## Respuesta canónica (implementación)

```python
from __future__ import annotations


def clasificar_campos(campos, umbral):
    auto, revisar = [], []
    for nombre, datos in campos.items():
        conf = datos.get("confidence")
        if conf is None or conf < umbral:
            revisar.append(nombre)
        else:
            auto.append(nombre)
    return {"auto": auto, "revisar": revisar}


def total_cuadra(items, total_declarado, tolerancia=0.01):
    suma = sum(item["monto"] for item in items)
    return abs(suma - total_declarado) <= tolerancia


def decidir_procesamiento(doc, umbral, tolerancia=0.01):
    motivos = []
    clasificados = clasificar_campos(doc["campos"], umbral)
    for nombre in clasificados["revisar"]:
        motivos.append(f"campo '{nombre}' bajo el umbral de confianza")
    if not total_cuadra(doc["items"], doc["total_declarado"], tolerancia):
        motivos.append("el total declarado no cuadra con la suma de las líneas")
    accion = "auto" if not motivos else "revision_humana"
    return {"accion": accion, "motivos": motivos}
```

## Razonamiento paso a paso

1. **El gate es un `>=` con cuidado del `None`.** `confidence == umbral` se acepta (la
   regla documentada es `>= umbral`), así que la condición de *revisar* es estrictamente
   `conf < umbral`. El caso resbaloso es `conf is None`: un campo sin confidence no es
   "confianza 0", es *desconocido* → va a revisión. Hay que chequear `None` **antes** de
   comparar, o `None < umbral` revienta con `TypeError`.
2. **El orden se preserva** porque iteramos `campos.items()` (dict ordenado por
   inserción) y vamos agregando a las listas en ese orden.
3. **`total_cuadra` compara con tolerancia, no con `==`.** Los montos son floats;
   `0.1 + 0.2` no es exactamente `0.3`. `abs(suma - total) <= tolerancia` es la forma
   correcta de comparar floats. La tolerancia por defecto (0.01 = un centavo) es razonable
   para montos en pesos/dólares.
4. **`decidir_procesamiento` compone, no reimplementa.** Llama a `clasificar_campos` para
   los motivos de confianza y a `total_cuadra` para la aritmética. La acción es `"auto"`
   **solo** si no hay ningún motivo (lista vacía). Se **acumulan** los motivos (no return
   temprano) para que el humano vea todo lo que debe revisar.

### Traza de los 3 casos del README (umbral 0.90, tolerancia 0.01)
- **Caso A:** todos los campos ≥ 0.90 (revisar=[]) y 60.000+30.000=90.000 cuadra →
  `{"accion": "auto", "motivos": []}`.
- **Caso B:** `Total` 0.71 &lt; 0.90 → revisar=["Total"]; total cuadra → 1 motivo →
  `revision_humana` ("campo 'Total' bajo el umbral...").
- **Caso C:** todos los campos ≥ 0.90 (revisar=[]) pero 90.000 ≠ 100.000 → 1 motivo →
  `revision_humana` ("el total declarado no cuadra..."). **Este es el caso clave:** el
  gate de confianza solo lo habría dejado pasar; la validación cruzada lo atrapa.

## Puntos resbalosos (donde el corrector debe mirar)

1. **`None` mal manejado:** `if conf < umbral` sin chequear `None` primero lanza
   `TypeError`. `test_clasificar_confidence_none_va_a_revisar` lo atrapa.
2. **`>` en vez de `>=`:** un campo justo en el umbral cae a revisión.
   `test_clasificar_en_el_umbral_se_acepta` lo atrapa.
3. **`==` sobre floats** en `total_cuadra`: pasa por casualidad con enteros, pero revienta
   con `0.1 + 0.2`. `test_total_cuadra_con_tolerancia_de_floats` lo atrapa.
4. **`decidir_procesamiento` que mira solo confidence o solo el total:** falla uno de los
   dos tests de HITL.
5. **return temprano al primer motivo:** `test_decidir_acumula_ambos_motivos` exige ≥ 2
   motivos cuando ambos fallan.
6. **No vaciar `motivos` en el caso auto:** `test_decidir_auto_todo_limpio` exige
   `motivos == []`.

## Rango de soluciones aceptables

- Usar una comprensión de listas en `clasificar_campos` en vez del bucle explícito es
  igual de válido si maneja `None` y `>=`.
- `math.isclose(suma, total_declarado, abs_tol=tolerancia)` es una alternativa válida (y
  hasta más idiomática) a `abs(...) <= tolerancia`.
- El **texto exacto** de los motivos es libre, siempre que (a) el motivo del campo
  contenga el nombre del campo y (b) el motivo del total mencione "total". Los tests solo
  chequean esas subcadenas, no el texto literal.
- **Profundización opcional (excelente, no requerida):** parametrizar umbrales distintos
  por campo (el monto exige más confianza que la fecha), o devolver también la lista de
  campos a revisar dentro del resultado para alimentar la cola de HITL. No penalizar a
  quien hace solo lo pedido.
