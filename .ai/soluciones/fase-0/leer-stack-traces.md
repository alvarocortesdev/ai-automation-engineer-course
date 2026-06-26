---
ejercicio_id: fase-0/leer-stack-traces
fase: fase-0
sub_unidad: "0.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Lee el stack trace (a mano)

> Lo que se evalúa es el **método de lectura**, no que adivine el número de línea exacto. Un alumno
> puede confundir un detalle y aun así demostrar que lee de abajo hacia arriba y razona la causa raíz.

## Caso 1 — `KeyError: 'precio'`

| Punto | Respuesta canónica |
|---|---|
| **Tipo y significado** | `KeyError`: se pidió una clave que no existe en el diccionario. La clave faltante es la que aparece en el mensaje: `'precio'`. |
| **Frame culpable** | `caso1.py`, **línea 7**, dentro de `precio_total`: `total += item["precio"]`. Es el frame de **más abajo**; el de arriba (línea 15, `<module>`, `print(precio_total(carro))`) sólo llamó a la función. |
| **Causa raíz** | El **segundo** item del carrito usa la clave `"valor"` en vez de `"precio"` (`{"nombre": "té", "valor": 1990}`). Al iterar, `item["precio"]` no existe para ese dato. |
| **Fix de una línea** | Corregir el dato (`"valor"` → `"precio"`), o leer con `item.get("precio", 0)` para tolerar la ausencia, o validar las claves antes de sumar. Cualquiera dirigido a "la clave que falta". |

## Caso 2 — `TypeError: unsupported operand type(s) for +=: 'int' and 'str'`

| Punto | Respuesta canónica |
|---|---|
| **Tipo y significado** | `TypeError`: se intentó una operación entre tipos incompatibles. Aquí, sumar (`+=`) un `int` con un `str`. |
| **Frame culpable** | `caso2.py`, **línea 7**, dentro de `suma_montos`: `total += m`. El frame de arriba (línea 12, `<module>`) es sólo el llamador. |
| **Causa raíz** | El tercer elemento de `datos` es el **texto** `"3000"`, no el número `3000`. En la tercera vuelta, `total` (int) se intenta sumar con un `str`. |
| **Fix de una línea** | Convertir el dato en su origen (`"3000"` → `3000`), o convertir al sumar (`total += int(m)`), o validar que todos los elementos sean numéricos antes de sumar. |

## Caso 3 — `ZeroDivisionError: division by zero`

| Punto | Respuesta canónica |
|---|---|
| **Tipo y significado** | `ZeroDivisionError`: se dividió por cero. |
| **Frame culpable** | `caso3.py`, **línea 5**, dentro de `promedio`: `return sum(numeros) / len(numeros)`. Los marcadores `~~~^~~~` señalan el operador `/`. **Tres frames**: `<module>` (línea 12) → `reporte` (línea 9) → `promedio` (línea 5). El culpable es el de más abajo (`promedio`); los otros dos son el camino. |
| **Causa raíz** | Se llamó `reporte([])` con una lista **vacía**. `len([])` es `0`, así que `sum([]) / 0` divide por cero. |
| **Fix de una línea** | Guardar el caso de lista vacía: `if not numeros: return 0` (o lanzar un `ValueError` con mensaje propio) antes de dividir. |

## Lo que distingue niveles
- **`competente`:** los tres tipos correctos, el frame de más abajo señalado en cada uno, y una causa
  raíz que apunta al **dato** (clave `"valor"`, el `str "3000"`, la lista vacía).
- **`excelente`:** además nombra explícitamente la dirección de lectura ("de abajo hacia arriba,
  `most recent call last`"), distingue camino vs causa en el caso 3 (tres frames), y propone el fix en
  el **origen del dato**, no sólo un parche local.
- **`en-progreso`:** acierta los tipos pero señala el frame de arriba como culpable, o da una causa
  vaga ("el código está mal") sin nombrar el dato.

## Señal anti-trampa
Si el diagnóstico es perfecto pero no hay rastro de proceso (todo "correcto sin titubeos" y redactado
como salida de modelo), pedir que prediga, **sin ejecutar**, el tipo de error de una cuarta variante:
p. ej. `caso3.py` llamado con `reporte([7])` (no falla → imprime 7.0) o un `IndexError` por
`carrito[5]`. Si leyó de verdad, lo resuelve; si dependió de la IA, se traba.
