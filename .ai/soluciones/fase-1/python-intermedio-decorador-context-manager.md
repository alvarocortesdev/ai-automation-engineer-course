---
ejercicio_id: fase-1/python-intermedio-decorador-context-manager
fase: fase-1
sub_unidad: "1.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Un decorador de reintento y un context manager con limpieza garantizada

## Respuesta canónica

```python
import functools
from contextlib import contextmanager


def reintentar(veces: int):
    def decorador(func):
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            ultimo_error = None
            for _ in range(veces):
                try:
                    return func(*args, **kwargs)      # éxito: corta el bucle
                except Exception as e:
                    ultimo_error = e                  # falló: guarda y reintenta
            raise ultimo_error                        # se agotaron los intentos
        return envoltura
    return decorador


@contextmanager
def conexion(registro: list):
    registro.append("conectado")                     # setup
    try:
        yield registro                               # entrega el recurso al `as ...`
    finally:
        registro.append("desconectado")              # teardown: corre SIEMPRE
```

## Razonamiento paso a paso
1. **Tres niveles del decorador parametrizado.** `reintentar(veces)` recibe el parámetro y devuelve
   `decorador`; `decorador(func)` recibe la función y devuelve `envoltura`; `envoltura` es lo que se
   ejecuta en cada llamada. El nivel extra (respecto de un decorador simple) existe **solo** para
   capturar `veces`.
2. **El bucle de reintento.** `for _ in range(veces)`: en cada vuelta intenta `return func(...)`; si
   funciona, el `return` sale de la envoltura y del bucle. Si lanza, se captura, se **guarda** en
   `ultimo_error` y se reintenta. Si el bucle termina sin haber retornado, significa que todas
   fallaron: `raise ultimo_error` re-lanza la última (falla ruidoso, no devuelve `None`).
3. **`functools.wraps`.** Copia `__name__`, `__doc__` y la metadata de `func` a `envoltura`. Sin él,
   `descargar_datos.__name__` sería `"envoltura"` y el test de identidad fallaría.
4. **El context manager.** Lo de antes del `yield` es el setup (`"conectado"`); el `yield registro`
   entrega el recurso al `as`; el `finally` después del `yield` es el teardown que corre **siempre**.
   Como no hay `except`, una excepción dentro del `with` se propaga después de ejecutar el `finally`.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Dos niveles en vez de tres**: `@reintentar` sin `()` no captura `veces`. El test usa
   `@reintentar(veces=3)`, así que un decorador de dos niveles ni siquiera importa bien.
2. **No re-lanzar**: tras el bucle, olvidar `raise ultimo_error` hace que la función devuelva `None`
   en silencio cuando todo falla — bug peligroso. `test_relanza_la_ultima_excepcion_si_todas_fallan`
   lo atrapa.
3. **Número de intentos equivocado**: `range(veces + 1)` reintenta de más; un `while` mal puesto, de
   menos o infinito. El test verifica `llamadas["n"] == 3` con `veces=3`.
4. **Olvidar `functools.wraps`**: `test_preserva_el_nombre_de_la_funcion` falla.
5. **Tragarse la excepción del `with`**: poner un `except` alrededor del `yield`, o hacer que un
   `__exit__` devuelva `True`, esconde el error. El test exige que el `ValueError` se propague.
6. **`"desconectado"` fuera del `finally`**: si el bloque revienta, nunca se agrega.

## Rango de soluciones aceptables
- **Versión basada en clase** del context manager (`__enter__`/`__exit__`) es válida y **excelente**
  si entiende que `__exit__` debe devolver `False`/`None` para propagar la excepción:
  ```python
  class conexion:
      def __init__(self, registro): self.registro = registro
      def __enter__(self):
          self.registro.append("conectado"); return self.registro
      def __exit__(self, exc_type, exc, tb):
          self.registro.append("desconectado")  # return None => propaga
  ```
  (Nota: si la implementa como clase, el nombre `conexion` sigue funcionando con `with conexion(log)`.)
- Capturar `except Exception` es lo esperado; capturar un tipo más específico es aceptable si el
  enunciado de los tests lo permite (los tests lanzan `ValueError`/`RuntimeError`, ambos `Exception`).
- Reintentar con `time.sleep`/backoff entre intentos es **mejor de lo pedido** (anticipa la Fase 6);
  acéptalo si no rompe los tests (no deben tardar de más).
- Anotaciones de tipo presentes o ausentes: irrelevante para el comportamiento.
