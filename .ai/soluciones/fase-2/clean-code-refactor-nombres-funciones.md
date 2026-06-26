---
ejercicio_id: fase-2/clean-code-refactor-nombres-funciones
fase: fase-2
sub_unidad: "2.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Refactor: nombres con intención + funciones pequeñas

## Punto de partida (lo que recibe el alumno)

```python
def total_pedido(d):
    r = 0
    for i in d:
        if i[3] == True:
            r = r + i[1] * i[2]
    if r > 100000:
        r = r - int(r * 0.1)
    return r
```

## Respuesta canónica

```python
UMBRAL_DESCUENTO_VOLUMEN = 100_000   # CLP desde los cuales aplica el descuento por volumen
TASA_DESCUENTO_VOLUMEN = 0.10        # 10%


def total_pedido(lineas):
    subtotal = subtotal_de_lineas_activas(lineas)
    return con_descuento_por_volumen(subtotal)


def subtotal_de_lineas_activas(lineas):
    return sum(precio * cantidad
               for _, precio, cantidad, activo in lineas
               if activo)


def con_descuento_por_volumen(subtotal):
    if subtotal > UMBRAL_DESCUENTO_VOLUMEN:
        return subtotal - int(subtotal * TASA_DESCUENTO_VOLUMEN)
    return subtotal
```

## Razonamiento paso a paso (el proceso importa más que el resultado)
1. **Nombres del dominio.** `calc`→`total_pedido`, `d`→`lineas`, `r`→`total/subtotal`, `i`→`linea`. Cada nombre responde *qué es* sin leer *cómo se calcula*.
2. **Adiós a los índices mágicos.** `i[1] * i[2]` y `i[3]` se vuelven frágiles ante cualquier cambio de la tupla. Desempaquetar (`producto, precio, cantidad, activo`) hace el contrato explícito. Se acepta también el desempaquetado dentro de un `for` clásico, no solo en la comprehension.
3. **`== True` fuera.** `if activo` es suficiente; `activo` ya es el booleano.
4. **Números mágicos → constantes.** `100000`→`UMBRAL_DESCUENTO_VOLUMEN`, `0.1`→`TASA_DESCUENTO_VOLUMEN`. Un solo lugar para cambiarlos, con nombre que explica.
5. **Una responsabilidad por función.** `total_pedido` orquesta; `subtotal_de_lineas_activas` decide *qué se suma*; `con_descuento_por_volumen` decide *la regla del descuento*. Dos razones para cambiar = dos funciones.
6. **Comportamiento preservado.** Cada paso se valida corriendo la suite. La firma pública `total_pedido(lineas)` no cambia.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Índices mágicos sobrevivientes:** dejar `linea[1] * linea[2]` "porque funciona". Es justo lo que O1 ataca; márcalo aunque los tests estén verdes.
2. **Partir de más:** extraer una función trivial de una sola línea usada una vez (p. ej. `es_activa(linea)`) que solo agrega un salto mental sin ganar legibilidad. SRP es semántico, no aritmético.
3. **Cambiar la firma o el formato de entrada** (aceptar dicts en vez de tuplas) para "que se vea mejor": rompe los tests y NO es lo pedido.
4. **Constantes crípticas:** `LIMITE = 100000` o `X = 0.1` no mejoran sobre el literal.
5. **`activo == True` o `activo is True`** en vez de `activo`: tolerable pero señala falta de confianza; coméntalo.

## Rango de soluciones aceptables
- **Bucle clásico en vez de `sum(...)`** es perfectamente válido y a veces más legible para un novato:
  ```python
  def subtotal_de_lineas_activas(lineas):
      subtotal = 0
      for producto, precio, cantidad, activo in lineas:
          if activo:
              subtotal += precio * cantidad
      return subtotal
  ```
- **Nombres distintos** del mismo espíritu (`calcular_total`, `aplicar_descuento_volumen`, `lineas_activas`) son válidos si revelan intención.
- **Una sola función bien nombrada y limpia** (sin extraer) puede ser **competente** en C1/C3 pero quedará en `en-progreso` en C2 si mezcla las dos responsabilidades; está bien marcar el matiz.
- Usar `@dataclass`/`NamedTuple` para la línea es **excelente** SOLO si el alumno lo entiende y lo defiende; si no, es sofisticación impropia del nivel (ver señales de dependencia-IA).
- Mantener `producto` como `_` en la comprehension (no se usa) es idiomático y correcto.
