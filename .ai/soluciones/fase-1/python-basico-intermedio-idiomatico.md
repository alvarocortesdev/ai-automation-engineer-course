---
ejercicio_id: fase-1/python-basico-intermedio-idiomatico
fase: fase-1
sub_unidad: "1.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Inventario idiomático, empaquetado

## Respuesta canónica

`despensa/inventario.py`:

```python
def resumen_inventario(productos):
    for p in productos:
        if p["precio"] < 0:
            raise ValueError(f"precio negativo en {p['nombre']!r}")
        if p["stock"] < 0:
            raise ValueError(f"stock negativo en {p['nombre']!r}")
    return {
        "unidades": sum(p["stock"] for p in productos),
        "valor": sum(p["precio"] * p["stock"] for p in productos),
        "agotados": [p["nombre"] for p in productos if p["stock"] == 0],
    }


def formatear_lineas(productos):
    return [
        f"{i}. {p['nombre']} — ${p['precio']} (x{p['stock']})"
        for i, p in enumerate(productos, start=1)
    ]
```

`despensa/__init__.py`:

```python
from despensa.inventario import resumen_inventario, formatear_lineas
```

## Razonamiento paso a paso
1. **Validar antes de acumular.** Un solo recorrido valida precio y stock; si algo es negativo,
   `raise ValueError` corta ahí y el total nunca se contamina. Validar **después** de sumar dejaría
   entrar el dato malo.
2. **`sum` con generator, no lista intermedia.** `sum(p["stock"] for p in productos)` y
   `sum(p["precio"] * p["stock"] for p in productos)` recorren sin construir listas que se tiran.
   Para la lista vacía, `sum(...)` de un generator vacío devuelve `0` — el caso borde sale gratis,
   sin un `if not productos` explícito (aunque ponerlo también es válido).
3. **Comprehension para `agotados`.** `[p["nombre"] for p in productos if p["stock"] == 0]` se lee
   como "el nombre de cada producto donde el stock es 0". Lista vacía → `[]`.
4. **`formatear_lineas` con `enumerate(..., start=1)`.** Numera desde 1 sin contador manual. La
   f-string arma el formato exacto; ojo con el em dash `—` (no `-`) y el `(x{stock})`.
5. **El paquete.** `test_import_desde_paquete` hace `despensa.resumen_inventario(...)`. Eso solo
   funciona si `__init__.py` re-exporta el nombre desde el módulo. Sin esa línea, `despensa` no
   tiene atributo `resumen_inventario` → `AttributeError`/`ImportError`.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Verde pero estilo "C".** Es lo más importante: tests pasan con `range(len(...))`, `str(...) +`,
   y `append` en bucle. Cumple C1 pero **falla C2 (idiomático)**, que es el objetivo central de 1.1.
2. **Formato inexacto:** numerar desde 0 (olvidar `start=1`), usar `-` en vez de `—`, o cambiar los
   espacios/paréntesis. `test_formatear_numera_desde_uno` lo atrapa.
3. **`__init__.py` sin re-export:** el alumno "arregla" moviendo o borrando el test de paquete en
   vez de re-exportar. Marcarlo: el objetivo O2 es justamente ese.
4. **Validación parcial:** validar solo stock o solo precio; ambos casos están testeados.
5. **Orden de validación con `None`:** no aplica aquí (el contrato garantiza las claves), pero si el
   alumno agrega `.get`, recordar que `None < 0` reventaría con `TypeError`.

## Rango de soluciones aceptables
- Usar `if not productos: return {"unidades": 0, "valor": 0, "agotados": []}` como guard explícito
  es **igual de válido** que dejar que `sum` de un generator vacío dé 0. Ambos cumplen.
- Extraer la validación a una función auxiliar (`_validar(p)`) es bienvenido (excelente).
- `from collections import defaultdict` no aporta aquí (no se agrupa por clave); si el alumno lo
  mete sin razón, es sobre-ingeniería, no excelencia.
- En `__init__.py`, tanto `from despensa.inventario import resumen_inventario, formatear_lineas`
  como `from .inventario import ...` (import relativo) son correctos.
- Mensajes de `ValueError` con otra redacción son válidos: el contrato solo exige que sea
  `ValueError`, no un texto específico.
