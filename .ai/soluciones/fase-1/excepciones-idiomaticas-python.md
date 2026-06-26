---
ejercicio_id: fase-1/excepciones-idiomaticas-python
fase: fase-1
sub_unidad: "1.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Excepciones de dominio en Python (parser de gastos)

## Respuesta canónica

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Gasto:
    comercio: str
    monto: int
    categoria: str


@dataclass(frozen=True)
class ErrorLinea:
    numero: int
    contenido: str
    motivo: str


class LineaInvalida(Exception):
    """La línea no respeta el formato 'comercio;monto;categoria'."""


def parsear_linea(linea: str) -> Gasto:
    partes = [p.strip() for p in linea.split(";")]
    if len(partes) != 3:
        raise LineaInvalida(f"esperaba 3 campos, llegaron {len(partes)}: {linea!r}")

    comercio, monto_raw, categoria = partes
    if not comercio or not categoria:
        raise LineaInvalida(f"comercio y categoría no pueden ser vacíos: {linea!r}")

    try:
        monto = int(monto_raw)                      # EAFP: intento, no pre-chequeo
    except ValueError as e:
        raise LineaInvalida(f"monto no es entero: {monto_raw!r}") from e   # encadena la causa

    if monto <= 0:
        raise LineaInvalida(f"monto debe ser > 0: {monto}")

    return Gasto(comercio=comercio, monto=monto, categoria=categoria)


def parsear_archivo(texto: str) -> tuple[list[Gasto], list[ErrorLinea]]:
    gastos: list[Gasto] = []
    errores: list[ErrorLinea] = []
    for numero, linea in enumerate(texto.splitlines(), start=1):
        if not linea.strip():                       # ignora blancas (pero el número avanza)
            continue
        try:
            gastos.append(parsear_linea(linea))
        except LineaInvalida as e:                  # específico, no `except:` pelado
            errores.append(ErrorLinea(numero=numero, contenido=linea, motivo=str(e)))
    return gastos, errores
```

Con esto pasan todos los tests.

## Razonamiento paso a paso

1. **La unidad lanza (contrato "válido o nada").** `parsear_linea` no tiene forma sensata de devolver
   "medio gasto": o produce un `Gasto` correcto o no produce nada. Lanzar una excepción de dominio
   `LineaInvalida` interrumpe el flujo y deja que el llamador decida.
2. **Excepción de dominio, no genérica.** `LineaInvalida(Exception)` permite al llamador hacer
   `except LineaInvalida` y distinguir "línea mala" de un bug real (`KeyError`, etc.). Hereda de
   `Exception` (no `BaseException`) para no tragarse `KeyboardInterrupt`/`SystemExit`.
3. **Encadenamiento (`from e`).** El monto se valida con EAFP: `int(monto_raw)` lanza `ValueError`;
   lo traducimos a `LineaInvalida` pero conservamos la causa con `from e`. Así `exc.__cause__` es el
   `ValueError` y la stack trace muestra "The above exception was the direct cause of...". Sin `from e`
   se pierde la pista del fallo de bajo nivel (peor observabilidad).
4. **El lote devuelve (contrato "todo lo que puedas + reporte").** `parsear_archivo` no debe caerse por
   una línea mala: el `except LineaInvalida` **acumula** un `ErrorLinea` y sigue. Los errores son
   **datos**, no control de flujo. `enumerate(..., start=1)` numera 1-based; las blancas se saltan con
   `continue` pero el número ya avanzó (por eso la blanca de la línea 2 no aparece como error y la
   siguiente mala es la 3).

## Puntos resbalosos (donde el corrector debe mirar)
1. **`parsear_archivo` que relanza** en vez de acumular → se cae en la primera mala (rompe su contrato).
2. **Olvidar `from e`** → `test_monto_no_entero_encadena_la_causa` falla (`__cause__` es `None`).
3. **`except:` pelado o `except Exception`** en el lote → atraparía bugs reales, no solo `LineaInvalida`.
4. **Conteo de líneas:** no usar `start=1`, o descontar las blancas del número → `{e.numero}` no da `{3, 4}`.
5. **Pre-chequeo del monto con `.isdigit()`** → falla con negativos (`"-5".isdigit()` es `False`, lo trataría como "no entero" en vez de "monto ≤ 0") y con signos; EAFP con `int()` es lo idiomático.
6. **Heredar de `BaseException`** → mal por diseño aunque los tests pasen.

## Rango de soluciones aceptables
- **EAFP vs LBYL:** se acepta validar el monto con `try/except ValueError`; un pre-chequeo robusto con regex es defendible pero menos idiomático — señalarlo.
- **Mensajes:** el texto exacto de los mensajes es libre; lo que importa es que `LineaInvalida` se lance en los 4 casos y que `__cause__` esté seteado en el del monto.
- **`parsear_linea` separada vs inline:** aceptable que `parsear_archivo` llame a `parsear_linea` (recomendado, DRY) o que reimplemente la lógica; lo primero es `excelente`.
- **`ErrorLinea`:** aceptable como `dataclass`, `NamedTuple` o `tuple` simple, siempre que exponga `numero`, `contenido`, `motivo`.
- **Líneas en blanco:** ignorarlas es lo pedido; tratarlas como error también pasaría una versión distinta de los tests, pero los tests dados exigen ignorarlas (la blanca no está en `{3, 4}`).
- **No aceptable:** devolver `None`/`-1` desde `parsear_linea` en vez de lanzar; o un `parsear_archivo` que propague la excepción (no recolecta).
