---
ejercicio_id: fase-2/clean-code-dry-kiss-yagni
fase: fase-2
sub_unidad: "2.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — DRY/KISS/YAGNI con criterio

## Respuesta canónica (código)

```python
IVA = 0.19  # tasa de IVA en Chile (19%)


def con_iva(neto):
    """Única representación del cálculo del IVA (DRY: un solo lugar)."""
    return neto + int(neto * IVA)


def precio_con_iva(neto):
    return con_iva(neto)


def precio_con_iva_descuento(neto, descuento_pct):
    con_descuento = neto - int(neto * descuento_pct)
    return con_iva(con_descuento)


# Duplicación INCIDENTAL: se quedan separados a propósito. Un RUT y un SKU
# validan largo por razones independientes; unirlos los acoplaría.
def es_rut_valido(rut):
    return isinstance(rut, str) and len(rut) >= 3


def es_sku_valido(sku):
    return isinstance(sku, str) and len(sku) >= 3


# KISS/YAGNI: solo se usa formatear_precio(monto). Los otros parámetros eran futuro imaginado.
def formatear_precio(monto):
    return f"${monto:,}".replace(",", ".")
```

## `decisiones.md` de referencia (lo que debería razonar el alumno)
1. **DRY aplicado (IVA).** La fórmula `x + int(x * 0.19)` representa **el mismo conocimiento**: la tasa de IVA. Si el IVA sube al 20%, boleta y factura deben cambiar por la **misma razón**. Por eso vive en un solo `con_iva(neto)` que usa la constante `IVA`. Esto es DRY bien aplicado.
2. **Falsa DRY resistida (validadores).** `es_rut_valido` y `es_sku_valido` se ven idénticos hoy, pero validan conceptos **sin relación**. Si mañana el RUT exige dígito verificador, su regla cambia; el SKU no debería seguirla. Un `es_texto_valido` genérico los **acoplaría** y rompería el SKU en silencio. Es duplicación **incidental**: se dejan separados.
3. **KISS/YAGNI (formateo).** `formatear_precio` tenía cinco parámetros, pero en todo el código (los tests) solo se llama `formatear_precio(monto)`. Los knobs `moneda/separador_miles/simbolo/decimales` son futuro imaginado: deuda hoy por un beneficio que quizá nunca llega. Se simplifica a un parámetro, conservando la salida exacta del caso real.

## Razonamiento paso a paso
- La **pregunta rectora** para DRY: *"si esta regla cambiara mañana, ¿la otra debería cambiar con ella?"*. Sí → mismo conocimiento → extraer. No → incidental → dejar.
- El IVA pasa la prueba (sí cambian juntas). Los validadores la fallan (no tienen relación). El formateo no es duplicación: es exceso de generalidad.
- Todo se hace **manteniendo los tests verdes**: la simplificación de `formatear_precio` no altera su salida porque los tests solo ejercen el caso de un argumento.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Unir los validadores** en un genérico es el error central. Aunque los tests pasen, viola O2; márcalo como `incompleto` en C2 y explícale el daño concreto.
2. **DRY a medias:** extraer `con_iva` pero dejar el literal `0.19` en vez de la constante `IVA`.
3. **Romper el formateo** al simplificar (cambiar `$1.234`): la simplificación NO debe alterar comportamiento; lo atrapa `test_formatear_precio_*`.
4. **Sobre-abstraer el IVA** ("por si vienen más impuestos", una clase `Impuesto`): vuelve a caer en YAGNI.
5. **`decisiones.md` ausente o genérico:** sin el porqué por caso —sobre todo el de NO unificar— el ejercicio no demuestra criterio.

## Rango de soluciones aceptables
- `con_iva` con nombre distinto (`aplicar_iva`, `mas_iva`) es válido si reusa la constante `IVA`.
- `formatear_precio` con otra implementación equivalente: `f"${monto:,}".replace(",", ".")`, o construir el separador a mano, o `"${:,}".format(monto).replace(",", ".")`. Todas válidas si la salida es idéntica para los casos testeados.
- Dejar `con_iva` usando `round()` en vez de `int()` **NO** es aceptable si cambia algún resultado; el comportamiento original usa `int()` (trunca). Verifica que los tests sigan verdes.
- Mantener los validadores separados pero **renombrarlos** mejor (p. ej. extraer una constante `LARGO_MINIMO` distinta por cada uno) es **excelente**: refuerza que son reglas independientes.
- Es válido (y buena señal) que el alumno comente en el código *por qué* los validadores se quedan separados.
